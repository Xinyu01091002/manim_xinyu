from __future__ import annotations

import argparse
import shutil
import subprocess
import textwrap
import wave
from pathlib import Path

from build_narrated_slides_preview import combine_slides
from build_narrated_slides_preview import group_narration_runs


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "narration" / "rendered"
SRT_OUTPUT = OUTPUT_DIR / "bound_wave_intro_narrated.srt"
VTT_OUTPUT = OUTPUT_DIR / "bound_wave_intro_narrated.vtt"
MP4_INPUT = OUTPUT_DIR / "bound_wave_intro_narrated.mp4"
MP4_WITH_SUBTITLES = OUTPUT_DIR / "bound_wave_intro_narrated_with_subtitles.mp4"
DEFAULT_FFMPEG = Path(
    r"C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
)


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


def find_ffmpeg() -> Path:
    path = shutil.which("ffmpeg")
    if path:
        return Path(path)
    if DEFAULT_FFMPEG.exists():
        return DEFAULT_FFMPEG
    raise FileNotFoundError("Could not find ffmpeg on PATH or at the imageio-ffmpeg fallback path.")


def wrap_text(text: str, width: int, max_lines: int) -> str:
    one_line = " ".join(text.split())
    if max_lines <= 1 or len(one_line) <= width:
        return one_line

    wrapped = textwrap.wrap(one_line, width=width, break_long_words=False, break_on_hyphens=False)
    if len(wrapped) <= max_lines:
        return "\n".join(wrapped)

    words = one_line.split()
    best: list[str] | None = None
    best_score: tuple[int, int] | None = None
    for split in range(1, len(words)):
        left = " ".join(words[:split])
        right = " ".join(words[split:])
        if len(left) > width or len(right) > width:
            continue
        score = (abs(len(left) - len(right)), max(len(left), len(right)))
        if best_score is None or score < best_score:
            best_score = score
            best = [left, right]
    if best is not None:
        return "\n".join(best)

    return "\n".join(wrapped[: max_lines - 1] + [" ".join(wrapped[max_lines - 1 :])])


def build_cues(pause: float, audio_preroll: float, width: int, max_lines: int) -> list[tuple[float, float, str]]:
    slides = combine_slides(ROOT)
    runs = group_narration_runs(slides)
    cues: list[tuple[float, float, str]] = []
    cursor = 0.0
    for run in runs:
        duration = wav_duration(ROOT / "narration" / "audio" / f"{run.audio_index:03d}.wav")
        cues.append(
            (
                cursor + audio_preroll,
                cursor + audio_preroll + duration,
                wrap_text(run.narration, width, max_lines),
            )
        )
        cursor += audio_preroll + duration + pause
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


def mux_subtitles(mp4_input: Path, srt_path: Path, mp4_output: Path) -> None:
    ffmpeg = find_ffmpeg()
    mp4_output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(ffmpeg),
            "-y",
            "-i",
            str(mp4_input),
            "-i",
            str(srt_path),
            "-map",
            "0:v:0",
            "-map",
            "0:a:0",
            "-map",
            "1:0",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-c:s",
            "mov_text",
            "-metadata:s:s:0",
            "language=eng",
            "-metadata:s:s:0",
            "title=English narration",
            "-disposition:s:0",
            "0",
            str(mp4_output),
        ],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Export external subtitle files for the narrated preview video.")
    parser.add_argument("--pause", type=float, default=0.85, help="Pause length used when render_narrated_video.py created the MP4.")
    parser.add_argument("--audio-preroll", type=float, default=0.65, help="Preroll used when render_narrated_video.py created the MP4.")
    parser.add_argument("--wrap-width", type=int, default=68)
    parser.add_argument("--max-lines", type=int, default=2)
    parser.add_argument("--srt", type=Path, default=SRT_OUTPUT)
    parser.add_argument("--vtt", type=Path, default=VTT_OUTPUT)
    parser.add_argument("--mux-mp4", action="store_true", help="Also create an MP4 with a selectable mov_text subtitle track.")
    parser.add_argument("--mp4-input", type=Path, default=MP4_INPUT)
    parser.add_argument("--mp4-output", type=Path, default=MP4_WITH_SUBTITLES)
    args = parser.parse_args()

    srt_path = args.srt if args.srt.is_absolute() else (Path.cwd() / args.srt).resolve()
    vtt_path = args.vtt if args.vtt.is_absolute() else (Path.cwd() / args.vtt).resolve()
    mp4_input = args.mp4_input if args.mp4_input.is_absolute() else (Path.cwd() / args.mp4_input).resolve()
    mp4_output = args.mp4_output if args.mp4_output.is_absolute() else (Path.cwd() / args.mp4_output).resolve()
    srt_path.parent.mkdir(parents=True, exist_ok=True)
    vtt_path.parent.mkdir(parents=True, exist_ok=True)

    cues = build_cues(args.pause, args.audio_preroll, args.wrap_width, args.max_lines)
    write_srt(cues, srt_path)
    write_vtt(cues, vtt_path)
    print(f"Wrote {srt_path}")
    print(f"Wrote {vtt_path}")
    print(f"Cues: {len(cues)}")
    if args.mux_mp4:
        mux_subtitles(mp4_input, srt_path, mp4_output)
        print(f"Wrote {mp4_output}")


if __name__ == "__main__":
    main()
