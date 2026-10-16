// Shared helpers of the tests. Started through run.mjs, which passes every path; nothing here knows a location.
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

export const sleep = ms => new Promise(r => setTimeout(r, ms));
export const near = (v, w, e = 0.05) => Math.abs(v - w) < e;
export const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

// "--name value" pairs into an object; anything else goes to _
export function parseArgs(argv) {
  const o = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith('--')) o[argv[i].slice(2)] = argv[i + 1] !== undefined && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    else o._.push(argv[i]);
  }
  return o;
}

// Starts Chrome without a window, opens the tool and returns the helpers a test uses.
// name: the test's name in the summary line. opts: html, chrome, profile (a folder for temporary profiles), port, timeout.
export async function launch(name, opts) {
  const { html, chrome: chromePath, profile: base, port = 9334, timeout = 180000 } = opts;
  if (!html || !chromePath || !base) {
    console.log(`usage: node ${name}.mjs --html <tool> --chrome <chrome executable> --profile <folder> [--port n]`);
    process.exit(2);
  }
  mkdirSync(base, { recursive: true });
  const profile = mkdtempSync(join(base, 'run-'));
  const proc = spawn(chromePath, ['--headless=new', '--disable-extensions', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, '--window-size=1440,1000', '--no-first-run', 'about:blank'], { stdio: 'ignore' });

  let page;
  for (let i = 0; i < 100 && !page; i++) {
    try { page = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(t => t.type === 'page'); } catch (e) { /* not up yet */ }
    if (!page) await sleep(200);
  }
  if (!page) { console.log(`FAIL Chrome did not start\n${name}: 0 passed, 1 failed`); proc.kill(); process.exit(1); }
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => { ws.onopen = r; });

  const errors = [];
  let id = 0;
  const pending = new Map();
  const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  ws.onmessage = m => {
    const d = JSON.parse(m.data);
    if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); }
    else if (d.method === 'Runtime.exceptionThrown') errors.push(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
    else if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') errors.push('console.error: ' + d.params.args.map(a => a.value ?? a.description).join(' '));
    else if (d.method === 'Page.javascriptDialogOpening') send('Page.handleJavaScriptDialog', { accept: true });
  };

  // Results and the closing summary
  const results = [];
  let lastName = '(none)';
  const check = (n, ok, detail) => { results.push({ n, ok: !!ok, detail }); lastName = n; };
  const eq = (n, actual, expected) => check(n, same(actual, expected), { expected, actual });

  let closed = false;
  const close = async () => {
    if (closed) return; closed = true;
    try { ws.close(); } catch (e) { /* already closed */ }
    proc.kill();
    await sleep(400);
    try { rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 }); } catch (e) { /* Chrome still holds a file */ }
  };
  const finish = async () => {
    clearTimeout(timer);
    check('no script errors in the page', errors.length === 0, errors.slice(0, 3));
    await close();
    const bad = results.filter(r => !r.ok);
    for (const r of bad) console.log(`FAIL ${r.n}${r.detail !== undefined ? ' :: ' + JSON.stringify(r.detail).slice(0, 400) : ''}`);
    console.log(`${name}: ${results.length - bad.length} passed, ${bad.length} failed`);
    process.exit(bad.length ? 1 : 0);
  };
  const timer = setTimeout(() => { check(`finished within ${timeout} ms (last check: ${lastName})`, false); finish(); }, timeout);
  for (const ev_ of ['uncaughtException', 'unhandledRejection']) process.on(ev_, e => { check(`the test script itself failed`, false, String(e && e.stack || e).split('\n').slice(0, 3).join(' | ')); finish(); });

  // Page access
  const ev = async expr => {
    const r = (await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true })).result;
    if (r.exceptionDetails) { errors.push('evaluate failed: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text) + ' in ' + String(expr).slice(0, 80)); return undefined; }
    return r.result.value;
  };
  const stubSave = () => ev('window.__saved = null; saveFile = async (n, d) => { window.__saved = { n, d }; return true; }; 1');
  const waitReady = async () => {
    for (let i = 0; i < 100; i++) {
      if (await ev("document.readyState === 'complete' && typeof view !== 'undefined' && typeof autosave === 'function'")) break;
      await sleep(100);
    }
    await stubSave();
  };

  await send('Runtime.enable'); await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: pathToFileURL(html).href });
  await sleep(500);
  await waitReady();

  // The tool's own starting values of every control, restored by reset()
  const defaults = await ev(`(() => { const o = {}; document.querySelectorAll('input, select, textarea').forEach(e => { if (e.id && e.type !== 'file') o[e.id] = e.type === 'checkbox' || e.type === 'radio' ? e.checked : e.value; }); return o; })()`);

  // Mouse and keys. x and y are drawing coordinates unless the name says screen.
  const mouse = (type, x, y, extra = {}) => send('Input.dispatchMouseEvent', { type, x, y, button: 'left', clickCount: 1, ...extra });
  const toScreen = async (x, y) => {
    const [a, e, d, f] = await ev('(() => { const c = view.getScreenCTM(); return [c.a, c.e, c.d, c.f]; })()');
    return [a * x + e, d * y + f];
  };
  const moveScreen = (x, y) => mouse('mouseMoved', x, y, { button: 'none' });
  const clickScreen = async (x, y) => { await moveScreen(x, y); await mouse('mousePressed', x, y); await mouse('mouseReleased', x, y); };
  const dragScreen = async (x1, y1, x2, y2, steps = 6) => {
    await moveScreen(x1, y1); await mouse('mousePressed', x1, y1);
    for (let i = 1; i <= steps; i++) await mouse('mouseMoved', x1 + (x2 - x1) * i / steps, y1 + (y2 - y1) * i / steps, { buttons: 1 });
    await mouse('mouseReleased', x2, y2);
  };
  const move = async (x, y) => moveScreen(...await toScreen(x, y));
  const click = async (x, y) => clickScreen(...await toScreen(x, y));
  const drag = async (x1, y1, x2, y2, steps) => { const [a, b] = await toScreen(x1, y1), [c, d] = await toScreen(x2, y2); await dragScreen(a, b, c, d, steps); };
  const rclick = () => ev("view.dispatchEvent(new MouseEvent('contextmenu', { bubbles: true })); 1");
  const key = async (k, mod = 0) => {
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key: k, text: k.length === 1 ? k : undefined, modifiers: mod });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: k, modifiers: mod });
  };
  const holdShift = async fn => {
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Shift', modifiers: 8 });
    await fn();
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Shift' });
  };

  // Back to the tool's starting state: trace, layers, ids, underlays, controls, view, autosave
  const reset = async () => {
    await ev(`(d => {
      for (const k in d) {
        const e = document.getElementById(k); if (!e) continue;
        const box = e.type === 'checkbox' || e.type === 'radio', now = box ? e.checked : e.value;
        if (now === d[k]) continue;
        if (box) e.checked = d[k]; else e.value = d[k];
        e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true }));
      }
      return 1;
    })(${JSON.stringify(defaults)})`);
    await ev(`(() => {
      gTrace.textContent = ''; sel.clear(); hover = null; undoS = []; redoS = []; calib = null;
      endDraw();
      layers = [{ name: 'Default', visible: true, locked: false }]; activeLayer = 'Default'; idN = 0;
      unders.forEach(u => u.url && URL.revokeObjectURL(u.url)); unders = []; activeU = -1; rebuildUnderDom();
      if (ui.map) { ui.map = false; if (typeof syncMap === 'function') syncMap(); }
      setTool('line'); syncLayers(); syncControls(); fitCamera(); paint();
      $('toast').textContent = '';
      $('help').open = false;
      autosave(); dirty = false;
      return 1;
    })()`);
  };
  const reload = async () => { await ev('dirty = false'); await send('Page.reload'); await sleep(400); await waitReady(); };

  // Saved files: the stub keeps the last file the tool tried to save
  const captureSave = async (action, wait = 10000) => {
    await ev('window.__saved = null; 1');
    await ev(action);
    for (let t0 = Date.now(); Date.now() - t0 < wait && !(await ev('!!window.__saved'));) await sleep(50);
    return ev(`window.__saved ? { name: window.__saved.n, size: typeof window.__saved.d === 'string' ? window.__saved.d.length : window.__saved.d.size } : null`);
  };
  const savedText = () => ev('(async () => { const d = window.__saved.d; return typeof d === "string" ? d : await d.text(); })()');
  // Size of the saved PNG and the colors "r,g,b" at the given pixels
  const savedImage = (points = []) => ev(`(async () => {
    const bm = await createImageBitmap(window.__saved.d), c = document.createElement('canvas');
    c.width = bm.width; c.height = bm.height;
    const x = c.getContext('2d'); x.drawImage(bm, 0, 0);
    return { w: bm.width, h: bm.height, px: ${JSON.stringify(points)}.map(([X, Y]) => Array.from(x.getImageData(X, Y, 1, 1).data).slice(0, 3).join(',')) };
  })()`);
  const screenshot = async file => writeFileSync(file, Buffer.from((await send('Page.captureScreenshot', { format: 'png' })).result.data, 'base64'));

  // Common reads and set-ups of the trace
  const lines = () => ev("[...document.querySelectorAll('#trace line')].map(l => [l.getAttribute('x1'), l.getAttribute('y1'), l.getAttribute('x2'), l.getAttribute('y2')].map(Number).map(v => +v.toFixed(2)).join(','))");
  const add = (...ls) => ev('(() => { ' + ls.map(l => 'gTrace.appendChild(mkLine(' + l.join(',') + '));').join('') + ' paint(); return 1; })()');
  const toast = () => ev("$('toast').textContent");
  const ops = () => ev('undoS.length');
  const kids = () => ev("[...gTrace.children].map(e => e.tagName + ':' + e.id).join(',')");
  const svg = () => ev('buildSvg()');
  const reopen = () => ev("(() => { const doc = new DOMParser().parseFromString(buildSvg(), 'image/svg+xml'); importTrace(doc.querySelectorAll('#trace > *')); return 1; })()");

  // Setting a field the way typing does, picking an image, and opening a plan SVG through the tool's own file input
  const setField = (id, v) => ev(`(() => { const e = $('${id}'); e.value = '${v}'; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); return 1; })()`);
  // A name the drawing already holds without an image gets its image back instead of a new underlay.
  const mkU = async (name, color) => {
    const n = await ev('unders.length'), known = await ev(`unders.some(u => u.name === '${name}' && !u.url)`);
    await ev(`new Promise(res => { const c = document.createElement('canvas'); c.width = 200; c.height = 100; const x = c.getContext('2d'); x.fillStyle = '${color}'; x.fillRect(0, 0, 200, 100); c.toBlob(b => { addUnderlayFile(new File([b], '${name}', { type: 'image/png' })); res(1); }); })`);
    if (known) await sleep(300);
    else for (let i = 0; i < 60 && (await ev('unders.length')) === n; i++) await sleep(50);
    await sleep(100);
  };
  // Waits for the tool's answer in the toast
  const openText = async (text, name = 'x.svg') => {
    await ev("$('toast').textContent = ''; 1");
    await ev(`(() => { const dt = new DataTransfer(); dt.items.add(new File([${JSON.stringify(text)}], '${name}', { type: 'image/svg+xml' })); $('openFile').files = dt.files; $('openFile').dispatchEvent(new Event('change')); return 1; })()`);
    for (let i = 0; i < 60 && !(await toast()); i++) await sleep(50);
  };

  return { send, ev, errors, check, eq, finish, sleep, mouse, toScreen, move, click, drag, moveScreen, clickScreen, dragScreen, rclick, key, holdShift, reset, reload, captureSave, savedText, savedImage, screenshot, lines, add, toast, ops, kids, svg, reopen, setField, mkU, openText };
}
