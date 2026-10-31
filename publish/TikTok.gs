/**
 * NOT JUST YOU – TikTok: Videos automatisch ins TikTok-Postfach (Inbox) hochladen.
 *
 * Zur geplanten Zeit (gleiche Zeilen/Termine wie Instagram) lädt das Skript das Video über die
 * TikTok Content Posting API ("Upload", Scope video.upload) in dein TikTok-Postfach. TikTok schickt dir
 * eine Benachrichtigung; du tippst darauf, fügst die Caption ein (kommt parallel per Mail) und postest.
 * Ein echtes Auto-Posten ("Direct Post") verlangt ein TikTok-Audit – das hier funktioniert ohne Posting-Rechte.
 *
 * Einrichtung (siehe SETUP.md, Abschnitt TikTok):
 *   Script-Eigenschaften: TT_CLIENT_KEY, TT_CLIENT_SECRET, TT_REDIRECT (= URL der Web-App-Bereitstellung)
 *   1. Projekt als Web-App bereitstellen (Ausführen als: ich · Zugriff: jeder) → URL als TT_REDIRECT + in der TikTok-App eintragen
 *   2. tiktokAuthLink() ausführen → Link aus dem Log öffnen → mit dem TikTok-Konto erlauben → "Verbunden ✓"
 *   3. setup() erneut ausführen (legt zusätzlich den Trigger tiktokRun an)
 *
 * Spalte "tiktok_done" (L): leer = noch offen · "posted"/"x" = schon auf TikTok (wird übersprungen)
 *   · "inbox …" = hochgeladen · "tt-error: …" = Fehler (Zelle leeren = neuer Versuch).
 * Datenschutz: speichert nur Token in den Script-Eigenschaften, sendet nur an TikTok (open.tiktokapis.com).
 */

const TT_API = 'https://open.tiktokapis.com';
const TT_SCOPES = 'user.info.basic,video.upload';
const TT_MAX_DELAY_H = 12;          // verpasste Termine bis 12 h nachholen, ältere bleiben für die Montags-Mail

/** Schritt 2: erzeugt den Freigabe-Link für dein TikTok-Konto (im Log). */
function tiktokAuthLink() {
  const p = props_();
  ['TT_CLIENT_KEY', 'TT_CLIENT_SECRET', 'TT_REDIRECT'].forEach(k => { if (!p[k]) throw new Error('Script-Eigenschaft fehlt: ' + k); });
  const state = Utilities.getUuid();
  PropertiesService.getScriptProperties().setProperty('TT_STATE', state);
  const url = 'https://www.tiktok.com/v2/auth/authorize/?client_key=' + encodeURIComponent(p.TT_CLIENT_KEY) +
              '&scope=' + encodeURIComponent(TT_SCOPES) + '&response_type=code' +
              '&redirect_uri=' + encodeURIComponent(p.TT_REDIRECT) + '&state=' + state;
  Logger.log('Diesen Link öffnen und mit @vascoda.soda erlauben:\n' + url);
  return url;
}

/** Rücksprung von TikTok nach der Freigabe (Web-App). */
function doGet(e) {
  const q = (e && e.parameter) || {};
  const sp = PropertiesService.getScriptProperties();
  const page = msg => HtmlService.createHtmlOutput('<div style="font:18px Roboto,Arial,sans-serif;padding:32px">' + msg + '</div>');
  if (!q.code) return page('Not just you – TikTok-Verbindung. Kein Code empfangen.');
  if (!q.state || q.state !== sp.getProperty('TT_STATE')) return page('Ungültiger Link – bitte tiktokAuthLink() neu ausführen.');
  try {
    tiktokToken_({ grant_type: 'authorization_code', code: q.code, redirect_uri: props_().TT_REDIRECT });
    sp.deleteProperty('TT_STATE');
    return page('<b>Verbunden ✓</b><br>TikTok-Uploads ins Postfach sind aktiv. Du kannst dieses Fenster schließen.');
  } catch (err) {
    return page('Fehler: ' + String(err.message).replace(/</g, '&lt;'));
  }
}

/** Alle 15 Minuten (Trigger): fällige Folge ins TikTok-Postfach laden (max. 1 pro Lauf). */
function tiktokRun() {
  const p = props_();
  if (!p.TT_REFRESH) return;                                   // noch nicht verbunden
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30 * 1000)) return;
  try {
    const sh = sheet_(); const tz = sh.getParent().getSpreadsheetTimeZone();
    const values = sh.getDataRange().getValues(); const now = new Date();
    for (let i = 1; i < values.length; i++) {
      const r = values[i], row = i + 1;
      if (String(r[COL.tiktok - 1] || '').trim() !== '') continue;            // erledigt, übersprungen oder Fehler
      const due = dueDate_(r[COL.date - 1], r[COL.time - 1], tz);
      if (!due || due > now || now - due > TT_MAX_DELAY_H * 3600000) continue;
      try {
        const id = tiktokUpload_(String(r[COL.video - 1]));
        sh.getRange(row, COL.tiktok).setValue('inbox ' + Utilities.formatDate(now, TZ, 'yyyy-MM-dd HH:mm') + ' · ' + id);
        MailApp.sendEmail(notify_(), 'TikTok: No. ' + r[COL.no - 1] + ' liegt in deinem Postfach',
          'Öffne TikTok → Benachrichtigung → Video bearbeiten → diese Caption einfügen → Titelbild: erster Frame → Posten.\n\n' +
          String(r[COL.caption - 1] || ''));
      } catch (err) {
        sh.getRange(row, COL.tiktok).setValue('tt-error: ' + String(err.message).substring(0, 160));
        MailApp.sendEmail(notify_(), 'Not just you – TikTok-Upload fehlgeschlagen (No. ' + r[COL.no - 1] + ')',
          String(err.message) + '\n\nZum erneuten Versuch: Zelle in Spalte "tiktok_done" leeren.');
      }
      break;                                                     // höchstens ein Upload pro Lauf (Rate-Limit)
    }
  } finally {
    lock.releaseLock();
  }
}

/** Test: lädt die erste Folge des Plans sofort ins Postfach (ohne Sheet-Änderung). */
function tiktokTestUpload() {
  const r = sheet_().getDataRange().getValues()[1];
  Logger.log('Hochgeladen, publish_id: ' + tiktokUpload_(String(r[COL.video - 1])) + ' – schau in dein TikTok-Postfach.');
}

function tiktokUpload_(videoFile) {
  const p = props_();
  const res = UrlFetchApp.fetch(p.MEDIA_BASE + videoFile, { muteHttpExceptions: true, followRedirects: true });
  if (res.getResponseCode() !== 200) throw new Error('Video nicht erreichbar: ' + videoFile + ' (HTTP ' + res.getResponseCode() + ')');
  const bytes = res.getContent(); const size = bytes.length;
  if (size > 64 * 1024 * 1024) throw new Error('Video größer als 64 MB – bitte kleiner rendern');
  const init = tiktokApi_('/v2/post/publish/inbox/video/init/', {
    source_info: { source: 'FILE_UPLOAD', video_size: size, chunk_size: size, total_chunk_count: 1 }
  });
  const up = UrlFetchApp.fetch(init.data.upload_url, {
    method: 'put', contentType: 'video/mp4', payload: bytes, muteHttpExceptions: true,
    headers: { 'Content-Range': 'bytes 0-' + (size - 1) + '/' + size }
  });
  if (up.getResponseCode() >= 300) throw new Error('Upload: HTTP ' + up.getResponseCode() + ' ' + up.getContentText().substring(0, 200));
  return init.data.publish_id;
}

function tiktokApi_(path, body) {
  const res = UrlFetchApp.fetch(TT_API + path, {
    method: 'post', contentType: 'application/json; charset=UTF-8', payload: JSON.stringify(body), muteHttpExceptions: true,
    headers: { Authorization: 'Bearer ' + tiktokAccess_() }
  });
  const j = JSON.parse(res.getContentText() || '{}');
  if (res.getResponseCode() >= 400 || (j.error && j.error.code && j.error.code !== 'ok'))
    throw new Error((j.error && (j.error.code + ': ' + j.error.message)) || ('HTTP ' + res.getResponseCode()));
  return j;
}

function tiktokAccess_() {
  const p = props_();
  if (p.TT_ACCESS && Number(p.TT_ACCESS_EXP || 0) > Date.now() + 10 * 60000) return p.TT_ACCESS;
  if (!p.TT_REFRESH) throw new Error('TikTok nicht verbunden – tiktokAuthLink() ausführen');
  return tiktokToken_({ grant_type: 'refresh_token', refresh_token: p.TT_REFRESH });
}

function tiktokToken_(params) {
  const p = props_();
  const res = UrlFetchApp.fetch(TT_API + '/v2/oauth/token/', {
    method: 'post', contentType: 'application/x-www-form-urlencoded', muteHttpExceptions: true,
    payload: Object.assign({ client_key: p.TT_CLIENT_KEY, client_secret: p.TT_CLIENT_SECRET }, params)
  });
  const j = JSON.parse(res.getContentText() || '{}');
  if (!j.access_token) throw new Error('Token: ' + (j.error_description || j.error || res.getContentText().substring(0, 200)));
  const sp = PropertiesService.getScriptProperties();
  sp.setProperty('TT_ACCESS', j.access_token);
  sp.setProperty('TT_ACCESS_EXP', String(Date.now() + (j.expires_in || 86400) * 1000));
  if (j.refresh_token) sp.setProperty('TT_REFRESH', j.refresh_token);      // TikTok kann einen neuen Refresh-Token liefern
  return j.access_token;
}
