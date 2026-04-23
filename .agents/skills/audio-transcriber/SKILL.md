---
name: audio-transcriber
description: Transcribes audio files to SRT subtitle format with precise timestamps using faster-whisper. Processes audio in overlapping chunks to preserve context across boundaries. Use when the user wants to transcribe audio, generate subtitles, convert speech to text, or produce a .srt file from any audio or video file.
---

# Audio Transcriber Skill

Converts audio files of any length to well-formatted `.srt` subtitle files using [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — a CTranslate2-accelerated reimplementation of OpenAI Whisper that runs 4× faster at the same accuracy.

Audio is processed in overlapping chunks so long files stay memory-efficient and context is never lost at chunk boundaries. The last few transcribed sentences are passed as `initial_prompt` to each subsequent chunk, keeping the model grounded in the preceding speech.

## When to Use

- "Transcribe this audio/video file"
- "Generate subtitles for…"
- "Convert this recording to text with timestamps"
- "Create an SRT file from…"
- User provides an audio file (`.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`, `.opus`, `.webm`, `.mp4`, …)

---

## Instructions

### Step 1 — Verify ffmpeg

`pydub` requires `ffmpeg` for non-WAV formats. Check and install if missing:

```bash
ffmpeg -version 2>/dev/null || echo "ffmpeg not found"

# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows (winget)
winget install ffmpeg
```

### Step 2 — Locate the transcription script

The skill ships a ready-to-run script at `scripts/transcribe.py` (relative to this skill's directory).
Find its absolute path and use it in subsequent steps.

The script uses [PEP 723 inline metadata](https://peps.python.org/pep-0723/) — `uv run` reads the
`# /// script` block and installs `faster-whisper` automatically into an isolated environment on
first run. No manual `pip install` needed. Audio loading uses `ffmpeg` directly (already required),
so there are no fragile Python-version-sensitive dependencies.

### Step 3 — Run transcription

```bash
uv run <skill_dir>/scripts/transcribe.py <audio_file> [options]
```

**Key options:**

| Option | Default | Notes |
|---|---|---|
| `-o / --output` | `<input>.srt` | Override the output path |
| `-m / --model` | `base` | See model guide below |
| `-l / --language` | auto-detect | BCP-47 code (e.g. `en`, `es`, `pt`) |
| `--chunk-duration` | `30` | Seconds per processing chunk |
| `--overlap` | `3` | Overlap window on each side of a chunk |
| `--device` | `auto` | `cpu`, `cuda`, or `auto` |

**Typical invocations:**

```bash
# Quick transcription — auto language, base model
uv run transcribe.py interview.mp3

# Specify language and higher-quality model
uv run transcribe.py lecture.m4a -m small -l en

# Long file with custom output path
uv run transcribe.py podcast.mp3 -o podcast.srt -m medium -l en

# GPU acceleration
uv run transcribe.py video.mp4 --device cuda -m large-v3
```

### Step 4 — Report the result

After the script finishes, tell the user:
- The path to the generated `.srt` file
- The number of subtitle segments written
- The model and language used
- Any warnings or errors from the run

---

## Model Selection Guide

| Model | Speed | Accuracy | VRAM / RAM | When to use |
|---|---|---|---|---|
| `tiny` | Fastest | Low | ~1 GB | Quick drafts, testing |
| `base` | Fast | Good | ~1 GB | Default — good balance |
| `small` | Moderate | Better | ~2 GB | Recommended for production |
| `medium` | Slow | High | ~5 GB | Technical/accented speech |
| `large-v2` | Slowest | Highest | ~10 GB | Maximum accuracy |
| `large-v3` | Slowest | Highest | ~10 GB | Best available model |

**Rule of thumb:**
- Use `base` for casual recordings or drafts.
- Use `small` or `medium` for meetings, interviews, or unclear audio.
- Use `large-v3` only when accuracy is critical and time/memory allow.

---

## How Chunked Processing Works

```
Audio: |──────────────────────────────────────────────────────|
                                                                total
Chunk 1 fetch:  |── overlap ──|────── core (0–30s) ──────|── overlap ──|
Chunk 2 fetch:              |── overlap ──|── core (30–60s) ──|── overlap ──|
Chunk 3 fetch:                          |── overlap ──|── core (60–90s) ──|
```

- **Core region**: the canonical window for this chunk; only segments whose start time falls here are kept.
- **Overlap region**: extra audio fetched on both sides so the model hears complete words/sentences at the boundary. The resulting segments are discarded (they belong to the neighboring chunk's core).
- **`initial_prompt`**: the last 3 transcribed segments from the previous chunk are passed as text context, preserving style, vocabulary, and casing continuity across chunk boundaries.

This combination — audio overlap + text prompt — prevents the most common failure modes: truncated words at cuts and vocabulary drift between chunks.

---

## SRT Output Format

```
1
00:00:00,000 --> 00:00:04,380
Welcome to today's session on distributed systems.

2
00:00:04,380 --> 00:00:09,120
We'll begin with a brief overview of consensus algorithms.

3
00:00:09,120 --> 00:00:14,760
The Raft protocol was designed to be more understandable than Paxos.
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `No module named 'faster_whisper'` | Not installed | `pip install faster-whisper` |
| `ffmpeg not found` | ffmpeg missing | Install via brew / apt / winget |
| `FileNotFoundError` | Wrong path | Use absolute path for the audio file |
| Empty or blank SRT | VAD filtered all audio | Try `--chunk-duration 60` or disable VAD (edit script) |
| Garbled output | Wrong language | Specify `-l <lang>` explicitly |
| Out of memory | Model too large | Use a smaller model (`-m small`) |
| Timestamps drift | Overlap too small | Increase `--overlap 5` |
| Slow on CPU | Default device | Add `--device cpu` and use `tiny` or `base` |

---

## Examples

- "Transcribe interview.mp3" → run with `base` model, auto-language
- "Generate subtitles for my lecture recording in Spanish" → run with `-l es -m small`
- "Transcribe this 2-hour podcast accurately" → suggest `medium` or `large-v2`, warn about runtime
- "Create SRT from video.mp4 with high accuracy" → run with `-m large-v3`
