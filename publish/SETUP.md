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
Render → `publish/media/njXX.(mp4|jpg)` → schedule.csv/json → Repo `notjustyou-media` pushen → in Apps Script `importSchedule` ausführen (Status bereits geposteter Folgen bleibt).

## Plan
2 Reels/Tag (12:30, 18:30), Test No. 17 am 27.10. 21:15 → live. Bereits vorher online: Doorway, When talks end, Focusing illusion, More pain (No. 13).
