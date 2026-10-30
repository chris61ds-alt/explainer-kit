# Projekt „Not just you“ – Briefing (Stand 30.10.2026)

## 1 · Projekt-Anweisungen (in die Projekt-Instructions kopieren)
- Antworte auf Deutsch, kurz und präzise, visuell formatiert. Videos immer im Instagram-Reel-Format (1080×1920) und immer mit Instagram-Caption.
- Serie **„Not just you“** auf @vascoda.soda (Instagram + TikTok), **englische** Explainer-Reels: Psychologie/Daten zu Dingen, die man für „nicht normal“ hält.
- **Nur gewagte Themen** (Sex, Dating, Lügen, Rache, Geld, Ego). Brave Themen sind geparkt.
- **Keine erfundenen Zahlen.** Nicht alles muss eine Peer-Review-Studie sein, aber das Label ist ehrlich: SMALL STUDY · CASE STUDY · SURVEY · UNSOLVED · PLATFORM DATA · SELF-REPORTED. Quellen vor jeder Folge per Websuche prüfen.
- **Look C+D, dark:** große Roboto-Typografie, ein Signalorange, Punktraster-Silhouetten (halftone). **Keine Strichfiguren, keine unnötige UI** (kein Header, Titel, Fortschrittsbalken, Kapitel).
- Stimme: Kokoro TTS `af_heart`, Speed 1.1. Länge ca. 25–35 s. Ende: „Not just you.“ + Quellen-Endkarte.
- Automatisierung nur mit **Google Apps Script** (kein Make.com). Code immer als komplette Datei, keine großen Änderungen ohne Absprache.

## 2 · Wo was liegt
| Was | Ort |
|---|---|
| Code, Skripte, Captions aller Folgen | GitHub `chris61ds-alt/explainer-kit` (`epXX_*/script.json · render.py · caption.md`) |
| Videos, Cover, Posting-Plan (öffentlich) | GitHub Pages `chris61ds-alt.github.io/notjustyou-media/` (`njXX.mp4/.jpg`, `schedule.json`) |
| Posting-Steuerung | Google Sheet „Not just you – Posting-Plan“ (Konto vascoda.soda@gmail.com) + Apps Script `publish/Code.gs` |
| Abhak-Liste (TikTok/IG manuell) | Claude-Artefakt „Not just you Posting“ |
| Backlog & Folgenübersicht | `BACKLOG.md` · Setup-Anleitung `publish/SETUP.md` |

## 3 · Ablauf einer neuen Folge
1. Thema + Quelle prüfen → `script.json` (Beats) + `caption.md` + `render.py` (Toolkit `shared/thread.py`, Dating-Props `shared/dating.py`).
2. `python3 shared/build.py epXX_name` → TTS, Spracherkennungs-Check, Render, Technik-Check, Cover.
3. `publish/media/njXX.mp4/.jpg` + `schedule.json` aktualisieren → Repo `notjustyou-media` pushen.
4. Apps Script `autoImport` holt den Plan **stündlich automatisch** (nur bei Änderung). Sofort: `importSchedule`.

## 4 · Publishing
- **Instagram:** automatisch, 2×/Tag **12:30 + 18:30** (Graph API über Facebook-Login, Seiten-Token läuft nicht ab). Fehler → Mail.
- **TikTok:** manuell (montags Digest-Mail; Abhak-Liste). Läuft bisher **besser als Instagram**.
- Insights (24 h / 72 h) im Sheet: braucht Token mit `instagram_manage_insights` + `setup`.

## 5 · Stand
- Fertig: No. 01–81 (Übersicht in `BACKLOG.md`). Geplant auf Instagram bis **17.11.2026**.
- Letzter Sprint (73–81, „Dataclysm“, PLATFORM DATA · OkCupid): Love Is Blind Day · Fake Match · Bio <10 % · Alte Fotos · Casual Sex 6,1 vs 0,8 % · 80 % below average · Beer Question · Forever 20 · Split Opinion.
- Sonderfolge No. 72 „You decide“ (Top-Kommentar = nächstes Video), 30.10. 21:00.

## 6 · Offen
- **TikTok-Automatisierung:** Vorschlag = Upload ins TikTok-Postfach per Apps Script testen (1 Tipp pro Video) + parallel Audit für Direct Post beantragen. Entscheidung offen.
- Instagram-Insights aktivieren (Token-Recht `instagram_manage_insights`).
- Option: Dataclysm-Folgen im Plan nach vorne ziehen; ältere gewagte Folgen (38–58, Strichfiguren) auf Look C+D umbauen, falls der neue Look besser performt.
- Top-Kommentar aus No. 72 als nächste Folge umsetzen.
