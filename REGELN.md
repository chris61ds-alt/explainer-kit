# NOT JUST YOU – Regeln (gültig ab 25.11.2026)

**Diese Datei ist die einzige gültige Regelquelle.** Vor JEDER neuen Folge und jedem Remake komplett lesen.
`shared/rulecheck.py` prüft die mit ⚙ markierten Regeln automatisch beim Build (`build.py` → „rules PASS/FAIL“).
Alte, ersetzte Regeln stehen in `REGELN_ARCHIV.md` (nur zum Nachlesen, nicht anwenden).

---

## Ablauf jeder Folge (Pflicht)
1. `REGELN.md` lesen.
2. Quellen per Websuche prüfen, Zahlen notieren (Regel 1).
3. **Chris den Plan für die ersten 3 Sekunden zeigen** (Regel 11) – erst nach OK bauen. Läuft niemand mit: Plan oben in die Antwort schreiben und markieren.
4. `script.json` mit `"kind"` (Format, siehe Tabelle) + `caption.md` + `render.py`.
5. `python3 tools/preview.py epXX` ansehen → `python3 shared/build.py epXX` → muss **verify PASS** und **rules PASS** melden.
6. Veröffentlichen (Media-Repo, Sendeplan, Checkliste) und Caption mitliefern.

---

## A · Inhalt
1. **Keine erfundenen Zahlen.** Ehrliches Label (SURVEY · SMALL STUDY · PLATFORM DATA · MATH · ESTIMATE …). Vorbehalte in Fußzeile **und** Caption. Schematische Darstellungen als „schematic“ markieren. ⚙ (`sources` im script.json)
2. **Themen:** Daten, die überraschen – Psychologie, Geld, Beziehungen, Länder, Geschichte, Welt. Kein „sex“ im ersten Satz und auf dem Cover (Instagram).
3. **Cover = Frage** statt Behauptung („Is Black Friday really the cheapest day?“).

## B · Skript (Englisch)
4. **Hook spricht dich direkt an** (you / your), ohne Anlauf. ⚙
5. **Ein Gedanke pro Satz**, max. ~12 Wörter, Zahlen ausgeschrieben, Tempo `speed` 1.0 (Hook 1.05).
6. **Erst das Setup, dann die Zahl:** einmal gesprochen sagen, was ein Punkt / Balken / Korn bedeutet („Each dot is one child.“).
7. **Pausen:** 0,4–0,6 s zwischen Beats, **nach der Schlüsselzahl 0,8 s** (Beat in script.json mit `"key": true` markieren). ⚙
8. **Das Warum mit einem Alltagsvergleich** erklären, nicht nur mit Mathe.
9. **Pointe statt Loop:** letzter Satz ist ein vollständiger Schlusssatz; die Auflösung bleibt bis zum letzten Frame stehen; kein Rücksprung. Danach Beat `end` = „Not just you.“ – er wird automatisch **stumm** geschaltet (kurzes Halten auf dem Schlussbild, kein gesprochenes „Not just you“). ⚙
10. **Länge** je Format (Tabelle). ⚙

## C · Bild
11. **Die ersten 3 Sekunden** – die These als Mini-Film (1,5–2,5 s), **Bewegung ab Frame 0**, nah / Ich-Perspektive, ein Ereignis pro Satzteil mit Sound, ein plakatives Element IM Bild (Stempel, Zahl, Person) – kein leeres Erklär-Objekt, kein großer Titel. Dann Kamera raus ins Erklär-Objekt. **Plan vorher an Chris.** ⚙ (Bewegung ab Frame 0)
12. **Ein durchgehendes Objekt** trägt die Folge, alle Schnitte `"stay"`.
13. **Nichts steht still:** im Bildbereich nie länger als **1,5 s** ohne sichtbare Bewegung (Zähler, Wachsen, Schimmern, Kamera). ⚙
14. **Kamera zur Pointe:** in `why`/`end` fährt die Kamera (`fx2.camera` + `cam_path` bzw. `stand.payoff_cam`) – Rückzug aufs Gesamtbild oder langsames Heranfahren an die Antwort. ⚙
15. **Bild = Ton:** kleine Headline (BLK 84) zeigt genau, was gesagt wird, + ein Live-Zähler. Große Typo nur für die eine Zahl. Nie zwei neue Dinge gleichzeitig.
16. **Look (Chris, 13.11.2026):** außer Format `doku`: hell (Papier, weiche Schatten, `light_look` + `shadowed` bzw. `payoff_cam(..., ep=EP)`) für **alle** Formate, Reveal auf Schwarz, Orange nur als Akzent. Komplett dunkel nur, wenn die Geschichte es braucht (Nacht, Lichtkegel). *Offen (Entscheidung Chris):* Zeitreise-Linie dunkel wie die Referenz – bis dahin vorläufig erlaubt. ⚙
17. **Karten:** geht es um ein Land/eine Region, nur diesen Ausschnitt zeigen; Weltkarte nur bei echten Ländervergleichen.

## D · Caption
18. Aufbau: Hook-Frage + 1 Emoji · 2–3 kurze Absätze mit Ziffern · Pointe · Frage an die Zuschauer + 👇 · „Not just you (Vorbehalt)“ · „Source: …“. **Keine Hashtags.** ⚙

## E · Storytelling (Chris, 25.11.2026 – Referenz: Höhlentaucher-Video Boesmansgat)
19. **Startszene = Höhepunkt, nicht Frage:** Die Folge beginnt im spannendsten Moment (Ort, Zeit, Handlung), danach Rückblende. ⚙ (`story`: Beat `cold`)
20. **Einsatz-Satz in den ersten 10 s:** ein Satz, der eine Frage bis zum Ende offen hält („That one glance would cost him his life.“). ⚙ (Beat `stakes`)
21. **Eine Figur:** konkrete Person mit Name/Rolle/Zeit/Ort, der die Daten passieren; echt mit Quelle oder als „illustrative“ gekennzeichnet. Zahlen sind Kulisse, nicht Hauptsache.
22. **Aber / deshalb statt „und dann“:** jeder Abschnitt ist eine Wende (*But*) oder eine Folge (*So*). ⚙ (mind. ein „But“ und ein „So“)
23. **Früh platzieren, spät einlösen:** ein Detail aus den ersten 15 s kehrt in der Auflösung zurück. ⚙ (`"plant"` in script.json muss im Anfang und im `why`-Beat vorkommen)
24. **Licht erzählt mit:** Dunkel nur, wenn die Geschichte es verlangt (Nacht, Kerze, Höhle) – und dann bewusst als Dramaturgie (z. B. die Welt wird heller, wenn die Lösung kommt).

---

## F · Formate
| `kind` | Format | Länge ⚙ | Look | Pflicht-Bausteine |
|---|---|---|---|---|
| `standard` | Erklär-Folge | 24–32 s | hell | Regeln 1–18 |
| `stand` | Where do you stand? | 24–32 s | hell | Frage-Cover, „YOU?“-Marker (`stand.you_marker`) |
| `cliche` | Klischee-Check | 24–32 s | hell | Zitat → Daten → Stempel TRUE/HALF TRUE/FALSE |
| `riddle` | Rätsel | 24–34 s | hell | Frage → Regeln → kurzer 3-2-1 „Lock in your answer“ → Bauchgefühl → Lösung **im selben Video** |
| `pour` | Pour Test | 24–34 s | hell | wie `riddle`, Lösung als Sand, der in etwas Bekanntes rieselt |
| `board` | Beweiswand (Dyatlov-Referenz) | 45–120 s | dunkel | `shared/board.py`: eine durchgehende Wand, Kamerafahrt statt Schnitte, Fotos + Schreibmaschinenkarten + rote Fäden/Markierungen, echte PD-Zeitungsausschnitte, Stempel, Schluss-Zoom-out; **nie nur Karten (Chris 26.11.2026): etwa alle 8–12 s ein Zwischenschnitt – Archivfilm (`VideoInsert`), Bild/Zeichnung (`ShotInsert`), Zeitung auf dem Tisch (`BoardInsert`)**; Ton `audio="doku"` (durchgehendes Bett, Foley), −14 LUFS; Mythos nur als Behauptung |
| `top3` | Top-3-Legenden mit Schwarzblenden | 45–120 s | dunkel | Steigerung 3→1, jede Legende ehrlich als Legende markiert |
| `race` | Zeitreise-Linie | 24–40 s | dunkel vorläufig (offen) | `shared/race.py`: Scrubber + Ereignis-Marker, Fläche, Farbwechsel, Tempo bremst zum Höhepunkt; Stimme nur an 3–5 Stellen, dazwischen Musik |
| `map` | 3D-Karte | 24–32 s | hell | Regel 17, Blöcke = Werte |
| `story` | Geschichte mit Daten | 40–75 s | hell, dunkel nur szenisch (Regel 24) | Regeln 19–24: `cold` → `stakes` → Rückblende → *But* → *So* → Auflösung (`why`) mit eingelöstem Detail |
| `doku` | Doku-Look mit echten Bildern (Chris, 26.11.2026 – Referenz: Teotihuacan-Reel @jimswormhole) | 28–75 s, zügig: kein Bild steht und wartet | dunkel/erdig erlaubt, Licht erzählt mit (Regel 24) | wie `story` (Regeln 19–24) + `shared/doku.py`: Archivbilder (Wikimedia Commons: gemeinfrei/CC0/CC BY) mit langsamer Kamera, Orts-/Jahres-Tag oben links, **Quellenzeile pro Bild** (Titel · Urheber · Lizenz, klein und senkrecht am linken Rand) ⚙, Untertitel weiß + Gold. **Regel 12 hier:** Bildwechsel erlaubt, ein goldenes Element (Linie/Zähler) läuft über alle Bilder durch |
| `mystery` | Rätsel im Ancient-Aliens-Stil, echte Auflösung (Chris, 26.11.2026) | 28–75 s, zügig | Doku-Look | wie `doku` + **Spannungsbogen:** `cold` öffnet EINE Frage (offene Schleife, nicht im ersten Satz auflösen) → `stakes` macht sie groß → `back` nennt den Mythos nur als Behauptung (*„Some said: aliens.“*) ⚙ → *But* die echte Spur (eine Person, ein Fund, eine Zahl) → *So* was wir wirklich wissen → `why` schließt die Schleife und greift den ersten Satz auf ⚙. Der Mythos wird nie bestätigt, die Auflösung ist belegte Forschung. **Offenes Ende erlaubt (Chris 26.11.2026):** Manche Rätsel bleiben ein Mysterium – dann sagt `why` ehrlich, was man weiß und was nicht, und hält die Spannung (kein erfundenes „gelöst“, keine Alien-Bestätigung) |

Bausteine: `fx2.camera/cam_path/stamp/light_look`, `stand.shadowed/you_marker/dashed/stamp_box/payoff_cam`, `race.Race`, `doku.DokuEpisode/Shot/Meter/compare/paper_card` (Untertitel brechen automatisch um, max. 860 px breit – nie über den Rand oder unter die Instagram-Buttons, Chris 26.11.2026) (paper_card = Papier-Karte mit Marker, nur gemeinfreie Zeitungen vor 1930 oder neutrale Studien-Karte mit echtem Titel; Bilder laden: `tools/wikimedia.py`, nur Standardbreiten 500/960/1280/1920 px).


**Stimme (26.11.2026):** Standard `pocket:alba`. Letzte Caption-Zeile immer `Voice: Kyutai Pocket TTS (alba), CC BY 4.0` (Lizenz).

**Karten (27.11.2026):** `shared/maps.py` – Satelliten-Zoom und Routen als Zwischenschnitt (`MapInsert`). Bilder NUR EOX Sentinel-2 cloudless 2016/2017 (CC BY 4.0, Credit `maps.CREDIT`); 2018+ ist CC BY-NC-SA → verboten. Kein Google Maps (Nutzungsbedingungen).
