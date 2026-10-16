// Drawing, snapping, selecting, editing, history and layers on the trace.
// One page; every section starts from reset(). Tracking guides are off unless a section turns them on.
import { launch, parseArgs, near } from './harness.mjs';

const t = await launch('editing', parseArgs(process.argv));
const { ev, click, move, drag, key, rclick, eq, check, lines, add, toast, ops, kids, svg, reopen } = t;

const fresh = async () => { await t.reset(); await ev("$('tracking').checked = false; 1"); };
const tool = n => ev(`setTool('${n}')`);
const attr = (s, a) => ev(`(document.querySelector('#trace ${s}') || { getAttribute: () => 'none' }).getAttribute('${a}')`);
const styles = () => ev("[...gTrace.children].map(l => l.getAttribute('stroke') + '/' + l.getAttribute('stroke-width')).join(',')");
const colors = () => ev("[...gTrace.children].map(l => l.getAttribute('data-color') + '/' + l.getAttribute('stroke-width')).join(',')");
const selTags = () => ev("[...sel].map(e => e.tagName).join(',')");
const selectOnly = i => ev(`sel = new Set([gTrace.children[${i}]]); selChanged(); 1`);
const count = s => ev(`gTrace.querySelectorAll('${s}').length`);
const setLayer = (name, vis, lock) => ev(`(() => { $('layerSel').value = '${name}'; $('layerSel').dispatchEvent(new Event('change')); $('layerVis').checked = ${vis}; $('layerVis').dispatchEvent(new Event('change')); $('layerLock').checked = ${lock}; $('layerLock').dispatchEvent(new Event('change')); return 1; })()`);
let r;

// ---------- 1 lines: dragging, clicking, ortho, typed length, chain, cancel ----------
await fresh(); await drag(100, 100, 300, 100);
eq('drag draws a line', await lines(), ['100,100,300,100']);
await click(100, 200); await click(200, 250); r = await lines();
check('click, click draws a second line', r.length === 2 && r[1] === '100,200,200,250', r);
await fresh(); await ev("$('orthoBtn').click()"); await drag(100, 100, 300, 120);
eq('ortho drag is level', await lines(), ['100,100,300,100']);
eq('ortho button label and checkbox', await ev("$('orthoBtn').textContent + '|' + $('ortho').checked"), 'Ortho: on|true');
await fresh(); await t.holdShift(() => drag(100, 100, 300, 120));
eq('Shift acts as ortho', await lines(), ['100,100,300,100']);
await fresh(); await drag(100, 100, 100.2, 100.2);
check('a tiny drag counts as a click', (await ev('startPt !== null')) === true && (await lines()).length === 0);
await fresh();
{ const [a1, b1] = await t.toScreen(100, 100), [a2, b2] = await t.toScreen(300, 150);
  await t.moveScreen(a1, b1); await t.mouse('mousePressed', a1, b1); await t.mouse('mouseMoved', a2, b2, { buttons: 1 }); await rclick(); await t.mouse('mouseReleased', a2, b2); }
check('right-click during a drag draws nothing', (await lines()).length === 0 && (await ev('startPt === null')) === true, await lines());
await fresh(); await click(100, 100); await rclick();
check('right-click cancels a pending point', (await ev('startPt === null')) === true);

await fresh(); await click(100, 200); await move(200, 200); await key('5');
check('typed length shows in the status', (await ev("$('status').textContent")).includes('typed length 5'), await ev("$('status').textContent"));
await key('Enter');
eq('typed length places the end', await lines(), ['100,200,150,200']);
await fresh(); await click(100, 200); await move(200, 200); await key('2'); await key('Backspace'); await key('Escape');
eq('Esc clears the typed length and the start', await ev("typed + '|' + (startPt === null)"), '|true');
await fresh(); await click(100, 200); await move(200, 200); await ev("$('upm').value = '0'"); await key('5'); await key('Enter');
check('typed length needs units per meter', (await toast()).startsWith('Set units per meter') && (await lines()).length === 0, await toast());

await fresh(); await ev("$('chain').checked = true"); await drag(100, 100, 200, 100);
eq('chain keeps the start after a drag', await ev('startPt && Math.round(startPt.x) + "," + Math.round(startPt.y)'), '200,100');
await click(200, 200);
eq('chain continues from the last end', await lines(), ['100,100,200,100', '200,100,200,200']);

await fresh(); await ev("$('orthoBtn').click()"); await tool('rect'); await click(100, 300); await click(200, 350); r = await lines();
check('ortho rectangle is a square', r.length === 4 && r[0] === '100,300,200,300' && r[1] === '200,300,200,400', r);

await fresh(); await tool('dimension'); await click(0, 0); await click(100, 0); await click(50, 30); r = await lines();
check('dimension draws its lines', r.length === 3 && r[0] === '0,0,0,30' && r[2] === '0,30,100,30', r);
eq('dimension text', await ev("document.querySelector('#trace text').textContent"), '10.00 m');
await ev('undo()');
eq('undo removes the whole dimension', await ev('gTrace.children.length'), 0);
await fresh(); await tool('dimension'); await click(0, 0); await click(100, 0); await click(50, 0);
check('dimension refuses a click on the line', (await toast()).startsWith('Click to one side') && (await ops()) === 0, await toast());

// ---------- 2 each kind: create, handles, move, hit, save ----------
// polyline
await fresh(); await tool('polyline'); await click(100, 100); await click(200, 150); await click(300, 100); await rclick();
eq('polyline points', await attr('polyline', 'points'), '100,100 200,150 300,100');
eq('polyline preview hidden after finishing', await ev("$('polyPrev').getAttribute('visibility')"), 'hidden');
await tool('polyline'); await click(100, 300); await click(200, 300);
await ev("window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))");
eq('Enter finishes a polyline', await count('polyline'), 2);
await tool('polyline'); await click(400, 300); await click(450, 300); await click(450, 300);
eq('a second click on the last point finishes', await count('polyline'), 3);
await tool('polyline'); await click(500, 300); await rclick();
check('one point makes no polyline', (await count('polyline')) === 3 && (await toast()) === 'Click at least 2 points.', await toast());
await tool('polyline'); await click(100, 400); await move(200, 450);
eq('polyline preview while drawing', await ev("$('preview').getAttribute('visibility')"), 'visible');
await click(200, 450);
check('polyline state holds two points', (await ev('poly.length')) === 2 && (await ev("$('polyPrev').getAttribute('visibility')")) === 'visible');
await ev('endDraw()');
await ev("setTool('select')"); await selectOnly(0);
eq('polyline has a handle per vertex', await ev('gHandles.children.length'), 3);
await drag(200, 150, 220, 190);
eq('dragging a vertex', (await attr('polyline', 'points')).split(' ')[1], '220,190');
await ev('undo()');
eq('undo of the vertex drag', (await attr('polyline', 'points')).split(' ')[1], '200,150');
await drag(250, 125, 270, 145);
eq('dragging a segment moves the polyline', (await attr('polyline', 'points')).split(' ')[0], '120,120');
await ev('undo()');
await ev('sel.clear(); selChanged()'); await click(150, 125);
eq('a click on a polyline selects it', await selTags(), 'polyline');
check('polyline is saved with its id', (await svg()).includes('<polyline id="poly1" points="100,100 200,150 300,100"'), (await svg()).slice(0, 400));

// circle
await fresh(); await tool('circle'); await click(300, 300); await move(350, 300);
eq('circle preview', await ev("$('circlePrev').getAttribute('visibility')"), 'visible');
await click(350, 300);
eq('circle centre and radius', await ev("(() => { const c = gTrace.querySelector('circle'); return [c.getAttribute('cx'), c.getAttribute('cy'), c.getAttribute('r')].join(','); })()"), '300,300,50');
eq('circle preview hidden afterwards', await ev("$('circlePrev').getAttribute('visibility')"), 'hidden');
await tool('select'); await click(350, 300);
eq('a click on the rim selects the circle', await selTags(), 'circle');
await ev('sel.clear(); selChanged()'); await click(300, 300);
eq('the centre is not a hit', await ev('sel.size'), 0);
await click(350, 300); await drag(350, 300, 380, 300);
check('radius handle', near(+(await attr('circle', 'r')), 80, 0.2), await attr('circle', 'r'));
await ev('undo()'); await drag(300, 250, 320, 270);
eq('moving a circle by its rim', [await attr('circle', 'cx'), await attr('circle', 'cy')], ['320', '320']);
await ev('undo()');
check('circle is saved with its id', (await svg()).includes('<circle id="circle1" cx="300" cy="300" r="50"'), (await svg()).slice(0, 300));

// path
await fresh(); await tool('path'); await click(100, 100); await click(200, 200); await click(300, 100); await rclick();
eq('straight path d', await attr('path', 'd'), 'M 100 100 L 200 200 L 300 100');
eq('path keeps its points', await attr('path', 'data-points'), '100,100 200,200 300,100');
await ev("$('pathSmooth').checked = true"); await tool('path'); await click(100, 300); await click(200, 400); await click(300, 300); await rclick();
r = await ev("gTrace.querySelectorAll('path')[1].getAttribute('d')");
check('smooth path uses curves and stays open', r.startsWith('M 100 300 C') && !r.includes('Z'), r);
await ev("$('pathClosed').checked = true"); await tool('path'); await click(400, 300); await click(500, 300); await click(450, 400); await rclick();
r = await ev("gTrace.querySelectorAll('path')[2].getAttribute('d')");
check('closed smooth path has three curves and closes', r.endsWith('Z') && (r.match(/C/g) || []).length === 3, r);
await ev("$('pathSmooth').checked = false"); await tool('path'); await click(400, 100); await click(500, 100); await rclick();
check('a closed path needs three points', (await count('path')) === 3 && (await toast()) === 'Click at least 3 points.', await toast());
await ev("$('pathClosed').checked = false; setTool('select'); sel.clear(); selChanged()"); await click(200, 200);
eq('a click on a straight path selects it', await selTags(), 'path');
await drag(200, 200, 220, 260);
check('dragging a path vertex rewrites points and d', (await attr('path', 'data-points')).split(' ')[1] === '220,260' && (await attr('path', 'd')).includes('220 260'), await attr('path', 'data-points'));
await ev('undo()');
eq('undo of the path vertex', (await attr('path', 'data-points')).split(' ')[1], '200,200');
await ev('sel.clear(); selChanged()'); await click(200, 400);
eq('a click on a smooth curve selects it', await ev('sel.size'), 1);
check('path flags saved', (await svg()).includes('data-smooth="false" data-closed="false"'));
await reopen();
check('paths survive open', (await count('path')) === 3 && (await ev("gTrace.querySelectorAll('path')[2].getAttribute('d').endsWith('Z')")) === true);

// symbols
await fresh(); await tool('symbol');
for (const [i, k] of ['stairs', 'rack', 'door', 'gate', 'dock', 'column', 'pallet', 'ramp', 'elevator'].entries()) {
  await ev(`$('symType').value = '${k}'; $('symType').dispatchEvent(new Event('change'))`); await click(60 + i * 75, 300);
}
eq('nine symbols with their shapes', await ev("[...gTrace.children].map(g => g.getAttribute('data-symbol') + ':' + g.children.length).join(',')"),
  'stairs:11,rack:2,door:3,gate:2,dock:3,column:1,pallet:2,ramp:5,elevator:2');
eq('symbol is sized in metres and centred', await ev("(() => { const g = gTrace.children[0]; return [g.getAttribute('data-width'), g.getAttribute('data-depth'), g.getAttribute('data-cx'), g.getAttribute('data-cy'), g.getAttribute('transform')].join('|'); })()"),
  '1.2|3|60|300|translate(60 300) rotate(0) translate(-6 -15) scale(10)');
eq('column is filled', await ev("gTrace.children[5].children[0].getAttribute('fill')"), 'currentColor');
eq('door and column are square', await ev("gTrace.children[2].getAttribute('data-depth') + '|' + gTrace.children[5].getAttribute('data-depth')"), '0.9|0.4');
r = await svg(); check('symbols are saved as named groups', r.includes('data-symbol="stairs"') && r.includes('data-symbol="elevator"') && r.includes('<path d="M0 0H1.2V3H0Z"'), r.slice(0, 300));
await tool('select'); await ev('sel.clear(); selChanged()'); await click(60, 300);
eq('a click inside a symbol selects it', await ev("[...sel].map(e => e.getAttribute('data-symbol')).join(',')"), 'stairs');
await ev('sel.clear(); selChanged()'); await click(60, 340);
eq('a click outside misses', await ev('sel.size'), 0);
await click(60, 300);
eq('symbol fields follow the selection', await ev("$('symType').value + '|' + $('symW').value + '|' + $('symD').value"), 'stairs|1.2|3');
await ev("$('symRotate').click()");
r = await ev("(() => { const g = gTrace.children[0]; return g.getAttribute('data-rot') + '|' + g.getAttribute('transform'); })()");
check('rotate by 90', r.startsWith('90|') && r.includes('rotate(90)'), r);
await ev('undo()');
eq('undo of the rotation', await ev("gTrace.children[0].getAttribute('data-rot')"), '0');
await ev("$('symW').value = '2'; $('symD').value = '4'; $('symRot').value = '180'; $('symApply').click()");
eq('apply size and rotation', await ev("(() => { const g = gTrace.children[0]; return [g.getAttribute('data-width'), g.getAttribute('data-depth'), g.getAttribute('data-rot'), g.getAttribute('transform')].join('|'); })()"), '2|4|180|translate(60 300) rotate(180) translate(-10 -20) scale(10)');
await ev('undo()');
eq('undo of apply', await ev("gTrace.children[0].getAttribute('data-width')"), '1.2');
await drag(60, 300, 80, 330);
eq('moving a symbol', await ev("gTrace.children[0].getAttribute('data-cx') + ',' + gTrace.children[0].getAttribute('data-cy')"), '80,330');
await ev('undo()');
eq('undo of the move', await ev("gTrace.children[0].getAttribute('data-cx')"), '60');
await ev("$('upm').value = '20'; $('upm').dispatchEvent(new Event('input', { bubbles: true }))");
check('units per meter rescales symbols', (await ev("gTrace.children[0].getAttribute('transform')")).includes('scale(20)'));
await ev("$('upm').value = '10'; $('upm').dispatchEvent(new Event('input', { bubbles: true }))");
await reopen();
check('symbols survive open', (await ev('gTrace.children.length')) === 9 && (await ev("gTrace.children[8].children.length")) === 2 && (await ev("gTrace.children[0].getAttribute('transform')")).includes('scale(10)'));
await ev("sel = new Set([gTrace.children[0]]); deleteSelected()");
eq('delete a symbol', await ev('gTrace.children.length'), 8);
await ev('undo()');
eq('undo of the delete', await ev('gTrace.children.length'), 9);
await ev("sel = new Set([gTrace.children[0]]); duplicateSelected()");
check('duplicate a symbol', (await ev('gTrace.children.length')) === 10 && (await ev('gTrace.lastElementChild.children.length')) === 11);
await ev("sel.clear(); $('symType').value = 'door'; $('symType').dispatchEvent(new Event('change'))");
eq('depth field is disabled for square symbols', await ev("$('symD').disabled"), true);
await ev("sel = new Set([gTrace.children[0]]); $('lineC').value = '#ff0000'; $('applyLine').click(); sel.clear(); paint()");
eq('symbol color', await ev("gTrace.children[0].getAttribute('stroke') + '|' + gTrace.children[0].getAttribute('color')"), '#ff0000|#ff0000');
r = await svg(); check('symbol color is saved', r.includes('stroke="#ff0000"') && r.includes('color="#ff0000"'));

// ---------- 3 ids on every kind ----------
await fresh(); await tool('line'); await click(100, 100); await click(200, 100);
await tool('polyline'); await click(100, 200); await click(150, 250); await click(200, 200); await rclick();
await tool('circle'); await click(300, 300); await click(340, 300);
await tool('path'); await click(400, 100); await click(450, 150); await click(500, 100); await rclick();
await ev("setTool('text'); $('textValue').value = 'T'; $('attachNew').checked = false"); await click(500, 300);
await ev("setTool('symbol'); $('symType').value = 'column'; $('symType').dispatchEvent(new Event('change'))"); await click(600, 300);
eq('every kind gets an id', await kids(), 'line:line1,polyline:poly2,circle:circle3,path:path4,text:text5,g:sym6');
eq('ids are unique', await ev('new Set([...gTrace.children].map(e => e.id)).size === gTrace.children.length'), true);
eq('every element is stamped with the layer', await ev("[...gTrace.children].every(e => e.getAttribute('data-layer') === 'Default')"), true);
r = await svg(); check('ids are saved', ['id="line1"', 'id="poly2"', 'id="circle3"', 'id="path4"', 'id="text5"', 'id="sym6"'].every(s => r.includes(s)), r.slice(0, 200));
await reopen();
eq('ids are kept after open', await kids(), 'line:line1,polyline:poly2,circle:circle3,path:path4,text:text5,g:sym6');
await ev("setTool('select'); sel = new Set([gTrace.children[0]]); duplicateSelected()");
check('a duplicate gets a new unique id', (await ev('gTrace.lastElementChild.id')) !== 'line1' && (await ev('new Set([...gTrace.children].map(e => e.id)).size === gTrace.children.length')) === true, await kids());
await ev('undo(); redo()');
eq('undo and redo keep the id', await ev('gTrace.lastElementChild.id'), 'line7');
eq('the next id continues after open', await ev("(() => { idN = 0; const d = new DOMParser().parseFromString(buildSvg(), 'image/svg+xml'); importTrace(d.querySelectorAll('#trace > *')); return idN; })()"), 7);
await selectOnly(0);
eq('the id field shows the id', await ev("$('elId').value"), 'line1');
await ev("$('elId').value = 'Wall_north'; $('applyId').click()");
eq('rename an id', await ev('gTrace.children[0].id'), 'Wall_north');
await ev("$('elId').value = '9bad'; $('applyId').click()");
check('an invalid id is refused', (await ev('gTrace.children[0].id')) === 'Wall_north' && (await toast()).startsWith('An ID starts'), await toast());
await ev("$('elId').value = 'poly2'; $('applyId').click()");
eq('a duplicate id is refused', await toast(), 'That ID is already used.');
await ev('undo()');
eq('undo of the rename', await ev('gTrace.children[0].id'), 'line1');

// ---------- 4 snapping and tracking ----------
const track = async () => { await fresh(); await ev("$('tracking').checked = true; $('snapGrid').checked = false; 1"); };
const st = () => ev('({ k: snapKind, g: guides.length, d: gGuides.children.length, sp: startPt && [startPt.x, startPt.y] })');

await track(); await add([100, 100, 200, 100]); await move(203, 300); r = await st();
check('alignment guide shown', r.k === 'align' && r.g === 1 && r.d === 1, r);
await click(203, 300); r = await st();
check('alignment snaps x exactly', r.sp && r.sp[0] === 200, r);
await track(); await add([100, 100, 200, 100], [400, 300, 400, 400]); await move(203, 303); r = await st();
check('crossing of two alignments', r.k === 'align' && r.g === 2, r);
await click(203, 303); r = await st();
check('the crossing snaps both axes', r.sp && r.sp[0] === 200 && r.sp[1] === 300, r);
await track(); await add([100, 100, 300, 100]); await click(202, 300); r = await st();
check('alignment with a midpoint', r.sp && r.sp[0] === 200, r);

await track(); await add([100, 100, 200, 100]); await move(260, 104); r = await st();
check('extension snap', r.k === 'ext' && r.g === 1, r);
await move(50, 103); r = await st();
check('extension before the start', r.k === 'ext', r);
await move(150, 104); r = await st();
check('no extension over the line itself', r.k !== 'ext', r);
await track(); await add([100, 100, 200, 100], [300, 300, 300, 200]); await click(302, 103); r = await st();
check('extension crossing', r.sp && near(r.sp[0], 300, 0.01) && near(r.sp[1], 100, 0.01), r);

await track(); await add([100, 100, 300, 100]); await click(180, 300); await move(183, 103); r = await st();
check('perpendicular snap', r.k === 'perp' && r.g === 1, r);
await click(183, 103);
eq('perpendicular line', await lines(), ['100,100,300,100', '180,300,180,100']);
await track(); await add([100, 100, 300, 100]); await tool('rect'); await click(180, 300); await move(183, 103); r = await st();
check('no perpendicular for rectangles', r.k !== 'perp', r);
await track(); await add([100, 100, 300, 100]); await click(500, 300); await move(500, 103); r = await st();
check('no perpendicular when the foot is off the line', r.k !== 'perp', r);

await track(); await add([100, 100, 200, 150]); await click(300, 300); await move(150, 125); await move(502, 404); r = await st();
check('parallel snap', r.k === 'par' && r.g === 1, r);
r = await ev('(() => { const q = drawPoint(lastP); return (q.y - 300) / (q.x - 300); })()');
check('parallel direction', near(r, 0.5, 0.005), r);
await ev('endDraw()');
eq('parallel reference cleared', await ev('parRef === null'), true);
await track(); await add([100, 100, 200, 150]); await click(300, 300); await move(502, 404); r = await st();
check('no parallel without hovering the line', r.k !== 'par', r);

await track(); await click(200, 300); await move(375, 203); r = await st();
check('polar snap', r.k === 'polar' && r.g === 1, r);
check('status shows the angle', (await ev("$('status').textContent")).includes('at 30.0°'), await ev("$('status').textContent"));
check('info box shows the angle', (await ev("[...document.querySelectorAll('#info div')].map(d => d.textContent).join(' / ')")).includes('angle 30.0°'));
await click(375, 203); r = (await lines())[0].split(',').map(Number);
check('the polar line is at 30 degrees', near(Math.atan2(-(r[3] - r[1]), r[2] - r[0]) * 180 / Math.PI, 30, 0.01), r);
for (const [name, dx, dy] of [['0', 202, 2], ['90', 2, -198], ['45', 100 * Math.cos(Math.PI / 4) + 2, -100 * Math.sin(Math.PI / 4) - 2], ['60', 100 * Math.cos(Math.PI / 3) + 2, -100 * Math.sin(Math.PI / 3) - 2], ['150', -100 * Math.cos(Math.PI / 6) - 2, -100 * Math.sin(Math.PI / 6) - 2]]) {
  await track(); await click(200, 300); await move(200 + dx, 300 + dy); r = await st();
  check('polar ' + name + ' degrees', r.k === 'polar', r);
}
await track(); await click(200, 300); await move(206, 302); r = await st();
check('no polar close to the start point', r.k !== 'polar', r);
await track(); await click(200, 300); await ev("$('orthoBtn').click()"); await move(375, 203); r = await st();
check('ortho turns tracking off while drawing', r.k === null && r.g === 0, r);

await track(); await add([100, 100, 200, 100]); await ev("$('tracking').checked = false"); await move(203, 300); r = await st();
check('tracking off: no guide', r.k === null && r.g === 0, r);
await click(203, 300); r = await st();
check('tracking off: the raw point', r.sp && r.sp[0] !== 200, r);

await track(); await add([100, 100, 200, 100]); await move(201, 102); r = await st();
check('an end snap beats the guides', r.k === 'end', r);
await track(); await add([100, 100, 203, 100]); await ev("$('snapGrid').checked = true; $('gridSize').value = '10'"); await click(205, 300); r = await st();
check('tracking beats the grid', r.sp && r.sp[0] === 203, r);

await track(); await add([100, 100, 200, 100]); await tool('rect'); await click(203, 300); r = await st();
check('a rectangle corner aligns', r.sp && r.sp[0] === 200, r);
await track(); await add([100, 100, 200, 100]); await tool('measure'); await click(203, 300); r = await st();
check('a measure point aligns', r.sp && r.sp[0] === 200, r);
await track(); await tool('dimension'); await click(200, 300); await move(375, 203); r = await st();
check('the dimension second point has polar', r.k === 'polar', r);
await track(); await add([100, 100, 200, 100]); await ev("setTool('text'); $('textValue').value = 'T'"); await click(203, 300);
eq('text aligns', await ev("gTrace.lastElementChild.getAttribute('x')"), '200');

await track(); await add([100, 100, 200, 100], [300, 300, 300, 350]); await ev("setTool('select')"); await click(150, 100); await drag(200, 100, 303, 150);
eq('a dragged line end aligns', (await lines())[0].split(',')[2], '300');
eq('guides are cleared after the drag', await ev('gGuides.children.length'), 0);
await ev('undo()');
eq('undo of the line end', (await lines())[0], '100,100,200,100');
await track(); await add([100, 100, 200, 100]); await tool('line'); await drag(203, 300, 203, 380); r = await lines();
check('a drag-drawn line starts aligned', r.length === 2 && r[1].split(',')[0] === '200', r);
await track(); await add([100, 100, 200, 100]); await move(260, 104);
eq('the snap marker is visible for an extension', await ev("$('snapMark').getAttribute('visibility')"), 'visible');
await tool('line');
eq('guides hide on a tool change', await ev('gGuides.children.length'), 0);

await track(); await ev("(() => { for (let i = 0; i < 400; i++) gTrace.appendChild(mkLine(i * 2, 0, i * 2, 600)); paint(); })()");
{ const t0 = Date.now(); for (let i = 0; i < 20; i++) await move(100 + i, 300 + i); const dt = (Date.now() - t0) / 20; check('400 lines: under 120 ms per mouse move', dt < 120, dt); }

// ---------- 5 select, edit, arrange ----------
await fresh(); await add([0, 0, 100, 0], [0, 50, 100, 50]);
await ev("selectAll(); $('lineW').value = '3'; $('lineC').value = '#ff0000'; $('applyLine').click(); sel.clear(); paint();");
eq('apply style to all lines', await styles(), '#ff0000/3,#ff0000/3');
check('the style is saved', (await svg()).includes('stroke="#ff0000" stroke-width="3"'));
await ev('undo()');
eq('undo of the style', await styles(), '#000000/1.5,#000000/1.5');
await ev('redo()');
await ev("(() => { const doc = new DOMParser().parseFromString(buildSvg(), 'image/svg+xml'); importTrace(doc.querySelectorAll('#trace > *')); })()");
eq('the style survives open', await colors(), '#ff0000/3,#ff0000/3');
await fresh(); await add([0, 0, 10, 0]);
await ev("selectAll(); $('lineC').value = '#00ff00'; $('applyLine').click(); sel.clear(); paint(); autosave(); importTrace([]); restore();");
eq('the style survives autosave', await ev("gTrace.children[0] && gTrace.children[0].getAttribute('data-color')"), '#00ff00');

await fresh(); await add([0, 0, 10, 0], [0, 5, 10, 5]); await ev('document.activeElement && document.activeElement.blur()'); await key('a', 2);
eq('Ctrl+A selects all', await ev('sel.size'), 2);

await fresh(); await add([100, 100, 150, 100]); await ev("$('orthoBtn').click(); setTool('select')"); await click(125, 100); await drag(125, 100, 165, 110);
eq('an ortho move keeps the dominant axis', await lines(), ['140,100,190,100']);
await fresh(); await add([100, 100, 200, 100]); await ev("setTool('select')"); await click(150, 100); await ev("$('orthoBtn').click()"); await drag(200, 100, 300, 110);
eq('an ortho handle drag keeps the line level', await lines(), ['100,100,300,100']);

await fresh(); await add([100, 100, 150, 100], [130, 200, 200, 200], [50, 300, 90, 300]);
await ev("selectAll(); arrange('left')");
eq('align left', await lines(), ['50,100,100,100', '50,200,120,200', '50,300,90,300']);
await ev('undo()');
eq('undo of the alignment', await lines(), ['100,100,150,100', '130,200,200,200', '50,300,90,300']);
await ev("arrange('distx')");
eq('distribute horizontally', await lines(), ['92.5,100,142.5,100', '130,200,200,200', '50,300,90,300']);
await ev("undo(); arrange('centery')"); r = await lines();
check('centre vertically', r.every(s => s.split(',')[1] === '200' && s.split(',')[3] === '200'), r);
await fresh(); await add([100, 100, 200, 100]); await ev("gTrace.appendChild(mkText(150, 200, 'abc', 20)); paint(); selectAll(); arrange('left')");
eq('a text aligns with a line', await ev("[gTrace.children[1].getAttribute('x'), gTrace.children[1].getAttribute('y')].join(',')"), '100,200');
await ev('undo()');
eq('undo of the text alignment', await ev("gTrace.children[1].getAttribute('x')"), '150');
await fresh(); await add([0, 0, 50, 0]); await ev("sel.clear(); arrange('left')");
eq('align needs two elements', await toast(), 'Select at least two elements.');
await ev("selectAll(); arrange('distx')");
eq('distribute needs three elements', await toast(), 'Select at least three elements.');

await fresh(); await add([0, 0, 50, 0], [50, 0, 100, 0], [80, 0, 150, 0], [0, 10, 10, 10]);
await ev('sel.clear(); joinCollinear()');
eq('join collinear lines', await lines(), ['0,0,150,0', '0,10,10,10']);
await ev('undo()');
eq('undo of the join', await lines(), ['0,0,50,0', '50,0,100,0', '80,0,150,0', '0,10,10,10']);
await ev('redo()');
eq('redo of the join', await lines(), ['0,0,150,0', '0,10,10,10']);
await fresh(); await add([0, 0, 50, 0], [60, 0, 100, 0]); await ev('joinCollinear()');
check('a gap is not joined', (await toast()) === 'Nothing to join.' && (await lines()).length === 2);
await fresh(); await add([0, 0, 50, 0], [50, 0, 100, 0], [100, 0, 150, 0]); await ev('sel = new Set([gTrace.children[0], gTrace.children[1]]); joinCollinear()');
eq('join only within the selection', await lines(), ['0,0,100,0', '100,0,150,0']);
await fresh(); await add([0, 0, 50, 0]); await ev("gTrace.appendChild(mkLine(50, 0, 100, 0, { w: 1.5, c: '#ff0000' })); paint(); sel.clear(); joinCollinear()");
check('different colors are not joined', (await lines()).length === 2 && (await toast()) === 'Nothing to join.');
await fresh(); await add([0, 0, 50, 0], [50.005, 0.004, 100, 0]); await ev('joinCollinear()');
eq('join within the tolerance', await lines(), ['0,0,100,0']);
await fresh(); await add([0, 0, 50, 0], [0, 5, 50, 5]); await ev('joinCollinear()');
eq('parallel lines are not joined', (await lines()).length, 2);
await fresh(); await add([0, 0, 50, 50], [50, 50, 100, 100]); await ev('joinCollinear()');
eq('a diagonal join', await lines(), ['0,0,100,100']);

await fresh(); await add([0, 0, 100, 0]); await ev("$('offDist').value = '1'; setTool('select')"); await click(50, 0); await tool('offset'); await click(50, 50);
eq('offset to the clicked side', await lines(), ['0,0,100,0', '0,10,100,10']);
await ev('undo()');
eq('undo of the offset', (await lines()).length, 1);
await fresh(); await add([0, 0, 50, 0]); await tool('offset'); await ev('sel.clear()'); await click(25, 20);
check('offset needs a selection', (await toast()).startsWith('Select the lines first'), await toast());

await fresh(); await add([0, 100, 300, 100], [100, 0, 100, 200], [200, 0, 200, 200]); await tool('trim'); await click(150, 100); r = await lines();
check('trim the middle between two crossings', r.length === 4 && r[0] === '0,100,100,100' && r[3] === '200,100,300,100', r);
await ev('undo()'); r = await lines();
check('undo of the trim', r.length === 3 && r[0] === '0,100,300,100', r);
await click(250, 100); r = await lines();
check('trim the end part', r[0] === '0,100,200,100' && r.length === 3, r);
await fresh(); await add([0, 0, 50, 0]); await tool('trim'); await click(25, 0);
eq('trim without a crossing', await toast(), 'No crossing line to trim at.');
await click(500, 500);
eq('trim on empty space', await toast(), 'Click a line.');

await fresh(); await add([0, 0, 50, 0], [100, -50, 100, 50]); await tool('extend'); await click(40, 0);
eq('extend to the next line', (await lines())[0], '0,0,100,0');
await ev('undo()');
eq('undo of the extend', (await lines())[0], '0,0,50,0');
await fresh(); await add([0, 0, 50, 0]); await tool('extend'); await click(25, 0);
eq('extend without a target', await toast(), 'No line to extend to.');

// ---------- 6 text attached to elements ----------
await fresh(); await tool('line'); await click(100, 100); await click(300, 100);
await ev("setTool('text'); $('textValue').value = 'Wall'; $('fontSize').value = '12'"); await click(200, 100);
eq('a text clicked on a line is attached', await ev("(() => { const e = gTrace.querySelector('text'); return [e.getAttribute('data-for'), e.getAttribute('x'), e.getAttribute('y'), e.getAttribute('text-anchor'), e.hasAttribute('transform')].join('|'); })()"), 'line1|200|94|middle|false');
await ev("setTool('text'); $('attachNew').checked = false"); await click(400, 400);
eq('a text is free when the option is off', await ev("gTrace.lastElementChild.hasAttribute('data-for')"), false);
await ev("$('attachNew').checked = true; sel.clear(); selChanged(); setTool('select')");
await click(250, 100); await selectOnly(0); await drag(150, 100, 150, 160);
eq('the text follows a moved line', await ev("(() => { const e = gTrace.querySelector('text'); return [e.getAttribute('x'), e.getAttribute('y')].join(','); })()"), '200,154');
await ev('undo()');
eq('undo of the move', await ev("gTrace.querySelector('text').getAttribute('y')"), '94');
await selectOnly(0); await drag(300, 100, 300, 160);
r = await ev("(() => { const e = gTrace.querySelector('text'); return [e.getAttribute('x'), e.getAttribute('y'), e.getAttribute('transform')].join('|'); })()");
check('the text follows a line end and turns along the line', r.startsWith('200|') && r.includes('rotate(') && near(+r.split('|')[1], 124, 3), r);
await ev('undo()');
await ev("sel = new Set([gTrace.querySelector('text')]); selChanged()"); await drag(200, 94, 230, 70);
eq('dragging the text changes only its offset', await ev("(() => { const e = gTrace.querySelector('text'); return [e.getAttribute('data-dx'), e.getAttribute('data-dy'), e.getAttribute('x'), e.getAttribute('y')].join(','); })()"), '30,-30,230,70');
await ev('undo()');
await ev("sel = new Set([gTrace.children[0], gTrace.querySelector('text')]); selChanged()"); await drag(150, 100, 150, 140);
eq('a text selected with its line moves once', await ev("(() => { const e = gTrace.querySelector('text'); return e.getAttribute('data-dx') + ',' + e.getAttribute('y'); })()"), '0,134');
await ev('undo()');
await ev("sel = new Set([gTrace.children[0]]); deleteSelected()");
check('deleting the line deletes its text', (await count('text[data-for]')) === 0 && (await ev('gTrace.children.length')) === 1, await kids());
await ev('undo()');
check('undo brings both back', (await ev('gTrace.children.length')) === 3 && (await count('text[data-for]')) === 1, await kids());
await ev("sel = new Set([gTrace.children[0], gTrace.querySelector('text')]); duplicateSelected()");
r = await ev("[...gTrace.querySelectorAll('text[data-for]')].map(e => e.getAttribute('data-for')).join(',')");
check('a duplicate text stays attached to the duplicate line', r.startsWith('line1,') && r.split(',')[1] !== 'line1' && r.split(',').length === 2, r);
await ev("sel = new Set([gTrace.lastElementChild]); selChanged(); duplicateSelected()");
eq('the duplicate of a text alone is free', await ev("gTrace.lastElementChild.hasAttribute('data-for')"), false);
await ev('undo(); undo(); undo()');
await ev("sel = new Set([gTrace.querySelector('text')]); selChanged(); $('detachText').click()");
eq('detach a text', await ev("gTrace.querySelector('text').hasAttribute('data-for')"), false);
await ev('undo()');
eq('undo of the detach', await ev("gTrace.querySelector('text').getAttribute('data-for')"), 'line1');
await ev("sel = new Set([gTrace.querySelector('text')]); selChanged(); $('detachText').click(); sel = new Set([gTrace.children[0], gTrace.querySelector('text')]); selChanged(); $('attachText').click()");
eq('attach by button', await ev("gTrace.querySelector('text').getAttribute('data-for')"), 'line1');
await ev("sel = new Set([gTrace.children[0]]); selChanged(); $('attachText').click()");
eq('attach needs a text and an element', await toast(), 'Select one text and one element to attach it to.');
r = await svg(); check('the attachment is saved', /<text id="text\d+" data-for="line1" data-dx="0" data-dy="-6" x="200" y="94" font-size="12" fill="#000" text-anchor="middle">Wall<\/text>/.test(r), r.slice(0, 600));
await reopen();
eq('the attachment survives open', await ev("gTrace.querySelector('text[data-for]').getAttribute('data-for')"), 'line1');
await ev("sel = new Set([gTrace.children[0]]); selChanged(); $('elId').value = 'Wall_1'; $('applyId').click()");
eq('renaming an id keeps the attachment', await ev("gTrace.querySelector('text[data-for]')?.getAttribute('data-for')"), 'Wall_1');
await ev('undo()');
eq('undo of the rename restores the attachment', await ev("gTrace.querySelector('text[data-for]').getAttribute('data-for')"), 'line1');

await fresh(); await tool('circle'); await click(300, 300); await click(340, 300);
await ev("setTool('text'); $('textValue').value = 'Tank'"); await click(340, 300);
eq('a text on a circle sits at its centre', await ev("gTrace.querySelector('text').getAttribute('x') + ',' + gTrace.querySelector('text').getAttribute('y')"), '300,300');
await fresh(); await tool('polyline'); await click(100, 100); await click(200, 100); await click(200, 200); await rclick();
await ev("setTool('text'); $('textValue').value = 'P'"); await click(200, 100);
eq('a text on a polyline', await ev("gTrace.querySelector('text').getAttribute('data-for')"), 'poly1');
await fresh(); await ev("setTool('symbol'); $('symType').value = 'pallet'; $('symType').dispatchEvent(new Event('change'))"); await click(300, 300);
await ev("setTool('text'); $('textValue').value = 'Pal'"); await click(300, 300);
eq('a text on a symbol', await ev("gTrace.querySelector('text').getAttribute('data-for')"), 'sym1');

// ---------- 7 history over a mixed sequence ----------
await fresh(); await add([0, 100, 300, 100], [100, 0, 100, 200], [200, 0, 200, 200]);
const s0 = JSON.stringify(await lines());
await tool('trim'); await click(150, 100);
await ev("selectAll(); arrange('left')"); await ev('sel.clear(); joinCollinear()');
await ev("setTool('select'); sel = new Set([gTrace.children[0]]); $('offDist').value = '1'; setTool('offset')"); await click(50, 150);
const s1 = JSON.stringify(await lines()), n = await ops();
for (let i = 0; i < n; i++) await ev('undo()');
check('undoing every step returns the start', JSON.stringify(await lines()) === s0, await lines());
for (let i = 0; i < n; i++) await ev('redo()');
check('redoing every step returns the end', JSON.stringify(await lines()) === s1, await lines());

// ---------- 8 layers against drawing, picking, selecting and snapping ----------
await fresh(); await tool('line'); await click(100, 100); await click(300, 100);
eq('one layer to start', await ev("layers.map(l => l.name).join(',') + '|' + $('layerSel').options.length"), 'Default|1');
await ev("$('layerName').value = 'Walls'; $('layerAdd').click()");
eq('add a layer', await ev("layers.map(l => l.name).join(',') + '|' + activeLayer"), 'Default,Walls|Walls');
await click(100, 200); await click(300, 200);
eq('a new element goes to the active layer', await ev("gTrace.lastElementChild.getAttribute('data-layer')"), 'Walls');
await ev("$('layerName').value = 'Walls'; $('layerAdd').click()");
eq('a duplicate layer name is refused', await toast(), 'A layer with that name exists.');
await ev("$('layerVis').checked = false; $('layerVis').dispatchEvent(new Event('change'))");
eq('a hidden layer hides its elements', await ev("gTrace.lastElementChild.getAttribute('display') + '|' + gTrace.children[0].getAttribute('display')"), 'none|inline');
await ev("setTool('select')"); await click(200, 200);
eq('hidden elements cannot be picked', await ev('sel.size'), 0);
await ev("selectAll()");
eq('select all skips hidden layers', await ev('sel.size'), 1);
await ev("sel.clear(); setTool('line')"); await click(100, 300); await click(300, 300);
check('drawing on a hidden layer is refused', (await toast()) === 'The active layer is hidden or locked.' && (await ev('gTrace.children.length')) === 2);
await ev('endDraw()');
await ev("$('layerVis').checked = true; $('layerVis').dispatchEvent(new Event('change'))"); await tool('select'); await click(200, 200);
eq('visible again', await ev('sel.size'), 1);
await ev("$('layerLock').checked = true; $('layerLock').dispatchEvent(new Event('change'))");
eq('locking deselects', await ev('sel.size'), 0);
await click(200, 200);
eq('locked elements cannot be picked', await ev('sel.size'), 0);
await drag(50, 150, 350, 250);
eq('the rubber band skips locked layers', await ev('sel.size'), 0);
await ev('selectAll()');
eq('select all skips locked layers', await ev('sel.size'), 1);
await ev("sel.clear(); setTool('line')"); await click(100, 300); await click(300, 300);
eq('drawing on a locked layer is refused', await toast(), 'The active layer is hidden or locked.');
await ev("endDraw(); $('layerLock').checked = false; $('layerLock').dispatchEvent(new Event('change'))");
await ev("$('layerSel').value = 'Default'; $('layerSel').dispatchEvent(new Event('change'))");
eq('switch the active layer', await ev('activeLayer'), 'Default');
await ev("sel = new Set([gTrace.children[1]]); selChanged(); $('layerSel').value = 'Default'; $('toLayer').click()");
eq('move the selection to a layer', await ev("gTrace.children[1].getAttribute('data-layer')"), 'Default');
await ev('undo()');
eq('undo of the move to a layer', await ev("gTrace.children[1].getAttribute('data-layer')"), 'Walls');
await ev("$('layerSel').value = 'Walls'; $('layerSel').dispatchEvent(new Event('change')); $('layerName').value = 'Outer walls'; $('layerRename').click()");
eq('rename a layer', await ev("layers.map(l => l.name).join(',') + '|' + gTrace.children[1].getAttribute('data-layer')"), 'Default,Outer walls|Outer walls');
await ev("$('layerLock').checked = true; $('layerLock').dispatchEvent(new Event('change')); $('layerName').value = 'Empty'; $('layerAdd').click(); $('layerVis').checked = false; $('layerVis').dispatchEvent(new Event('change'))");
r = await svg();
check('layers are saved as groups with their state', r.includes('<g data-layer="Default">') && r.includes('<g data-layer="Outer walls" data-locked="true">') && r.includes('<g data-layer="Empty" display="none">'), r.slice(r.indexOf('id="trace"'), r.indexOf('id="trace"') + 500));
check('layer order in the file', r.indexOf('data-layer="Default"') < r.indexOf('data-layer="Outer walls"') && r.indexOf('data-layer="Outer walls"') < r.indexOf('data-layer="Empty"'));
check('elements sit inside their layer group', /<g data-layer="Outer walls" data-locked="true">\s*<line id="line2"/.test(r), r.slice(r.indexOf('Outer walls') - 20, r.indexOf('Outer walls') + 200));
await reopen();
const layerState = "layers.map(l => l.name + ':' + l.visible + ':' + l.locked).join(',')";
eq('layers survive open', await ev(layerState), 'Default:true:false,Outer walls:true:true,Empty:false:false');
eq('the layer list shows the state', await ev("[...$('layerSel').options].map(o => o.textContent).join(',')"), 'Default,Outer walls (locked),Empty (hidden)');
await ev('autosave(); layers = []; importTrace([]); restore()');
check('autosave restores layers', (await ev("layers.map(l => l.name).join(',')")) === 'Default,Outer walls,Empty' && (await ev('gTrace.children.length')) === 2, await ev("layers.map(l => l.name).join(',')"));
await ev("$('layerSel').value = 'Outer walls'; $('layerSel').dispatchEvent(new Event('change')); $('layerDel').click()");
check('deleting a layer moves its elements', (await ev("layers.map(l => l.name).join(',')")) === 'Default,Empty' && (await ev("gTrace.children[1].getAttribute('data-layer')")) === 'Default');
await ev("$('layerSel').value = 'Empty'; $('layerSel').dispatchEvent(new Event('change')); $('layerDel').click(); $('layerDel').click()");
check('the last layer stays', (await ev('layers.length')) === 1 && (await toast()) === 'The last layer cannot be deleted.');

await fresh(); await tool('line'); await click(100, 100); await click(300, 100);
await ev("$('layerName').value = 'Hide'; $('layerAdd').click(); sel = new Set([gTrace.children[0]]); $('layerSel').value = 'Hide'; $('toLayer').click()");
await setLayer('Hide', false, false);
await move(301, 101);
eq('snapping ignores hidden lines', await ev('snapKind'), null);
await setLayer('Hide', true, false); await tool('line'); await move(301, 101);
eq('snapping sees visible lines', await ev('snapKind'), 'end');

// ---------- 9 every kind together ----------
await fresh(); await tool('line'); await click(100, 100); await click(200, 100); await tool('circle'); await click(300, 300); await click(330, 300);
await tool('polyline'); await click(400, 100); await click(450, 150); await rclick();
await ev("setTool('symbol'); $('symType').value = 'column'; $('symType').dispatchEvent(new Event('change'))"); await click(500, 300);
await ev("setTool('select'); sel.clear(); selChanged()"); await drag(50, 50, 600, 400);
eq('the rubber band selects every kind', await ev('sel.size'), 4);
await ev('sel.clear(); selChanged(); selectAll()');
eq('select all takes every kind', await ev('sel.size'), 4);
await ev("arrange('top')"); r = await ev("[...sel].map(e => Math.round(bboxOf(e).y)).join(',')");
check('align top across kinds', new Set(r.split(',')).size === 1, r);
await ev('undo()');
check('undo of the alignment across kinds', new Set((await ev("[...sel].map(e => Math.round(bboxOf(e).y)).join(',')")).split(',')).size > 1);
await ev("$('lineW').value = '4'; $('lineC').value = '#0000ff'; $('applyLine').click()");
eq('style applies to every shape kind', await colors(), '#0000ff/4,#0000ff/4,#0000ff/4,#0000ff/4');
await ev('sel.clear(); paint()');
eq('every kind is saved with its style', ((await svg()).match(/stroke="#0000ff" stroke-width="4"/g) || []).length, 4);

await t.finish();
