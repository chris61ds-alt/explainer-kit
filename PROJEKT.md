# Projekt „Not just you“ – Briefing (Stand 31.10.2026)

## 0 · Arbeitsweise: so entstehen fertige Videos
**Jeder Chat produziert selbst ein fertiges Video**, nicht nur ein Skript. Grundlage ist der Skill **`not-just-you-reel`**:
Repo klonen → `bash setup.sh` → recherchieren → script.json + caption.md → render.py nach Vorlage (Look C+D) → Vorschau ansehen → `shared/build.py` → MP4 + Caption an Chris.
Voraussetzung: Code-Ausführung und Netzzugriff auf github.com. Veröffentlichen (Push ins Media-Repo) nur dort, wo Schreibzugriff besteht.

Nur wenn ein Chat **nicht rendern kann** oder keinen Schreibzugriff hat, liefert er das Übergabe-Paket unten. Chris kopiert es dann in eine Session, die bauen und veröffentlichen kann.

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
- **Szenen-Hintergründe (ab No. 93, automatisch in `ThreadEpisode`):** die **Auflösungs-Slide nach jedem Teaser** („…: NEXT“) ist **vollflächig orange** (Text schwarz, die Antwort weiß; Chrome + Untertitel blenden mit). Eine Szene namens **`study`** bekommt **helles, gedämpftes Grau** (blendet nachts nicht). Sonst dunkel. Override pro Folge: `EP.bg = {"szene": "dark"|"orange"|"light"}`; `NJY_BGS=0/1` schaltet global. Ältere Folgen (< 93) bleiben dunkel, auch beim Neu-Rendern.
- Stimme: Kokoro TTS **Mischung 50 % `af_heart` + 50 % `af_bella`** (`"voice": "af_heart:0.5+af_bella:0.5"`, seit 02.11. etwas fröhlicher; vorher reines `af_heart`), `lang: en-us`, Speed 1.1. (`bf_emma` am 31.10. getestet und wieder verworfen: klang schlechter.) Länge ca. 25–35 s.
- **Audio v5 (seit 01.11., Standard für neue Folgen):** `music=dict(..., audio="v5")` im render.py. Musik folgt dem Skript (leises Intro bei der Rate-Frage → Aufbau mit sich öffnendem Filter → Drop beim Reveal → ausgedünntes Outro), Wirbel vor Schnitten, Variation alle 4 Takte, Zähler bekommen eine steigende Tonleiter + Glocke; Kit „After Dark“ (808, Claps, Hats, Arp). Code: `shared/sound5.py`. Bestehende Folgen bleiben auf v3, bis Chris anders entscheidet.
- **Version ohne Musik:** nur auf Wunsch (Chris braucht sie nicht standardmäßig): `python3 tools/nomusic.py epNN_x` → `epNN_x_nomusic.mp4`.
- **Einstieg abwechseln (seit 01.11.):** nicht immer eine Rate-Frage. Etwa jede zweite Folge startet mit einem **Statement** (Beat `claim` mit `screen`-Zeilen, optional `stamp` = Gegenzahl/Kontext, z. B. „1990: 3 %“): Behauptung groß ab Frame 0, letzte Zeile orange, darunter „Here's the data.“. Eigene Bildelemente: `EP.scenes["claim"]` = Funktion, die `EP.claim_scene()` aufruft und ergänzt (Beispiele No. 89, 91). Im Plan Frage und Statement abwechseln.
- **Erzählerin „Dot“ (seit 02.11., No. 92):** die KI-Stimme ist eine **Katze im Punktraster-Look** (Silhouette aus Dots, ausgesparte Augen mit orangem Iris, ω-Mund, drei Punkte auf der Stirn, **orange Kopfhörer** = einzige Ausnahme von „Orange = nur die Antwort“). Spricht lippensynchron, blinzelt, wedelt mit dem Schwanz, Ausdrücke talk/happy/wow. Charakter: neugierig, trocken-witzig, nerdig, nie werblich; sagt offen, dass sie KI ist. Code: `ep92_meet_dot/dot_cat.py` + Lip-Sync-Helfer in `ep92_meet_dot/render.py`. (Menschliche/Anime-Entwürfe verworfen: „zu menschlich“, „Stil passt nicht“.)
- **Erzählton lebendig (seit 02.11., A/B-Test No. 86):** neugierig, leicht ungläubig, nicht werblich. Kurze Einwürfe („Okay, quick guess!“, „Here's the wild part.“, „Not even close.“, „And it gets better.“, „And here's the kicker.“), Ausrufezeichen und Rückfragen („Men? Only twenty-one.“). Tempo-Kontrast pro Beat: Einstieg/Hook/Re-Hook `"speed": 1.12–1.17`, Reveals bleiben langsam (automatisch). Zahlen bleiben exakt.
- **Pausen (seit 02.11.):** innerhalb eines Beats max. 0,15 s (`squeeze()` in tts.py), zwischen Beats 0,34–0,4 s (Timeline, tight pace). Der Satz fließt, Luft gibt es zwischen den Gedanken.
- **Drei Einstiege, im Plan mischen:** ① Rate-Frage zu den Daten (`guess`, Label „GUESS FIRST“) ② Statement (`claim`) ③ Frage an den Zuschauer (`guess` mit `"guess_label": "BE HONEST"` und z. B. `"guess_prompt": "Yes or no?"`, Text beginnt mit „Be honest: …“; Beispiel No. 88).
- **Rate-Frage:** optional `"guess_prompt": "Yes or no?"` im script.json (Standard: „Your number?“).
- **Ende (seit 31.10.):** harter Schnitt auf die Pointe, ~1 s stehen lassen, dann Loop in den Hook. Kein gesprochenes „Not just you“, keine Endkarte, kein Wisch-Übergang. Quellen stehen in der Caption, das Label oben rechts bleibt. (Der `end`-Beat bleibt im script.json, wird aber stumm geschaltet; `Timeline(..., end="card")` für Ausnahmen.)
- **Impuls-Takt (Standard seit 31.10.):** jede gesprochene Zahl = Zoom-Puls + Klick; Build-Report zeigt `longest_calm_s` – über 3 s ohne Ereignis wird markiert → in render.py einen Moment ergänzen (Label springt auf, Häkchen, Puls …).
- **Magic Move (Pflicht für neue Folgen, ThreadEpisode):** jede Szene gibt ein Element an die nächste weiter: `EP.carry = {"zielszene": [(src_box, dst_box)]}` (Element fliegt, Rest wischt); gleiche Grafik mit neuen Werten → `EP.cuts = {"zielszene": "stay"}` und in der Szene von den alten Werten aus animieren. Nur wo es Sinn ergibt (Ring → Ring, Person → Datenpunkt, YES → Überschrift); Text → anderer Text oder Balken → Figur wirkt erzwungen, dann normal wischen. Vorbild: ep66_cheating/render.py.
- **Stil v3 (Standard seit 31.10.):** Orange nur für die Antwort (Banner weiß, Label grau), Wisch-Übergang 0,3 s mit Bewegungsunschärfe, Musik mit Hi-Hats/Arp, vor jeder Auflösung Riser → Stille → Bass-Schlag, Stimme komprimiert, Auflösungen langsamer mit Pause vor der Zahl. `NJY_STYLE=v2` = alter Look.
- **Format v2 (Test seit 31.10., Folgen 66 50 69 39 67 49):** TikTok-Daten zeigen: die Hälfte ist nach 1 s weg. Daher:
  1. erster Beat `guess` mit `"screen": [Zeilen]` → Rate-Frage groß ab Frame 0 + 3-2-1-Countdown („GUESS FIRST“);
  2. pro Beat optional `"tease"` (Teilstring des Texts, offene Schleife) + `"show"` (Banner) → **Rehook nach Hook**, alle ~6–8 s einer;
  3. oben im script.json `"ask"` → Kommentarfrage als Banner auf der letzten Szene, Caption: erste Zeile = Rate-Frage, letzte = Frage + 👇;
  4. Pausen automatisch kurz (`NJY_PACE=tight`, max. 0,3 s), Slam-Zoom auf Frame 0. Alte Skripte liegen als `script_v1.json` daneben.
  Auswertung nach ~6 TikToks: Views, Ø-Wiedergabe, Kommentare vs. bisherige C+D-Folgen.
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
