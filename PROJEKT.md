# Projekt „Not just you“ – Briefing (Stand 31.10.2026)

## 0 · Zusammenarbeit: wer macht was
Es gibt zwei Claude-Arbeitsplätze. Bitte nicht vermischen:

| | **Projekt-Chat** (hier) | **Produktions-Session** (Claude mit Repo-Schreibzugriff) |
|---|---|---|
| Aufgabe | Themen finden, Quellen prüfen, **Skript + Caption schreiben** | **render.py bauen**, Stimme erzeugen, Sprach-Check, rendern, GitHub, Posting-Plan, Checkliste |
| Repo | nur lesen | lesen + schreiben |
| Ergebnis | Übergabe-Paket (Format unten) | fertiges Video + Caption + eingeplant |

**Der Projekt-Chat baut keine render.py und legt keine Dateien ab.** Er liefert nur das Übergabe-Paket. Chris kopiert es in die Produktions-Session.

### Übergabe-Paket (genau dieses Format, je Folge)
**1. Kopf:** Nummer + Ordnername, z. B. `No. 83 · ep83_onlyfans`. Nächste freie Nummer = höchste Nummer in `BACKLOG.md` + 1. Wenn unklar: Platzhalter `No. ??`, dann vergibt die Produktion die Nummer.

**2. `script.json`** als Codeblock:
```json
{
 "voice": "af_heart", "speed": 1.1, "lang": "en-us",
 "beats": [
  {"id": "hook", "text": "…"},
  {"id": "study", "text": "…"},
  {"id": "result", "text": "…"},
  {"id": "point", "text": "…"},
  {"id": "end", "text": "Not just you."}
 ],
 "sources": ["Autor (Jahr). Titel. Journal/Quelle. Stichprobe; genaue Zahlen; wo gefunden."]
}
```
Regeln fürs Skript:
- **Englisch**, 5–7 Beats, gesamt ca. 70–95 Wörter (= 25–35 s). Ein Beat = ein Gedanke.
- **Zahlen ausschreiben**, wie sie gesprochen werden („forty-seven percent“, „twenty fourteen“). Die Sprachausgabe liest Ziffern sonst falsch.
- Hook = erster Satz, provokant, ohne Anlauf. Letzter Beat immer `"end": "Not just you."`
- Seltene Wörter vermeiden oder umschreiben (die TTS stolpert, z. B. „fetish“ → „fetish interests“).

**3. `caption.md`** als Codeblock, Aufbau:
```
<Hook-Satz> <1 Emoji>

<2–3 kurze Absätze mit den Zahlen (hier Ziffern: 47%, 2014)>

<Pointe> <Emoji>

<Frage an die Zuschauer> 👇

Not just you · <After Dark, falls Sex-Thema> (<ehrliches Label, z. B. Platform data, not peer-reviewed>)

Source: <Autor (Jahr), Quelle>

#notjustyou #… (6–8 Hashtags)
```

**4. Visuelle Notizen (optional, kurz):** 1 Zeile pro Beat, was groß zu sehen sein soll (Zahl, Wort, Silhouette, Diagramm). Die Produktion setzt das im Look C+D um.

**5. Quellen-Notizen:** Was belegt ist, was selbst gerechnet ist, was offen ist. (So wie bisher: lieber weglassen als runden.)

## 1 · Projekt-Anweisungen (Regeln für jede Folge)
- Antworte auf Deutsch, kurz und präzise, visuell formatiert. Videos immer im Instagram-Reel-Format (1080×1920) und immer mit Instagram-Caption.
- Serie **„Not just you“** auf @vascoda.soda (Instagram + TikTok), **englische** Explainer-Reels: Psychologie/Daten zu Dingen, die man für „nicht normal“ hält.
- **Nur gewagte Themen** (Sex, Dating, Lügen, Rache, Geld, Ego). Brave Themen sind geparkt.
- **Keine erfundenen Zahlen.** Nicht alles muss eine Peer-Review-Studie sein, aber das Label ist ehrlich: SMALL STUDY · CASE STUDY · SURVEY · UNSOLVED · PLATFORM DATA · SELF-REPORTED · INDUSTRY DATA. Quellen vor jeder Folge per Websuche prüfen.
- **Look C+D, dark:** große Roboto-Typografie, ein Signalorange, Punktraster-Silhouetten (halftone), Zähler, Balken. **Keine Strichfiguren, keine unnötige UI** (kein Header, Titel, Fortschrittsbalken, Kapitel). Schematische Diagramme werden als „schematic“ markiert.
- Stimme: Kokoro TTS `af_heart`, Speed 1.1 (nur Englisch möglich). Länge ca. 25–35 s. Ende: „Not just you.“ + Quellen-Endkarte.
- Automatisierung nur mit **Google Apps Script** (kein Make.com). Code immer als komplette Datei, keine großen Änderungen ohne Absprache.

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
- **TikTok:** manuell (montags Digest-Mail; Abhak-Liste). Läuft bisher **besser als Instagram**.
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
