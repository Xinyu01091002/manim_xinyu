from __future__ import annotations

import html
import json
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
OUTPUT = "phd_confirmation_slides_linked_preview.html"


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def load_slide_sources(root: Path) -> list[tuple[str, str, bool]]:
    sources: list[tuple[str, str, bool]] = [("Cover", COVER_VIDEO, True)]
    for deck in DECKS:
        data = json.loads((root / "slides" / f"{deck}.json").read_text(encoding="utf-8-sig"))
        for index, slide in enumerate(data["slides"], start=1):
            sources.append((f"{deck} / {index}", normalize_path(slide["file"]), bool(slide.get("loop", False))))
    return sources


def video_section(index: int, title: str, src: str, loop: bool) -> str:
    loop_attr = " loop" if loop else ""
    return f"""<section class="slide" data-index="{index}" data-title="{html.escape(title)}">
  <video preload="metadata" playsinline muted{loop_attr}>
    <source src="{html.escape(src)}" type="video/mp4" />
  </video>
</section>"""


def build_html(slides: list[tuple[str, str, bool]]) -> str:
    sections = "\n".join(
        video_section(index, title, src, loop)
        for index, (title, src, loop) in enumerate(slides)
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>PhD Confirmation Slides Linked Preview</title>
  <style>
    html, body {{ margin: 0; width: 100%; height: 100%; background: #030712; overflow: hidden; }}
    body {{ font-family: system-ui, sans-serif; color: #f8fafc; }}
    .slide {{ display: none; width: 100vw; height: 100vh; place-items: center; background: #030712; }}
    .slide.active {{ display: grid; }}
    video {{ width: 100vw; height: 100vh; object-fit: contain; background: #030712; }}
    .hud {{ position: fixed; left: 16px; right: 16px; top: 12px; display: flex; justify-content: space-between; gap: 16px; color: rgba(248,250,252,.62); font-size: 14px; pointer-events: none; }}
    .help {{ position: fixed; right: 16px; top: 12px; color: rgba(248,250,252,.48); font-size: 13px; }}
  </style>
</head>
<body>
{sections}
  <div class="help">Left/Right navigate | Space play/pause | R restart | F fullscreen</div>
  <div class="hud"><span id="title"></span><span id="count"></span></div>
  <script>
    const slides = [...document.querySelectorAll('.slide')];
    const title = document.getElementById('title');
    const count = document.getElementById('count');
    let current = 0;

    function show(index) {{
      current = Math.max(0, Math.min(slides.length - 1, index));
      slides.forEach((section, i) => {{
        const video = section.querySelector('video');
        section.classList.toggle('active', i === current);
        if (i === current) {{
          video.currentTime = 0;
          video.play().catch(() => {{}});
        }} else {{
          video.pause();
        }}
      }});
      title.textContent = slides[current].dataset.title;
      count.textContent = `${{current + 1}} / ${{slides.length}}`;
    }}

    document.addEventListener('keydown', event => {{
      const video = slides[current].querySelector('video');
      if (event.key === 'ArrowRight' || event.key === 'PageDown') show(current + 1);
      if (event.key === 'ArrowLeft' || event.key === 'PageUp') show(current - 1);
      if (event.key === ' ') {{ event.preventDefault(); video.paused ? video.play() : video.pause(); }}
      if (event.key.toLowerCase() === 'r') {{ video.currentTime = 0; video.play(); }}
      if (event.key.toLowerCase() === 'f') {{ document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }}
    }});

    show(0);
  </script>
</body>
</html>
"""


def main() -> None:
    root = Path(__file__).resolve().parent
    slides = load_slide_sources(root)
    (root / OUTPUT).write_text(build_html(slides), encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(slides)} linked slides.")


if __name__ == "__main__":
    main()
