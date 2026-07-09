import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const main = readFileSync(join(root, "src", "main.tsx"), "utf8");
const styles = readFileSync(join(root, "src", "styles.css"), "utf8");

assert.match(main, /function CopyButton/, "generated text output should expose a reusable copy button");
assert.match(main, /navigator\.clipboard\.writeText/, "copy button should write generated text to the clipboard");
assert.match(main, /className="leftPaneScroll"/, "left pane should separate scrollable content from fixed controls");
assert.match(main, /className="leftPaneFooter"/, "left pane should keep action controls outside the scroll area");
assert.match(main, /className="resultHeader"/, "generated text area should include a header with actions");
assert.match(main, /content=\{activeContent\}/, "copy button should copy the active generated text");

assert.match(styles, /\.leftPane\s*\{[\s\S]*display:\s*flex/, "left pane should use flex layout");
assert.match(styles, /\.leftPane\s*\{[\s\S]*max-height:\s*calc\(100vh - 48px\)/, "left pane should be viewport bounded");
assert.match(styles, /\.leftPaneScroll\s*\{[\s\S]*overflow-y:\s*auto/, "left pane content should scroll vertically");
assert.match(styles, /\.leftPaneFooter\s*\{[\s\S]*flex-shrink:\s*0/, "left pane footer should not scroll away");
