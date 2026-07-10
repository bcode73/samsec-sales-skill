import { chromium } from "playwright";
import path from "path";

const dir = path.dirname(new URL(import.meta.url).pathname);
const htmlPath = `file://${dir}/full.html`;
const outPath = `${dir}/../exports/pdf/sales-blueprint.pdf`;

// Playwright's pinned browser build may not match what's pre-installed on this
// machine. If launch() fails with "Executable doesn't exist", either run
// `npx playwright install chromium` or point executablePath at a chromium
// binary already present on the system (e.g. /opt/pw-browsers/chromium-*/chrome-linux/chrome).
const browser = await chromium.launch({
  args: ["--no-sandbox"],
});
const page = await browser.newPage();
await page.goto(htmlPath, { waitUntil: "networkidle" });
await page.pdf({
  path: outPath,
  width: "6in",
  height: "9in",
  printBackground: true,
  margin: { top: "0in", bottom: "0.4in", left: "0in", right: "0in" },
  displayHeaderFooter: true,
  headerTemplate: "<span></span>",
  footerTemplate: `
    <div style="width:100%; font-size:8pt; font-family:'Liberation Sans',Arial,sans-serif; color:#1B1F1E; text-align:center; padding-top:2px;">
      <span class="pageNumber"></span>
    </div>`,
});
await browser.close();
console.log("PDF written to", outPath);
