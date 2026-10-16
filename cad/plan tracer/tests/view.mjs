// Underlays and the view: placing, rotating, ordering, filters, rulers, scale bar, overview map, zoom window.
// Changes the view and the stored interface state, so it runs on its own page.
import { launch, parseArgs, near } from './harness.mjs';

const t = await launch('view', parseArgs(process.argv));
const { ev, click, move, drag, key, eq, check, lines, add, toast, mkU } = t;

const fresh = async () => { await t.reset(); await ev("$('tracking').checked = false; 1"); };
const place = (i, x, y) => ev(`(() => { const u = unders[${i}]; Object.assign(u, { x: ${x}, y: ${y}, rot: 0, scale: 1, opacity: 1 }); renderU(u); syncControls(); return 1; })()`);
const world = (i, lx, ly) => ev(`(() => { const q = uWorld(unders[${i}], ${lx}, ${ly}); return [q.x, q.y]; })()`);
const fire = id => ev(`(() => { $('${id}').dispatchEvent(new Event('input', { bubbles: true })); return 1; })()`);
const order = () => ev("unders.map(u => u.name).join(',') + '|' + activeU");
const lockedToast = async () => (await toast()) === 'The underlay is locked.';
const buttonOffset = () => ev("(() => { const v = view.getBoundingClientRect(); return Math.round(parseFloat($('orthoBtn').style.left) - v.left) + '|' + Math.round(parseFloat($('orthoBtn').style.top) - v.top); })()");
const noOverlap = () => ev("(() => { const a = $('orthoBtn').getBoundingClientRect(), b = $('mapBtn').getBoundingClientRect(); return b.left >= a.right; })()");
const mapBox = () => ev("(() => { const b = $('minimap').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; })()");
let r;

// ---------- 1 two underlays: names, brightness, contrast, saving, autosave ----------
await fresh(); await mkU('a.png', '#808080'); await mkU('b.png', '#ff0000');
check('two underlays, the last one active', (await ev('unders.length')) === 2 && (await ev('activeU')) === 1, await ev('unders.length'));
await ev("$('ulabel').value = 'Basement'"); await fire('ulabel');
eq('rename sets the label', await ev("unders[1].label + '|' + $('underSel').options[1].textContent"), 'Basement|Basement');
eq('rename keeps the file name', await ev('unders[1].name'), 'b.png');
r = await ev('buildSvg()');
check('the label and the file name are saved', r.includes('data-label="Basement"') && r.includes('href="b.png"'));
await ev("$('ubright').value = '1.5'"); await fire('ubright');
eq('brightness is applied', await ev("unders[1].bright + '|' + unders[1].el.style.filter"), '1.5|brightness(1.5) contrast(1)');
r = await ev('buildSvg()');
check('brightness is saved, defaults are not', r.includes('data-brightness="1.5"') && !r.includes('data-contrast'), r.slice(0, 300));
await ev("$('ucontrast').value = '0.8'"); await fire('ucontrast');
check('contrast is saved', (await ev('buildSvg()')).includes('data-contrast="0.8"'));
eq('opening reads label and filters back', await ev("(() => { const doc = new DOMParser().parseFromString(buildSvg(), 'image/svg+xml'); const us = [...doc.querySelectorAll('#underlays image')].map(underFromImage); return us.map(u => [u.name, u.label, u.bright, u.contrast].join('/')).join(','); })()"), 'a.png//1/1,b.png/Basement/1.5/0.8');
await ev('autosave(); unders = []; restore()');
eq('autosave keeps label and filters', await ev("unders.map(u => [u.name, u.label, u.bright, u.contrast].join('/')).join(',')"), 'a.png//1/1,b.png/Basement/1.5/0.8');

// ---------- 2 raise and lower ----------
await fresh(); await mkU('a.png', '#808080'); await mkU('b.png', '#ff0000');
await ev('activeU = 0; syncControls()'); await ev("$('underUp').click()");
eq('raise', await order(), 'b.png,a.png|1');
r = await ev('buildSvg()');
check('raise changes the order in the file', r.indexOf('href="b.png"') < r.indexOf('href="a.png"'));
await ev("$('underUp').click()");
eq('raise at the top does nothing', await order(), 'b.png,a.png|1');
await ev("$('underDown').click()");
eq('lower', await order(), 'a.png,b.png|0');
await ev("$('underDown').click()");
eq('lower at the bottom does nothing', await ev('activeU'), 0);
eq('the drawing order follows the list', await ev("gUnder.querySelectorAll('image').length"), 2);

// ---------- 3 nudge ----------
await fresh(); await mkU('a.png', '#808080'); await place(0, 100, 100);
await ev("$('nudgeStep').value = '5'; $('nudgeR').click(); $('nudgeD').click(); $('nudgeD').click()");
eq('nudge right and down', await ev('[unders[0].x, unders[0].y]'), [105, 110]);
await ev("$('nudgeL').click(); $('nudgeU').click()");
eq('nudge left and up', await ev('[unders[0].x, unders[0].y]'), [100, 105]);
await ev("unders[0].locked = true; $('nudgeR').click()");
check('nudge is blocked when locked', (await ev('unders[0].x')) === 100 && await lockedToast());

// ---------- 4 rotate tool ----------
await fresh(); await mkU('a.png', '#808080'); await place(0, 300, 300); await ev("setTool('rotate')"); await drag(500, 350, 400, 450);
check('rotate by 90 degrees', near(await ev('unders[0].rot'), 90, 1), await ev('unders[0].rot'));
r = await world(0, 100, 50);
check('rotation keeps the centre in place', near(r[0], 400, 0.1) && near(r[1], 350, 0.1), r);
check('the rotation field follows', near(parseFloat(await ev("$('urot').value")), await ev('unders[0].rot'), 0.01));
await place(0, 300, 300); await t.holdShift(() => drag(500, 350, 476.6, 414.3));
check('Shift snaps to 15 degrees', near(await ev('unders[0].rot'), 45, 0.01), await ev('unders[0].rot'));
await place(0, 300, 300); await ev('unders[0].crop = { x: 0, y: 0, w: 100, h: 100 }; renderU(unders[0])'); await drag(450, 350, 350, 350);
r = await world(0, 50, 50);
check('rotation about the centre of the crop', near(r[0], 350, 0.2) && near(r[1], 350, 0.2), r);
await ev('unders[0].crop = null; renderU(unders[0]); unders[0].locked = true');
{ const before = await ev('unders[0].rot'); await drag(500, 350, 400, 450);
  check('rotate is blocked when locked', (await lockedToast()) && (await ev('unders[0].rot')) === before, before); }
await ev('unders[0].locked = false');
await fresh(); await mkU('a.png', '#808080'); await place(0, 300, 300); await add([100, 100, 500, 100]); await ev("setTool('rotate')"); await drag(500, 350, 400, 450);
eq('rotating an underlay leaves the traced lines alone', await lines(), ['100,100,500,100']);

// ---------- 5 make horizontal ----------
await fresh(); await mkU('a.png', '#808080'); await place(0, 100, 100); await ev("setTool('horizontal')"); await click(100, 100); await click(300, 150);
r = await world(0, 0, 0);
check('make horizontal keeps the first point', near(r[0], 100, 0.05) && near(r[1], 100, 0.05), r);
r = await world(0, 200, 50);
check('make horizontal levels the line', near(r[1], 100, 0.05), r);
await place(0, 300, 300); await ev("setTool('horizontal')"); await click(300, 300); await click(100, 260);
r = await world(0, -200, -40);
check('make horizontal for a line pointing left', near(r[1], 300, 0.05) && near(await ev('unders[0].rot'), -11.31, 0.05), [r, await ev('unders[0].rot')]);
await ev('unders[0].locked = true'); await click(100, 100); await click(300, 150);
check('make horizontal is blocked when locked', await lockedToast());
await fresh(); await ev("setTool('horizontal')"); await click(100, 100);
eq('make horizontal needs an underlay', await toast(), 'Pick an underlay image first.');

// ---------- 6 rulers and scale bar ----------
await fresh();
eq('rulers are shown and sized', await ev("(() => { const H = $('rulerH'), V = $('rulerV'), v = view.getBoundingClientRect(); return [H.style.display, V.style.display, Math.round(parseFloat(H.style.width) - v.width), Math.round(parseFloat(V.style.height) - (v.height - 20))].join('|'); })()"), 'block|block|0|0');
r = await ev("(() => { const sb = $('scaleBar'); const ppm = view.getScreenCTM().a * num('upm'); return [sb.style.display, $('scaleTxt').textContent, Math.abs(parseFloat(sb.style.width) - parseFloat($('scaleTxt').textContent) * ppm) < 1, parseFloat(sb.style.width) >= 59 && parseFloat(sb.style.width) <= 151].join('|'); })()");
check('the scale bar has the stated length and a usable size', r.startsWith('block|') && r.endsWith('|true|true'), r);
r = await ev("(() => { const H = $('rulerH'), m = view.getScreenCTM(), rc = view.getBoundingClientRect(); const x = Math.round(m.e - rc.left), c = H.getContext('2d'), d = H.width / parseFloat(H.style.width); const px = X => Array.from(c.getImageData(Math.round(X * d), Math.round(5 * d), 1, 1).data).join(','); return [px(x), px(x + 5)]; })()");
check('the ruler has a tick at the frame corner', r[0] !== r[1], r);
await move(300, 300);
r = await ev("(() => { const V = $('rulerV'), rc = view.getBoundingClientRect(), m = view.getScreenCTM(); const y = Math.round(m.d * 300 + m.f - rc.top - 20), d = V.width / parseFloat(V.style.width); return Array.from(V.getContext('2d').getImageData(Math.round(8 * d), Math.round(y * d), 1, 1).data).join(','); })()");
check('the cursor marker shows on the vertical ruler', (() => { const q = r.split(',').map(Number); return q[0] > 150 && q[1] < 90; })(), r);
await ev('zoomCenter(0.5)');
check('the scale bar follows the zoom', (await ev("$('scaleTxt').textContent")) !== '10 m', await ev("$('scaleTxt').textContent"));
await ev('fitCamera()');
await ev("$('upm').value = '0'; $('upm').dispatchEvent(new Event('input', { bubbles: true }))");
eq('the scale bar is hidden without units per meter', await ev("$('scaleBar').style.display"), 'none');
await ev("$('upm').value = '10'; $('upm').dispatchEvent(new Event('input', { bubbles: true }))");
await ev("$('rulers').checked = false; $('rulers').dispatchEvent(new Event('change'))");
eq('rulers off hides rulers and scale bar', await ev("$('rulerH').style.display + '|' + $('rulerV').style.display + '|' + $('scaleBar').style.display"), 'none|none|none');
eq('the buttons move up when the rulers are off', await buttonOffset(), '8|8');
await ev("$('rulers').checked = true; $('rulers').dispatchEvent(new Event('change'))");
eq('the buttons sit below the rulers', await buttonOffset(), '26|26');
eq('the map button does not overlap the ortho button', await noOverlap(), true);
await ev("$('orthoBtn').click()");
eq('still no overlap after the label changes', await noOverlap(), true);

// ---------- 7 overview map ----------
await fresh(); await add([100, 100, 500, 100], [500, 100, 500, 400]);
check('the map is hidden by default', (await ev("$('minimap').style.display")) !== 'block');
await ev("$('mapBtn').click()"); await t.sleep(200);
eq('the map is shown', await ev("$('minimap').style.display + '|' + $('mapBtn').textContent"), 'block|Map: on');
r = await ev("(() => { const c = $('minimap'), x = c.getContext('2d'), d = x.getImageData(0, 0, c.width, c.height).data; let nonWhite = 0, blue = 0; for (let i = 0; i < d.length; i += 4) { if (d[i] < 200 || d[i + 1] < 200 || d[i + 2] < 200) nonWhite++; if (d[i] < 60 && d[i + 1] > 80 && d[i + 2] > 150) blue++; } return [nonWhite, blue]; })()");
check('the map draws the content and the view rectangle', r[0] > 100 && r[1] > 20, r);
eq('the map setting is stored', await ev("JSON.parse(localStorage.getItem('planTracer.ui')).map"), true);
{ const before = await ev('vb().x'), box = await mapBox();
  await t.clickScreen(box[0] + 15, box[1] + box[3] / 2);
  const after = await ev('vb().x');
  check('a click in the map moves the view', after < before - 50, [before, after]); }
await ev('fitCamera()');
{ const box = await mapBox(), v0 = await ev('vb().width');
  await t.dragScreen(box[0] + 90, box[1] + 65, box[0] + 120, box[1] + 80);
  const v1 = await ev('vb().width');
  check('a drag in the map keeps the zoom', near(v1, v0, 0.001), [v0, v1]); }
await ev('fitCamera()');
await ev("$('mapBtn').click()");
eq('the map is hidden again', await ev("$('minimap').style.display"), 'none');

// ---------- 8 underlay and trace in the PNG ----------
// The underlay covers x 0 to 200 and y 300 to 400; the line runs across it at y 350. The PNG is drawn at twice the size.
await fresh(); await mkU('a.png', '#808080'); await place(0, 0, 300);
await ev("gTrace.appendChild(mkLine(100, 350, 900, 350, { w: 6, c: '#ff0000' })); unders[0].bright = 1.5; renderU(unders[0]); paint(); 1");
const shot = await t.captureSave("$('exportPng').click()");
check('a PNG was saved', shot && shot.size > 100, shot);
r = await t.savedImage([[100, 640], [300, 700], [1000, 700]]);
check('the PNG applies brightness to the underlay', near(+r.px[0].split(',')[0], 192, 4), r);
eq('the PNG draws the trace over the underlay', r.px[1], '255,0,0');
eq('the PNG draws the trace outside the underlay', r.px[2], '255,0,0');
await ev('unders[0].bright = 1; renderU(unders[0]); 1');
await t.captureSave("$('exportPng').click()");
r = await t.savedImage([[100, 640]]);
check('the PNG without brightness', near(+r.px[0].split(',')[0], 128, 4), r);

// ---------- 9 zoom window (last, it changes the view) ----------
await fresh(); await ev("fitCamera(); setTool('select'); setTool('zoomwin')"); await drag(100, 100, 300, 200);
r = await ev('[vb().x, vb().y, vb().width, vb().height]');
check('zoom window sets the view', near(r[0], 100, 1) && near(r[1], 100, 1) && near(r[2], 200, 2) && near(r[3], 100, 2), r);
eq('the tool returns after the zoom', await ev('tool'), 'select');
await ev("fitCamera(); setTool('line'); setTool('zoomwin')"); await key('Escape');
eq('Esc leaves zoom window', await ev('tool'), 'line');
await ev("setTool('zoomwin')"); await drag(100, 100, 101, 101);
eq('a tiny drag does not zoom', await ev('tool'), 'line');

await t.finish();
