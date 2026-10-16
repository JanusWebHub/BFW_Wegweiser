// What the tool writes and reads: the plan SVG layout, save, open, older and foreign files, autosave, New, reload, PNG export.
// Reloads the page, so it runs on its own page.
import { launch, parseArgs, same } from './harness.mjs';

const t = await launch('files', parseArgs(process.argv));
const { ev, click, rclick, eq, check, lines, toast, kids, svg, setField, mkU, openText } = t;

const fresh = async () => { await t.reset(); await ev("$('tracking').checked = false; 1"); };
const tool = n => ev(`setTool('${n}')`);
const A = s => s.split(' ').sort().join(' ');
// Structure of the plan SVG the tool would write now: root attributes, top groups, and per element its tag and attribute names
const describe = () => ev(`(() => {
  const doc = new DOMParser().parseFromString(buildSvg(), 'image/svg+xml'), root = doc.documentElement;
  const names = e => [...e.attributes].map(a => a.name).sort().join(' ');
  const attrs = {}; for (const a of root.attributes) attrs[a.name] = a.value;
  const el = e => e.tagName + ':' + names(e) + (e.tagName === 'g' ? ' [' + [...e.children].map(c => c.tagName + ':' + names(c)).join('; ') + ']' : '');
  return {
    root: attrs,
    top: [...root.children].map(e => e.id),
    underlays: [...doc.querySelector('#underlays').children].map(e => e.tagName + ':' + names(e)),
    layers: [...doc.querySelector('#trace').children].map(g => ({ tag: g.tagName, attrs: names(g), els: [...g.children].map(el) })),
    image: (i => i ? Object.fromEntries([...i.attributes].map(a => [a.name, a.value])) : null)(doc.querySelector('#underlays image'))
  };
})()`);
const blueIn = (x0, y0, x1, y1) => ev(`(async () => {
  const bm = await createImageBitmap(window.__saved.d), c = document.createElement('canvas'); c.width = bm.width; c.height = bm.height;
  const x = c.getContext('2d'); x.drawImage(bm, 0, 0);
  const d = x.getImageData(${x0}, ${y0}, ${x1 - x0}, ${y1 - y0}).data; let n = 0;
  for (let i = 0; i < d.length; i += 4) if (d[i] < 60 && d[i + 1] < 60 && d[i + 2] > 150) n++;
  return n;
})()`);

// One of every kind on two layers, a hidden layer, a locked layer, and an underlay. plain: keep the default floor values.
const scene = async ({ plain = false } = {}) => {
  await fresh();
  if (!plain) for (const [id, v] of [['floorId', 'OG1'], ['level', '1'], ['fx', '10'], ['fy', '20'], ['fw', '800'], ['fh', '600'], ['upm', '20']]) await setField(id, v);
  await tool('line'); await click(100, 100); await click(300, 100);
  await tool('polyline'); await click(100, 200); await click(150, 250); await click(200, 200); await rclick();
  await tool('circle'); await click(400, 200); await click(430, 200);
  await ev("$('pathSmooth').checked = true"); await tool('path'); await click(500, 100); await click(550, 150); await click(600, 100); await rclick();
  await ev("$('pathSmooth').checked = false; setTool('text'); $('textValue').value = 'Wall'"); await click(200, 100);
  await ev("setTool('symbol'); $('symType').value = 'column'; $('symType').dispatchEvent(new Event('change'))"); await click(600, 300);
  await ev("$('layerName').value = 'Notes'; $('layerAdd').click()");
  await tool('line'); await click(100, 300); await click(300, 300);
  await ev("$('layerVis').checked = false; $('layerVis').dispatchEvent(new Event('change'))");
  await ev("$('layerName').value = 'Frozen'; $('layerAdd').click(); $('layerLock').checked = true; $('layerLock').dispatchEvent(new Event('change'))");
  await ev("$('layerSel').value = 'Default'; $('layerSel').dispatchEvent(new Event('change'))");
};
const addUnderlay = async () => {
  await mkU('plan.png', '#c8d8e8');
  await ev("Object.assign(unders[0], { x: 50, y: 60, rot: -12, scale: 3, opacity: 0.6, label: 'Ground floor', bright: 1.2, flipX: true, crop: { x: 0, y: 0, w: 100, h: 80 } }); renderU(unders[0]); syncControls(); changed(); 1");
};
let r;

// ---------- 1 the layout of the plan SVG ----------
await scene(); await addUnderlay();
const d = await describe();
eq('root attributes', d.root, { xmlns: 'http://www.w3.org/2000/svg', viewBox: '10 20 800 600', 'data-floor-id': 'OG1', 'data-level': '1', 'data-units-per-meter': '20' });
eq('underlays come before the trace', d.top, ['underlays', 'trace']);
eq('a crop gives a clip path, then the image', d.underlays, ['defs:', 'image:' + A('href width height transform opacity data-label data-brightness clip-path data-x data-y data-rotation data-scale data-flip-x data-crop')]);
eq('the placement of the image', ['href', 'opacity', 'data-x', 'data-y', 'data-rotation', 'data-scale', 'data-label', 'data-brightness', 'data-flip-x', 'data-crop'].map(k => d.image[k]), ['plan.png', '0.6', '50', '60', '-12', '3', 'Ground floor', '1.2', 'true', '0 0 100 80']);
eq('one group per layer, in order, with their state', d.layers.map(l => l.tag + ':' + l.attrs), ['g:' + A('data-layer'), 'g:' + A('data-layer display'), 'g:' + A('data-layer data-locked')]);
const style = 'fill stroke stroke-width vector-effect';
eq('the elements of the first layer and their attributes', d.layers[0].els, [
  'line:' + A('id x1 y1 x2 y2 stroke stroke-width vector-effect'),
  'polyline:' + A('id points ' + style),
  'circle:' + A('id cx cy r ' + style),
  'path:' + A('id d data-points data-smooth data-closed ' + style),
  'text:' + A('id data-for data-dx data-dy x y font-size fill text-anchor'),
  'g:' + A('id data-symbol data-cx data-cy data-rot data-width data-depth transform fill stroke stroke-width color') + ' [path:' + A('d fill vector-effect') + ']'
]);
eq('the hidden layer holds its line', d.layers[1].els, ['line:' + A('id x1 y1 x2 y2 stroke stroke-width vector-effect')]);
eq('the locked layer is empty', d.layers[2].els, []);
eq('every element has its id', await ev("[...new DOMParser().parseFromString(buildSvg(), 'image/svg+xml').querySelectorAll('#trace [id]')].map(e => e.id).join(',')"), 'line1,poly2,circle3,path4,text5,sym6,line7');
eq('the attached text names its element', await ev("new DOMParser().parseFromString(buildSvg(), 'image/svg+xml').querySelector('#trace text').getAttribute('data-for')"), 'line1');

// ---------- 2 save and open ----------
const built = await svg();
let s = await t.captureSave("$('save').click()");
eq('save offers <floor id>-plan.svg', s && s.name, 'OG1-plan.svg');
eq('the saved text is the built text', await t.savedText(), built);
eq('save clears the unsaved flag', await ev('dirty'), false);
eq('save says so', await toast(), 'Saved.');
await ev("$('includeUnder').checked = false");
await t.captureSave("$('save').click()");
check('without the underlay reference there is no image', !(await t.savedText()).includes('<image'));
await ev("$('includeUnder').checked = true");
await openText(built);
eq('opening says to pick the images again', await toast(), 'Opened. Pick the underlay images again: plan.png');
const again = await svg();
check('opening and saving again gives the same file', again === built, (() => { let i = 0; while (i < built.length && built[i] === again[i]) i++; return { at: i, was: built.slice(Math.max(0, i - 30), i + 60), now: again.slice(Math.max(0, i - 30), i + 60) }; })());
eq('opening restores the floor values', await ev("['floorId', 'level', 'fx', 'fy', 'fw', 'fh', 'upm'].map(id => $(id).value).join(',')"), 'OG1,1,10,20,800,600,20');
eq('opening clears the unsaved flag', await ev('dirty'), false);
await mkU('plan.png', '#c8d8e8');
check('picking the image again keeps the placement', (await ev('unders.length')) === 1 && (await ev('!!unders[0].url')) === true && same(await ev('[unders[0].x, unders[0].y, unders[0].rot, unders[0].scale, unders[0].label]'), [50, 60, -12, 3, 'Ground floor']), await ev('[unders.length, unders[0].x, unders[0].y, unders[0].rot, unders[0].scale, unders[0].label]'));

await fresh(); await setField('fw', '0');
await ev("window.__saved = null; 1");
await ev("$('save').click()"); await t.sleep(300);
check('save refuses a zero frame', (await toast()).startsWith('Cannot save: the frame width and height must be above zero') && (await ev('window.__saved')) === null, await toast());
await setField('fw', '1000'); await setField('floorId', ' ');
await ev("$('save').click()"); await t.sleep(300);
check('save refuses an empty floor id', (await toast()).includes('the floor ID is empty'), await toast());
await setField('floorId', 'EG'); await setField('upm', '0');
await ev("$('save').click()"); await t.sleep(300);
check('save refuses zero units per meter', (await toast()).includes('units per meter must be above zero'), await toast());

// ---------- 3 older and foreign files ----------
await fresh();
await openText('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" data-floor-id="UG1" data-level="-1" data-units-per-meter="5"><g id="trace"><line x1="0" y1="0" x2="10" y2="0"/></g></svg>');
eq('an older flat file opens', await ev("['floorId', 'level', 'fx', 'fy', 'fw', 'fh', 'upm'].map(id => $(id).value).join(',') + '|' + layers.map(l => l.name).join(',') + '|' + gTrace.children.length"), 'UG1,-1,0,0,500,300,5|Default|1');
eq('opening a file with no underlay says only Opened', await toast(), 'Opened.');
await openText('hello');
eq('a file that is not an SVG is refused', await toast(), 'Not an SVG file.');

await fresh();
r = await ev(`(() => {
  const doc = new DOMParser().parseFromString('<svg xmlns="http://www.w3.org/2000/svg"><g id="trace"><line x1="0" y1="0" x2="10" y2="0" stroke="#000" stroke-width="1.5"/><line id="a1" x1="0" y1="1" x2="10" y2="1"/><line id="a1" x1="0" y1="2" x2="10" y2="2" onclick="alert(1)"/><text x="1" y="1" font-size="5" onmouseover="alert(2)">t</text><script>x</script><rect/></g></svg>', 'image/svg+xml');
  importTrace(doc.querySelectorAll('#trace > *'));
  return [layers.map(l => l.name).join(','), [...gTrace.children].map(e => e.tagName + ':' + e.id).join(','), [...gTrace.querySelectorAll('*')].some(e => e.hasAttribute('onclick') || e.hasAttribute('onmouseover'))].join('|');
})()`);
eq('foreign content is dropped, ids are made unique, scripts never reach the drawing', r, 'Default|line:line1,line:a1,line:line2,text:text3|false');
r = await ev(`(() => {
  const doc = new DOMParser().parseFromString('<svg xmlns="http://www.w3.org/2000/svg"><g id="trace"><line x1="0" y1="0" x2="5" y2="0"/><line x1="0" y1="1" x2="5" y2="1" stroke="javascript:x" stroke-width="-2"/><line x1="0" y1="2" x2="5" y2="2" stroke="#0a0" stroke-width="2"/></g></svg>', 'image/svg+xml');
  importTrace(doc.querySelectorAll('#trace > *'));
  return [...gTrace.children].map(l => l.getAttribute('data-color') + '/' + l.getAttribute('stroke-width')).join(',');
})()`);
eq('missing and unsafe colors and widths fall back to the defaults', r, '#000/1.5,#000/1.5,#0a0/2');
await ev("sel = new Set([gTrace.children[2]]); selChanged()");
eq('the line fields follow the selection', await ev("$('lineW').value + '|' + $('lineC').value"), '2|#00aa00');
await ev('duplicateSelected()');
check('a duplicate keeps the style', (await ev("gTrace.children[3].getAttribute('data-color') + '/' + gTrace.children[3].getAttribute('stroke-width')")) === '#0a0/2' && (await ev('gTrace.children.length')) === 4);

// ---------- 4 autosave, New, reload ----------
await scene(); await addUnderlay();
eq('an edit sets the unsaved flag', await ev('dirty'), true);
await ev('autosave(); 1'); await t.reload();
eq('reload restores the drawing', await kids(), 'line:line1,polyline:poly2,circle:circle3,path:path4,text:text5,g:sym6,line:line7');
eq('reload restores the layers and their state', await ev("layers.map(l => l.name + ':' + l.visible + ':' + l.locked).join(',')"), 'Default:true:false,Notes:false:false,Frozen:true:true');
eq('reload restores the floor values', await ev("['floorId', 'level', 'fx', 'fy', 'fw', 'fh', 'upm'].map(id => $(id).value).join(',')"), 'OG1,1,10,20,800,600,20');
check('reload restores the underlay placement but not the image', (await ev('unders.length')) === 1 && (await ev('!!unders[0].url')) === false && (await ev('unders[0].label + "|" + unders[0].rot')) === 'Ground floor|-12');
check('reload says what it restored', (await toast()).startsWith('Restored the autosave') && (await toast()).includes('Pick the underlay images again'), await toast());
eq('a restored drawing counts as unsaved', await ev('dirty'), true);

await ev("$('newDoc').click()");
eq('New asks first', await ev("$('newDoc').textContent"), 'Really clear?');
await ev("$('newDoc').click()");
check('New clears the drawing, layers and underlays', (await ev('gTrace.children.length')) === 0 && (await ev("layers.map(l => l.name).join(',')")) === 'Default' && (await ev('unders.length')) === 0);
eq('New says so and clears the unsaved flag', (await toast()) + '|' + (await ev('dirty')), 'Cleared.|false');
await t.reload();
eq('a reload straight after New restores nothing', await ev('gTrace.children.length + "|" + unders.length'), '0|0');

await fresh(); await click(800, 500); await t.move(900, 560);
await ev("$('newDoc').click(); $('newDoc').click()");
check('New cancels a pending line', (await ev('startPt === null')) === true && (await ev("$('preview').getAttribute('visibility')")) === 'hidden' && (await ev("$('snapMark').getAttribute('visibility')")) === 'hidden');
await click(800, 500);
eq('the first click after New starts a line instead of ending one', (await lines()).length, 0);

// ---------- 5 PNG export ----------
await fresh();
await ev("gTrace.appendChild(mkLine(100, 350, 900, 350, { w: 6, c: '#ff0000' })); gTrace.appendChild(mkText(100, 100, 'Hi', 40)); paint(); 1");
s = await t.captureSave("$('exportPng').click()");
eq('the PNG is named after the floor id', s && s.name, 'EG-preview.png');
r = await t.savedImage([[1000, 700], [1000, 660], [1000, 100], [300, 1100]]);
eq('the PNG is twice the frame, with the red line and white around it', [r.w, r.h, r.px], [2000, 1400, ['255,0,0', '255,255,255', '255,255,255', '255,255,255']]);
r = await t.savedImage(Array.from({ length: 200 }, (_, i) => [1000, 600 + i]));
check('a line of thickness 6 is about 8 pixels thick in the PNG', (() => { const n = r.px.filter(p => +p.split(',')[1] < 128).length; return n >= 7 && n <= 9; })(), r.px.filter(p => +p.split(',')[1] < 128).length);
await setField('fw', '0');
await ev("$('exportPng').click()"); await t.sleep(300);
eq('export refuses a zero frame', await toast(), 'Cannot export: the frame width and height must be above zero.');

await fresh();
await ev("gTrace.appendChild(mkLine(100, 100, 300, 100, { w: 6, c: '#000000' })); $('layerName').value = 'Hide'; $('layerAdd').click(); gTrace.appendChild(mkLine(100, 150, 300, 150, { w: 6, c: '#000000' })); $('layerVis').checked = false; $('layerVis').dispatchEvent(new Event('change')); paint(); 1");
await t.captureSave("$('exportPng').click()");
r = await t.savedImage([[400, 200], [400, 300]]);
eq('the PNG leaves hidden layers out', r.px, ['0,0,0', '255,255,255']);

await scene({ plain: true });
await ev("selectAll(); $('lineW').value = '4'; $('lineC').value = '#0000ff'; $('applyLine').click(); sel.clear(); paint(); 1");
s = await t.captureSave("$('exportPng').click()");
check('a PNG of the whole scene was saved', s && s.size > 100, [s, await toast(), await ev("$('fw').value + '|' + $('fh').value")]);
for (const [name, box] of [['line', [200, 190, 600, 210]], ['polyline', [200, 400, 400, 500]], ['circle', [740, 340, 860, 460]], ['smooth path', [1000, 200, 1200, 300]], ['symbol', [1180, 580, 1220, 620]]]) {
  const n = await blueIn(...box);
  check(`the PNG draws the ${name}`, n > 20, n);
}

await t.finish();
