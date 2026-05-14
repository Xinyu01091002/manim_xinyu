from __future__ import annotations

import argparse
import html
import re
import wave
from pathlib import Path

from build_narrated_slides_preview import OUTPUT as HTML_OUTPUT
from build_narrated_slides_preview import combine_slides
from build_narrated_slides_preview import group_narration_runs


ROOT = Path(__file__).resolve().parent
RENDERED_DIR = ROOT / "narration" / "rendered"
VIDEO_WORK_DIR = ROOT / "narration" / "video_work"
SRT_OUTPUT = RENDERED_DIR / "bound_wave_intro_narrated.srt"
VTT_OUTPUT = RENDERED_DIR / "bound_wave_intro_narrated.vtt"
MP4_OUTPUT = RENDERED_DIR / "bound_wave_intro_narrated.mp4"
MP4_WITH_SUBTITLES = RENDERED_DIR / "bound_wave_intro_narrated_with_subtitles.mp4"
SECTION_RE = re.compile(r'<section class="slide"(?P<attrs>.*?)</section>', re.S)
ATTR_RE = re.compile(r'(data-[\w-]+)="(.*?)"', re.S)
SOURCE_RE = re.compile(r'<source src="(.*?)"')
SRT_CUE_RE = re.compile(r"^\d+\s*$", re.M)


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / float(audio.getframerate())


def srt_time(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def parse_html_sections(path: Path) -> list[dict[str, object]]:
    sections = []
    text = path.read_text(encoding="utf-8")
    for match in SECTION_RE.finditer(text):
        attrs_text = match.group("attrs")
        attrs = {key: html.unescape(value) for key, value in ATTR_RE.findall(attrs_text)}
        sources = [html.unescape(source) for source in SOURCE_RE.findall(attrs_text)]
        sections.append({"attrs": attrs, "sources": sources})
    return sections


def check_html(slides, html_path: Path) -> list[str]:
    errors: list[str] = []
    sections = parse_html_sections(html_path)
    if len(sections) != len(slides):
        errors.append(f"HTML section count mismatch: html={len(sections)} slides={len(slides)}")
        return errors

    for index, (section, slide) in enumerate(zip(sections, slides)):
        attrs = section["attrs"]
        sources = section["sources"]
        expected_audio = f"narration/audio/{slide.audio_index:03d}.wav"
        expected_video = slide.video.replace("\\", "/")
        expected_audio_run_start = index == 0 or slide.audio_index != slides[index - 1].audio_index
        actual_audio_index = attrs.get("data-audio-index")
        actual_audio_run_start = attrs.get("data-audio-run-start")
        actual_script = attrs.get("data-script")
        actual_video = sources[0] if len(sources) > 0 else ""
        actual_audio = sources[1] if len(sources) > 1 else None

        if str(slide.audio_index) != actual_audio_index:
            errors.append(f"HTML slide {index:03d}: data-audio-index={actual_audio_index}, expected {slide.audio_index}")
        if str(expected_audio_run_start).lower() != actual_audio_run_start:
            errors.append(
                f"HTML slide {index:03d}: data-audio-run-start={actual_audio_run_start}, "
                f"expected {str(expected_audio_run_start).lower()}"
            )
        if actual_script != slide.narration:
            errors.append(f"HTML slide {index:03d}: script text does not match mapped narration")
        if expected_audio_run_start and actual_audio != expected_audio:
            errors.append(f"HTML slide {index:03d}: audio source={actual_audio}, expected {expected_audio}")
        if not expected_audio_run_start and actual_audio is not None:
            errors.append(f"HTML slide {index:03d}: continued audio run should not repeat source {actual_audio}")
        if actual_video != expected_video:
            errors.append(f"HTML slide {index:03d}: video source={actual_video}, expected {expected_video}")
    return errors


def check_render_inputs(slides) -> list[str]:
    errors: list[str] = []
    for index, slide in enumerate(slides):
        video_path = ROOT / slide.video
        audio_path = ROOT / "narration" / "audio" / f"{slide.audio_index:03d}.wav"
        if not video_path.exists():
            errors.append(f"Slide {index:03d}: missing video {video_path}")
        if not audio_path.exists():
            errors.append(f"Slide {index:03d}: missing audio {audio_path}")
    return errors


def check_subtitle_wrapping(srt: str, max_lines: int, max_line_length: int) -> list[str]:
    errors: list[str] = []
    blocks = [block.strip() for block in re.split(r"\n\s*\n", srt.strip()) if block.strip()]
    for cue_number, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        if len(lines) < 3:
            continue
        subtitle_lines = lines[2:]
        if len(subtitle_lines) > max_lines:
            errors.append(f"SRT cue {cue_number:03d}: {len(subtitle_lines)} subtitle lines, expected <= {max_lines}")
        for line in subtitle_lines:
            if len(line) > max_line_length:
                errors.append(
                    f"SRT cue {cue_number:03d}: line length {len(line)} exceeds {max_line_length}: {line}"
                )
    return errors


def check_subtitles(
    slides,
    srt_path: Path,
    vtt_path: Path,
    pause: float,
    audio_preroll: float,
    max_lines: int,
    max_line_length: int,
) -> list[str]:
    errors: list[str] = []
    if not srt_path.exists():
        errors.append(f"Missing SRT {srt_path}")
    if not vtt_path.exists():
        errors.append(f"Missing VTT {vtt_path}")
    if errors:
        return errors

    srt = srt_path.read_text(encoding="utf-8")
    vtt = vtt_path.read_text(encoding="utf-8")
    runs = group_narration_runs(slides)
    srt_cues = len(SRT_CUE_RE.findall(srt))
    vtt_cues = vtt.count("-->")
    if srt_cues != len(runs):
        errors.append(f"SRT cue count mismatch: srt={srt_cues} runs={len(runs)}")
    if vtt_cues != len(runs):
        errors.append(f"VTT cue count mismatch: vtt={vtt_cues} runs={len(runs)}")
    errors.extend(check_subtitle_wrapping(srt, max_lines, max_line_length))

    cursor = 0.0
    expected_srt_times = []
    for run in runs:
        duration = wav_duration(ROOT / "narration" / "audio" / f"{run.audio_index:03d}.wav")
        expected_srt_times.append(f"{srt_time(cursor + audio_preroll)} --> {srt_time(cursor + audio_preroll + duration)}")
        cursor += audio_preroll + duration + pause

    for index in (0, min(40, len(runs) - 1), len(runs) - 1):
        if expected_srt_times[index] not in srt:
            errors.append(f"SRT cue {index:03d}: expected time range not found: {expected_srt_times[index]}")
    return errors


def check_rendered_files(expected_segment_count: int, mp4_path: Path, mp4_with_subtitles: Path) -> list[str]:
    errors: list[str] = []
    segments = sorted(VIDEO_WORK_DIR.glob("segment_*.mp4"))
    if len(segments) != expected_segment_count:
        errors.append(f"Rendered segment count mismatch: segments={len(segments)} runs={expected_segment_count}")
    if not mp4_path.exists():
        errors.append(f"Missing rendered MP4 {mp4_path}")
    elif mp4_path.stat().st_size <= 0:
        errors.append(f"Rendered MP4 is empty: {mp4_path}")
    if not mp4_with_subtitles.exists():
        errors.append(f"Missing embedded-subtitle MP4 {mp4_with_subtitles}")
    elif mp4_with_subtitles.stat().st_size <= 0:
        errors.append(f"Embedded-subtitle MP4 is empty: {mp4_with_subtitles}")
    return errors


def print_review_transitions(slides) -> None:
    print("Review transitions:")
    for index, (left, right) in enumerate(zip(slides, slides[1:])):
        delta = right.audio_index - left.audio_index
        if delta < 0 or delta > 3:
            print(f"  visual {index:03d}->{index + 1:03d}: audio {left.audio_index:03d}->{right.audio_index:03d}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify that narration mapping drives HTML, subtitles, and render inputs consistently.")
    parser.add_argument("--pause", type=float, default=0.85)
    parser.add_argument("--audio-preroll", type=float, default=0.65)
    parser.add_argument("--html", type=Path, default=ROOT / HTML_OUTPUT)
    parser.add_argument("--srt", type=Path, default=SRT_OUTPUT)
    parser.add_argument("--vtt", type=Path, default=VTT_OUTPUT)
    parser.add_argument("--mp4", type=Path, default=MP4_OUTPUT)
    parser.add_argument("--mp4-with-subtitles", type=Path, default=MP4_WITH_SUBTITLES)
    parser.add_argument("--max-subtitle-lines", type=int, default=2)
    parser.add_argument("--max-subtitle-line-length", type=int, default=68)
    args = parser.parse_args()

    slides = combine_slides(ROOT)
    runs = group_narration_runs(slides)
    errors = []
    errors.extend(check_render_inputs(slides))
    errors.extend(check_html(slides, args.html))
    errors.extend(
        check_subtitles(
            slides,
            args.srt,
            args.vtt,
            args.pause,
            args.audio_preroll,
            args.max_subtitle_lines,
            args.max_subtitle_line_length,
        )
    )
    errors.extend(check_rendered_files(len(runs), args.mp4, args.mp4_with_subtitles))

    print(f"Slides checked: {len(slides)}")
    print(f"Narration runs checked: {len(runs)}")
    print_review_transitions(slides)
    if errors:
        print("FAILED")
        for error in errors:
            print(f"  {error}")
        raise SystemExit(1)
    print("PASSED")


if __name__ == "__main__":
    main()
