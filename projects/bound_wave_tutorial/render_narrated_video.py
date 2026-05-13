from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import wave
from pathlib import Path

from build_narrated_slides_preview import combine_slides


ROOT = Path(__file__).resolve().parent
DEFAULT_FFMPEG = Path(
    r"C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
)
WORK_DIR = ROOT / "narration" / "video_work"
OUTPUT_DIR = ROOT / "narration" / "rendered"
OUTPUT = OUTPUT_DIR / "bound_wave_intro_narrated.mp4"
VIDEO_DURATION_RE = re.compile(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)")


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


def video_duration(ffmpeg: Path, path: Path) -> float:
    result = subprocess.run(
        [str(ffmpeg), "-hide_banner", "-i", str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    match = VIDEO_DURATION_RE.search(result.stdout)
    if not match:
        raise RuntimeError(f"Could not read video duration for {path}")
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def run(args: list[str]) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def render_segment(
    ffmpeg: Path,
    index: int,
    video_path: Path,
    audio_path: Path,
    loop_video: bool,
    pause: float,
    audio_preroll: float,
    width: int,
    height: int,
    fps: int,
) -> Path:
    audio_seconds = wav_duration(audio_path)
    target_seconds = audio_preroll + audio_seconds + pause
    out_path = WORK_DIR / f"segment_{index:03d}.mp4"

    video_args: list[str] = []
    if loop_video:
        video_args.extend(["-stream_loop", "-1"])
    video_args.extend(["-i", str(video_path)])

    if loop_video:
        video_filter = (
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,"
            f"fps={fps},trim=duration={target_seconds:.3f},setpts=PTS-STARTPTS[v]"
        )
    else:
        source_seconds = video_duration(ffmpeg, video_path)
        hold_seconds = max(0.0, target_seconds - source_seconds)
        trim_seconds = min(source_seconds, target_seconds)
        video_filter = (
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,"
            f"fps={fps},trim=duration={trim_seconds:.3f},"
            f"tpad=stop_mode=clone:stop_duration={hold_seconds:.3f},setpts=PTS-STARTPTS[v]"
        )

    filter_complex = (
        f"{video_filter};"
        "[1:a]aresample=48000,aformat=channel_layouts=stereo[a0];"
        "[2:a]aresample=48000,aformat=channel_layouts=stereo[pre];"
        "[3:a]aresample=48000,aformat=channel_layouts=stereo[post];"
        "[pre][a0][post]concat=n=3:v=0:a=1[a]"
    )

    run(
        [
            str(ffmpeg),
            "-y",
            *video_args,
            "-i",
            str(audio_path),
            "-f",
            "lavfi",
            "-t",
            f"{max(audio_preroll, 0.001):.3f}",
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-f",
            "lavfi",
            "-t",
            f"{pause:.3f}",
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "23",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-movflags",
            "+faststart",
            "-shortest",
            str(out_path),
        ]
    )
    return out_path


def concat_segments(ffmpeg: Path, segments: list[Path], output: Path, width: int, height: int, fps: int) -> None:
    concat_list = WORK_DIR / "concat_segments.txt"
    concat_list.write_text(
        "\n".join(f"file '{segment.as_posix()}'" for segment in segments) + "\n",
        encoding="utf-8",
    )
    run(
        [
            str(ffmpeg),
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-vf",
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,fps={fps},setpts=N/({fps}*TB)",
            "-af",
            "aresample=async=1:first_pts=0",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "23",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a narrated MP4 from the current linked slide videos and page audio.")
    parser.add_argument("--pause", type=float, default=0.85, help="Seconds of silence to keep after each page narration.")
    parser.add_argument(
        "--audio-preroll",
        type=float,
        default=0.65,
        help="Seconds to let each slide reveal settle before narration begins.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Render only the first N pages for a smoke test.")
    parser.add_argument(
        "--audio-shift",
        type=int,
        default=0,
        help="Shift narration relative to video index. Use 1 if audio sounds one page behind the animation.",
    )
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--concat-only", action="store_true", help="Reuse existing per-page segments and only rebuild the final MP4.")
    args = parser.parse_args()

    ffmpeg = find_ffmpeg()
    output = args.output if args.output.is_absolute() else (Path.cwd() / args.output).resolve()
    slides = combine_slides(ROOT)
    if args.limit is not None:
        slides = slides[: args.limit]

    output.parent.mkdir(parents=True, exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    if args.concat_only:
        segments = [WORK_DIR / f"segment_{index:03d}.mp4" for index in range(len(slides))]
        missing_segments = [segment for segment in segments if not segment.exists()]
        if missing_segments:
            raise FileNotFoundError(f"Missing {len(missing_segments)} segment files; rerun without --concat-only.")
    else:
        segments = []
        for index, slide in enumerate(slides):
            video_path = ROOT / slide.video
            audio_index = index if index == 0 else index + args.audio_shift
            if audio_index < 0 or audio_index >= len(slides):
                print(f"[{index + 1}/{len(slides)}] {slide.title} skipped: shifted audio index {audio_index} is out of range")
                continue
            audio_path = ROOT / "narration" / "audio" / f"{audio_index:03d}.wav"
            if not video_path.exists():
                raise FileNotFoundError(video_path)
            if not audio_path.exists():
                raise FileNotFoundError(audio_path)
            print(f"[{index + 1}/{len(slides)}] {slide.title} + audio {audio_index:03d}")
            segments.append(
                render_segment(
                    ffmpeg=ffmpeg,
                    index=index,
                    video_path=video_path,
                    audio_path=audio_path,
                    loop_video=slide.loop,
                    pause=args.pause,
                    audio_preroll=args.audio_preroll,
                    width=args.width,
                    height=args.height,
                    fps=args.fps,
                )
            )

    concat_segments(ffmpeg, segments, output, args.width, args.height, args.fps)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
