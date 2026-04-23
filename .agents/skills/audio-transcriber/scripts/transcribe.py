#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "faster-whisper",
# ]
# ///
"""Transcribe audio files to SRT format using faster-whisper with chunked processing."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def format_srt_timestamp(seconds: float) -> str:
    total_ms = int(seconds * 1000)
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def check_dependencies() -> None:
    missing = []
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        missing.append("faster-whisper  →  pip install faster-whisper")
    for tool in ("ffmpeg", "ffprobe"):
        try:
            subprocess.run([tool, "-version"], capture_output=True, check=True)
        except FileNotFoundError:
            missing.append(f"{tool}  →  brew install ffmpeg / apt install ffmpeg")
    if missing:
        print("Missing dependencies:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)


def get_duration_ms(path: str) -> int:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "json", path],
        capture_output=True, text=True, check=True,
    )
    return int(float(json.loads(result.stdout)["format"]["duration"]) * 1000)


def extract_chunk(src: str, dst: str, start_ms: int, end_ms: int) -> None:
    """Extract [start_ms, end_ms) from src as 16 kHz mono WAV into dst."""
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "quiet",
            "-i", src,
            "-ss", f"{start_ms / 1000:.3f}",
            "-to", f"{end_ms / 1000:.3f}",
            "-ar", "16000",
            "-ac", "1",
            dst,
        ],
        check=True,
    )


def transcribe_audio(
    input_path: str,
    output_path: str | None = None,
    model_size: str = "base",
    language: str | None = None,
    chunk_duration: int = 30,
    overlap: int = 3,
    device: str = "auto",
) -> str:
    check_dependencies()

    from faster_whisper import WhisperModel

    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"Audio file not found: {src}")

    dst = Path(output_path) if output_path else src.with_suffix(".srt")

    print(f"[1/4] Loading audio: {src.name}")
    total_ms = get_duration_ms(str(src))
    print(f"      Duration: {total_ms / 1000:.1f}s")

    compute_type = "float16" if device == "cuda" else "int8"
    print(f"[2/4] Loading Whisper model '{model_size}' ({device}/{compute_type})")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    chunk_ms = chunk_duration * 1000
    overlap_ms = overlap * 1000
    num_chunks = max(1, (total_ms + chunk_ms - 1) // chunk_ms)

    print(f"[3/4] Transcribing {num_chunks} chunk(s) — {chunk_duration}s each, {overlap}s overlap")
    all_segments: list[dict] = []
    prev_context = ""

    for idx, core_start_ms in enumerate(range(0, total_ms, chunk_ms)):
        core_end_ms = min(core_start_ms + chunk_ms, total_ms)

        # Extend fetch window with overlap on both sides for audio context
        fetch_start_ms = max(0, core_start_ms - overlap_ms)
        fetch_end_ms = min(core_end_ms + overlap_ms, total_ms)
        audio_offset_s = fetch_start_ms / 1000

        pct = (idx + 1) / num_chunks * 100
        print(
            f"      [{idx + 1}/{num_chunks}] "
            f"{core_start_ms / 1000:.1f}s – {core_end_ms / 1000:.1f}s  ({pct:.0f}%)"
        )

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            extract_chunk(str(src), tmp_path, fetch_start_ms, fetch_end_ms)

            raw_segments, _ = model.transcribe(
                tmp_path,
                language=language,
                beam_size=5,
                initial_prompt=prev_context,
                condition_on_previous_text=True,
                vad_filter=True,
                vad_parameters={"min_silence_duration_ms": 500},
            )

            core_start_s = core_start_ms / 1000
            core_end_s = core_end_ms / 1000
            chunk_segments: list[dict] = []

            for seg in raw_segments:
                abs_start = seg.start + audio_offset_s
                abs_end = seg.end + audio_offset_s
                text = seg.text.strip()
                if not text:
                    continue
                # Only keep segments whose start falls in this chunk's core window
                if core_start_s <= abs_start < core_end_s:
                    chunk_segments.append(
                        {"start": abs_start, "end": min(abs_end, core_end_s + overlap_ms / 1000), "text": text}
                    )

            if chunk_segments:
                prev_context = " ".join(s["text"] for s in chunk_segments[-3:])
                all_segments.extend(chunk_segments)

        finally:
            os.unlink(tmp_path)

    print(f"[4/4] Writing {len(all_segments)} subtitle(s) → {dst}")
    with open(dst, "w", encoding="utf-8") as f:
        for i, seg in enumerate(all_segments, 1):
            f.write(f"{i}\n")
            f.write(f"{format_srt_timestamp(seg['start'])} --> {format_srt_timestamp(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")

    print(f"\nDone: {dst}")
    return str(dst)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe audio to SRT using faster-whisper (chunked, context-preserving)"
    )
    parser.add_argument("input", help="Audio file (mp3, wav, m4a, flac, ogg, …)")
    parser.add_argument("-o", "--output", help="Output .srt path (default: <input>.srt)")
    parser.add_argument(
        "-m", "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
        help="Whisper model size (default: base). Larger = more accurate, slower.",
    )
    parser.add_argument(
        "-l", "--language",
        help="BCP-47 language code (e.g. en, es, pt, fr). Auto-detects if omitted.",
    )
    parser.add_argument(
        "--chunk-duration", type=int, default=30, metavar="SECS",
        help="Core chunk length in seconds (default: 30)",
    )
    parser.add_argument(
        "--overlap", type=int, default=3, metavar="SECS",
        help="Overlap window on each side of a chunk (default: 3)",
    )
    parser.add_argument(
        "--device", default="auto", choices=["auto", "cpu", "cuda"],
        help="Inference device (default: auto)",
    )

    args = parser.parse_args()
    transcribe_audio(
        args.input,
        args.output,
        args.model,
        args.language,
        args.chunk_duration,
        args.overlap,
        args.device,
    )
