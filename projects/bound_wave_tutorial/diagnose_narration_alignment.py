from __future__ import annotations

import argparse
import csv
import html
import json
import re
import shutil
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SLIDE_JSON = ROOT / "slides" / "BoundWaveIntroSlides.json"
SCRIPT_PATH = ROOT / "narration" / "draft_page_scripts.md"
AUDIO_DIR = ROOT / "narration" / "audio"
ALIGNMENT_MAP = ROOT / "narration" / "alignment_map.json"
OUTPUT_DIR = ROOT / "narration" / "alignment_diagnostics"
AUDIT_CSV = OUTPUT_DIR / "alignment_audit.csv"
PREVIEW_HTML = OUTPUT_DIR / "alignment_preview.html"
DEFAULT_FFMPEG = Path(
    r"C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
)

PAGE_HEADING = re.compile(r"^(?:##|###) Page (?P<number>\d+) - (?P<title>.+)$")
VIDEO_DURATION_RE = re.compile(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)")


@dataclass(frozen=True)
class NarrationPage:
    number: int
    title: str
    text: str


@dataclass(frozen=True)
class SlideRow:
    index: int
    video_file: str
    loop: bool
    video_seconds: float | None
    mapped_audio_index: int
    audio_file: str
    audio_seconds: float | None
    narration_title: str
    narration_text: str


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def parse_narration(path: Path) -> list[NarrationPage]:
    pages: list[NarrationPage] = []
    current_number: int | None = None
    current_title = ""
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_number, current_title, current_lines
        if current_number is None:
            return
        text = "\n".join(current_lines).strip()
        if not text:
            raise ValueError(f"Missing narration text for page {current_number}: {current_title}")
        pages.append(NarrationPage(current_number, current_title, text))
        current_number = None
        current_title = ""
        current_lines = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = PAGE_HEADING.match(raw_line.strip())
        if match:
            flush()
            current_number = int(match.group("number"))
            current_title = match.group("title")
            continue
        if current_number is not None:
            if raw_line.startswith("#"):
                continue
            current_lines.append(raw_line)
    flush()

    expected = list(range(len(pages)))
    actual = [page.number for page in pages]
    if actual != expected:
        raise ValueError(f"Narration pages must be contiguous from zero; got first={actual[:3]} last={actual[-3:]}")
    return pages


def load_slide_entries(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return list(data["slides"])


def load_alignment_map(slide_count: int, narration_count: int) -> list[int]:
    if not ALIGNMENT_MAP.exists():
        if slide_count != narration_count:
            raise ValueError(f"Slide/narration count mismatch: slides={slide_count} narration={narration_count}")
        return list(range(slide_count))
    data = json.loads(ALIGNMENT_MAP.read_text(encoding="utf-8"))
    mapping = data.get("audio_index_by_visual_index")
    if not isinstance(mapping, list):
        raise ValueError("alignment_map.json must contain audio_index_by_visual_index")
    if len(mapping) != slide_count:
        raise ValueError(f"Alignment map length mismatch: map={len(mapping)} slides={slide_count}")
    invalid = [value for value in mapping if not isinstance(value, int) or value < 0 or value >= narration_count]
    if invalid:
        raise ValueError(f"Alignment map contains invalid narration indices: {invalid[:5]}")
    return mapping


def find_ffmpeg() -> Path | None:
    path = shutil.which("ffmpeg")
    if path:
        return Path(path)
    if DEFAULT_FFMPEG.exists():
        return DEFAULT_FFMPEG
    return None


def video_duration(ffmpeg: Path | None, path: Path) -> float | None:
    if ffmpeg is None or not path.exists():
        return None
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
        return None
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def audio_duration(path: Path) -> float | None:
    if not path.exists():
        return None
    with wave.open(str(path), "rb") as audio:
        return audio.getnframes() / float(audio.getframerate())


def first_words(text: str, limit: int = 120) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def build_rows() -> list[SlideRow]:
    slides = load_slide_entries(SLIDE_JSON)
    pages = parse_narration(SCRIPT_PATH)
    mapping = load_alignment_map(len(slides), len(pages))

    ffmpeg = find_ffmpeg()
    rows: list[SlideRow] = []
    for index, slide in enumerate(slides):
        mapped_audio_index = mapping[index]
        page = pages[mapped_audio_index]
        video_file = normalize_path(slide["file"])
        audio_file = f"narration/audio/{mapped_audio_index:03d}.wav"
        rows.append(
            SlideRow(
                index=index,
                video_file=video_file,
                loop=bool(slide.get("loop", False)),
                video_seconds=video_duration(ffmpeg, ROOT / video_file),
                mapped_audio_index=mapped_audio_index,
                audio_file=audio_file,
                audio_seconds=audio_duration(AUDIO_DIR / f"{mapped_audio_index:03d}.wav"),
                narration_title=page.title,
                narration_text=page.text,
            )
        )
    return rows


def write_audit_csv(rows: list[SlideRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "index",
                "video_file",
                "loop",
                "video_duration_seconds",
                "mapped_audio_index",
                "audio_file",
                "audio_duration_seconds",
                "narration_title",
                "narration_first_words",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "index": row.index,
                    "video_file": row.video_file,
                    "loop": row.loop,
                    "video_duration_seconds": "" if row.video_seconds is None else f"{row.video_seconds:.3f}",
                    "mapped_audio_index": row.mapped_audio_index,
                    "audio_file": row.audio_file,
                    "audio_duration_seconds": "" if row.audio_seconds is None else f"{row.audio_seconds:.3f}",
                    "narration_title": row.narration_title,
                    "narration_first_words": first_words(row.narration_text),
                }
            )


def parse_range(text: str) -> tuple[int, int]:
    if "-" not in text:
        value = int(text)
        return value, value
    start, end = text.split("-", 1)
    start_i = int(start)
    end_i = int(end)
    if end_i < start_i:
        raise argparse.ArgumentTypeError(f"Invalid descending range: {text}")
    return start_i, end_i


def format_seconds(value: float | None) -> str:
    if value is None:
        return "unknown"
    return f"{value:.2f}s"


def rel_from_output(path: str) -> str:
    return normalize_path(str(Path("../..") / Path(path)))


def audio_rel_from_output(index: int) -> str:
    return normalize_path(str(Path("..") / "audio" / f"{index:03d}.wav"))


def preview_payload(rows: list[SlideRow], ranges: list[tuple[int, int]], shifts: list[int]) -> list[dict]:
    payload: list[dict] = []
    for start, end in ranges:
        if start < 0 or end >= len(rows):
            raise ValueError(f"Range {start}-{end} is outside available rows 0-{len(rows) - 1}")
        for visual_index in range(start, end + 1):
            visual = rows[visual_index]
            variants = []
            for shift in shifts:
                audio_index = visual.mapped_audio_index + shift
                if audio_index < 0 or audio_index >= len(rows):
                    continue
                audio = rows[audio_index]
                variants.append(
                    {
                        "shift": shift,
                        "audio_index": audio_index,
                        "audio_src": audio_rel_from_output(audio_index),
                        "audio_title": audio.narration_title,
                        "audio_text": audio.narration_text,
                        "audio_seconds": format_seconds(audio.audio_seconds),
                    }
                )
            payload.append(
                {
                    "range": f"{start}-{end}",
                    "visual_index": visual_index,
                    "video_src": rel_from_output(visual.video_file),
                    "loop": visual.loop,
                    "video_file": visual.video_file,
                    "video_seconds": format_seconds(visual.video_seconds),
                    "expected_title": visual.narration_title,
                    "expected_text": visual.narration_text,
                    "variants": variants,
                }
            )
    return payload


def write_preview_html(
    rows: list[SlideRow],
    ranges: list[tuple[int, int]],
    shifts: list[int],
    preroll: float,
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = preview_payload(rows, ranges, shifts)
    data = json.dumps(payload, ensure_ascii=False)
    shift_buttons = "".join(
        f'<button class="shift" type="button" data-shift="{shift}">{shift:+d}</button>' for shift in shifts
    )
    range_buttons = "".join(
        f'<button class="range" type="button" data-range="{start}-{end}">{start}-{end}</button>' for start, end in ranges
    )
    path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Bound Wave Narration Alignment Diagnostics</title>
  <style>
    html, body {{ margin: 0; min-height: 100%; background: #030712; color: #f8fafc; font-family: system-ui, sans-serif; }}
    body {{ display: grid; grid-template-columns: 320px minmax(0, 1fr); }}
    aside {{ height: 100vh; overflow: auto; border-right: 1px solid rgba(148,163,184,.25); background: #0f172a; padding: 14px; box-sizing: border-box; }}
    main {{ min-width: 0; padding: 14px; }}
    h1 {{ font-size: 18px; margin: 0 0 12px; }}
    h2 {{ font-size: 13px; margin: 18px 0 8px; color: #cbd5e1; text-transform: uppercase; letter-spacing: .06em; }}
    button {{ border: 1px solid rgba(148,163,184,.42); background: #111827; color: #f8fafc; border-radius: 6px; padding: 7px 9px; cursor: pointer; }}
    button.active {{ border-color: #38bdf8; background: #0c4a6e; }}
    .row-list {{ display: grid; gap: 6px; }}
    .row-button {{ text-align: left; line-height: 1.25; }}
    .button-row {{ display: flex; gap: 6px; flex-wrap: wrap; }}
    .viewer {{ position: relative; background: #020617; border: 1px solid rgba(148,163,184,.22); }}
    video {{ display: block; width: 100%; max-height: calc(100vh - 190px); background: #020617; }}
    .overlay {{ position: absolute; left: 12px; right: 12px; top: 12px; display: flex; justify-content: space-between; gap: 12px; pointer-events: none; }}
    .badge {{ background: rgba(2,6,23,.82); border: 1px solid rgba(148,163,184,.28); padding: 7px 9px; border-radius: 6px; font-size: 13px; }}
    .flash {{ position: absolute; inset: 0; border: 8px solid transparent; pointer-events: none; }}
    .flash.on {{ border-color: #facc15; }}
    .meta {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 12px; }}
    .panel {{ background: #0f172a; border: 1px solid rgba(148,163,184,.22); padding: 12px; border-radius: 6px; }}
    .panel h3 {{ margin: 0 0 8px; font-size: 15px; color: #e2e8f0; }}
    .panel p {{ margin: 8px 0 0; line-height: 1.45; }}
    .muted {{ color: #94a3b8; font-size: 13px; }}
    .controls {{ display: flex; gap: 8px; align-items: center; margin: 12px 0; flex-wrap: wrap; }}
    .warning {{ color: #facc15; }}
  </style>
</head>
<body>
  <aside>
    <h1>Narration Alignment</h1>
    <div class="muted">Preroll before audio: {preroll:.2f}s. Select a visual slide, then compare audio shifts.</div>
    <h2>Ranges</h2>
    <div class="button-row" id="ranges">{range_buttons}</div>
    <h2>Audio Shift</h2>
    <div class="button-row" id="shifts">{shift_buttons}</div>
    <h2>Visual Slides</h2>
    <div class="row-list" id="rows"></div>
  </aside>
  <main>
    <div class="viewer">
      <video id="video" muted playsinline></video>
      <audio id="audio"></audio>
      <div class="overlay">
        <div class="badge" id="leftBadge"></div>
        <div class="badge" id="rightBadge"></div>
      </div>
      <div class="flash" id="flash"></div>
    </div>
    <div class="controls">
      <button id="play" type="button">Play With Audio</button>
      <button id="pause" type="button">Pause</button>
      <button id="restart" type="button">Restart</button>
    </div>
    <div class="meta">
      <section class="panel">
        <h3>Visual slide expectation</h3>
        <div class="muted" id="videoMeta"></div>
        <p id="expectedText"></p>
      </section>
      <section class="panel">
        <h3>Audio being tested</h3>
        <div class="muted" id="audioMeta"></div>
        <p id="audioText"></p>
      </section>
    </div>
  <script>
    const data = {data};
    const prerollMs = {int(round(preroll * 1000))};
    let currentRange = data[0].range;
    let currentIndex = data[0].visual_index;
    let currentShift = 0;
    let audioTimer = null;

    const video = document.getElementById('video');
    const audio = document.getElementById('audio');
    const rows = document.getElementById('rows');
    const leftBadge = document.getElementById('leftBadge');
    const rightBadge = document.getElementById('rightBadge');
    const flash = document.getElementById('flash');
    const videoMeta = document.getElementById('videoMeta');
    const audioMeta = document.getElementById('audioMeta');
    const expectedText = document.getElementById('expectedText');
    const audioText = document.getElementById('audioText');

    function activeEntry() {{
      return data.find(item => item.visual_index === currentIndex) || data[0];
    }}

    function activeVariant(entry) {{
      return entry.variants.find(item => item.shift === currentShift) || entry.variants[0];
    }}

    function setActiveButtons() {{
      document.querySelectorAll('.range').forEach(button => button.classList.toggle('active', button.dataset.range === currentRange));
      document.querySelectorAll('.shift').forEach(button => button.classList.toggle('active', Number(button.dataset.shift) === currentShift));
      document.querySelectorAll('.row-button').forEach(button => button.classList.toggle('active', Number(button.dataset.index) === currentIndex));
    }}

    function renderRows() {{
      rows.innerHTML = '';
      data.filter(item => item.range === currentRange).forEach(item => {{
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'row-button';
        button.dataset.index = item.visual_index;
        button.textContent = `${{item.visual_index.toString().padStart(3, '0')}} - ${{item.expected_title}}`;
        button.addEventListener('click', () => {{
          currentIndex = item.visual_index;
          loadCurrent();
        }});
        rows.appendChild(button);
      }});
    }}

    function loadCurrent() {{
      const entry = activeEntry();
      const variant = activeVariant(entry);
      if (audioTimer) clearTimeout(audioTimer);
      video.pause();
      audio.pause();
      video.src = entry.video_src;
      video.loop = entry.loop;
      audio.src = variant.audio_src;
      video.currentTime = 0;
      audio.currentTime = 0;
      leftBadge.textContent = `visual ${{entry.visual_index}} | range ${{entry.range}} | video ${{entry.video_seconds}}`;
      rightBadge.textContent = `audio ${{variant.audio_index}} | shift ${{variant.shift >= 0 ? '+' : ''}}${{variant.shift}} | audio ${{variant.audio_seconds}}`;
      videoMeta.textContent = `${{entry.video_file}}`;
      audioMeta.textContent = `${{variant.audio_title}}`;
      expectedText.textContent = entry.expected_text;
      audioText.textContent = variant.audio_text;
      setActiveButtons();
    }}

    async function playWithAudio() {{
      if (audioTimer) clearTimeout(audioTimer);
      flash.classList.remove('on');
      audio.pause();
      audio.currentTime = 0;
      video.currentTime = 0;
      await video.play().catch(() => {{}});
      audioTimer = setTimeout(async () => {{
        flash.classList.add('on');
        setTimeout(() => flash.classList.remove('on'), 220);
        await audio.play().catch(() => {{}});
      }}, prerollMs);
    }}

    function pauseAll() {{
      if (audioTimer) clearTimeout(audioTimer);
      video.pause();
      audio.pause();
    }}

    document.querySelectorAll('.range').forEach(button => {{
      button.addEventListener('click', () => {{
        currentRange = button.dataset.range;
        currentIndex = data.find(item => item.range === currentRange).visual_index;
        renderRows();
        loadCurrent();
      }});
    }});

    document.querySelectorAll('.shift').forEach(button => {{
      button.addEventListener('click', () => {{
        currentShift = Number(button.dataset.shift);
        loadCurrent();
      }});
    }});

    document.getElementById('play').addEventListener('click', playWithAudio);
    document.getElementById('pause').addEventListener('click', pauseAll);
    document.getElementById('restart').addEventListener('click', playWithAudio);

    renderRows();
    loadCurrent();
  </script>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build audio/video alignment diagnostics for the bound-wave narrated deck.")
    parser.add_argument("--ranges", nargs="+", type=parse_range, default=[(25, 30), (45, 50), (75, 80), (105, 110)])
    parser.add_argument("--shifts", nargs="+", type=int, default=[-1, 0, 1])
    parser.add_argument("--preroll", type=float, default=0.65)
    parser.add_argument("--csv", type=Path, default=AUDIT_CSV)
    parser.add_argument("--html", type=Path, default=PREVIEW_HTML)
    args = parser.parse_args()

    rows = build_rows()
    write_audit_csv(rows, args.csv)
    write_preview_html(rows, args.ranges, args.shifts, args.preroll, args.html)

    print(f"Rows: {len(rows)}")
    print(f"Wrote CSV: {args.csv}")
    print(f"Wrote HTML: {args.html}")


if __name__ == "__main__":
    main()
