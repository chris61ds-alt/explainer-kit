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
- **Weniger Kleinkram (04.11.2026, ab No. 93 automatisch):** Label oben rechts **nur als ehrliche Einordnung** (SURVEY · CORRELATION, SMALL STUDY …), keine Deko wie „3 STUDIES“ – sonst `label=None`. Die Fig-Zeile zeigt **nur noch Vorbehalte** (A LINK, NOT PROOF · SCHEMATIC · SMALL STUDY), groß in Mono; Zahlen/Quellen stehen in Caption + Endkarte.
- **Sound (04.11.2026, ab No. 93):** Hall nur auf den Effekten (kurz 0,8 s; Reveal-Drop lang 1,8 s; < 300 Hz gefiltert), Stimme + Musik trocken. `music=dict(fxverb=False)` oder `NJY_FXVERB=0` schaltet ab. **Wischer-Sound (04.11.2026, Chris' Wahl „H“):** `shared/swoosh.py` – Swell + tiefer Körper → Snap mit Tiefen-Punch, wandert rechts → links mit dem Bild, eigener Hallschweif, etwas leiser; der Snap landet, wenn die neue Szene steht. Automatisch für alle Folgen ab No. 93 und mit `NJY_UPGRADE=1`. **Stereo (ab No. 93):** Stimme, Kick, Bass, Thuds mittig; Musik + Effekte über 200 Hz breiter (Seitensignal aus verzögerter Kopie → Mono-Summe bleibt identisch), Effekte weiter außen gepannt; Build loggt die Mono-Prüfung. `wide=False` / `NJY_WIDE=0` schaltet ab.
- **Hell öfter (Chris, 03.11.2026):** neben `study` auch **isometrische Objekt-Szenen** immer hell (`EP.bg = {"szene": "light"}`). Dunkel bleibt die Grundfarbe.
- **Isometrie mit Sinn (Chris, 04.11.2026):** Das Objekt zeigt entweder selbst die Daten (Würfel = Stunden, Münzen = Konto) oder jede Beschriftung zeigt auf ein Teil, das zum Tipp gehört (Timer = Pause). Keine reine Deko, keine Call-outs auf beliebige Teile (Negativbeispiel: No. 97 Sofa).
- **Mehr Isometrie (Chris, 04.11.2026): jede neue Folge hat mindestens eine isometrische Szene** (Hook-Aufbau, Recap mit Call-outs oder eine Daten-Szene wie die Stunden-Würfel in No. 100). Requisiten in `shared/tips.py` laufend erweitern (geplant: Smartphone-Explosion, Laptop, Kalender, Münzstapel, Ringschachtel, Torte, Uhr, Haus/Tür, Geschenk, Waage, Sprechblasen-Stapel).
- **Isometrische Objekt-Szenen (`shared/iso.py`, ab No. 96):** technische Linienzeichnung (weiße/graue Flächen, Tinten-Kontur), nummerierte Call-outs in Mono (die Antwort in Orange), Bodenraster, das ausblendet, Teile fallen nacheinander ein (`drop`) + Zähler „PARTS n / N“. Inspiriert von dannystuart („Anatomy“) – Prinzip übernehmen, nicht 1:1 kopieren. Gut für Hook (Aufbau) und Recap (Tipps als Call-outs, Save-Moment). Beispiel: No. 96 Café-Tisch.
- Stimme: Kokoro TTS **Mischung 50 % `af_heart` + 50 % `af_bella`** (`"voice": "af_heart:0.5+af_bella:0.5"`, seit 02.11. etwas fröhlicher; vorher reines `af_heart`), `lang: en-us`, Speed 1.1. (`bf_emma` am 31.10. getestet und wieder verworfen: klang schlechter.) Länge ca. 25–35 s.
- **Audio v5 (seit 01.11., Standard für neue Folgen):** `music=dict(..., audio="v5")` im render.py. Musik folgt dem Skript (leises Intro bei der Rate-Frage → Aufbau mit sich öffnendem Filter → Drop beim Reveal → ausgedünntes Outro), Wirbel vor Schnitten, Variation alle 4 Takte, Zähler bekommen eine steigende Tonleiter + Glocke; Kit „After Dark“ (808, Claps, Hats, Arp). Code: `shared/sound5.py`. Bestehende Folgen bleiben auf v3, bis Chris anders entscheidet.
- **Version ohne Musik:** nur auf Wunsch (Chris braucht sie nicht standardmäßig): `python3 tools/nomusic.py epNN_x` → `epNN_x_nomusic.mp4`.
- **Einstieg abwechseln (seit 01.11.):** nicht immer eine Rate-Frage. Etwa jede zweite Folge startet mit einem **Statement** (Beat `claim` mit `screen`-Zeilen, optional `stamp` = Gegenzahl/Kontext, z. B. „1990: 3 %“): Behauptung groß ab Frame 0, letzte Zeile orange, darunter „Here's the data.“. Eigene Bildelemente: `EP.scenes["claim"]` = Funktion, die `EP.claim_scene()` aufruft und ergänzt (Beispiele No. 89, 91). Im Plan Frage und Statement abwechseln.
- **Erzählerin „Dot“ (seit 02.11., No. 92):** die KI-Stimme ist eine **Katze im Punktraster-Look** (Silhouette aus Dots, ausgesparte Augen mit orangem Iris, ω-Mund, drei Punkte auf der Stirn, **orange Kopfhörer** = einzige Ausnahme von „Orange = nur die Antwort“). Spricht lippensynchron, blinzelt, wedelt mit dem Schwanz, Ausdrücke talk/happy/wow. Charakter: neugierig, trocken-witzig, nerdig, nie werblich; sagt offen, dass sie KI ist. Code: `ep92_meet_dot/dot_cat.py` + Lip-Sync-Helfer in `ep92_meet_dot/render.py`. (Menschliche/Anime-Entwürfe verworfen: „zu menschlich“, „Stil passt nicht“.)
- **Erzählton lebendig (seit 02.11., A/B-Test No. 86):** neugierig, leicht ungläubig, nicht werblich. Kurze Einwürfe („Okay, quick guess!“, „Here's the wild part.“, „Not even close.“, „And it gets better.“, „And here's the kicker.“), Ausrufezeichen und Rückfragen („Men? Only twenty-one.“). Tempo-Kontrast pro Beat: Einstieg/Hook/Re-Hook `"speed": 1.12–1.17`, Reveals bleiben langsam (automatisch). Zahlen bleiben exakt.
- **Pausen (seit 02.11.):** innerhalb eines Beats max. 0,15 s (`squeeze()` in tts.py), zwischen Beats 0,34–0,4 s (Timeline, tight pace). Der Satz fließt, Luft gibt es zwischen den Gedanken.
- **Einstieg (Chris, 04.11.2026): Standard ist das Statement (`claim`)** – wirkt stärker. Rate-Frage („Quick guess“) oder Zuschauer-Frage nur noch gelegentlich, höchstens jede 4. Folge, nie zwei hintereinander im Plan.
- **Kein „sex“ im ersten Satz (Chris, 11.11.2026):** Verdacht auf Reichweiten-Abstrafung. Das Wort darf nicht im ersten gesprochenen Satz, nicht im Claim-Screen, nicht auf dem Cover und nicht in der ersten Caption-Zeile stehen. Umschreiben: „it“, „hookups“, „bedroom“, „one good night together“. Später in der Folge ist es okay.
- **Simulationen (Chris, 11.11.2026):** öfter sichtbare Simulationen, bei denen man direkt sieht, was passiert (Vorbild RandomStuff „walk or run in rain“): live laufende Szene, Zähler wachsen mit, zwei Varianten nebeneinander. Label „SIMULATION · MATH MODEL“. Ein durchgehendes Bild-Objekt pro Folge (Vorbild lockd.in).
- **Fragen in der Stimme (Chris, 05.11.2026):** Kokoro senkt jede Frage am Ende ab → klang wie ein Punkt. Seit 05.11. hebt `shared/tts.py` Ja/Nein- und Fragment-Fragen („And men?“, „Did it work?“) am Ende um bis zu 12 Halbtöne an (Variante „C“, `NJY_QRISE=0` = aus); W-Fragen und „Or …?“ behalten ihren natürlichen Abfall. Klingt besser, aber noch etwas künstlich → **beim Schreiben weniger Rückfragen-Fragmente.** Statt „And men? Forty-one percent!“ lieber Doppelpunkt oder Statement: „And men: forty-one percent!“, „For men, it's forty-one percent!“. Teaser vor einem Reveal als Aussage („Now look at the joint accounts.“) oder als W-Frage („So who took over?“). Höchstens eine Ja/Nein-Frage pro Folge.
- **Du ab Satz 1 (Chris, 06.11.2026):** „Your weird fantasy“ (No. 41) und die Beer-Folge (No. 79) kamen besser an als der Rest. Gemeinsam: Es geht um **den Zuschauer selbst**, die Antwort ist in 1 Sekunde im Kopf, leicht tabu oder „was verrät das über mich?“. Deshalb spricht **jede Folge den Zuschauer ab dem ersten Satz direkt an** („You still check your ex's profile.“ statt „People check their exes.“). Gruppenvergleiche (Männer vs. Frauen) dürfen bleiben, aber erst nach dem Du-Einstieg. Test: 48, 46, 45 vorgezogen (07.–09.11.), dazu No. 109 (Fantasien über andere) und No. 110 (Ex-Profil checken); danach Zahlen vergleichen und entscheiden.
- **Frequenz (Chris, 06.11.2026):** Instagram ab 07.11. **4× pro Tag**: 09:00, 12:30, 18:30, 21:30 (Berlin). Bei diesem Tempo reicht der Vorrat bis 20.11. → Produktion muss mitziehen (≈ 4 neue Folgen pro Tag) oder die Frequenz danach wieder runter.
- **Drei Einstiege, im Plan mischen:** ① Rate-Frage zu den Daten (`guess`, Label „GUESS FIRST“) ② Statement (`claim`) ③ Frage an den Zuschauer (`guess` mit `"guess_label": "QUICK QUESTION"` und z. B. `"guess_prompt": "Yes or no?"`; die Frage kommt **direkt, ohne „Be honest“** – wirkt wie eine Fangfrage, Chris 03.11.2026; Beispiel No. 88).
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
- **LEVEL 2 – Storytelling-Standard (Chris, 12.11.2026, Pilot `ep124p_berkson_pilot`): gilt für jede neue Folge und jedes Remake, geht den älteren Regeln oben vor (Magic Move, Rehook-Banner, Claim-Screen, Ende):**
  1. **Cold Open im Bild:** ab Frame 0 ist das Objekt/die Daten sichtbar und bewegt sich (Welle, Aufbau). Kein Claim-Screen mit Textzeilen, kein „Here's the data.“. Erster Beat heißt `hook`, spricht den Zuschauer direkt an (Du-Regel, kein „sex“).
  2. **Ein durchgehendes Objekt:** eine Grafik/Szene trägt die ganze Folge (Punktwolke, Netzwerk, Kalender, Gitter …). Alle Schnitte `"stay"` (`EP.cuts = {k: "stay" for k in ORDER[1:]}`), keine Wisch-Übergänge, keine Rehook-Banner („…: NEXT“).
  3. **Keine reinen Text-Szenen:** oben eine kleine Headline (BLK 84) + ein **Live-Zähler** (die eine Zahl, die sich ändert). Große Typo nur für die eine Zahl.
  4. **Physische Bewegung:** `spring()` (Überschwingen), Schwerkraft beim Wegfallen, Ruhezustände schimmern leicht – nichts steht still.
  5. **Reveal = orange Hintergrund** (`EP.bg = {"reveal": "orange"}`), sonst dunkel.
  6. **Loop-Ende:** letzter Satz läuft in den ersten Satz hinein („… And it's why“ → „You think …“), das Objekt springt in den Anfangszustand zurück. Kein `ask`-Banner (Kommentar-Frage nur in der Caption), kein gesprochenes „Not just you“.
  7. **Länge 24–32 s** (vorher 18–22 s, Chris 13.11.2026: „zu schnell und zu unklar“), Beats `hook / setup / … / reveal / why`, `lead=.05`.
  10. **VERSTÄNDLICHKEIT GEHT VOR TEMPO (Chris, 13.11.2026):**
     - Sprechtempo `speed` **1.0** (Hook 1.05) statt 1.1/1.13; Lücken zwischen Beats 0,4–0,6 s, **nach der Schlüsselzahl 0,8 s Pause**.
     - **Ein Gedanke pro Satz,** max. ~12 Wörter. Keine Fachwörter ohne Alltagsbild („layers“ → „circles of people you call“).
     - **Erst das Setup verstehen lassen, dann die Zahl:** Was wird gezeigt? Was bedeutet ein Punkt / ein Balken? Das sagt die Stimme einmal klar („Each dot is one person.“).
     - **Das „Warum“ mit einem Alltagsvergleich** erklären, nicht nur mit Mathe-Begriffen („253 pairs“ → „every person can match with 22 others“).
     - **Bild = Ton:** die Headline zeigt genau das, was gerade gesagt wird; nie zwei neue Dinge gleichzeitig im Bild.
     - **Test vor dem Bauen:** Versteht es jemand nach einmal Ansehen ohne Ton-Pause? Sonst Satz streichen oder vereinfachen.
  8. **Formate mischen:** Simulation · Mythos vs. Daten · „3 Dinge“ · „Du hast gefragt“. Label bleibt ehrlich (SIMULATION · MATH MODEL, SURVEY …), Vorbehalte in Fig-Zeile + Caption.
  9. **Bausteine aus `shared/fx2.py`** (nach den „Funfacts“-Reels): `camera()`/`cam_path()` = Kamerafahrt auf das Objekt (Start nah, rauszoomen, beim Reveal reinfahren, Loop zurück), `glow()` = weicher Lichtschein für „aktiv/ja“, `Stream`/`dots()` = tausende Partikel, die sichtbar fließen. Pro Folge mindestens einen davon nutzen, wenn es passt. Erste Folge: No. 100.
  11. **HELLER LOOK = STANDARD (Chris, 13.11.2026):** neue Folgen auf hellem Papier mit **weichen Schatten** (`fx2.soft_shadow`), der Reveal auf **Schwarz** statt Orange (Orange bleibt nur als Akzent für die Antwort). Umsetzung: `ThreadEpisode(dark=True)` lassen und `fx2.light_look(EP, ORDER)` aufrufen; Schatten nur wenn `is_light(EP, t)`, Glow nur in dunklen Szenen. Komplett dunkel nur, wenn die Geschichte es braucht (Nacht, Lichtkegel). Fertige Folgen bleiben, wie sie sind.
  Helfer: `spring()` liegt in `shared/swiss.py`. Erste Remakes (12.11.): 124, 79, 116, 125, 126.
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
