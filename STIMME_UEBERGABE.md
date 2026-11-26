# Übergabe: neue Stimme „alba“ (Kyutai Pocket TTS) – Stand 26.11.2026

**Entscheidung (Chris, 26.11.2026):** Mit der Stimme **Nr. 01 „alba“** aus Kyutai Pocket TTS weitermachen
(Hörprobe mit 17 Stimmen, 00 = bisheriges Kokoro `af_heart:0.5+af_bella:0.5`).

## Was bekannt ist
| Punkt | Stand |
|---|---|
| Paket | `pocket-tts` 4.0.1 (PyPI), CLI `pocket-tts generate --voice alba --text "…" --output-path x.wav` |
| Installation | `pip install --break-system-packages pocket-tts --extra-index-url https://download.pytorch.org/whl/cpu` (CPU-PyTorch, dauert > 10 min) |
| Modell | Standard `--language english` (= `english_2026-10`), ~100M Parameter, läuft auf CPU, ~14 s für 8 s Audio inkl. Laden |
| Gewichte lädt es von | Hugging Face (von hier erreichbar, ohne Token; Warnung zu Rate-Limits ignorierbar) |
| Lizenz Modell | CC BY 4.0 (huggingface.co/kyutai/pocket-tts-without-voice-cloning) |
| Lizenz Stimme alba | CC BY 4.0 (huggingface.co/kyutai/tts-voices, Ordner alba-mackenna) → **kommerziell ok, Namensnennung nötig** |
| Verständlichkeit | Whisper-ASR-Test: 0 Fehler auf dem Testsatz; Sprechtempo ähnlich wie Kokoro (7,5 s vs. 7,6 s) |
| Verboten | Stimmen klonen ohne ausdrückliche Zustimmung (alba ist eine Fertigstimme, kein Problem) |

## Was noch zu tun ist (Reihenfolge)
1. **`shared/tts.py` erweitern:** `"voice": "pocket:alba"` in `script.json` → pro Beat mit Pocket TTS erzeugen (Modell nur einmal laden, Python-API statt CLI, falls vorhanden; sonst CLI je Beat), danach wie bisher `trim` + `squeeze` + Fades → `vo/<beat>.wav` + `meta.json`. Kokoro dann nicht laden (Muster: der `EXT`-Zweig für ElevenLabs, 22.11.2026). Der Hash in `build.py` enthält `voice`, ein Wechsel erzwingt neue Sprachaufnahmen.
2. **Aussprache prüfen:** Die `SAY`-Regeln in `tts.py` (z. B. „live“ → „liv“) sind für Kokoro gemacht – bei alba testen, ob sie noch nötig sind oder schaden.
3. **Test-Folge:** `ep163_light_story` mit `"voice": "pocket:alba"` neu bauen (verify + rules PASS), Chris alt und neu zum Vergleich schicken.
4. **Nach OK von Chris:**
   - Standardstimme in `REGELN.md` / `START_HIER.md` / `setup.sh` (Installation) eintragen.
   - **Caption-Regel 18 ergänzen:** letzte Zeile „Voice: Kyutai Pocket TTS (alba), CC BY 4.0“ – `rulecheck.py` prüft das.
   - Entscheiden (Chris), ob bereits geplante Folgen neu vertont werden oder nur neue Folgen alba bekommen.

## Wichtig
- Keine Folge mit alba veröffentlichen, bevor Chris den Vergleich gehört hat.
- Hörprobe der 17 Stimmen wurde nur im Chat verschickt (nicht im Repo). Neu erzeugen: Text „It's eighteen hundred. Mary wants her room as bright as yours, for just one hour. That one hour of light will cost her almost six hours of work.“
