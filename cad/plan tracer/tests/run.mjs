// Runs the tests, one after another, and prints failures and one summary line per test.
// node run.mjs                 all tests that exist
// node run.mjs static view     only these
// Options: --html <tool>  --chrome <Chrome executable>  --profile <folder for temporary profiles>  --port <n>
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from './harness.mjs';

// The only place with paths. Another machine or location changes only these.
const here = dirname(fileURLToPath(import.meta.url));
const args = parseArgs(process.argv);
const settings = {
  html: args.html || join(here, '..', 'plan-tracer.html'),
  chrome: args.chrome || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  profile: args.profile || join(tmpdir(), 'plan-tracer-tests'),
  port: args.port || '9334'
};

const ORDER = ['static', 'editing', 'view', 'files', 'shell', 'scenario'];
const wanted = args._.length ? args._ : ORDER;
const unknown = wanted.filter(n => !existsSync(join(here, n + '.mjs')));
if (args._.length && unknown.length) { console.log(`no such test: ${unknown.join(', ')}`); process.exit(2); }

let passed = 0, failed = 0, ran = 0;
const t0 = Date.now();
for (const name of wanted.filter(n => !unknown.includes(n))) {
  const r = spawnSync(process.execPath, [join(here, name + '.mjs'), '--html', settings.html, '--chrome', settings.chrome, '--profile', settings.profile, '--port', settings.port], { encoding: 'utf8', timeout: 600000 });
  const lines = (r.stdout || '').split(/\r?\n/).filter(Boolean);
  const summary = lines.find(l => new RegExp(`^${name}: \\d+ passed, \\d+ failed$`).test(l));
  ran++;
  for (const l of lines.filter(l => l.startsWith('FAIL'))) console.log(l);
  if (summary) {
    console.log(summary);
    const m = /(\d+) passed, (\d+) failed/.exec(summary);
    passed += +m[1]; failed += +m[2];
  } else {
    console.log(`${name}: did not finish${r.error ? ' (' + r.error.message + ')' : ''}`);
    for (const l of (r.stderr || r.stdout || '').split(/\r?\n/).filter(Boolean).slice(0, 5)) console.log('  ' + l);
    failed++;
  }
}
console.log(`all: ${passed} passed, ${failed} failed in ${ran} test${ran === 1 ? '' : 's'}, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
process.exit(failed ? 1 : 0);
