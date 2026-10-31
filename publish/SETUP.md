# Auto-Publisher – Setup (Stand 27.10.2026, live)

**Weg:** Instagram API mit Facebook-Login (Meta bot Instagram-Login nicht an). Creator-Konto @vascoda.soda ↔ FB-Seite "Not just you".

## Script-Eigenschaften (Apps Script im Sheet "Not just you – Posting-Plan", Konto vascoda.soda@gmail.com)
| Key | Wert |
|---|---|
| IG_USER_ID | 17841417377350549 |
| IG_TOKEN | Seiten-Token (läuft nie ab) |
| MEDIA_BASE | https://chris61ds-alt.github.io/notjustyou-media/ |
| SHEET_ID | 12bACi6zXtctLx8kazNtME_zKHWgZLt_1IdexWz2ABZY |
| API_HOST | graph.facebook.com |

## Token erneuern (z. B. nach Passwortwechsel)
1. Graph API Explorer → Generate Access Token (instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement, business_management)
2. ⓘ → Access-Token-Tool → **Zugriffsschlüssel verlängern** (wichtig! sonst läuft der Seiten-Token nach ~1 h ab)
3. Mit dem verlängerten Token: `me/accounts?fields=name,access_token,instagram_business_account`
4. Seiten-Token im Debugger prüfen → "Läuft ab: Nie" → in IG_TOKEN eintragen

## Neue Folgen
Render → `publish/media/njXX.(mp4|jpg)` → schedule.csv/json → Repo `notjustyou-media` pushen → fertig: `autoImport` prüft stündlich und importiert nur bei Änderungen (Status bereits geposteter Folgen bleibt). Sofort-Import: `importSchedule` manuell ausführen.

## Plan
2 Reels/Tag (12:30, 18:30), Test No. 17 am 27.10. 21:15 → live. Bereits vorher online: Doorway, When talks end, Focusing illusion, More pain (No. 13).

## TikTok: Upload ins Postfach (TikTok.gs)
Das Skript lädt jede Folge zur geplanten Zeit in dein TikTok-Postfach. Du tippst auf die Benachrichtigung, fügst die Caption ein (kommt parallel per Mail), wählst als Titelbild den **ersten Frame** und postest. Direktes Auto-Posten bräuchte ein TikTok-Audit.

1. **TikTok-Developer-App:** developers.tiktok.com → mit @vascoda.soda anmelden → *Manage apps* → *Connect an app*.
   - Name „Not just you publisher“, Kategorie *Entertainment*, Icon: `notjustyou-media/legal/icon.png`
   - Terms: `https://chris61ds-alt.github.io/notjustyou-media/legal/terms.html` · Privacy: `…/legal/privacy.html` · Website: `…/legal/`
   - Produkte hinzufügen: **Login Kit** und **Content Posting API** (nur „Upload“, *Direct Post* aus). Scopes: `user.info.basic`, `video.upload`
   - Oben auf **Sandbox** schalten → *Target users*: @vascoda.soda hinzufügen.
2. **Apps Script:** Datei `TikTok.gs` anlegen (Inhalt einfügen), `Code.gs` aktualisieren.
   *Bereitstellen → Neue Bereitstellung → Web-App* (Ausführen als: ich · Zugriff: jeder) → URL kopieren.
3. Die Web-App-URL in der TikTok-App unter Login Kit als **Redirect URI** eintragen.
4. Script-Eigenschaften: `TT_CLIENT_KEY`, `TT_CLIENT_SECRET` (aus der TikTok-App), `TT_REDIRECT` (Web-App-URL). Nie in den Chat kopieren.
5. `tiktokAuthLink` ausführen → Link aus dem Log öffnen → erlauben → „Verbunden ✓“.
6. `tiktokTestUpload` ausführen → im TikTok-Postfach sollte ein Video liegen. Dann `setup` ausführen (legt den Trigger `tiktokRun` an).

Spalte `tiktok_done`: leer = wird hochgeladen · `posted`/`x` = schon auf TikTok · `inbox …` = im Postfach · `tt-error: …` = Fehler (leeren = neuer Versuch). Max. 5 offene Uploads pro 24 h (TikTok-Limit): Postfach regelmäßig abarbeiten.
