// Static checks of plan-tracer.html. No browser. Prints one summary line and one line per failure.
// Started by run.mjs, which passes the path of the tool.
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { parseArgs } from './harness.mjs';

const { html: htmlPath } = parseArgs(process.argv);
if (!htmlPath) { console.log('usage: node static.mjs --html <path to the tool>'); process.exit(2); }
const html = readFileSync(htmlPath, 'utf8');

const results = [];
const check = (name, ok, detail) => results.push({ name, ok, detail });
const lineAt = (text, i) => text.slice(0, i).split('\n').length;
const list = a => a.join(', ');

// Split the file into markup and the one inline script
const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)];
check('exactly one inline script, no external script', scripts.length === 1 && !/\bsrc=/.test(scripts[0][1]), scripts.length);
const script = scripts[0][2];
const scriptStart = scripts[0].index + scripts[0][0].indexOf('>') + 1;
const scriptLine = lineAt(html, scriptStart) - 1;
const markup = html.slice(0, scripts[0].index) + html.slice(scripts[0].index + scripts[0][0].length);

// 1 syntax of the script
let syntaxOk = true;
try { new vm.Script(script, { filename: 'plan-tracer.html', lineOffset: scriptLine }); }
catch (e) { syntaxOk = false; check('script syntax', false, String(e.stack).split('\n').slice(0, 4).join(' | ')); }
if (syntaxOk) check('script syntax', true);

// 2 ids in the markup
const ids = [...markup.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]);
const dupIds = ids.filter((v, i) => ids.indexOf(v) !== i);
check('no duplicate ids in the markup', dupIds.length === 0, list([...new Set(dupIds)]));
const idSet = new Set(ids);
const used = new Set();
for (const m of script.matchAll(/\$\('([A-Za-z0-9_-]+)'\)/g)) used.add(m[1]);
for (const m of script.matchAll(/getElementById\('([A-Za-z0-9_-]+)'\)/g)) used.add(m[1]);
const missing = [...used].filter(i => !idSet.has(i));
check('every id the script looks up exists in the markup', missing.length === 0, list(missing));
const labelFor = [...markup.matchAll(/<label\b[^>]*\sfor="([^"]+)"/g)].map(m => m[1]);
check('every label for= points at an existing id', labelFor.every(i => idSet.has(i)), list(labelFor.filter(i => !idSet.has(i))));

// 3 balanced markup (non-void tags)
{
  const m = markup.replace(/<!--[\s\S]*?-->/g, '');
  const bad = [];
  for (const t of ['div', 'span', 'select', 'label', 'button', 'details', 'summary', 'section', 'fieldset', 'legend', 'ul', 'li', 'p', 'h1', 'h2', 'h3', 'svg', 'g', 'canvas', 'textarea', 'style']) {
    const open = (m.match(new RegExp(`<${t}(?=[\\s>/])[^>]*?(?<!/)>`, 'g')) || []).length, close = (m.match(new RegExp(`</${t}>`, 'g')) || []).length;
    if (open !== close) bad.push(`${t} ${open} open / ${close} close`);
  }
  check('opening and closing tags balance', bad.length === 0, list(bad));
}

// 4 calls to names that are never defined (lexical approximation)
{
  const strip = src => {
    let out = '', i = 0, prev = '', modes = ['code'], braces = [];
    const blank = s => s.replace(/[^\n]/g, ' ');
    while (i < src.length) {
      const c = src[i], n = src[i + 1], mode = modes[modes.length - 1];
      if (mode === 'tpl') {
        if (c === '\\') { out += blank(src.slice(i, i + 2)); i += 2; continue; }
        if (c === '`') { out += '`'; modes.pop(); prev = '`'; i++; continue; }
        if (c === '$' && n === '{') { out += '  '; modes.push('code'); braces.push(0); i += 2; continue; }
        out += c === '\n' ? '\n' : ' '; i++; continue;
      }
      if (c === '/' && n === '/') { const e = src.indexOf('\n', i); const j = e < 0 ? src.length : e; out += blank(src.slice(i, j)); i = j; continue; }
      if (c === '/' && n === '*') { const e = src.indexOf('*/', i + 2); const j = e < 0 ? src.length : e + 2; out += blank(src.slice(i, j)); i = j; continue; }
      if (c === '\'' || c === '"') {
        let j = i + 1; while (j < src.length && src[j] !== c) j += src[j] === '\\' ? 2 : 1;
        out += c + blank(src.slice(i + 1, j)) + c; i = j + 1; prev = c; continue;
      }
      if (c === '`') { out += '`'; modes.push('tpl'); i++; continue; }
      if (c === '/' && (prev === '' || '(,=:[!&|?{};'.includes(prev) || /(?:^|[^\w$])return$/.test(out.trimEnd()))) {
        let j = i + 1, cls = false;
        while (j < src.length && (src[j] !== '/' || cls)) { if (src[j] === '\\') j++; else if (src[j] === '[') cls = true; else if (src[j] === ']') cls = false; j++; }
        out += '/' + blank(src.slice(i + 1, j)) + '/'; i = j + 1; prev = '/'; continue;
      }
      if (modes.length > 1) {
        if (c === '{') braces[braces.length - 1]++;
        if (c === '}') { if (braces[braces.length - 1] === 0) { braces.pop(); modes.pop(); out += ' '; i++; continue; } braces[braces.length - 1]--; }
      }
      out += c; if (!/\s/.test(c)) prev = c; i++;
    }
    return out;
  };
  const code = strip(script);
  const D = new Set();
  const add = s => { for (const m of s.matchAll(/[A-Za-z_$][\w$]*/g)) D.add(m[0]); };
  for (const m of code.matchAll(/\b(?:function\*?|class)\s*([A-Za-z_$][\w$]*)/g)) D.add(m[1]);
  for (const m of code.matchAll(/\(([^()]*)\)\s*=>/g)) add(m[1]);
  for (const m of code.matchAll(/function\s*[\w$]*\s*\(([^()]*)\)/g)) add(m[1]);
  for (const m of code.matchAll(/([A-Za-z_$][\w$]*)\s*=>/g)) D.add(m[1]);
  for (const m of code.matchAll(/\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)/g)) D.add(m[1]);
  for (const m of code.matchAll(/\b(?:const|let|var)\s*([[{][^=;]*[\]}])/g)) add(m[1]);
  for (const m of code.matchAll(/\b(?:let|var)\s+([\w$,\s]+);/g)) add(m[1]);
  for (const m of code.matchAll(/(?<![=!<>])\b([A-Za-z_$][\w$]*)\s*=(?![=>])/g)) D.add(m[1]);
  for (const m of code.matchAll(/\bcatch\s*\(\s*([\w$]+)/g)) D.add(m[1]);
  for (const m of code.matchAll(/([A-Za-z_$][\w$]*)\s*\([^()]*\)\s*\{/g)) D.add(m[1]);
  const KEYWORDS = new Set('if for while switch catch function return typeof await async else do of in new delete void throw case with super class'.split(' '));
  const BUILTINS = new Set('parseFloat parseInt isNaN isFinite setTimeout clearTimeout setInterval clearInterval requestAnimationFrame cancelAnimationFrame fetch alert confirm prompt String Number Boolean Array Object Set Map WeakMap Promise Date URL File Blob Image DOMParser XMLSerializer FileReader Event MouseEvent KeyboardEvent PointerEvent WheelEvent DOMPoint DOMMatrix Uint8Array createImageBitmap showSaveFilePicker showOpenFilePicker atob btoa encodeURIComponent decodeURIComponent structuredClone matchMedia getComputedStyle requestIdleCallback queueMicrotask Symbol Error RegExp Function ResizeObserver IntersectionObserver TextEncoder TextDecoder Path2D addEventListener removeEventListener'.split(' '));
  const unknown = new Map();
  for (const m of code.matchAll(/(?<![.\w$])([A-Za-z_$][\w$]*)\s*\(/g)) {
    const name = m[1];
    if (KEYWORDS.has(name) || BUILTINS.has(name) || D.has(name)) continue;
    if (!unknown.has(name)) unknown.set(name, scriptLine + lineAt(code, m.index));
  }
  check('no call to a name that is never defined', unknown.size === 0, [...unknown].map(([n, l]) => `${n} (line ${l})`).join(', '));
}

// 5 the three attribute lists agree: written (elemMarkup), read (importElement), recorded for undo (SNAP_ATTRS)
{
  const fnText = name => {
    const i = script.indexOf(`function ${name}(`); if (i < 0) return '';
    const j = script.indexOf('\n}\n', i); return script.slice(i, j + 2);
  };
  const literal = (text, name) => {
    const i = text.indexOf(`const ${name} = {`); if (i < 0) return null;
    const j = text.indexOf('\n};', i); return new Function('return ' + text.slice(i + `const ${name} = `.length, j + 2))();
  };
  const SNAP = literal(script, 'SNAP_ATTRS'), KEEP = literal(script, 'KEEP_ATTRS');
  check('SNAP_ATTRS and KEEP_ATTRS found', !!SNAP && !!KEEP);
  const em = fnText('elemMarkup'), im = fnText('importElement');
  const marks = ['line', 'polyline', 'circle', 'path', 'text'].map(k => [k, em.indexOf(`if (k === '${k}')`)]).concat([['symbol', em.indexOf('const out = [')]]);
  const written = {};
  marks.forEach(([k, at], i) => {
    const end = i + 1 < marks.length ? marks[i + 1][1] : em.length;
    written[k] = [...new Set([...em.slice(at, end).matchAll(/\ba\('([\w-]+)'\)/g)].map(m => m[1]))].filter(a => a !== 'stroke-width');
  });
  const symRead = [...(im.match(/for \(const k of \[([^\]]*)\]\) if \(el\.hasAttribute/) || ['', ''])[1].matchAll(/'([\w-]+)'/g)].map(m => m[1]);
  const read = Object.assign({}, KEEP, { symbol: symRead });
  const sorted = a => [...a].sort();
  const same = (a, b) => JSON.stringify(sorted(a)) === JSON.stringify(sorted(b));
  // derived on load, so not read: the symbol transform is rebuilt by buildSymbol
  const derived = { symbol: ['transform'] };
  // written but not recorded for undo because no edit changes them
  const notUndone = { text: ['font-size'], path: ['data-smooth', 'data-closed'] };
  if (SNAP && KEEP) for (const k of Object.keys(written)) {
    const w = written[k], r = read[k] || [], s = SNAP[k] || [];
    const wr = w.filter(a => !(derived[k] || []).includes(a));
    check(`${k}: attributes saved equal attributes read on open`, same(wr, r), `saved ${list(wr)} | read ${list(r)}`);
    const wu = w.filter(a => !(notUndone[k] || []).includes(a));
    check(`${k}: attributes saved equal attributes recorded for undo`, same(wu, s), `saved ${list(wu)} | undo ${list(s)}`);
  }
}

// 6 the symbol library is well formed
{
  const i = script.indexOf('const SYMBOLS = {'), j = script.indexOf('\n};', i);
  let S = null, err = '';
  try { S = new Function('r6', 'return ' + script.slice(i + 'const SYMBOLS = '.length, j + 2))(v => Math.round(v * 1e6) / 1e6); } catch (e) { err = e.message; }
  check('SYMBOLS evaluates', !!S, err);
  if (S) {
    const bad = [];
    for (const [k, d] of Object.entries(S)) {
      if (typeof d.name !== 'string' || !(d.w > 0) || !(d.d > 0) || typeof d.shapes !== 'function') { bad.push(`${k}: name, w, d or shapes missing`); continue; }
      const shapes = d.shapes(d.w, d.d);
      if (!Array.isArray(shapes) || !shapes.length || shapes.some(s => typeof s.d !== 'string' || /NaN|undefined/.test(s.d))) bad.push(`${k}: bad shapes`);
    }
    check('every symbol has a name, size and valid shapes', bad.length === 0, list(bad));
    check('nine symbols', Object.keys(S).length === 9, Object.keys(S).length);
  }
}

// 7 text rules
{
  const nl = [...html.matchAll(/[äöüÄÖÜß]/g)];
  check('no German umlauts in the file', nl.length === 0, nl.slice(0, 5).map(m => `line ${lineAt(html, m.index)}`).join(', '));
  const words = ['Datei', 'Speichern', 'Öffnen', 'Abbrechen', 'Löschen', 'Linie', 'Rückgängig', 'Wiederholen', 'Fehler', 'Bitte', 'Ebene', 'Grundriss', 'Ansicht'];
  const gw = [...html.matchAll(new RegExp(`(?<!\\p{L})(${words.join('|')})(?!\\p{L})`, 'gu'))];
  check('no German words from the interface vocabulary', gw.length === 0, gw.slice(0, 5).map(m => `${m[1]} line ${lineAt(html, m.index)}`).join(', '));
  const dbg = [...html.matchAll(/console\.(log|debug)\b|\bdebugger\b|\bTODO\b|\bFIXME\b|\bXXX\b/g)];
  check('no debug output or work markers', dbg.length === 0, dbg.slice(0, 5).map(m => `${m[0]} line ${lineAt(html, m.index)}`).join(', '));
}

const failed = results.filter(r => !r.ok);
for (const r of failed) console.log(`FAIL ${r.name}${r.detail ? ' :: ' + r.detail : ''}`);
console.log(`static: ${results.length - failed.length} passed, ${failed.length} failed`);
process.exit(failed.length ? 1 : 0);
