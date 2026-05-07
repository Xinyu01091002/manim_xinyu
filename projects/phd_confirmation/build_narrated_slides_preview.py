from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path


DECKS = [
    "S0WhyNonlinearWavesSlides",
    "S1BoundHarmonicsSlides",
    "S2ExactInteractionsSlides",
    "S3VWAStructureSlides",
    "S4HigherOrderVWASlides",
    "S5SurfaceKinematicsSlides",
]

COVER_VIDEO = "media/videos/scenario_cover_eye_attractor/1080p60/VWAExtensionsCover.mp4"
SCRIPT_PATH = "narration/draft_page_scripts.md"
OUTPUT = "phd_confirmation_slides_narrated_preview.html"
PAGE_HEADING = re.compile(r"^(?:##|###) Page (?P<number>\d+) - (?P<title>.+)$")


@dataclass(frozen=True)
class SlideSource:
    title: str
    video: str
    loop: bool
    narration: str


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def load_slide_sources(root: Path) -> list[tuple[str, str, bool]]:
    sources: list[tuple[str, str, bool]] = [("Cover", COVER_VIDEO, True)]
    for deck in DECKS:
        data = json.loads((root / "slides" / f"{deck}.json").read_text(encoding="utf-8-sig"))
        for index, slide in enumerate(data["slides"], start=1):
            sources.append((f"{deck} / {index}", normalize_path(slide["file"]), bool(slide.get("loop", False))))
    return sources


def parse_narration(path: Path) -> list[str]:
    pages: list[str] = []
    current_number: int | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_number, current_lines
        if current_number is None:
            return
        pages.append("\n".join(current_lines).strip())
        current_number = None
        current_lines = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = PAGE_HEADING.match(raw_line.strip())
        if match:
            flush()
            current_number = int(match.group("number"))
            continue
        if current_number is not None:
            if raw_line.startswith("#"):
                continue
            current_lines.append(raw_line)
    flush()
    return pages


def combine_slides(root: Path) -> list[SlideSource]:
    videos = load_slide_sources(root)
    narration = parse_narration(root / SCRIPT_PATH)
    if len(videos) != len(narration):
        raise ValueError(f"Slide/narration count mismatch: videos={len(videos)} narration={len(narration)}")
    return [
        SlideSource(title=title, video=video, loop=loop, narration=text)
        for (title, video, loop), text in zip(videos, narration)
    ]


def video_section(index: int, slide: SlideSource) -> str:
    loop_attr = " loop" if slide.loop else ""
    audio_src = f"narration/audio/{index:03d}.wav"
    return f"""<section class="slide" data-index="{index}" data-title="{html.escape(slide.title)}" data-script="{html.escape(slide.narration)}">
  <video preload="metadata" playsinline muted{loop_attr}>
    <source src="{html.escape(slide.video)}" type="video/mp4" />
  </video>
  <audio preload="metadata">
    <source src="{html.escape(audio_src)}" type="audio/wav" />
  </audio>
</section>"""


def build_html(slides: list[SlideSource]) -> str:
    sections = "\n".join(video_section(index, slide) for index, slide in enumerate(slides))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>VWA Slides Narrated Preview</title>
  <style>
    html, body {{ margin: 0; width: 100%; height: 100%; background: #030712; overflow: hidden; }}
    body {{ font-family: system-ui, sans-serif; color: #f8fafc; }}
    .slide {{ display: none; width: 100vw; height: 100vh; place-items: center; background: #030712; }}
    .slide.active {{ display: grid; }}
    video {{ width: 100vw; height: 100vh; object-fit: contain; background: #030712; }}
    .hud {{ position: fixed; left: 16px; right: 16px; top: 12px; display: flex; justify-content: space-between; gap: 16px; color: rgba(248,250,252,.66); font-size: 14px; pointer-events: none; }}
    .help {{ position: fixed; right: 16px; bottom: 12px; color: rgba(248,250,252,.58); font-size: 13px; }}
    .controls {{ position: fixed; left: 16px; bottom: 12px; display: flex; gap: 8px; align-items: center; }}
    button {{ border: 1px solid rgba(248,250,252,.24); border-radius: 6px; background: rgba(15,23,42,.86); color: #f8fafc; padding: 8px 11px; cursor: pointer; }}
    button:hover {{ background: rgba(30,41,59,.94); }}
    .script {{ position: fixed; left: 16px; right: 16px; bottom: var(--script-bottom, 52px); max-height: 18vh; overflow: auto; padding: 12px 14px; border: 0; border-radius: 0; background: transparent; color: rgba(248,250,252,.96); font-size: 15px; line-height: 1.45; text-shadow: 0 2px 5px rgba(0,0,0,.95), 0 0 12px rgba(0,0,0,.8); display: none; }}
    .script.visible {{ display: block; }}
  </style>
</head>
<body>
{sections}
  <div class="hud"><span id="title"></span><span id="count"></span></div>
  <div id="script" class="script"></div>
  <div class="controls">
    <button id="play" type="button">Play</button>
    <button id="restart" type="button">Restart</button>
    <button id="toggleScript" type="button">Script</button>
  </div>
  <div class="help">Left/Right navigate | Space play/pause | R restart | S script | F fullscreen</div>
  <script>
    const slides = [...document.querySelectorAll('.slide')];
    const title = document.getElementById('title');
    const count = document.getElementById('count');
    const script = document.getElementById('script');
    const playButton = document.getElementById('play');
    const restartButton = document.getElementById('restart');
    const toggleScriptButton = document.getElementById('toggleScript');
    let current = 0;
    let playing = false;

    function media() {{
      const section = slides[current];
      return {{
        video: section.querySelector('video'),
        audio: section.querySelector('audio'),
      }};
    }}

    function updateHud() {{
      title.textContent = slides[current].dataset.title;
      count.textContent = `${{current + 1}} / ${{slides.length}}`;
      script.textContent = slides[current].dataset.script;
      playButton.textContent = playing ? 'Pause' : 'Play';
      updateScriptPosition();
    }}

    function videoContentRect(video) {{
      const bounds = video.getBoundingClientRect();
      const aspect = video.videoWidth && video.videoHeight ? video.videoWidth / video.videoHeight : 16 / 9;
      let width = bounds.width;
      let height = width / aspect;
      if (height > bounds.height) {{
        height = bounds.height;
        width = height * aspect;
      }}
      const left = bounds.left + (bounds.width - width) / 2;
      const top = bounds.top + (bounds.height - height) / 2;
      return {{ left, top, width, height, right: left + width, bottom: top + height }};
    }}

    function updateScriptPosition() {{
      const {{ video }} = media();
      const rect = videoContentRect(video);
      const offsetFromVideoBottom = 52;
      const bottom = Math.max(12, window.innerHeight - rect.bottom + offsetFromVideoBottom);
      document.documentElement.style.setProperty('--script-bottom', `${{bottom}}px`);
    }}

    function stopSection(section) {{
      const video = section.querySelector('video');
      const audio = section.querySelector('audio');
      video.pause();
      audio.pause();
      video.currentTime = 0;
      audio.currentTime = 0;
    }}

    async function playCurrent() {{
      const {{ video, audio }} = media();
      playing = true;
      updateHud();
      await video.play().catch(() => {{}});
      await audio.play().catch(() => {{}});
    }}

    function pauseCurrent() {{
      const {{ video, audio }} = media();
      video.pause();
      audio.pause();
      playing = false;
      updateHud();
    }}

    function show(index) {{
      current = Math.max(0, Math.min(slides.length - 1, index));
      slides.forEach((section, i) => {{
        if (i !== current) stopSection(section);
        section.classList.toggle('active', i === current);
      }});
      const {{ video, audio }} = media();
      video.currentTime = 0;
      audio.currentTime = 0;
      updateHud();
      if (playing) playCurrent();
    }}

    function togglePlay() {{
      if (playing) pauseCurrent();
      else playCurrent();
    }}

    function restart() {{
      const {{ video, audio }} = media();
      video.currentTime = 0;
      audio.currentTime = 0;
      playCurrent();
    }}

    document.addEventListener('keydown', event => {{
      if (event.key === 'ArrowRight' || event.key === 'PageDown') show(current + 1);
      if (event.key === 'ArrowLeft' || event.key === 'PageUp') show(current - 1);
      if (event.key === ' ') {{ event.preventDefault(); togglePlay(); }}
      if (event.key.toLowerCase() === 'r') restart();
      if (event.key.toLowerCase() === 's') script.classList.toggle('visible');
      if (event.key.toLowerCase() === 'f') {{ document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }}
    }});

    playButton.addEventListener('click', togglePlay);
    restartButton.addEventListener('click', restart);
    toggleScriptButton.addEventListener('click', () => script.classList.toggle('visible'));
    window.addEventListener('resize', updateScriptPosition);
    document.addEventListener('fullscreenchange', updateScriptPosition);
    slides.forEach(section => {{
      const audio = section.querySelector('audio');
      const video = section.querySelector('video');
      video.addEventListener('loadedmetadata', updateScriptPosition);
      audio.addEventListener('ended', () => {{
        if (section === slides[current]) {{
          playing = false;
          updateHud();
        }}
      }});
    }});

    show(0);
  </script>
</body>
</html>
"""


def main() -> None:
    root = Path(__file__).resolve().parent
    slides = combine_slides(root)
    missing_audio = [
        f"narration/audio/{index:03d}.wav"
        for index in range(len(slides))
        if not (root / "narration" / "audio" / f"{index:03d}.wav").exists()
    ]
    (root / OUTPUT).write_text(build_html(slides), encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(slides)} narrated slides.")
    if missing_audio:
        print(f"Warning: missing {len(missing_audio)} audio files. Run generate_narration_audio.py.")


if __name__ == "__main__":
    main()
