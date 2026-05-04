from __future__ import annotations

import html
import json
from pathlib import Path


OUTPUT = "nav_s0_slide_control_preview.html"
DECK = "S0WhyNonlinearWavesSlides"


def normalize(path: str) -> str:
    return path.replace("\\", "/")


def video_section(index: int, src: str) -> str:
    return f"""<section class="slide" data-index="{index}">
  <video preload="metadata" playsinline muted>
    <source src="{html.escape(src)}" type="video/mp4" />
  </video>
</section>"""


def main() -> None:
    root = Path(__file__).resolve().parent
    data = json.loads((root / "slides" / f"{DECK}.json").read_text(encoding="utf-8"))
    sections = "\n".join(
        video_section(index, normalize(slide["file"]))
        for index, slide in enumerate(data["slides"])
    )
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>S0 Slide-Controlled Navigation Preview</title>
  <style>
    html, body {{ margin: 0; width: 100%; height: 100%; background: #030712; overflow: hidden; }}
    body {{ font-family: "Segoe UI", system-ui, sans-serif; color: #f8fafc; }}
    .slide {{ display: none; width: 100vw; height: 100vh; place-items: center; background: #030712; }}
    .slide.active {{ display: grid; }}
    video {{ width: 100vw; height: 100vh; object-fit: contain; background: #030712; }}
    .help {{ position: fixed; right: 16px; top: 12px; color: rgba(248,250,252,.48); font-size: 13px; }}
    .hud {{ position: fixed; left: 16px; top: 12px; color: rgba(248,250,252,.62); font-size: 14px; pointer-events: none; }}
  </style>
</head>
<body>
{sections}
  <div class="help">Left/Right navigate | Space play/pause | R restart | F fullscreen</div>
  <div class="hud"><span id="count"></span></div>
  <script>
    const slides = [...document.querySelectorAll('.slide')];
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
      count.textContent = `S0 ${{current + 1}} / ${{slides.length}}`;
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
    (root / OUTPUT).write_text(html_doc, encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(data['slides'])} slide-controlled videos.")


if __name__ == "__main__":
    main()
