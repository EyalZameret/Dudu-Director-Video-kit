---
name: dudu-browser
description: Used by Dudu (AI promo video director) to drive Gemini (Nano Banana images, Veo video) and Kling (image-to-video) in a Playwright browser the owner logged into. Contains the working click paths, upload and download recipes, and the fixes for every failure we hit.
---

# Dudu: driving Gemini and Kling with Playwright

Uses the Playwright MCP server from `.mcp.json`. Selectors below were verified 2026-10 on the Hebrew Gemini UI and the English Kling UI. The Gemini labels are written as regexes that accept both Hebrew and English; the English wording was not verified, so on the first run in another UI language take a `browser_snapshot`, check the real button names and fix the regexes here. Web UIs change: when a selector fails, take a snapshot (`browser_snapshot` or `browser_find`), find the new one, and update this file.

## 0. Ground rules
- The owner logs in. Open the site, tell the owner "log in in the Playwright window and tell me when you're done", and wait. Never type credentials.
- Automating a consumer web UI may conflict with the site's terms. Tell the owner once, keep volumes human-scale, and offer the official API as the alternative.
- **Files must be inside the workspace** (Playwright MCP refuses other roots). Copy any reference the owner pastes into `project/frames/` first.
- **Look at every result** before moving on (Read the image; contact sheet for clips).

## 1. Gemini: images (Nano Banana)
**The order matters.** Sending a prompt without first choosing the image tool made Gemini answer in text ("I can't generate images here") and the next try hung for 5+ minutes. Always: new chat, then tool, then refs, then prompt.

Labels used below (Hebrew UI verified, English unverified):
| Regex | Hebrew UI | English UI (check) |
|---|---|---|
| `TOOLS` | העלאה וכלים | Upload and tools |
| `CREATE_IMAGE` | יצירת תמונה | Create image |
| `DOWNLOAD_IMAGE` | הורדת תמונה בגודל מלא | Download full size image |

Step A, one `browser_run_code_unsafe` call (opens the OS file chooser):
```js
async (page) => {
  const TOOLS = /העלאה וכלים|Upload and tools/i,   // substring match, like a plain string name CREATE_IMAGE = /^(יצירת תמונה|Create images?)$/i;
  await page.goto('https://gemini.google.com/app'); await page.waitForTimeout(3000);
  await page.getByRole('button', { name: TOOLS }).first().click(); await page.waitForTimeout(1000);
  await page.getByText(CREATE_IMAGE).first().click(); await page.waitForTimeout(1500);
  await page.getByRole('button', { name: TOOLS }).first().click(); await page.waitForTimeout(1000);
  await page.locator('[data-test-id="local-images-files-uploader-button"]').click();
  return 'chooser';
}
```
Step B: `browser_file_upload` with the absolute paths of the refs (1-4 files).
Step C, prompt and download:
```js
async (page) => {
  await page.waitForTimeout(4000);
  const box = page.getByRole('textbox').first();
  await box.fill(PROMPT); await page.waitForTimeout(800); await box.press('Enter');
  const btn = page.getByRole('button', { name: /הורדת תמונה בגודל מלא|Download full[- ]size image/i });
  await btn.first().waitFor({ state: 'attached', timeout: 180000 }); await page.waitForTimeout(3000);
  const [d] = await Promise.all([page.waitForEvent('download', { timeout: 60000 }), btn.last().click({ force: true })]);
  await d.saveAs(OUT_PATH); return 'ok';
}
```
**Edits in the same chat** (remove a logo, fix eyes, swap an extra): navigate to the chat URL, count the download buttons, send the edit, and wait until the count grows:
```js
await page.waitForFunction(n => document.querySelectorAll('button[aria-label="הורדת תמונה בגודל מלא"], button[aria-label="Download full size image"]').length > n, before, { timeout: 180000 });
```
Typical time: 20-40 s per image.

Pitfalls:
- `browser_run_code_unsafe` cannot run while a file chooser is open. Split into A / B / C as above.
- Earlier chats keep context: a fresh chat avoids "it returned the same image".

## 2. Gemini: video (Veo)
Same as images, but pick `יצירת סרטון` (English UI: "Create video") and attach the keyframe. Download with the `הורדת הסרטון` button (English UI: "Download video"). Several minutes per clip, 720p, about 8-10 s.

## 3. Kling: image-to-video
Kling has a real `input[type=file]`, so no chooser is needed. One call per shot (about 70-80 s each):
```js
async (page) => {
  const seen = () => page.evaluate(() => performance.getEntriesByType('resource')
                       .map(e => e.name).filter(n => /-output\.mp4\?/.test(n)));
  const gen = () => page.locator('button').filter({ hasText: /Generate/ }).filter({ hasNotText: /Generated/ }).last();
  await page.goto('https://kling.ai/app/video/new?ac=7'); await page.waitForTimeout(5000);
  const before = new Set(await seen());
  await page.locator('input[type=file]').first().setInputFiles(KEYFRAME); await page.waitForTimeout(5000);
  await page.locator('[contenteditable="true"], textarea').first().click();
  await page.keyboard.type(PROMPT, { delay: 1 });
  let label = await gen().innerText();
  if (/60/.test(label)) { await page.getByText('Native Audio', { exact: true }).click(); label = await gen().innerText(); }
  if (!/40/.test(label)) return 'unexpected cost: ' + label;          // stop and ask the owner
  await gen().click();
  const t0 = Date.now(); let url = null;
  while (Date.now() - t0 < 300000) { await page.waitForTimeout(8000); url = (await seen()).find(u => !before.has(u)); if (url) break; }
  return url;
}
```
Then download outside the browser: `python tools/download.py "<url>" project/clips/shotNN.mp4`.

Pitfalls:
- `getByText('Generate')` also matches the "1/1 Generated" label. Use the button filter above.
- The `<video>` uses a blob URL and `fetch` fails; take the CDN URL from the performance entries instead.
- Check the price on the Generate button every time; Native Audio adds cost.

## 4. Reviewing clips
Do not review in the browser: `<video>` seeking returns stale frames. Use `python tools/contact_sheet.py` and `python tools/motion_report.py`.
