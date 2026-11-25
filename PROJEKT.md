# Projekt „Not just you“ – Briefing (Stand 31.10.2026)

## 0 · Regeln
**Alle gültigen Regeln stehen in `REGELN.md`** (vor jeder Folge lesen; `shared/rulecheck.py` prüft sie beim Build).
Alte Fassungen: `REGELN_ARCHIV.md`.

## 1 · Allgemein
- Antworten an Chris auf Deutsch, kurz, visuell. Videos 1080×1920, immer mit Instagram-Caption.
- Serie „Not just you“ auf @vascoda.soda (Instagram + TikTok), englische Daten-Reels.
- Automatisierung nur mit Google Apps Script (kein Make.com); Secrets nur in den Script-Eigenschaften. Code immer als komplette Datei, keine großen Änderungen ohne Absprache.

## 2 · Wo was liegt
| Was | Ort |
|---|---|
| Code, Skripte, Captions aller Folgen | GitHub `chris61ds-alt/explainer-kit` (`epXX_*/script.json · render.py · caption.md`) |
| Videos, Cover, Posting-Plan (öffentlich) | GitHub Pages `chris61ds-alt.github.io/notjustyou-media/` (`njXX.mp4/.jpg`, `schedule.json`) |
| Posting-Steuerung | Google Sheet „Not just you – Posting-Plan“ (Konto vascoda.soda@gmail.com) + Apps Script `publish/Code.gs` |
| Abhak-Liste (TikTok/IG manuell) | Claude-Artefakt „Not just you Posting“ |
| Backlog & Folgenübersicht | `BACKLOG.md` · Setup-Anleitung `publish/SETUP.md` |

## 3 · Ablauf einer neuen Folge (Produktion)
1. Übergabe-Paket → `epXX_name/script.json` + `caption.md`, dazu `render.py` (Toolkit `shared/thread.py`, Dating-Props `shared/dating.py`).
2. `python3 shared/build.py epXX_name` → TTS, Sprach-Check, Render, Technik-Check, Cover. Vorschau: `python3 tools/preview.py epXX_name`.
3. `publish/media/njXX.mp4/.jpg` + `schedule.json` aktualisieren → Repo `notjustyou-media` pushen.
4. Apps Script `autoImport` holt den Plan **stündlich automatisch** (nur bei Änderung). Sofort: `importSchedule`.

## 4 · Publishing
- **Instagram:** automatisch, 2×/Tag **12:30 + 18:30** (Graph API über Facebook-Login, Seiten-Token läuft nicht ab). Fehler → Mail.
- **TikTok:** läuft **deutlich besser als Instagram** (Look C+D: 700–1.000 Aufrufe, alter Look ~260). Upload ins TikTok-Postfach per Apps Script (`TikTok.gs`, Einrichtung in SETUP.md), Posten per Tipp. Titelbild beim Posten: erster Frame.
- Insights (24 h / 72 h) im Sheet: braucht Token mit `instagram_manage_insights` + `setup`.

## 5 · Stand
- Fertig: No. 01–82 (Übersicht in `BACKLOG.md`). Instagram-Plan bis **17.11.2026**.
- Sprint 4 (73–81, „Dataclysm“, PLATFORM DATA · OkCupid): Love Is Blind Day · Fake Match · Bio <10 % · Alte Fotos · Casual Sex 6,1 vs 0,8 % · 80 % below average · Beer Question · Forever 20 · Split Opinion.
- No. 82 „This video, live“: das Video erzählt live seine eigene Zuschauerkurve (INDUSTRY DATA). Fertig, noch nicht eingeplant.
- In Arbeit (Sprint 5, Skripte aus dem Projekt-Chat): **No. 83 OnlyFans · No. 84 Slop**.
- Sonderfolge No. 72 „You decide“ (Top-Kommentar = nächstes Video) → bekommt die nächste freie Nummer.
- Außerhalb der Serie: Einzelvideo „Why nobody visits Algeria“ (`solo_algeria`, TRAVEL DATA).

## 6 · Offen
- **TikTok-Automatisierung:** Vorschlag = Upload ins TikTok-Postfach per Apps Script testen (1 Tipp pro Video) + parallel Audit für Direct Post beantragen. Entscheidung offen.
- Instagram-Insights aktivieren (Token-Recht `instagram_manage_insights`).
- Option: Dataclysm-Folgen im Plan nach vorne ziehen; ältere gewagte Folgen (38–58, Strichfiguren) auf Look C+D umbauen, falls der neue Look besser performt.

- Look v6 (03.11.2026, Kamera-Push + Parallaxe, handgezeichnete Markierungen, Glow/Korn/Vignette; Schalter NJY_LOOK=v6) getestet an No. 93 → **abgelehnt, Chris bleibt beim bisherigen Look.** Nicht erneut vorschlagen; Code bleibt nur als Opt-in im Toolkit.
