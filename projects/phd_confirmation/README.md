# PhD Confirmation Manim Workflow

This folder contains the current PhD confirmation presentation scenarios.

## Presentation Style

Keep text animation quiet and functional. The presentation should feel like a clear
scientific explanation, not a motion-graphics demo.

- Use simple `FadeIn`, `Write`, or direct `add` for titles, labels, equations, and
  takeaways.
- Avoid fancy text entrance effects unless they clarify meaning.
- Put animation effort into the wave physics and VWA logic: moving wave groups, probes,
  phase matching, kernel comparison, product/convolution structure, and transitions that
  explain the idea.
- Leave enough `wait()` time after major ideas for spoken explanation.
- Current S0-S5 convention: ordinary text and TeX should enter quietly, usually via a
  short `FadeIn`. Do not use letter-by-letter or decorative text motion for labels,
  titles, or takeaways. Keep the visual emphasis on wave groups, spectra, kernels,
  product structure, arrows, and probe motion.

## Persistent Navigation Bar

Use `presentation_nav.py` for the bottom navigation bar. The current preferred design is
`bottom_progress_nav`, a two-tier progress bar:

- Row 1: whole presentation progress across `S0`-`S5`.
- Row 2: subscenario progress inside the active scenario.

Current visual style:

- near-black background: `#030712`
- bright continuous scenario palette:
  `#FFE45E`, `#FFB84D`, `#FF7A59`, `#FF5DA2`, `#C77DFF`, `#8EA7FF`
- subscenario bars use a gradient derived from the active scenario color
- whole-presentation and subscenario segments are rounded bars, not hard-edged
  rectangles
- the whole-presentation row shows compact `S0`-`S5` labels, with the active
  scenario widened to show its short scenario name
- the subscenario row keeps all colored progress segments but shows text only
  for the currently active subscenario, avoiding squeezed inactive labels
- active labels are stroked for contrast; use ASCII separators such as `:`
  rather than typographic middots to avoid encoding artifacts in small labels

Performance rule:

Do not rebuild the whole navigation bar with `always_redraw`. That made S0 low-quality
rendering several times slower because Manim rebuilt `Text` and all segment rectangles
on every frame. Instead:

- create labels and base rectangles once
- animate or update only the fill rectangles' widths
- use small opacity updaters for active/inactive labels

Scenario setup pattern:

```python
from presentation_nav import bottom_progress_nav

SCENARIO0_SECONDS = 52.20
SCENARIO0_SUBSCENARIOS = [
    "opening",
    "linear baseline",
    "shape + spectrum",
    "fixed probe",
    "arrival drift",
    "bound harmonics",
]

nav_progress = ValueTracker(0)
nav_progress.add_updater(
    lambda tracker, dt: tracker.increment_value(
        len(SCENARIO0_SUBSCENARIOS) * dt / SCENARIO0_SECONDS
    )
)
nav = bottom_progress_nav(
    0,
    6,
    "nonlinear waves",
    SCENARIO0_SUBSCENARIOS,
    nav_progress,
    accent=C_NL,
)
self.add(nav_progress, nav)
```

Layout rule:

The progress bar is taller than the old bottom bar (`PROGRESS_NAV_HEIGHT = 0.72`), so
bottom axes, equations, and takeaway text must be moved upward. Check low-quality
snapshots or extracted frames before full rendering.

Timing rule:

After major animation edits, render a low-quality pass and measure the real video
duration with ffmpeg. Update `SCENARIO*_SECONDS` before rendering the final high-quality
version so the progress bar reaches the correct point at the end of each scenario.

Current calibrated high-quality durations:

| Scenario | Scene | Duration |
| --- | --- | ---: |
| S0 | `WhyNonlinearWaves` | `00:00:52.15` |
| S1 | `BoundHarmonicsIntro` | `00:00:42.53` |
| S2 | `WhyExactInteractionsAreExpensive` | `00:00:39.58` |
| S3 | `TheVWAIdea` | `00:01:27.28` |
| S4 | `HigherOrderVWA` | `00:00:53.53` |
| S5 | `SurfaceKinematicsVWA` | `00:00:30.00` |

Combined final duration: `00:05:05.08`.

## Render Commands

Run from this directory so Manim writes media under this project:

```powershell
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
$env:IMAGEIO_FFMPEG_EXE = "C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim -ql scenario0_why_nonlinear.py WhyNonlinearWaves
```

High-quality scenario renders:

```powershell
$manim = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim"

& $manim -qh scenario0_why_nonlinear.py WhyNonlinearWaves
& $manim -qh scenario1_bound_harmonics.py BoundHarmonicsIntro
& $manim -qh scenario2_exact_interactions.py WhyExactInteractionsAreExpensive
& $manim -qh scenario3_vwa_structure.py TheVWAIdea
& $manim -qh scenario4_higher_order_vwa.py HigherOrderVWA
& $manim -qh scenario5_surface_kinematics.py SurfaceKinematicsVWA
```

Merge high-quality scenario videos:

```powershell
& $env:IMAGEIO_FFMPEG_EXE -y -f concat -safe 0 -i concat_high_quality.txt -c copy media/videos/phd_confirmation_full_1080p60.mp4
```

## Manim Slides Workflow

The slide workflow is separate from the calibrated video workflow. The current
rule is: **do not rewrite the talk for slides**. A slide scene should be a
faithful presenter-controlled adaptation of the corresponding video scene,
preserving the original narrative logic, formulas, visual mechanisms, and bridge
phrases.

Current slide files:

- `slides_demo.py`: small mechanism proof of concept. It tests Manim Slides
  rendering, `next_slide()` pauses, and browser export. It is not a content
  template for the real talk.
- `slides_s0_why_nonlinear.py`: faithful S0 conversion derived directly from
  `scenario0_why_nonlinear.py`. It keeps the original wave panels, nonlinear
  overlay, crest lift, spectrum fingerprint, fixed-gauge time trace, arrival
  drift, takeaway, and bridge to bound harmonics. The only intended behavioral
  change is that major `wait()` points become presenter-controlled slide pauses.
- `slides_s1_bound_harmonics.py`: faithful S1 conversion derived directly from
  `scenario1_bound_harmonics.py`. It keeps the original linear component setup,
  set-down / second-harmonic / third-harmonic reveals, nonlinear-total shape
  change, locked-group animation, and handoff to exact interaction cost.
- `slides_s2_exact_interactions.py`: faithful S2 conversion for the exact
  interaction cost argument, including the full animated cost build rather than
  a static simplification.
- `slides_s3_vwa_structure.py`: faithful S3 conversion for the VWA structure and
  bridge logic.
- `slides_s4_higher_order_vwa.py`: faithful S4 conversion for the higher-order
  VWA extension.
- `slides_s5_surface_kinematics.py`: slide entry point for the S5 surface
  kinematics extension. For the full linked preview, S5 can also be reused as a
  looping rendered video when that is faster for review.

Recommended conversion pattern for S1-S5:

1. Copy the source video scene to a `slides_s*_*.py` file.
2. Change the scene base from `Scene` to a `Slide` fallback wrapper.
3. Replace major explanatory `self.wait(...)` calls with a small `slide_pause`
   helper that calls `next_slide(loop=False)`.
4. Keep long explanatory animations as animations. Do not replace them with
   summary cards unless the source video already used that visual language.
5. Drive the bottom navigation progress explicitly at slide pauses; do not use
   calibrated elapsed-time updaters in presenter-controlled slides.

Render the demo slide deck:

```powershell
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
$env:IMAGEIO_FFMPEG_EXE = "C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
$slides = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim-slides.exe"
& $slides render --CE --quality h slides_demo.py PhDConfirmationSlidesDemo
```

Present it:

```powershell
$slides = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim-slides.exe"
& $slides present PhDConfirmationSlidesDemo
```

If the native presenter has Qt issues, export a browser deck instead:

```powershell
$slides = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim-slides.exe"
& $slides convert --to html --one-file --offline PhDConfirmationSlidesDemo slides_demo_1080p_offline.html
```

Render the faithful S0 slide deck:

```powershell
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
$env:IMAGEIO_FFMPEG_EXE = "C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
$slides = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim-slides.exe"
& $slides render --CE --quality h slides_s0_why_nonlinear.py S0WhyNonlinearWavesSlides
& $slides convert --to html --one-file --offline S0WhyNonlinearWavesSlides slides_s0_why_nonlinear_1080p_offline.html
```

Render the faithful S1 slide deck:

```powershell
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
$env:IMAGEIO_FFMPEG_EXE = "C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
$slides = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim-slides.exe"
& $slides render --CE --quality h slides_s1_bound_harmonics.py S1BoundHarmonicsSlides
& $slides convert --to html --one-file --offline S1BoundHarmonicsSlides slides_s1_bound_harmonics_1080p_offline.html
```

Render the remaining faithful slide decks:

```powershell
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
$env:IMAGEIO_FFMPEG_EXE = "C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
$slides = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim-slides.exe"
& $slides render --CE --quality h slides_s2_exact_interactions.py S2ExactInteractionsSlides
& $slides render --CE --quality h slides_s3_vwa_structure.py S3VWAStructureSlides
& $slides render --CE --quality h slides_s4_higher_order_vwa.py S4HigherOrderVWASlides
& $slides render --CE --quality h slides_s5_surface_kinematics.py S5SurfaceKinematicsSlides
```

Recommended source-control shape:

- Keep the existing `scenario0_*.py` through `scenario5_*.py` files as the
  canonical video export path.
- Keep slide-specific entry points separate, either as `slides_demo.py` while
  prototyping or as `slides_s0_*.py` / `slides_deck.py` if the experiment grows.
- Share helper functions, colors, and visual builders where useful, but keep
  pacing separate: video scenes should remain duration-driven, while slide scenes
  should be presenter-step-driven.
- Avoid a global video/slides switch inside the same scene until there is a
  clear repeated pattern. A switch looks neat early, but it tends to entangle
  calibrated waits, navigation timing, and slide pauses.
- Keep `media/`, `slides/`, and exported offline HTML decks out of Git. Commit
  source `.py` files and documentation, then regenerate outputs locally.

HTML review modes:

- `--one-file --offline` HTML is best for sending one portable file to someone
  else. It embeds the slide videos into the HTML, so after re-rendering a slide
  you should export the HTML again.
- A linked preview HTML is better for local iteration. It references the short
  MP4 files under `slides/files/...` plus any deliberately reused scenario MP4s.
  If a short video is regenerated at the same path, refreshing the browser picks
  up the change.
- Rebuild the linked preview with `python build_linked_slides_preview.py` after
  re-rendering slide JSON/MP4 outputs, so the HTML points at the newest generated
  slide file hashes.
- Use `python build_s0_nav_slides_preview.py` after a low-quality S0 render when
  iterating on navigation typography or spacing. This produces
  `nav_s0_slide_control_preview.html`, which is intentionally ignored by Git.
- S5 is currently better treated as a linked looping video slide, because the
  original S5 scene is a continuous four-column application bridge. Reusing the
  rendered `SurfaceKinematicsVWA.mp4` is much faster than re-rendering the same
  heavy `always_redraw` scene through Manim Slides.

Current local Manim Slides caveat:

- `manim-slides present ...` currently fails on this machine because Manim
  Slides uses a Qt video API not available through the installed PyQt5 binding.
  The reliable review path is `manim-slides convert --to html --one-file
  --offline ...` and opening the generated HTML in a browser.

Current final outputs:

- `media/videos/phd_confirmation_full_1080p60.mp4`
- `media/videos/scenario0_why_nonlinear/1080p60/WhyNonlinearWaves.mp4`
- `media/videos/scenario1_bound_harmonics/1080p60/BoundHarmonicsIntro.mp4`
- `media/videos/scenario2_exact_interactions/1080p60/WhyExactInteractionsAreExpensive.mp4`
- `media/videos/scenario3_vwa_structure/1080p60/TheVWAIdea.mp4`
- `media/videos/scenario4_higher_order_vwa/1080p60/HigherOrderVWA.mp4`
- `media/videos/scenario5_surface_kinematics/1080p60/SurfaceKinematicsVWA.mp4`
