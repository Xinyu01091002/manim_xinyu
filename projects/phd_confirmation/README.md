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
- active labels are larger and stroked for contrast
- inactive labels remain visible but lower opacity

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

Current final outputs:

- `media/videos/phd_confirmation_full_1080p60.mp4`
- `media/videos/scenario0_why_nonlinear/1080p60/WhyNonlinearWaves.mp4`
- `media/videos/scenario1_bound_harmonics/1080p60/BoundHarmonicsIntro.mp4`
- `media/videos/scenario2_exact_interactions/1080p60/WhyExactInteractionsAreExpensive.mp4`
- `media/videos/scenario3_vwa_structure/1080p60/TheVWAIdea.mp4`
- `media/videos/scenario4_higher_order_vwa/1080p60/HigherOrderVWA.mp4`
- `media/videos/scenario5_surface_kinematics/1080p60/SurfaceKinematicsVWA.mp4`
