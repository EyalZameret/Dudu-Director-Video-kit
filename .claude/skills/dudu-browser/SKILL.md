---
name: dudu-browser
description: Used by Dudu (AI promo video director) to drive Gemini (Nano Banana images, Veo video), ChatGPT (GPT Image) and Kling (image-to-video) in a Playwright browser the owner logged into. Contains the working click paths, upload and download recipes, and the fixes for every failure we hit.
---

# Dudu: driving Gemini, ChatGPT and Kling with Playwright

Uses the Playwright MCP server from `.mcp.json`. Selectors below were verified 2026-10 on the Hebrew Gemini UI and the English Kling UI. The ChatGPT recipe (section 1b) is **not verified yet**. The Gemini labels are written as regexes that accept both Hebrew and English; the English wording was not verified, so on the first run in another UI language take a `browser_snapshot`, check the real button names and fix the regexes here. Web UIs change: when a selector fails, take a snapshot (`browser_snapshot` or `browser_find`), find the new one, and update this file.

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

## 1b. ChatGPT: images (GPT Image), for owners without Gemini
**Status: unverified.** This recipe was written from the general structure of chatgpt.com, not from a recorded run. On the first run: take a `browser_snapshot` at every step, use the real selectors, and replace the guesses below with what worked (and the date). Until then, go step by step with separate small `browser_*` calls rather than one long script.

Before starting, tell the owner once: OpenAI's terms restrict extracting output by automated means; keep volumes human-scale, or use the OpenAI Images API with their own key instead.

Flow (same order as Gemini: new chat, refs, prompt, wait, download):
1. `browser_navigate` to `https://chatgpt.com/` (a fresh chat each time avoids "it returned the same image"). The owner logs in.
2. **Refs:** look for a hidden `input[type=file]` and use `setInputFiles` with the absolute paths (1-4 files). If there is none, click the attach button (a "+" or paperclip; check the snapshot) and use `browser_file_upload` on the chooser. Wait until every thumbnail has finished uploading.
3. **Prompt:** the composer is usually a contenteditable box (often `#prompt-textarea`). Start the prompt with `Create an image:` so it does not answer in text, or pick the image tool from the "+" menu if the snapshot shows one. Then the usual prompt (refs, shot line, STYLE, negatives).
4. **Aspect:** ChatGPT offers square, portrait and landscape 3:2 (1536x1024), not 16:9. Ask for `landscape 3:2` and add `keep all important content inside the central 16:9 band`. `tools/build_cut.py` crops to 16:9 in the edit.
5. **Wait:** usually 30-120 s. Wait until a new `img` appears in the last answer (its alt text is often "Generated image") and the progress indicator is gone.
6. **Download:** prefer the image's own download button (hover the image; check the snapshot). Otherwise read the `src` of the new `img` and save it with the browser's cookies:
   ```js
   async (page) => {
     const src = await page.locator('img[alt*="Generated"]').last().getAttribute('src');
     const res = await page.request.get(src);
     require('fs').writeFileSync(OUT_PATH, await res.body()); return res.status();
   }
   ```
   If `require` is not available in `browser_run_code_unsafe`, use the download button or `browser_take_screenshot` of the image element as a last resort (lower quality; say so to the owner).
7. **Edits** (remove a logo, fix the eyes): stay in the same chat and write `Edit only ...: ... Change nothing else.` ChatGPT may also offer a "select area" editor; either works.

What we saw with GPT Image (2026-10, character sheets):
- It captured **character and expression** best (age, tension, wild hair), with very consistent panels.
- Lower resolution and smoother, "too clean" light than Nano Banana; in one close-up the eyes looked in different directions. Add `natural skin texture, visible pores, unretouched, sharp focus, both eyes looking at the camera` and check the eyes in every face.
- Plan quota: image generation on chat plans has limits that change. If it says to wait, stop and tell the owner instead of retrying.

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
