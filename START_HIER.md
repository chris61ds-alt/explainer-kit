# NOT JUST YOU – Übergabe für einen neuen Chat (Stand 26.11.2026)

**Ein neuer Chat liest diese Datei zuerst, dann `REGELN.md`.** Der Skill `not-just-you-reel` verweist ebenfalls hierher.

## 1 · In 2 Minuten startklar
```bash
cd /home/claude                                                          # beliebiger Ordner – beide Repos nebeneinander
git clone https://github.com/chris61ds-alt/explainer-kit explainer-kit   # vorhanden? git pull
git clone https://github.com/chris61ds-alt/notjustyou-media notjustyou-media
cd explainer-kit && ln -s ../../notjustyou-media publish/media              # (lokal, nicht committen)
bash setup.sh                                                             # Pakete, Kokoro-Stimme, Whisper-ASR
python3 shared/build.py ep162_wild_vs_farm                                # Test: verify PASS + rules PASS
```
Die Skripte in `tools/publish/` finden ihre Pfade selbst (Repo = zwei Ebenen über dem Skript, Media-Repo = Nachbarordner `notjustyou-media`; abweichend mit `NJY_MEDIA=/pfad`). Schreiben (Push) braucht Zugriff auf beide GitHub-Repos.

## 2 · Wo was steht
| Datei | Inhalt |
|---|---|
| `REGELN.md` | **einzige gültige Regelquelle** (24 Regeln + Formate). Vor jeder Folge lesen. |
| `REGELN_ARCHIV.md` | alte Regeln – nicht anwenden |
| `PROJEKT.md` | Projekt-Hintergrund, Ordner, Technik-Notizen |
| `shared/rulecheck.py` | automatische Prüfung der ⚙-Regeln (läuft in `build.py`, Ergebnis „rules PASS/FAIL“) |
| `shared/race.py` · `shared/stand.py` · `shared/fx2.py` | Bausteine: Zeitreise-Linie · Stempel/Marker/Kamera/Schatten · Kamera/Look |
| `tools/publish/` | `pub.sh` (neue Folge veröffentlichen) · `repub.sh` (Remake ersetzen) · `chain2.sh` (Builds nacheinander) · `sched.py` (Sendeplan) · `tl.py` (Länge/Timing einer Folge) |
| `tools/checklist/` | Posting-Liste: `make_eps.py` + `build.py` → Artefakt https://claude.ai/artifact/ED3wdyb1wHNpmtNRfyKr8t |
| `publish/schedule.json` | Sendeplan (date, time, no, title, video, cover, caption, …); Kopie im Media-Repo, Apps Script holt ihn stündlich |
| `publish/*.gs` | Google Apps Script (Instagram-Posting, ElevenLabs-Test). Secrets nur in den Script-Eigenschaften. |

## 3 · Workflow je Folge (Kurzform – Details in REGELN.md)
1. `REGELN.md` lesen → Quellen per Websuche prüfen.
2. **Plan der ersten 3 Sekunden an Chris** → auf OK warten.
3. `epNNN_name/` mit `script.json` (`kind`, `sources`, `key`-Beat, bei `story`: `plant`), `caption.md`, `render.py` (Vorlage desselben Formats kopieren).
4. `python3 shared/tts.py` (im Ordner) → `python3 tools/preview.py epNNN_name` ansehen → `python3 shared/build.py epNNN_name` → **verify PASS + rules PASS**.
5. `tools/publish/pub.sh epNNN_name JJJJ-MM-TT HH:MM` (Slots 09:00 · 12:30 · 18:30 · 21:30), Checkliste-Artefakt neu veröffentlichen, Video + Caption an Chris.

## 4 · Formate & Vorlagen
| `kind` | Vorlage |
|---|---|
| `standard` / `stand` | ep149_bank_normal, ep148_middle_class |
| `cliche` | ep151_black_friday, ep146_japan |
| `riddle` / `pour` | ep153_humanity_island, ep156_gold_cube, ep162_wild_vs_farm |
| `race` | ep154_life_england, ep155_murder_europe, ep159_child_mortality |
| `map` | ep144_best_country |
| `story` (neu, Ziel-Niveau) | ep163_light_story |
| `doku` (echte Bilder, 26.11.2026) | ep163d_light_doku (Bilder + `img/credits.json`; Netzwerk-Freigabe für `upload.wikimedia.org` + `commons.wikimedia.org` nötig) |

## 5 · Offene Entscheidungen (Chris)
- **Neue Stimme „alba“ (Kyutai Pocket TTS) ist gewählt, aber noch nicht eingebaut → siehe `STIMME_UEBERGABE.md`.**
- Zeitreise-Linien (`race`): hell oder dunkel wie die Referenz? Bis dahin vorläufig dunkel erlaubt.
- Cover-Regel aus der TikTok-Analyse (max. 3 Wörter, „YOUR …?“) und kürzerer Countdown bei Rätseln – vorgeschlagen, noch nicht bestätigt.
- ElevenLabs-Stimmtest (Apps Script `publish/ElevenLabs.gs`, Job `tts/ab150.json` im Media-Repo) – verschoben.
- Höheres Storytelling-Niveau: nächster Kandidat eine echte Geschichte mit Daten (Format `story`).
