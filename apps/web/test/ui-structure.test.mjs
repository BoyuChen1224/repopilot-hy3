import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const main = readFileSync(join(root, "src", "main.tsx"), "utf8");
const styles = readFileSync(join(root, "src", "styles.css"), "utf8");
const readme = readFileSync(join(root, "..", "..", "README.md"), "utf8");
const readmeCn = readFileSync(join(root, "..", "..", "README_CN.md"), "utf8");

assert.match(main, /function CopyButton/, "generated text output should expose a reusable copy button");
assert.match(main, /navigator\.clipboard\.writeText/, "copy button should write generated text to the clipboard");
assert.match(main, /className="leftPaneScroll"/, "left pane should separate scrollable content from fixed controls");
assert.match(main, /className="leftPaneFooter"/, "left pane should keep action controls outside the scroll area");
assert.match(main, /className="resultHeader"/, "generated text area should include a header with actions");
assert.match(main, /content=\{activeContent\}/, "copy button should copy the active generated text");
assert.match(main, /type Language = "en" \| "zh"/, "frontend should define English and Chinese UI languages");
assert.match(main, /className="languageToggle"/, "frontend should expose a language toggle button");
assert.match(main, /setLanguage/, "language toggle should switch UI language state");
assert.match(main, /项目复现与错误诊断助手/, "Chinese UI copy should be available");

assert.match(styles, /\.leftPane\s*\{[\s\S]*display:\s*flex/, "left pane should use flex layout");
assert.match(styles, /\.app\s*\{[\s\S]*height:\s*100vh/, "app shell should be fixed to the viewport height");
assert.match(styles, /\.app\s*\{[\s\S]*overflow:\s*hidden/, "app shell should prevent document-level scrolling");
assert.match(styles, /\.workspace\s*\{[\s\S]*height:\s*100%/, "workspace should fill the fixed app shell");
assert.match(styles, /\.leftPane\s*\{[\s\S]*height:\s*100%/, "left pane should stay fixed while right output scrolls");
assert.match(styles, /\.leftPaneScroll\s*\{[\s\S]*overflow-y:\s*auto/, "left pane content should scroll vertically");
assert.match(styles, /\.leftPaneFooter\s*\{[\s\S]*flex-shrink:\s*0/, "left pane footer should not scroll away");
assert.match(styles, /\.rightPane\s*\{[\s\S]*height:\s*100%/, "right pane should be viewport bounded");
assert.match(styles, /\.markdown\s*\{[\s\S]*flex:\s*1/, "generated text area should take remaining right pane height");
assert.match(styles, /\.markdown\s*\{[\s\S]*min-height:\s*0/, "generated text area should be allowed to shrink before scrolling");
assert.match(styles, /\.markdown\s*\{[\s\S]*overflow-y:\s*auto/, "generated text area should scroll internally");
assert.match(styles, /\.languageToggle\s*\{/, "language toggle should have dedicated styling");

assert.doesNotMatch(readme, /WSL|WINDOWS_HOST/, "English README should not include WSL-specific API guidance");
assert.doesNotMatch(readmeCn, /WSL|WINDOWS_HOST/, "Chinese README should not include WSL-specific API guidance");
