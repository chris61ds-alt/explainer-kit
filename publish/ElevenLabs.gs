/**
 * NOT JUST YOU – ElevenLabs-Stimmtest (Google Apps Script, gleiches Projekt wie Code.gs)
 *
 * Holt einen Sprech-Auftrag (JSON) aus MEDIA_BASE + 'tts/<job>.json', lässt jeden Satz-Block von ElevenLabs
 * einsprechen und legt alle MP3s als EIN ZIP in deinen Drive-Ordner "NJY_TTS". Claude holt das ZIP dort ab.
 *
 * Einrichtung (einmalig):
 *   Projekteinstellungen → Script-Eigenschaften → ELEVEN_KEY = dein ElevenLabs-API-Key
 *   (MEDIA_BASE ist schon gesetzt, siehe Code.gs)
 * Ausführen: Funktion elevenAB150 auswählen → ▶ Ausführen (beim ersten Mal Drive-Zugriff erlauben).
 *
 * Datenschutz: Der Key bleibt in den Script-Eigenschaften. Gesendet wird nur der Sprechtext an api.elevenlabs.io.
 */

const ELEVEN_FOLDER = 'NJY_TTS';

function elevenAB150() { elevenJob_('ab150'); }

function elevenJob_(job) {
  const sp = PropertiesService.getScriptProperties();
  const key = sp.getProperty('ELEVEN_KEY');
  if (!key) throw new Error('Script-Eigenschaft ELEVEN_KEY fehlt.');
  const base = sp.getProperty('MEDIA_BASE');
  const res = UrlFetchApp.fetch(base + 'tts/' + job + '.json?t=' + Date.now(), { muteHttpExceptions: true });
  if (res.getResponseCode() !== 200) throw new Error('Auftrag nicht gefunden: ' + res.getResponseCode());
  const J = JSON.parse(res.getContentText());

  const blobs = [], log = [];
  let chars = 0;
  Object.keys(J.voices).forEach(function (name) {
    const vid = J.voices[name];
    J.beats.forEach(function (b, i) {
      const body = {
        text: b.text,
        model_id: J.model || 'eleven_multilingual_v2',
        voice_settings: J.settings || { stability: 0.4, similarity_boost: 0.75, style: 0.3, use_speaker_boost: true, speed: 1.08 },
        previous_text: i > 0 ? J.beats[i - 1].text : undefined,     // gleiche Satzmelodie über die Blöcke hinweg
        next_text: i < J.beats.length - 1 ? J.beats[i + 1].text : undefined
      };
      const r = UrlFetchApp.fetch('https://api.elevenlabs.io/v1/text-to-speech/' + vid + '?output_format=mp3_44100_128', {
        method: 'post', contentType: 'application/json', payload: JSON.stringify(body),
        headers: { 'xi-api-key': key, accept: 'audio/mpeg' }, muteHttpExceptions: true
      });
      if (r.getResponseCode() !== 200) {
        log.push(name + '/' + b.id + ': Fehler ' + r.getResponseCode() + ' ' + r.getContentText().slice(0, 200));
        return;
      }
      blobs.push(r.getBlob().setName(name + '/' + b.id + '.mp3'));
      chars += b.text.length;
    });
  });
  blobs.push(Utilities.newBlob(log.join('\n') || 'ok', 'text/plain', 'log.txt'));

  const it = DriveApp.getFoldersByName(ELEVEN_FOLDER);
  const folder = it.hasNext() ? it.next() : DriveApp.createFolder(ELEVEN_FOLDER);
  const zip = Utilities.zip(blobs, 'njy_tts_' + job + '.zip');
  const old = folder.getFilesByName(zip.getName());
  while (old.hasNext()) old.next().setTrashed(true);              // nur die alte Version desselben Tests
  const f = folder.createFile(zip);
  Logger.log('Fertig: ' + f.getName() + ' · ' + (blobs.length - 1) + ' Dateien · ' + chars + ' Zeichen' + (log.length ? '\n' + log.join('\n') : ''));
}
