// The interface around the drawing: panel, status bar, info box, toast, markers, theme, sections, panel width and what is remembered.
// Changes the layout and the stored interface state and reloads the page, so it runs on its own page.
import { launch, parseArgs, near } from './harness.mjs';

const t = await launch('shell', parseArgs(process.argv));
const { ev, click, move, eq, check, add, toast } = t;

const fresh = async () => { await t.reset(); await ev("$('tracking').checked = false; 1"); };
const tool = n => ev(`setTool('${n}')`);
const status = () => ev("$('status').textContent");
const info = () => ev("[...document.querySelectorAll('#info div')].map(d => d.textContent)");
const selectLines = (...i) => ev(`sel = new Set([${i.map(n => `gTrace.children[${n}]`).join(', ')}]); selChanged(); 1`);
const legend = name => ev(`[...document.querySelectorAll('#panel legend')].find(l => l.textContent === '${name}').click()`);
const collapsed = name => ev(`[...document.querySelectorAll('#panel legend')].find(l => l.textContent === '${name}').parentElement.classList.contains('collapsed')`);
const visible = id => ev(`$('${id}').offsetParent !== null`);
const theme = () => ev("$('themeBtn').textContent + '|' + (document.documentElement.dataset.theme || 'none')");
const panelColor = () => ev("getComputedStyle($('help')).backgroundColor");
const view = () => ev('[vb().x, vb().y, vb().width, vb().height]');
let r;

// ---------- 1 the start ----------
check('the panel does not overflow sideways', (await ev("$('panel').scrollWidth <= $('panel').clientWidth")) === true, await ev("[$('panel').scrollWidth, $('panel').clientWidth]"));
check('the status bar names the tool, the hint and the selection', (await status()).startsWith('Line: click or drag from the start point') && (await status()).endsWith('0 selected'), await status());
eq('the info box shows the tool, the hint and the selection', await info(), ['Line', 'click or drag from the start point', '0 selected']);

// ---------- 2 status bar and info box ----------
await fresh(); await tool('circle');
check('a tool change shows in the status bar and the info box', (await status()).startsWith('Circle: click the center') && (await info())[0] === 'Circle' && (await info())[1] === 'click the center', await status());
await move(100, 50);
check('the cursor position shows in both', (await status()).includes('100.0, 50.0') && (await info()).includes('x 100.0, y 50.0'), await info());

await fresh(); await add([0, 0, 100, 0], [0, 50, 30, 50]); await tool('select');
await selectLines(0);
check('one selected line shows its length', (await status()).endsWith('1 selected') && (await info()).includes('1 selected') && (await info()).includes('length 100.0 units = 10.00 m'), await info());
await selectLines(0, 1);
check('two selected lines show the total length', (await status()).endsWith('2 selected') && (await info()).includes('total length 130.0 units = 13.00 m'), await info());

await fresh(); await click(100, 100); await move(200, 100);
check('the length of the line being drawn shows live', (await status()).includes('length 100.0 units = 10.00 m') && (await info()).includes('drawing length 100.0 units = 10.00 m'), await info());

// ---------- 3 markers and previews at the cursor ----------
await fresh(); await add([100, 100, 200, 100]); await tool('line'); await move(201, 101);
eq('the snap marker shows at an end', await ev("$('snapMark').getAttribute('visibility')"), 'visible');
await move(500, 500);
eq('the snap marker hides on empty space', await ev("$('snapMark').getAttribute('visibility')"), 'hidden');
await tool('select'); await move(201, 101);
eq('the snap marker does not show with the Select tool', await ev("$('snapMark').getAttribute('visibility')"), 'hidden');
await ev("setTool('text'); $('textValue').value = 'Hello'"); await move(300, 300);
eq('the text preview shows the text at the cursor', await ev("$('textPreview').getAttribute('visibility') + '|' + $('textPreview').textContent"), 'visible|Hello');
await tool('line');
eq('the text preview hides on a tool change', await ev("$('textPreview').getAttribute('visibility')"), 'hidden');

// ---------- 4 toast and the unsaved warning ----------
await ev("msg('Hello toast')");
eq('the toast shows the message', (await toast()) + '|' + (await ev("$('toast').classList.contains('show')")), 'Hello toast|true');
await t.sleep(4000);
eq('the toast fades', await ev("$('toast').classList.contains('show')"), false);
eq('closing with unsaved changes is blocked', await ev("(() => { dirty = true; const e = new Event('beforeunload', { cancelable: true }); window.dispatchEvent(e); return e.defaultPrevented; })()"), true);
eq('closing without unsaved changes is not blocked', await ev("(() => { dirty = false; const e = new Event('beforeunload', { cancelable: true }); window.dispatchEvent(e); return e.defaultPrevented; })()"), false);

// ---------- 5 theme ----------
eq('the theme starts as system', await theme(), 'Theme: system|none');
await ev("$('themeBtn').click()");
eq('the first click gives light', await theme(), 'Theme: light|light');
const light = await panelColor();
await ev("$('themeBtn').click()");
eq('the second click gives dark', await theme(), 'Theme: dark|dark');
check('light and dark differ in the background color', light !== (await panelColor()), [light, await panelColor()]);
await ev("$('themeBtn').click()");
eq('the third click returns to system', await theme(), 'Theme: system|none');
await ev("$('themeBtn').click(); $('themeBtn').click()");

// ---------- 6 collapsible sections ----------
eq('a section starts open', [await collapsed('Floor'), await visible('floorId')], [false, true]);
await legend('Floor');
eq('a click on the title collapses it', [await collapsed('Floor'), await visible('floorId')], [true, false]);
await legend('Floor');
eq('a second click opens it', [await collapsed('Floor'), await visible('floorId')], [false, true]);
await legend('Underlays');

// ---------- 7 panel width and the overlays ----------
const width0 = await ev("Math.round($('panel').getBoundingClientRect().width)");
{ const bx = await ev("Math.round($('resizer').getBoundingClientRect().left + 3)"); await t.dragScreen(bx, 500, 420, 500); }
eq('dragging the bar sets the panel width', await ev("Math.round($('panel').getBoundingClientRect().width)"), 420);
check('the width changed', width0 !== 420, width0);
eq('the status bar follows the panel', await ev("$('status').style.left"), '434px');
eq('the buttons follow the panel and sit below the rulers', await ev("(() => { const v = view.getBoundingClientRect(); return Math.round(parseFloat($('orthoBtn').style.left) - v.left) + '|' + Math.round(parseFloat($('orthoBtn').style.top) - v.top); })()"), '26|26');
check('the overlays lie inside the drawing area', await ev("(() => { const v = view.getBoundingClientRect(), b = $('orthoBtn').getBoundingClientRect(), i = $('info').getBoundingClientRect(); return b.left >= v.left && b.top >= v.top && i.right <= v.right && i.top >= v.top; })()"));
eq('the width is stored', await ev("JSON.parse(localStorage.getItem('planTracer.ui')).panelWidth"), 420);

// ---------- 8 what a reload keeps ----------
await ev("fitCamera(); setTool('select'); setTool('zoomwin')");
await t.drag(100, 100, 300, 200);
const zoomed = await view();
await t.sleep(900);
await t.reload();
eq('the theme is kept', await theme(), 'Theme: dark|dark');
eq('a collapsed section stays collapsed and an open one open', [await collapsed('Underlays'), await collapsed('Floor')], [true, false]);
eq('the panel width is kept and the overlays follow', await ev("Math.round($('panel').getBoundingClientRect().width) + '|' + $('status').style.left"), '420|434px');
r = await view();
check('the last view is kept', r.every((v, i) => near(v, zoomed[i], 0.5)), [zoomed, r]);

await t.finish();
