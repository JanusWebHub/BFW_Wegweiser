// One floor drawn the way a person would: underlay, layers, walls, symbols, dimension, edits, save, New, open, reload, PNG.
// Real mouse and key events, tracking guides on. Optional: --shot <file> writes a screenshot at the end.
import { launch, parseArgs, near } from './harness.mjs';

const args = parseArgs(process.argv);
const t = await launch('scenario', args);
const { ev, click, move, drag, key, rclick, eq, check, lines, svg, mkU, openText } = t;

const tool = n => ev(`setTool('${n}')`);
const norm = ls => ls.map(l => { const [a, b, c, d] = l.split(',').map(Number); return a < c || (a === c && b <= d) ? l : [c, d, a, b].join(','); }).sort();
const layerNames = () => ev("layers.map(l => l.name).join(',')");
const addLayer = name => ev(`$('layerName').value = '${name}'; $('layerAdd').click(); 1`);
const symbols = () => ev("[...gTrace.children].filter(e => e.hasAttribute('data-symbol')).map(e => [e.getAttribute('data-symbol'), +e.getAttribute('data-cx'), +e.getAttribute('data-cy')])");
const rackX = () => ev("[...gTrace.children].filter(e => e.getAttribute('data-symbol') === 'rack').map(e => +e.getAttribute('data-cx'))");
const darkIn = (x0, y0, x1, y1) => ev(`(async () => {
  const bm = await createImageBitmap(window.__saved.d), c = document.createElement('canvas'); c.width = bm.width; c.height = bm.height;
  const x = c.getContext('2d'); x.drawImage(bm, 0, 0);
  const d = x.getImageData(${x0}, ${y0}, ${x1 - x0}, ${y1 - y0}).data; let n = 0;
  for (let i = 0; i < d.length; i += 4) if (d[i] < 100 && d[i + 1] < 100 && d[i + 2] < 100) n++;
  return n;
})()`);
let r;

// ---------- a clean start with an underlay fitted to the frame ----------
await t.reset();
await mkU('scan.png', '#c8d8e8');
await ev("$('underFit').click()");
eq('fit to frame scales the image to the frame width and puts it in the corner', await ev('[unders[0].scale, unders[0].x, unders[0].y, unders[0].rot]'), [5, 0, 0, 0]);

// ---------- layers ----------
await ev("$('layerName').value = 'Walls'; $('layerRename').click(); 1");
await addLayer('Equipment'); await addLayer('Notes');
eq('three layers', await layerNames(), 'Walls,Equipment,Notes');

// ---------- walls: a rectangle and an inner wall by midpoint snap, ortho and typed length ----------
await ev("$('layerSel').value = 'Walls'; $('layerSel').dispatchEvent(new Event('change'))");
await tool('rect'); await click(50, 50); await click(850, 550);
eq('the outer walls', norm(await lines()), norm(['50,50,850,50', '850,50,850,550', '850,550,50,550', '50,550,50,50']));
await tool('line'); await ev("$('orthoBtn').click()");
await click(450, 50); await move(450, 200); await key('2'); await key('5'); await key('Enter');
await ev("$('orthoBtn').click()");
check('the inner wall starts at the midpoint of the top wall and is 25 m long', norm(await lines()).includes('450,50,450,300'), await lines());

// ---------- equipment: symbols snap to the wall points ----------
await ev("$('layerSel').value = 'Equipment'; $('layerSel').dispatchEvent(new Event('change'))");
for (const [type, x, y] of [['column', 50, 50], ['dock', 850, 300], ['door', 450, 550], ['rack', 200, 200], ['rack', 200, 260], ['rack', 200, 320]]) {
  await ev(`setTool('symbol'); $('symType').value = '${type}'; $('symType').dispatchEvent(new Event('change'))`); await click(x, y);
}
eq('the symbols sit on the wall points they were clicked near', (await symbols()).slice(0, 3), [['column', 50, 50], ['dock', 850, 300], ['door', 450, 550]]);
eq('the racks', await rackX(), [200, 200, 200]);
await tool('circle'); await click(700, 400); await click(730, 400);
await tool('polyline'); await click(100, 500); await click(300, 500); await click(300, 450); await rclick();
eq('the equipment layer holds the symbols, the circle and the polyline', await ev("[...gTrace.children].filter(e => e.getAttribute('data-layer') === 'Equipment').length"), 8);

// ---------- notes: a dimension and a label ----------
await ev("$('layerSel').value = 'Notes'; $('layerSel').dispatchEvent(new Event('change'))");
await tool('dimension'); await click(50, 50); await click(850, 50); await click(450, 20);
eq('the dimension reads the wall length', await ev("[...gTrace.querySelectorAll('text')].map(e => e.textContent).join(',')"), '80.00 m');
await ev("setTool('text'); $('textValue').value = 'Office'"); await click(650, 150);
eq('the label is free text on the notes layer', await ev("(() => { const e = gTrace.lastElementChild; return e.textContent + '|' + e.hasAttribute('data-for') + '|' + e.getAttribute('data-layer'); })()"), 'Office|false|Notes');

// ---------- edit: move the racks together, undo ----------
await ev("$('layerSel').value = 'Equipment'; $('layerSel').dispatchEvent(new Event('change'))");
await tool('select'); await drag(150, 150, 260, 360);
eq('the rubber band takes the three racks', await ev("[...sel].map(e => e.getAttribute('data-symbol')).join(',')"), 'rack,rack,rack');
await drag(200, 260, 300, 260);
r = await rackX();
check('dragging one rack moves all three by the same amount', r.length === 3 && r.every(x => near(x, 300, 0.01)), r);
await ev('undo()');
eq('undo puts them back', await rackX(), [200, 200, 200]);
await ev('sel.clear(); selChanged()');

// ---------- save, New, open, reload ----------
const before = await svg();
const saved = await t.captureSave("$('save').click()");
eq('the file is offered under the floor id', saved && saved.name, 'EG-plan.svg');
const text = await t.savedText();
check('the saved file has the layers and the underlay', ['data-layer="Walls"', 'data-layer="Equipment"', 'data-layer="Notes"', 'href="scan.png"'].every(s => text.includes(s)));
await ev("$('newDoc').click(); $('newDoc').click()");
eq('New empties the drawing', await ev('gTrace.children.length + "|" + unders.length + "|" + layers.length'), '0|0|1');
await openText(text);
check('opening the saved file gives the same file back', (await svg()) === before);
eq('the layers are back', await layerNames(), 'Walls,Equipment,Notes');
await t.sleep(900);
await t.reload();
check('after a reload the autosave gives the same file back', (await svg()) === before);

// ---------- PNG with a layer hidden ----------
await ev("$('layerSel').value = 'Walls'; $('layerSel').dispatchEvent(new Event('change'))");
await t.captureSave("$('exportPng').click()");
const wall = await darkIn(1190, 95, 1210, 105), dim = await darkIn(1100, 36, 1300, 44);
check('the PNG shows the wall and the dimension line', wall > 5 && dim > 5, [wall, dim]);
await ev("$('layerSel').value = 'Notes'; $('layerSel').dispatchEvent(new Event('change')); $('layerVis').checked = false; $('layerVis').dispatchEvent(new Event('change'))");
await t.captureSave("$('exportPng').click()");
check('with the notes layer hidden the dimension line is gone and the wall stays', (await darkIn(1100, 36, 1300, 44)) === 0 && (await darkIn(1190, 95, 1210, 105)) > 5);

if (args.shot) await t.screenshot(args.shot);
await t.finish();
