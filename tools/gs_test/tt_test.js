const fs = require('fs');
const src = fs.readFileSync('../../publish/Code.gs', 'utf8') + '\n' + fs.readFileSync('../../publish/TikTok.gs', 'utf8');
let props = { MEDIA_BASE: 'https://x/', SHEET_ID: 's', IG_TOKEN: 't', IG_USER_ID: 'u', TT_CLIENT_KEY: 'ck', TT_CLIENT_SECRET: 'cs', TT_REDIRECT: 'https://script/exec' };
const calls = []; let mails = [];
const now = new Date(); const ds = d => d.toISOString().slice(0, 10), ts = d => d.toISOString().slice(11, 16);
const past = new Date(now - 30 * 60000), future = new Date(+now + 3600000), old = new Date(now - 20 * 3600000);
let grid = [['date','time','no','title','video','cover','caption','status','c','m','p','tiktok'],
  [ds(old), ts(old), '60', 'old', 'nj60.mp4', '', 'capOld', '', '', '', '', ''],
  [ds(past), ts(past), '61', 'a', 'nj61.mp4', '', 'capA', '', '', '', '', 'posted'],
  [ds(past), ts(past), '62', 'b', 'nj62.mp4', '', 'capB', '', '', '', '', ''],
  [ds(future), ts(future), '63', 'c', 'nj63.mp4', '', 'capC', '', '', '', '', '']];
function rng(r, c, nr, nc) { return { getValues: () => Array.from({length: nr}, (_, i) => Array.from({length: nc}, (_, j) => (grid[r-1+i]||[])[c-1+j] ?? '')),
  setValue: x => { grid[r-1][c-1] = x; }, setValues: v => {}, setNumberFormat: () => rng(r,c,nr,nc) }; }
const sheet = { getDataRange: () => rng(1, 1, grid.length, 12), getRange: (r, c, nr=1, nc=1) => rng(r, c, nr, nc), getParent: () => ({ getSpreadsheetTimeZone: () => 'UTC' }) };
global.SpreadsheetApp = { openById: () => ({ getSheets: () => [sheet] }) };
global.PropertiesService = { getScriptProperties: () => ({ getProperties: () => ({...props}), getProperty: k => props[k] ?? null, setProperty: (k, v) => props[k] = v, deleteProperty: k => delete props[k] }) };
global.LockService = { getScriptLock: () => ({ tryLock: () => true, releaseLock: () => {} }) };
global.MailApp = { sendEmail: (a, s, b) => mails.push(s) };
global.Session = { getEffectiveUser: () => ({ getEmail: () => 'me' }) };
global.Logger = { log: console.log };
global.HtmlService = { createHtmlOutput: h => h };
global.Utilities = { getUuid: () => 'state123', formatDate: (d) => d.toISOString().slice(0, 16).replace('T', ' '),
  parseDate: (s) => new Date(s.replace(' ', 'T') + ':00Z') };
global.UrlFetchApp = { fetch: (url, o = {}) => { calls.push((o.method || 'get') + ' ' + url.split('?')[0]);
  const R = (code, body, bytes) => ({ getResponseCode: () => code, getContentText: () => JSON.stringify(body), getContent: () => bytes });
  if (url.endsWith('/v2/oauth/token/')) return R(200, { access_token: 'AT' + calls.length, expires_in: 86400, refresh_token: 'RT2' });
  if (url.includes('/inbox/video/init/')) { if (o.headers.Authorization.indexOf('Bearer AT') !== 0) throw new Error('no auth');
    const b = JSON.parse(o.payload); if (b.source_info.video_size !== 5 || b.source_info.total_chunk_count !== 1) throw new Error('bad init');
    return R(200, { data: { upload_url: 'https://upload/x?sig=1', publish_id: 'v_pub_1' }, error: { code: 'ok' } }); }
  if (url.startsWith('https://upload/')) { if (o.headers['Content-Range'] !== 'bytes 0-4/5' || o.method !== 'put') throw new Error('bad put'); return R(201, {}); }
  if (url.startsWith('https://x/')) return R(200, {}, [1, 2, 3, 4, 5]);
  throw new Error('unexpected ' + url); } };
eval(src + '\n;Object.assign(globalThis,{tiktokAuthLink,doGet,tiktokRun});');
const link = tiktokAuthLink(); console.log(link.includes('client_key=ck') && link.includes('state=state123') ? 'auth link ok' : 'auth link BAD');
console.log(doGet({ parameter: { code: 'C', state: 'wrong' } }).includes('Ungültig') ? 'bad state rejected' : 'BAD');
console.log(doGet({ parameter: { code: 'C', state: 'state123' } }).includes('Verbunden') ? 'connected' : 'BAD', props.TT_REFRESH);
tiktokRun(); tiktokRun();
console.log(grid.map(r => r[2] + ':' + r[11]).slice(1).join(' | '));
console.log('mails:', mails); console.log('calls:', calls.join(', '));
