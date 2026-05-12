# Manim Slides HTML Workflow Reference

## Local Tools

Use these known local executables in this repo:

```powershell
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
$env:IMAGEIO_FFMPEG_EXE = "C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
$python = "C:\Users\spet5947\AppData\Local\anaconda3\python.exe"
$manim = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim.exe"
$slides = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim-slides.exe"
```

Current verified versions after upgrade:

- `manim 0.20.1`
- `manim-slides 5.6.0`

## Slide Scene Pattern

Use this fallback import:

```python
from manim import *

try:
    from manim_slides import Slide
except Exception:
    Slide = Scene
```

Use a pause helper:

```python
def slide_pause(scene, *, loop=False):
    if hasattr(scene, "next_slide"):
        scene.next_slide(loop=loop)
    else:
        scene.wait(0.5)
```

For class-local helpers:

```python
class MyDeck(Slide):
    def _slide_pause(self, *, loop=False):
        if hasattr(self, "next_slide"):
            self.next_slide(loop=loop)
        else:
            self.wait(0.5)
```

## Render And Export

Run from the project directory so outputs land in that project.

For iterative Manim Slides development in this repository, prefer the
scene-specific clean-render wrapper:

```powershell
python tools/manim_slides_clean_render.py example.py BasicExample -q l
```

It renders into `.manim_media/` by default and removes only matching generated
assets for the requested scene before rendering:

- `slides/<Scene>.json`
- `slides/files/<Scene>/`
- matching scene outputs under `.manim_media/videos/<file_stem>/**/`
- matching scene images under `.manim_media/images/<file_stem>/**/`

Use `--dry-run` before unusual cleanup. `--flush-cache` is enabled by default;
add `--disable-caching` only when stale cache behavior is suspected.

Render one deck:

```powershell
cd C:\Research\manim\projects\phd_confirmation
& $slides render --CE --quality h slides_s0_why_nonlinear.py S0WhyNonlinearWavesSlides
```

Low-quality iteration with cache disabled:

```powershell
& $slides render --CE -- --quality l --disable_caching slides_s0_why_nonlinear.py S0WhyNonlinearWavesSlides
```

Export portable one-file offline HTML:

```powershell
& $slides convert --to html --one-file --offline S0WhyNonlinearWavesSlides slides_s0_why_nonlinear_1080p_offline.html
```

Render all current PhD confirmation slide decks:

```powershell
& $slides render --CE --quality h slides_s0_why_nonlinear.py S0WhyNonlinearWavesSlides
& $slides render --CE --quality h slides_s1_bound_harmonics.py S1BoundHarmonicsSlides
& $slides render --CE --quality h slides_s2_exact_interactions.py S2ExactInteractionsSlides
& $slides render --CE --quality h slides_s3_vwa_structure.py S3VWAStructureSlides
& $slides render --CE --quality h slides_s4_higher_order_vwa.py S4HigherOrderVWASlides
& $slides render --CE --quality h slides_s5_surface_kinematics.py S5SurfaceKinematicsSlides
```

## Linked Preview

Use linked preview for local iteration because it points at generated MP4s under `slides/files/...`.

```powershell
cd C:\Research\manim\projects\phd_confirmation
& $python build_linked_slides_preview.py
```

The output is:

```text
phd_confirmation_slides_linked_preview.html
```

For S0 navigation typography/spacing QA:

```powershell
& $python build_s0_nav_slides_preview.py
```

The output is:

```text
nav_s0_slide_control_preview.html
```

## New Manim Slides 5.6 Features To Consider

- HTML exports support vertical slides.
- Slides can reference static images with the `src` option.
- Reveal.js CDN selection is configurable; default Reveal.js is 6.0.1.

Use static-image slides for result figures or checkpoints that do not need animation. Use vertical slides only when a section genuinely benefits from subnavigation; keep the PhD confirmation deck mostly linear unless the user asks otherwise.

## Verification Checklist

- Confirm `manim --version` and `manim-slides --version` use the intended Anaconda executables.
- Render at least one representative low-quality deck after code changes.
- Confirm `slides/<DeckName>.json` exists and references valid MP4 paths.
- For linked previews, rebuild the HTML after slide JSON/MP4 changes.
- For portable one-file decks, rerun `convert --to html --one-file --offline` after any slide rerender.
- Check `git status --short`; generated decks should normally remain untracked/ignored.
