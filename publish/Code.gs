/**
 * NOT JUST YOU – Auto-Publisher für Instagram Reels (Google Apps Script)
 *
 * Liest den Plan aus dem Google Sheet "Not just you – Posting-Plan" und veröffentlicht fällige Reels
 * über die Instagram API (Instagram Login, funktioniert mit Creator-Konten). Für TikTok kommt jeden
 * Montag eine Mail mit den Folgen der Woche (Caption + Download-Link) zum Einplanen in TikTok Studio.
 *
 * Ablauf pro Reel (verteilt auf mehrere Läufe, weil Instagram das Video erst verarbeitet):
 *   1. Termin erreicht  → Container anlegen (video_url, cover_url, caption)  → Status "processing"
 *   2. nächster Lauf    → Status prüfen; FINISHED → veröffentlichen          → Status "live"
 *   Fehler              → Status "error: …" + Mail an dich
 *
 * Plan: importSchedule() lädt schedule.json aus MEDIA_BASE ins Sheet (Status bleibt erhalten).
 *   autoImport() läuft stündlich und importiert nur, wenn sich schedule.json geändert hat.
 * Insights: trackInsights() schreibt 24 h / 72 h nach dem Post Views, Reach, Likes, Shares, Saves, Watch-Time, Skip-Rate
 *   (Token braucht dafür zusätzlich instagram_manage_insights).
 * Einrichtung: siehe Setup-Anleitung. Script-Eigenschaften (Projekteinstellungen → Script-Eigenschaften):
 *   IG_USER_ID   – deine Instagram-User-ID (aus dem Meta-Dashboard)
 *   IG_TOKEN     – Long-lived Access Token (60 Tage gültig, wird automatisch erneuert)
 *   MEDIA_BASE   – z. B. https://raw.githubusercontent.com/chris61ds-alt/notjustyou-media/main/
 *   SHEET_ID     – ID des Posting-Plans (aus der Sheet-URL)
 *   API_VERSION  – optional, Standard v26.0
 *   API_HOST     – optional: graph.instagram.com (Instagram-Login, Standard) oder graph.facebook.com
 *                  (Facebook-Login; dann IG_TOKEN = Seiten-Token, läuft nicht ab)
 *   NOTIFY_EMAIL – optional, Standard: dein Google-Konto
 *   TT_CLIENT_KEY / TT_CLIENT_SECRET / TT_REDIRECT – optional: TikTok-Postfach-Upload (Datei TikTok.gs)
 *
 * Datenschutz: Das Skript speichert nur Token und IDs in den Script-Eigenschaften deines Kontos,
 * sendet nichts an Dritte außer an die Instagram/Meta Graph API und protokolliert keine Nutzerdaten.
 */

const TZ = 'Europe/Berlin';
const SHEET_NAME = null;            // null = erstes Tabellenblatt
const CHECK_EVERY_MIN = 15;         // Prüfintervall
const MAX_POSTS_PER_RUN = 1;        // Sicherheitsbremse
const MAX_DELAY_H = 6;              // verpasste Termine nur bis 6 h nachholen, ältere → "missed"

const COL = {                        // Spalten im Sheet (1-basiert)
  date: 1, time: 2, no: 3, title: 4, video: 5, cover: 6, caption: 7,
  status: 8, container: 9, mediaId: 10, postedAt: 11, tiktok: 12
};
// Insights: ab Spalte 13 je ein Block für 24 h und 72 h nach Veröffentlichung
const INS_METRICS = ['views', 'reach', 'likes', 'shares', 'saved', 'ig_reels_avg_watch_time', 'reels_skip_rate'];
const INS_LABELS  = ['views', 'reach', 'likes', 'shares', 'saves', 'avg_watch_s', 'skip_rate'];
const INS_START = 13, INS_AT = [24, 72];
const LAST_COL = INS_START + INS_LABELS.length * INS_AT.length - 1;

// ---------------------------------------------------------------- Einrichtung

/** Einmal ausführen: prüft die Einstellungen und legt die Zeit-Trigger an. */
function setup() {
  const p = props_();
  ['IG_USER_ID', 'IG_TOKEN', 'MEDIA_BASE', 'SHEET_ID'].forEach(k => {
    if (!p[k]) throw new Error('Script-Eigenschaft fehlt: ' + k);
  });
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('run').timeBased().everyMinutes(CHECK_EVERY_MIN).create();
  ScriptApp.newTrigger('refreshToken').timeBased().everyDays(1).atHour(4).inTimezone(TZ).create();
  ScriptApp.newTrigger('trackInsights').timeBased().everyHours(1).create();
  ScriptApp.newTrigger('weeklyTikTokDigest').timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(9).inTimezone(TZ).create();
  ScriptApp.newTrigger('autoImport').timeBased().everyHours(1).create();
  if (p.TT_CLIENT_KEY) ScriptApp.newTrigger('tiktokRun').timeBased().everyMinutes(CHECK_EVERY_MIN).create();   // TikTok.gs
  const me = igGet_(p.IG_USER_ID, { fields: 'username' });
  Logger.log('Verbunden mit @' + me.username + ' · Trigger angelegt.');
  autoImport();
  checkMediaUrls();
}

/** Prüft, ob alle Video- und Cover-Dateien öffentlich erreichbar sind (Instagram muss sie abrufen können). */
function checkMediaUrls() {
  const base = props_().MEDIA_BASE;
  const rows = sheet_().getDataRange().getValues().slice(1);
  const bad = [];
  rows.forEach(r => {
    [r[COL.video - 1], r[COL.cover - 1]].forEach(f => {
      if (!f) return;
      const res = UrlFetchApp.fetch(base + f, { method: 'get', muteHttpExceptions: true, followRedirects: true,
                                                 headers: { Range: 'bytes=0-0' } });
      if ([200, 206].indexOf(res.getResponseCode()) < 0) bad.push(f + ' (' + res.getResponseCode() + ')');
    });
  });
  Logger.log(bad.length ? 'Nicht erreichbar: ' + bad.join(', ') : 'Alle Dateien erreichbar ✓');
  return bad;
}

/** Zeigt, wie viele Posts im 24-h-Fenster noch frei sind. */
function showPublishingLimit() {
  const p = props_();
  Logger.log(JSON.stringify(igGet_(p.IG_USER_ID + '/content_publishing_limit', { fields: 'config,quota_usage' })));
}

// ---------------------------------------------------------------- Hauptlauf

/** Wird alle 15 Minuten ausgeführt. */
function run() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30 * 1000)) return;
  try {
    const sh = sheet_();
    const tz = sh.getParent().getSpreadsheetTimeZone();
    const values = sh.getDataRange().getValues();
    const now = new Date();
    let started = 0;

    for (let i = 1; i < values.length; i++) {
      const r = values[i], row = i + 1;
      const status = String(r[COL.status - 1] || '').trim();
      if (status === 'live' || status.indexOf('error') === 0 || status === 'skip' || status === 'missed') continue;

      if (status === 'processing') {           // Schritt 2: Verarbeitung prüfen, dann veröffentlichen
        handleProcessing_(sh, row, r);
        continue;
      }
      if (status === '' && started < MAX_POSTS_PER_RUN) {   // Schritt 1: fällige Zeile starten
        const due = dueDate_(r[COL.date - 1], r[COL.time - 1], tz);
        if (due && due <= now) {
          if (now - due > MAX_DELAY_H * 3600000) {   // zu alt → nicht nachholen (verhindert Post-Flut)
            sh.getRange(row, COL.status).setValue('missed');
            continue;
          }
          startContainer_(sh, row, r);
          started++;
        }
      }
    }
  } finally {
    lock.releaseLock();
  }
}

/**
 * Verteilt alle noch nicht veröffentlichten Zeilen (Status leer oder "missed") neu:
 * ab START_DAYS_FROM_NOW Tagen, eine Folge pro Slot (TIMES), Reihenfolge bleibt erhalten.
 */
function rescheduleFromToday() {
  const START_DAYS_FROM_NOW = 1, TIMES = ['12:30', '18:30'];   // Slots pro Tag
  const sh = sheet_(); const values = sh.getDataRange().getValues();
  let day = new Date(); day.setDate(day.getDate() + START_DAYS_FROM_NOW); let slot = 0;
  for (let i = 1; i < values.length; i++) {
    const st = String(values[i][COL.status - 1] || '').trim();
    if (st !== '' && st !== 'missed') continue;
    sh.getRange(i + 1, COL.date, 1, 2).setNumberFormat('@')
      .setValues([[Utilities.formatDate(day, TZ, 'yyyy-MM-dd'), TIMES[slot]]]);
    sh.getRange(i + 1, COL.status).setValue('');
    if (++slot >= TIMES.length) { slot = 0; day.setDate(day.getDate() + 1); }
  }
  Logger.log('Neu geplant ab ' + Utilities.formatDate(new Date(Date.now() + START_DAYS_FROM_NOW * 86400000), TZ, 'dd.MM.yyyy'));
}

/**
 * Lädt den aktuellen Plan (schedule.json aus MEDIA_BASE) ins Sheet.
 * Bereits gestartete/veröffentlichte Folgen (Status nicht leer) behalten Termin und Status.
 */
function importSchedule() {
  const lock = LockService.getScriptLock();             // nicht gleichzeitig mit run() ins Sheet schreiben
  if (!lock.tryLock(60 * 1000)) throw new Error('Sheet gerade in Benutzung – bitte gleich nochmal ausführen.');
  try {
    const text = fetchSchedule_();
    importData_(JSON.parse(text));
    PropertiesService.getScriptProperties().setProperty('SCHEDULE_HASH', hash_(text));
  } finally {
    lock.releaseLock();
  }
}

/** Stündlich (Trigger): importiert schedule.json nur, wenn sich die Datei seit dem letzten Import geändert hat. */
function autoImport() {
  const sp = PropertiesService.getScriptProperties();
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(60 * 1000)) return;                 // run() läuft gerade → nächste Stunde
  try {
    const text = fetchSchedule_();
    const h = hash_(text);
    if (sp.getProperty('SCHEDULE_HASH') === h) return;  // unverändert → nichts tun
    importData_(JSON.parse(text));
    sp.setProperty('SCHEDULE_HASH', h);
    sp.deleteProperty('IMPORT_ERR_DAY');
  } catch (e) {
    Logger.log('autoImport: ' + e.message);
    const today = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd');
    if (sp.getProperty('IMPORT_ERR_DAY') !== today) {    // höchstens eine Fehler-Mail pro Tag
      sp.setProperty('IMPORT_ERR_DAY', today);
      MailApp.sendEmail(notify_(), 'Not just you – Plan-Import fehlgeschlagen', e.message);
    }
  } finally {
    lock.releaseLock();
  }
}

function fetchSchedule_() {
  const url = props_().MEDIA_BASE + 'schedule.json?t=' + Date.now();   // Cache umgehen (GitHub Pages)
  const res = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  if (res.getResponseCode() !== 200) throw new Error('schedule.json nicht erreichbar (HTTP ' + res.getResponseCode() + ')');
  return res.getContentText('UTF-8');
}

function hash_(text) {
  return Utilities.base64Encode(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, text, Utilities.Charset.UTF_8));
}

function importData_(data) {                             // [header, ...rows] – 12 Spalten
  if (!Array.isArray(data) || data.length < 2) throw new Error('schedule.json ist leer oder ungültig');
  const sh = sheet_();
  const tz = sh.getParent().getSpreadsheetTimeZone();
  const width = LAST_COL;
  const pad = r => { const m = r.slice(0, width); while (m.length < width) m.push(''); return m; };
  const old = sh.getLastRow() > 0 ? sh.getRange(1, 1, sh.getLastRow(), Math.max(width, sh.getLastColumn())).getValues() : [];
  const keep = {}, keepOrder = [];
  old.slice(1).forEach(r => {
    if (String(r[COL.status - 1] || '').trim() === '') return;
    keep[String(r[COL.no - 1])] = r; keepOrder.push(String(r[COL.no - 1]));
  });
  const fix = m => {
    if (m[COL.date - 1] instanceof Date) m[COL.date - 1] = Utilities.formatDate(m[COL.date - 1], tz, 'yyyy-MM-dd');
    if (m[COL.time - 1] instanceof Date) m[COL.time - 1] = Utilities.formatDate(m[COL.time - 1], tz, 'HH:mm');
    if (m[COL.postedAt - 1] instanceof Date) m[COL.postedAt - 1] = Utilities.formatDate(m[COL.postedAt - 1], tz, 'yyyy-MM-dd HH:mm');
    return m;
  };
  const inPlan = {};
  data.slice(1).forEach(r => inPlan[String(r[COL.no - 1])] = true);
  // bereits gestartete/veröffentlichte Folgen, die nicht mehr im Plan stehen, bleiben oben erhalten
  const history = keepOrder.filter(n => !inPlan[n]).map(n => fix(pad(keep[n])));
  const rows = data.slice(1).map(r => {
    const k = keep[String(r[COL.no - 1])];
    if (!k) return pad(r);
    const m = pad(r);
    [COL.date, COL.time, COL.status, COL.container, COL.mediaId, COL.postedAt, COL.tiktok].forEach(c => m[c - 1] = k[c - 1]);
    for (let c = INS_START; c <= width; c++) m[c - 1] = k[c - 1];
    return fix(m);
  });
  const out = [pad(data[0]).map((h, i) => i >= INS_START - 1 ? insHeader_(i + 1) : h)].concat(history, rows);
  sh.clearContents();
  sh.getRange(1, 1, out.length, 2).setNumberFormat('@');
  sh.getRange(1, COL.postedAt, out.length, 1).setNumberFormat('@');
  sh.getRange(1, 1, out.length, width).setValues(out);
  sh.setFrozenRows(1);
  SpreadsheetApp.flush();
  Logger.log('Plan importiert: ' + rows.length + ' Folgen im Plan, ' + history.length + ' ältere behalten, ' +
             Object.keys(keep).length + ' mit Status übernommen.');
}

function startContainer_(sh, row, r) {
  const p = props_();
  const payload = {
    media_type: 'REELS',
    video_url: p.MEDIA_BASE + r[COL.video - 1],
    caption: String(r[COL.caption - 1] || ''),
    share_to_feed: 'true'
  };
  if (r[COL.cover - 1]) payload.cover_url = p.MEDIA_BASE + r[COL.cover - 1];
  try {
    const res = igPost_(p.IG_USER_ID + '/media', payload);
    sh.getRange(row, COL.container).setValue(res.id);
    sh.getRange(row, COL.status).setValue('processing');
  } catch (e) {
    fail_(sh, row, r, 'Container: ' + e.message);
  }
}

function handleProcessing_(sh, row, r) {
  const p = props_();
  const cid = r[COL.container - 1];
  try {
    const st = igGet_(String(cid), { fields: 'status_code,status' });
    if (st.status_code === 'FINISHED') {
      const pub = igPost_(p.IG_USER_ID + '/media_publish', { creation_id: String(cid) });
      sh.getRange(row, COL.mediaId).setValue(pub.id);
      sh.getRange(row, COL.postedAt).setValue(Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm'));
      sh.getRange(row, COL.status).setValue('live');
    } else if (st.status_code === 'ERROR' || st.status_code === 'EXPIRED') {
      fail_(sh, row, r, 'Verarbeitung: ' + st.status_code + ' ' + (st.status || ''));
    }
    // IN_PROGRESS → beim nächsten Lauf erneut prüfen
  } catch (e) {
    fail_(sh, row, r, 'Veröffentlichen: ' + e.message);
  }
}

function fail_(sh, row, r, msg) {
  sh.getRange(row, COL.status).setValue('error: ' + msg.substring(0, 180));
  MailApp.sendEmail(notify_(), 'Not just you – Instagram-Post fehlgeschlagen (No. ' + r[COL.no - 1] + ')',
    'Folge: ' + r[COL.no - 1] + ' – ' + r[COL.title - 1] + '\nZeile: ' + row + '\nFehler: ' + msg +
    '\n\nZum erneuten Versuch: Status-Zelle leeren (und Container-Zelle löschen).');
}

// ---------------------------------------------------------------- Token & TikTok

/** Täglich: verlängert den Long-lived Token (Instagram erlaubt das ab 24 h nach Ausstellung). */
function refreshToken() {
  const p = props_();
  if (p.API_HOST === 'graph.facebook.com') return;   // Seiten-Token aus Facebook-Login läuft nicht ab
  const url = 'https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=' +
              encodeURIComponent(p.IG_TOKEN);
  const res = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  const j = JSON.parse(res.getContentText());
  if (j.access_token) {
    PropertiesService.getScriptProperties().setProperty('IG_TOKEN', j.access_token);
  } else {
    MailApp.sendEmail(notify_(), 'Not just you – Token-Erneuerung fehlgeschlagen', res.getContentText());
  }
}

/** Montags: Mail mit allen Folgen der nächsten 7 Tage für TikTok Studio. */
function weeklyTikTokDigest() {
  const p = props_();
  const sh = sheet_(); const tz = sh.getParent().getSpreadsheetTimeZone();
  const now = new Date(), until = new Date(now.getTime() + 7 * 86400000);
  const rows = sh.getDataRange().getValues().slice(1).filter(r => {
    const due = dueDate_(r[COL.date - 1], r[COL.time - 1], tz);
    return due && due >= now && due < until && !r[COL.tiktok - 1];
  });
  if (!rows.length) return;
  const body = rows.map(r => {
    const due = dueDate_(r[COL.date - 1], r[COL.time - 1], tz);
    return '━━━ ' + Utilities.formatDate(due, TZ, 'EEE dd.MM. HH:mm') + ' · No. ' + r[COL.no - 1] + ' – ' + r[COL.title - 1] +
           '\nVideo: ' + p.MEDIA_BASE + r[COL.video - 1] + '\n\n' + r[COL.caption - 1] + '\n';
  }).join('\n');
  MailApp.sendEmail(notify_(), 'Not just you – TikTok-Plan dieser Woche (' + rows.length + ' Folgen)',
    'In TikTok Studio (Desktop) → Hochladen → "Planen" mit diesen Terminen.\nDanach im Sheet Spalte "tiktok_done" ankreuzen.\n\n' + body);
}

// ---------------------------------------------------------------- Insights

function insHeader_(col) {
  const i = col - INS_START, block = Math.floor(i / INS_LABELS.length);
  return INS_LABELS[i % INS_LABELS.length] + '_' + INS_AT[block] + 'h';
}

/** Stündlich: schreibt 24 h und 72 h nach Veröffentlichung die Reel-Kennzahlen ins Sheet. */
function trackInsights() {
  const sh = sheet_(); const tz = sh.getParent().getSpreadsheetTimeZone();
  const last = sh.getLastRow(); if (last < 2) return;
  const head = sh.getRange(1, INS_START, 1, LAST_COL - INS_START + 1);
  if (!head.getValues()[0][0]) head.setValues([head.getValues()[0].map((_, i) => insHeader_(INS_START + i))]);
  const values = sh.getRange(1, 1, last, LAST_COL).getValues();
  const now = new Date();
  for (let i = 1; i < values.length; i++) {
    const r = values[i];
    if (String(r[COL.status - 1]).trim() !== 'live' || !r[COL.mediaId - 1] || !r[COL.postedAt - 1]) continue;
    const posted = r[COL.postedAt - 1] instanceof Date ? r[COL.postedAt - 1]
                 : Utilities.parseDate(String(r[COL.postedAt - 1]).substring(0, 16), TZ, 'yyyy-MM-dd HH:mm');
    const ageH = (now - posted) / 3600000;
    INS_AT.forEach((h, b) => {
      const c0 = INS_START + b * INS_LABELS.length;
      if (ageH < h || r[c0 - 1] !== '') return;
      sh.getRange(i + 1, c0, 1, INS_LABELS.length).setValues([fetchInsights_(String(r[COL.mediaId - 1]))]);
    });
  }
}

function fetchInsights_(mediaId) {
  const sets = [INS_METRICS, ['reach', 'likes', 'shares', 'saved', 'ig_reels_avg_watch_time']];   // Fallback ohne Beta-Metriken
  let err = '';
  for (const metrics of sets) {
    try {
      const j = igGet_(mediaId + '/insights', { metric: metrics.join(',') });
      const v = {};
      (j.data || []).forEach(d => v[d.name] = d.total_value ? d.total_value.value : (d.values && d.values[0] ? d.values[0].value : ''));
      return INS_METRICS.map(m => {
        if (v[m] === undefined || v[m] === '') return '';
        if (m === 'ig_reels_avg_watch_time') return Math.round(v[m] / 100) / 10;      // ms → s
        return v[m];
      });
    } catch (e) { err = e.message; }
  }
  const row = INS_METRICS.map(() => ''); row[0] = 'error: ' + err.substring(0, 120);   // Zelle leeren = erneut versuchen
  return row;
}

// ---------------------------------------------------------------- Helfer

function dueDate_(d, t, sheetTz) {
  if (!d) return null;
  const ds = d instanceof Date ? Utilities.formatDate(d, sheetTz, 'yyyy-MM-dd') : String(d).trim();
  let ts = '18:30';
  if (t instanceof Date) ts = Utilities.formatDate(t, sheetTz, 'HH:mm');
  else if (t) ts = String(t).trim().substring(0, 5);
  return Utilities.parseDate(ds + ' ' + ts, TZ, 'yyyy-MM-dd HH:mm');
}

function props_() {
  const p = PropertiesService.getScriptProperties().getProperties();
  p.API_VERSION = p.API_VERSION || 'v26.0';
  p.API_HOST = (p.API_HOST || 'graph.instagram.com').replace(/^https?:\/\//, '').replace(/\/+$/, '');
  if (p.MEDIA_BASE && p.MEDIA_BASE.slice(-1) !== '/') p.MEDIA_BASE += '/';
  return p;
}

function notify_() { return props_().NOTIFY_EMAIL || Session.getEffectiveUser().getEmail(); }

function sheet_() {
  const ss = SpreadsheetApp.openById(props_().SHEET_ID);
  return SHEET_NAME ? ss.getSheetByName(SHEET_NAME) : ss.getSheets()[0];
}

function igGet_(path, params) {
  const p = props_();
  const q = Object.keys(params || {}).map(k => k + '=' + encodeURIComponent(params[k])).join('&');
  const url = 'https://' + p.API_HOST + '/' + p.API_VERSION + '/' + path + '?' + (q ? q + '&' : '') +
              'access_token=' + encodeURIComponent(p.IG_TOKEN);
  return parse_(UrlFetchApp.fetch(url, { muteHttpExceptions: true }));
}

function igPost_(path, payload) {
  const p = props_();
  payload = Object.assign({}, payload, { access_token: p.IG_TOKEN });
  const url = 'https://' + p.API_HOST + '/' + p.API_VERSION + '/' + path;
  return parse_(UrlFetchApp.fetch(url, { method: 'post', payload: payload, muteHttpExceptions: true }));
}

function parse_(res) {
  const j = JSON.parse(res.getContentText() || '{}');
  if (res.getResponseCode() >= 400 || j.error) throw new Error((j.error && j.error.message) || ('HTTP ' + res.getResponseCode()));
  return j;
}
