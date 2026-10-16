import { cp, mkdir, rm } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const web = resolve(root, 'apps/web');
const dist = resolve(web, 'dist');
await rm(dist, { recursive: true, force: true });
await mkdir(resolve(dist, 'assets'), { recursive: true });
const compiler = spawnSync('tsc', ['-p', resolve(web, 'tsconfig.json')], { stdio: 'inherit' });
if (compiler.status !== 0) process.exit(compiler.status ?? 1);
await cp(resolve(web, 'index.html'), resolve(dist, 'index.html'));
await cp(resolve(web, 'src/styles.css'), resolve(dist, 'assets/styles.css'));
await cp(resolve(web, 'public'), dist, { recursive: true });
console.log('Built apps/web/dist');
