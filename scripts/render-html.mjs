#!/usr/bin/env node
// HTML → PNG über CDP. Port 0 + DevToolsActivePort, damit nie ein fremder Chrome gesteuert wird.
//   node scripts/render-html.mjs <datei.html|http-url> <ziel.png> <breite> <hoehe|auto> [scale]
// hoehe=auto misst die tatsächliche Dokumenthöhe, nichts wird abgeschnitten.
import { spawn } from 'node:child_process';
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
const [html, out, W, H, S] = process.argv.slice(2);
const w = +W || 1080, auto = String(H) === 'auto', scale = +S || 2;
let h = auto ? 1200 : (+H || 1350);
const chrome = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const profile = path.join(os.tmpdir(), 'lm-cdp-profile-' + process.pid);
fs.mkdirSync(profile, { recursive: true });
const child = spawn(chrome, ['--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--disable-extensions','--hide-scrollbars','--remote-debugging-port=0',`--user-data-dir=${profile}`,'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let port = null;
for (let i = 0; i < 120 && !port; i++) { try { port = +fs.readFileSync(path.join(profile, 'DevToolsActivePort'), 'utf8').split('\n')[0]; } catch { await sleep(250); } }
if (!port) { child.kill(); throw new Error('Chrome kam nicht hoch'); }
const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); const events = [];
ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } else events.push(m); });
const send = (method, params = {}) => new Promise(res => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: scale, mobile: false });
const url = /^https?:\/\//.test(html) ? html : 'file://' + path.resolve(html);
await send('Page.navigate', { url });
for (let i = 0; i < 80; i++) { if (events.some(e => e.method === 'Page.loadEventFired')) break; await sleep(100); }
await send('Runtime.evaluate', { expression: 'document.fonts.ready.then(()=>true)', awaitPromise: true });
await sleep(900);   // dynamische Seiten holen ihre Daten erst nach dem Load
if (auto) {
  const m = await send('Runtime.evaluate', { expression: 'Math.ceil(document.documentElement.scrollHeight)', returnByValue: true });
  h = m.result.result.value;
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: scale, mobile: false });
  await sleep(200);
}
const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
fs.writeFileSync(out, Buffer.from(shot.result.data, 'base64'));
ws.close(); child.kill();
console.log(`${out} ${w}x${h} @${scale}x`);
