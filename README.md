# Explainer-Baukasten „Not just you“

## START HIER (Stand 31.10.2026) – so entsteht eine Folge wie im Original-Chat
```bash
git clone https://github.com/chris61ds-alt/explainer-kit && cd explainer-kit
bash setup.sh                                 # einmal pro Umgebung: Pakete, Stimme, Spracherkennung (Fonts liegen im Repo)
python3 shared/build.py ep77_casual           # Funktionstest: muss "verify PASS" melden
```
1. **Recherche:** Quelle per Websuche prüfen, genaue Zahlen notieren. Keine erfundenen Zahlen, ehrliches Label (PROJEKT.md).
2. **`epXX_name/script.json`:** Englisch, 5–7 Beats, 70–95 Wörter, Zahlen ausgeschrieben, letzter Beat `"end": "Not just you."`.
3. **`epXX_name/caption.md`:** Format siehe PROJEKT.md, Abschnitt 0.
4. **`epXX_name/render.py`:** im aktuellen **Look C+D (dark)**. Eine Vorlage kopieren und anpassen:
   - `ep77_casual` (Zähler, Raster, Checkbox) · `ep70_kinky` (Silhouetten-Duo, Balken) · `ep81_split_opinion` (Bewertungen, Glitch)
   - `ep82_live` (Live-Diagramm über das ganze Video) · `ep73_blind_day` (Profilkarten, Chat-Blasen aus `shared/dating.py`)
   - Bausteine: `shared/thread.py` (ThreadEpisode, halftone/silhouette, bust/front_bust/body, bbox, glitch, dot_field) +
     `shared/swiss.py` (counter, words_in, box_label, hbar, dim_v, fig, Sound: thud/pop/riser/whoosh/rewind_sfx).
   - Glyphen →, ≈, ✓, ⅓ gibt es in Roboto nicht: als Text schreiben. Keine Strichfiguren, keine Kapitel/Titel/Fortschritts-UI.
5. **Vorschau:** `python3 tools/preview.py epXX_name` → `epXX_name/preview.png` (2 Bilder pro Beat) ansehen, Überlappungen beheben.
6. **Bauen:** `python3 shared/build.py epXX_name` → MP4 (1080×1920, −16 LUFS), Sprach-Check, Technik-Check, Cover. Bei ASR-Fehlern prüfen,
   ob nur der Erkenner irrt (Eigennamen) oder die Aussprache; dann Text umformulieren und neu bauen.
7. **Ausliefern:** MP4 + Caption an Chris. Veröffentlichen (nur mit Schreibzugriff): `publish/media/njXX.mp4/.jpg` (Cover als JPG),
   `publish/schedule.json` erweitern, Repo `notjustyou-media` pushen – Apps Script importiert stündlich automatisch.

---

## Historie (Stand 25.10.2026)

Programmatische Explainer-Reels: 1080×1920, 30 fps, Instagram-Safe-Zones, KI-Stimme, Sound per Code, Endprüfung.

## Ordner
- `ep02_doorway/` – **aktueller Hausstil „Soft & Cute"** (Bohnen-Figur, Pastell, Dur-Sound), Stimme `af_heart`, Tempo 1.05
- `ep01_voice/` – Editorial-Monochrome-Variante (dunkel, Rot-Akzent)
- `pilot_monty/` – Ziegenproblem-Pilot inkl. Beweis (`proof.py`)
- `shared/asr_check.py` – Spracherkennung + Wortfehlerrate gegen das Skript
- `shared/verify.py` – Endprüfung des fertigen MP4 (Format, Schwarzbilder, LUFS, True Peak, Größe, SHA-256)
- `tools/` – Stimmproben-Video, Style-Frames

## Setup (neue Session)
```bash
pip install kokoro-onnx soundfile sherpa-onnx scipy numpy pillow --break-system-packages
mkdir -p ~/kokoro && cd ~/kokoro
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
mkdir -p ~/asr && cd ~/asr && curl -L -o w.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2 && tar xjf w.tar.bz2
# Fonts (Roboto Black/Bold/Condensed + Roboto Mono) aus npm: roboto-fontface@0.10.0, typeface-roboto-mono@1.1.13 → ../fonts/
```

## Ablauf pro Folge
1. Quellen per Websuche prüfen → `script.json` (beats + sources)
2. `python3 tts.py` → `vo/*.wav` + `meta.json`
3. `python3 ../shared/asr_check.py` → Aussprache prüfen, Text anpassen
4. `python3 render.py sheet.png --t 1,5,10` → Kontaktbogen mit Safe-Zone-Overlay
5. `python3 render.py folge.mp4` → Video + Sound (−16 LUFS)
6. `python3 ../shared/verify.py folge.mp4` + ASR am fertigen Video
7. `caption.md` schreiben und immer mit dem Video ausliefern (Englisch: Hook-Frage, Kernaussage mit Zahlen, „Not just you. 💜“, Quellen, CTA, 5–7 Hashtags inkl. #notjustyou)

## Regeln
- Jede Zahl aus Beleg/Quelle, nichts erfinden; Schematisches als „schematic" kennzeichnen
- Visuals an Wörter im Sprechtext gebunden (`cue()`), deterministisch pro Frame
- Inhalte in Safe Zones: oben 200 px, unten 440 px, rechts 120 px frei

## Hausstil „Swiss Detail“ (seit No. 06)
`shared/swiss.py` – Raster, Riesen-Typo (Roboto Black/Condensed), eine Signalfarbe (Orange), Aicher-Piktogramme mit Posen
(IDLE, TALK, WORRY, FACEPALM, LAUGH, SHRUG, OPEN, SING, WAVE, WALK, SIT), Requisiten (cup, table, chair, mic, phone, door, stage),
Anmerkungen (note, dim_h/dim_v, box_label, ruler, scale7, hbar, legend, fig), Kapitel + Fortschrittsbalken, Untertitel mit
orangem aktuellem Wort (max. 3 Zeilen pro Seite), Endkarte, dunkler Beat (Am–F–C–G, 96 bpm) + sfx (thud, rewind_sfx, riser).
Vorlage: `ep07_beautiful_mess/render.py` (`Episode(...)`, `EP.scenes = {...}`, `EP.run(FX)`). Hook ab Frame 0, Stimme ab 0,15 s, Tempo 1.1.
Der weiche Stil (`shared/cute.py`) bleibt für No. 02–05 erhalten.

## Swiss Detail v2 (seit No. 11)
- **Ein Befehl pro Folge:** `python3 shared/build.py epXX_name` → TTS (nur wenn script.json geändert), ASR Stimme, Render, verify,
  ASR auf dem fertigen Mix pro Beat (keine 30-s-Fenster-Fehler, Zahlen/Halluzinationen normalisiert), Cover-PNG, Caption-Check → `build_report.json`
- **Weiche Posen:** `pose_seq(t, [(t0, POSE), ...])` morpht statt zu springen; `move(t, [(t0, x), ...])` für Positionen
- **Figuren über Szenen hinweg:** `EP.layers.append(fn)` – Akteure gleiten zwischen Szenen-Zielen (Match-Cut statt Neu-Erscheinen)
- **Kamera:** langsamer Push pro Szene (`drift`), Punch-in bei jedem Schnitt
- **Musik pro Folge:** `music=dict(bpm, root, prog=minor|major|warm|dream|tense, kick=half|four, gaps=[(t0, t1)])` – Stille vor der Pointe
- **Loop-Ende:** letzte 0,5 s wischen zurück auf Frame 0 (nahtloser Instagram-Loop)
- **Cover:** `cover=dict(words=[...], kicker=...)` → `epXX_cover.png` (Inhalt im 3:4-Grid-Ausschnitt)
- Ziel-Länge 25–35 s · pro Szene eine Haupt-Aussage
