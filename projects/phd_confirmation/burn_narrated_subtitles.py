from __future__ import annotations

import argparse
import shutil
import subprocess
import textwrap
import wave
from pathlib import Path

from build_narrated_slides_preview import combine_slides


ROOT = Path(__file__).resolve().parent
DEFAULT_FFMPEG = Path(
    r"C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
)
INPUT_VIDEO = ROOT / "narration" / "rendered" / "phd_confirmation_narrated_preview.mp4"
OUTPUT_VIDEO = ROOT / "narration" / "rendered" / "phd_confirmation_narrated_preview_subtitled.mp4"
ASS_PATH = ROOT / "narration" / "rendered" / "phd_confirmation_narrated_preview.ass"


def find_ffmpeg() -> Path:
    path = shutil.which("ffmpeg")
    if path:
        return Path(path)
    if DEFAULT_FFMPEG.exists():
        return DEFAULT_FFMPEG
    raise FileNotFoundError("Could not find ffmpeg on PATH or at the imageio-ffmpeg fallback path.")


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / float(audio.getframerate())


def ass_time(seconds: float) -> str:
    centiseconds = round(seconds * 100)
    hours, remainder = divmod(centiseconds, 360000)
    minutes, remainder = divmod(remainder, 6000)
    secs, centis = divmod(remainder, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"


def escape_ass(text: str) -> str:
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")


def wrap_caption(text: str, width: int) -> str:
    one_line = " ".join(text.split())
    lines = textwrap.wrap(one_line, width=width, break_long_words=False, break_on_hyphens=False)
    return r"\N".join(escape_ass(line) for line in lines)


def build_ass(pause: float, wrap_width: int, margin_v: int, font_size: int) -> str:
    slides = combine_slides(ROOT)
    events: list[str] = []
    cursor = 0.0
    for index, slide in enumerate(slides):
        audio_path = ROOT / "narration" / "audio" / f"{index:03d}.wav"
        duration = wav_duration(audio_path)
        start = cursor
        end = cursor + duration
        text = wrap_caption(slide.narration, wrap_width)
        events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{text}")
        cursor = end + pause

    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,{font_size},&H00F8FAFC,&H00F8FAFC,&HDC000000,&H00000000,0,0,0,0,100,100,0,0,1,2.2,1.0,2,80,80,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
{chr(10).join(events)}
"""


def burn_subtitles(ffmpeg: Path, input_video: Path, ass_path: Path, output_video: Path) -> None:
    output_video.parent.mkdir(parents=True, exist_ok=True)
    subtitle_filter = f"subtitles={ass_path.relative_to(ROOT).as_posix()}"
    subprocess.run(
        [
            str(ffmpeg),
            "-y",
            "-i",
            str(input_video),
            "-vf",
            subtitle_filter,
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "21",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            str(output_video),
        ],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Burn page narration subtitles into the narrated preview MP4.")
    parser.add_argument("--pause", type=float, default=0.85, help="Pause length used when render_narrated_video.py created the MP4.")
    parser.add_argument("--wrap-width", type=int, default=86)
    parser.add_argument("--margin-v", type=int, default=58)
    parser.add_argument("--font-size", type=int, default=31)
    parser.add_argument("--input", type=Path, default=INPUT_VIDEO)
    parser.add_argument("--output", type=Path, default=OUTPUT_VIDEO)
    parser.add_argument("--ass", type=Path, default=ASS_PATH)
    args = parser.parse_args()

    input_video = args.input if args.input.is_absolute() else (Path.cwd() / args.input).resolve()
    output_video = args.output if args.output.is_absolute() else (Path.cwd() / args.output).resolve()
    ass_path = args.ass if args.ass.is_absolute() else (Path.cwd() / args.ass).resolve()

    ass_path.parent.mkdir(parents=True, exist_ok=True)
    ass_path.write_text(build_ass(args.pause, args.wrap_width, args.margin_v, args.font_size), encoding="utf-8")
    burn_subtitles(find_ffmpeg(), input_video, ass_path, output_video)
    print(f"Wrote {output_video}")
    print(f"Wrote {ass_path}")


if __name__ == "__main__":
    main()
