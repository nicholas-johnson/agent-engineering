#!/usr/bin/env node
// clip-deck: run from a folder of clips (one folder per clip, each with an index.html).
//
//   clip-deck serve           serve the clips at http://127.0.0.1:8765, with the engine at /clip-deck/
//   clip-deck new 02-slug     start a new clip from the template
//   clip-deck check [02-slug] step through a clip in Chrome: list its captions, report anything
//                             cut off, and save a picture of every step to output/<clip>/

import { createServer } from 'node:http';
import { cp, mkdir, readdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const engine = path.join(here, 'src');
const template = path.join(here, 'template');
const root = process.cwd();
const PORT = 8765;

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2',
  '.mp4': 'video/mp4',
};

function fail(message) {
  console.error(message);
  process.exit(1);
}

async function exists(file) {
  return stat(file).then(
    (info) => info,
    () => null,
  );
}

async function clips() {
  const found = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    if (entry.isDirectory() && (await exists(path.join(root, entry.name, 'index.html')))) found.push(entry.name);
  }
  return found.sort();
}

async function title(clip) {
  const html = await readFile(path.join(root, clip, 'index.html'), 'utf8');
  return html.match(/<title>(.*?)<\/title>/)?.[1] ?? clip;
}

// Serving

async function listing() {
  const items = [];
  for (const clip of await clips()) items.push(`<li><a href="/${clip}/">${await title(clip)}</a></li>`);
  return `<!doctype html><meta charset="utf-8"><title>Clips</title>
<style>body{font:20px system-ui;background:#0f172a;color:#f1f5f9;padding:40px}a{color:#38bdf8}li{margin:12px 0}</style>
<h1>Clips</h1><ul>${items.join('')}</ul>`;
}

function server() {
  return createServer(async (request, response) => {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    if (pathname === '/') {
      response.writeHead(200, { 'content-type': TYPES['.html'] });
      return response.end(await listing());
    }
    const [base, rest] = pathname.startsWith('/clip-deck/')
      ? [engine, pathname.slice('/clip-deck/'.length)]
      : [root, pathname.slice(1)];
    let file = path.join(base, rest);
    if (file !== base && !file.startsWith(base + path.sep)) {
      response.writeHead(403);
      return response.end();
    }
    if ((await exists(file))?.isDirectory()) {
      if (!pathname.endsWith('/')) {
        response.writeHead(301, { location: `${pathname}/` });
        return response.end();
      }
      file = path.join(file, 'index.html');
    }
    try {
      const body = await readFile(file);
      response.writeHead(200, {
        'content-type': TYPES[path.extname(file)] ?? 'application/octet-stream',
        'cache-control': 'no-store',
      });
      response.end(body);
    } catch {
      response.writeHead(404);
      response.end('Not found');
    }
  });
}

function listen(app, port) {
  return new Promise((resolve, reject) => {
    app.once('error', reject);
    app.listen(port, '127.0.0.1', () => resolve(`http://127.0.0.1:${app.address().port}`));
  });
}

async function serve() {
  const origin = await listen(server(), PORT).catch((error) =>
    fail(error.code === 'EADDRINUSE' ? `Port ${PORT} is busy: is the clip server already running?` : error.message),
  );
  console.log(`Serving clips at ${origin}/`);
  for (const clip of await clips()) console.log(`  ${origin}/${clip}/`);
  console.log('Open one in Chrome. Ctrl-C to stop.');
}

// Starting a clip

async function newClip(name) {
  if (!/^\d\d-[a-z0-9-]+$/.test(name ?? '')) fail('Name the clip like 02-embeddings: two digits, a dash, then a short slug.');
  const destination = path.join(root, name);
  if (await exists(destination)) fail(`${name}/ already exists.`);
  await cp(template, destination, { recursive: true });
  for (const file of ['index.html', 'script.md']) {
    const target = path.join(destination, file);
    const text = await readFile(target, 'utf8');
    await writeFile(target, text.replaceAll('{{clip}}', name).replaceAll('{{number}}', String(Number(name.slice(0, 2)))));
  }
  console.log(`Started ${name}/ with index.html and script.md.`);
  console.log('Write the script first, then the frames. Serve it to look at it, and check it before recording.');
}

// Checking

async function launch(chromium) {
  const args = ['--use-fake-device-for-media-stream'];
  for (const channel of ['chrome', 'msedge', undefined]) {
    try {
      return await chromium.launch({ channel, args });
    } catch {
      // try the next browser
    }
  }
  fail('Could not launch a browser. Install Google Chrome.');
}

// Runs in the page: anything cut off, as plain sentences.
function layoutProblems() {
  const problems = [];
  document.querySelectorAll('.frame').forEach((frame, i) => {
    const children = [...frame.children];
    if (!children.length) return;
    const bottom = Math.max(...children.map((child) => child.offsetTop + child.offsetHeight));
    if (bottom > frame.clientHeight) {
      problems.push(`Frame ${i + 1} is ${bottom - frame.clientHeight}px too tall: it runs into the camera box.`);
    }
    for (const element of frame.querySelectorAll('*')) {
      if (getComputedStyle(element).display === 'inline' || element.matches('.typed')) continue;
      if (element.scrollWidth > element.clientWidth + 1) {
        const text = element.textContent.trim().slice(0, 40);
        problems.push(`Frame ${i + 1}: "${text}" is ${element.scrollWidth - element.clientWidth}px too wide.`);
      }
    }
  });
  return problems;
}

async function check(only) {
  const { chromium } = await import('playwright-core');
  const names = only ? [only] : await clips();
  if (only && !(await exists(path.join(root, only, 'index.html')))) fail(`No ${only}/index.html here.`);

  const app = server();
  const origin = await listen(app, 0);
  const browser = await launch(chromium);
  // Reduced motion tells scripts such as network.js to jump straight to each step's final state.
  const context = await browser.newContext({ viewport: { width: 540, height: 960 }, reducedMotion: 'reduce' });
  await context.grantPermissions(['camera', 'microphone'], { origin });
  // Skip the animations so every step can be read straight away.
  await context.addInitScript(() => {
    Element.prototype.animate = () => ({ finished: Promise.resolve(), cancel() {} });
    addEventListener('DOMContentLoaded', () => {
      const style = document.createElement('style');
      style.textContent = '*, *::before, *::after { transition: none !important; animation: none !important; }';
      document.head.append(style);
    });
  });

  let failed = false;
  for (const clip of names) {
    const out = path.join(root, 'output', clip);
    await rm(out, { recursive: true, force: true });
    await mkdir(out, { recursive: true });

    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', (error) => errors.push(error.message));
    page.on('console', (message) => message.type() === 'error' && errors.push(message.text()));
    await page.goto(`${origin}/${clip}/`);
    await page.waitForTimeout(500);

    const problems = await page.evaluate(layoutProblems);
    const steps = [];
    for (let n = 0; n < 200; n++) {
      await page.waitForTimeout(80);
      const state = await page.evaluate(() => ({
        at: location.hash.slice(1),
        caption: document.querySelector('.caption').textContent,
        lines: Math.round((document.querySelector('.caption').offsetHeight - 36) / 57.5),
        full: document.querySelector('.stage').classList.contains('camera-full'),
      }));
      if (steps.length && steps.at(-1).at === state.at) break;
      const file = path.join(out, `${String(n).padStart(2, '0')}.png`);
      await page.screenshot({ path: file });
      steps.push({ ...state, file });
      if (state.lines > 2) problems.push(`Caption ${n} runs to ${state.lines} lines: "${state.caption}". Split it.`);
      if (!state.caption) problems.push(`Step ${state.at} has no caption.`);
      await page.keyboard.press('Space');
    }
    await page.close();
    problems.push(...errors.map((error) => `Page error: ${error}`));

    const cells = steps
      .map((step, n) => `<figure><img src="${pathToFileURL(step.file)}"><figcaption>${n} · #${step.at}</figcaption></figure>`)
      .join('');
    await writeFile(
      path.join(out, 'sheet.html'),
      `<!doctype html><style>body{margin:0;background:#444;display:grid;grid-template-columns:repeat(6,270px);gap:8px;padding:8px;width:max-content;font:13px sans-serif;color:#fff}img{width:270px;display:block}figure{margin:0}</style>${cells}`,
    );
    const sheet = await context.newPage();
    await sheet.goto(pathToFileURL(path.join(out, 'sheet.html')).href);
    await sheet.waitForTimeout(300);
    await sheet.screenshot({ path: path.join(out, 'sheet.png'), fullPage: true });
    await sheet.close();

    console.log(`\n${clip}: ${steps.length} steps`);
    steps.forEach((step, n) => {
      console.log(`${String(n).padStart(3)}  #${step.at.padEnd(5)} ${step.full ? '[camera] ' : ''}${step.caption}`);
    });
    const words = steps.reduce((total, step) => total + step.caption.split(/\s+/).filter(Boolean).length, 0);
    console.log(`About ${words} words: roughly ${Math.round(words / 2.5)} seconds spoken.`);
    console.log(`Pictures: ${path.relative(root, out)}/ (sheet.png shows every step)`);
    if (problems.length) {
      failed = true;
      console.log(`Problems:\n  ${problems.join('\n  ')}`);
    } else {
      console.log('No problems found.');
    }
  }

  await browser.close();
  app.close();
  if (failed) process.exit(1);
}

const [command, argument] = process.argv.slice(2);
if (command === 'serve') await serve();
else if (command === 'new') await newClip(argument);
else if (command === 'check') await check(argument);
else fail('Usage: clip-deck serve | clip-deck new 02-slug | clip-deck check [02-slug]');
