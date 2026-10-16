import { readFile } from 'node:fs/promises';
import { glob } from 'node:fs/promises';

let failures = 0;
for await (const file of glob('apps/web/src/**/*.{ts,css}', { cwd: process.cwd() })) {
  const text = await readFile(file, 'utf8');
  if (text.includes('\t')) {
    console.error(`${file}: tab character found`);
    failures += 1;
  }
  if (!text.endsWith('\n')) {
    console.error(`${file}: missing final newline`);
    failures += 1;
  }
}
if (failures) process.exit(1);
console.log('Web source checks passed');
