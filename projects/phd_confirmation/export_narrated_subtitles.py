from __future__ import annotations

import argparse
import textwrap
import wave
from pathlib import Path

from build_narrated_slides_preview import combine_slides


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "narration" / "rendered"
SRT_OUTPUT = OUTPUT_DIR / "phd_confirmation_narrated_preview.srt"
VTT_OUTPUT = OUTPUT_DIR / "phd_confirmation_narrated_preview.vtt"


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / float(audio.getframerate())


def srt_time(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def vtt_time(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


def wrap_text(text: str, width: int) -> str:
    one_line = " ".join(text.split())
    return "\n".join(textwrap.wrap(one_line, width=width, break_long_words=False, break_on_hyphens=False))


def build_cues(pause: float, width: int) -> list[tuple[float, float, str]]:
    slides = combine_slides(ROOT)
    cues: list[tuple[float, float, str]] = []
    cursor = 0.0
    for index, slide in enumerate(slides):
        duration = wav_duration(ROOT / "narration" / "audio" / f"{index:03d}.wav")
        cues.append((cursor, cursor + duration, wrap_text(slide.narration, width)))
        cursor += duration + pause
    return cues


def write_srt(cues: list[tuple[float, float, str]], path: Path) -> None:
    blocks = []
    for index, (start, end, text) in enumerate(cues, start=1):
        blocks.append(f"{index}\n{srt_time(start)} --> {srt_time(end)}\n{text}")
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def write_vtt(cues: list[tuple[float, float, str]], path: Path) -> None:
    blocks = ["WEBVTT"]
    for start, end, text in cues:
        blocks.append(f"{vtt_time(start)} --> {vtt_time(end)} line:88% position:50% align:middle\n{text}")
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export external subtitle files for the narrated preview video.")
    parser.add_argument("--pause", type=float, default=0.85, help="Pause length used when render_narrated_video.py created the MP4.")
    parser.add_argument("--wrap-width", type=int, default=86)
    parser.add_argument("--srt", type=Path, default=SRT_OUTPUT)
    parser.add_argument("--vtt", type=Path, default=VTT_OUTPUT)
    args = parser.parse_args()

    srt_path = args.srt if args.srt.is_absolute() else (Path.cwd() / args.srt).resolve()
    vtt_path = args.vtt if args.vtt.is_absolute() else (Path.cwd() / args.vtt).resolve()
    srt_path.parent.mkdir(parents=True, exist_ok=True)
    vtt_path.parent.mkdir(parents=True, exist_ok=True)

    cues = build_cues(args.pause, args.wrap_width)
    write_srt(cues, srt_path)
    write_vtt(cues, vtt_path)
    print(f"Wrote {srt_path}")
    print(f"Wrote {vtt_path}")
    print(f"Cues: {len(cues)}")


if __name__ == "__main__":
    main()
