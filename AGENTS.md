# Repository Working Notes

## Manim Presentation Style

Use a restrained presentation style for all Manim animation work in this repo.

- Prefer clear, stable layouts over decorative motion.
- Keep text entrance animations simple and quiet: `Write`, `FadeIn`, or direct `add`
  are usually enough.
- Avoid flashy or decorative text animation unless it directly supports the explanation.
- Spend animation complexity on visual understanding: wave motion, transforms, mappings,
  highlighted kernels, phase matching, diagrams, probes, and other conceptual mechanics.
- When a text element is only a label, title, subtitle, or takeaway, keep its motion minimal
  so it does not compete with the scientific visualization.
- Use pauses deliberately after important ideas so the presenter has time to explain.
- For recurring UI elements such as navigation bars, create stable objects once and update
  only small state changes; avoid per-frame reconstruction of text.

## Manim Slides workflow

- When modifying Manim Slides scenes, prefer `tools/manim_slides_clean_render.py`
  over raw `manim-slides render`.
- Default iterative command: `python tools/manim_slides_clean_render.py <file.py> <SceneName> -q l`.
- Keep development render outputs in `.manim_media/`.
- Clean only scene-specific generated assets unless the user explicitly asks for broader cleanup.
- Use `--dry-run` before broad or unusual cleanup.
- Never delete generated assets outside the repository root unless the user explicitly provides
  `--allow-outside-project`.
- Use `--flush-cache` during iterative work. Use `--disable-caching` only when stale Manim cache
  behavior is suspected.
- Do not commit generated media, slide files, or converted assets.

## PhD Confirmation Navigation Bar

For `projects/phd_confirmation/`, use the persistent two-tier navigation bar in
`projects/phd_confirmation/presentation_nav.py` when updating scenarios.

- Import `bottom_progress_nav` for scenario pages that should show presentation progress.
- The first row is whole-talk progress (`S0`-`S5`) and should advance through the current
  scenario as its local `ValueTracker` progresses.
- The second row is subscenario progress within the current scenario and should use the
  current scenario's gradient palette.
- Keep the current high-contrast style: near-black background, bright continuous
  scenario palette, and scenario-colored subscenario gradient.
- Use the current softened navigation style from `presentation_nav.py`: rounded
  segment bars, rounded fill bars, and compact `S0`-`S5` labels in the whole-talk
  row. Do not put long scenario titles into the narrow top-row segments; keep
  longer labels in the active subscenario row or the scene content. In the
  subscenario row, create all labels once but show text only for the currently
  active subscenario to avoid cramped inactive labels.
- Keep navigation labels as plain CMU Serif text with direct high-contrast
  colors: cool white for inactive labels and warm white for active labels. Do
  not add text strokes, dark label capsules, or other backdrops around nav text.
- Avoid `always_redraw` for the full navigation bar. It made rendering much slower by
  recreating `Text` and rectangles every frame.
- Preferred implementation: create bar rectangles and labels once, then use updaters only
  to change fill widths and small opacity changes.
- Reserve bottom space for the larger bar (`PROGRESS_NAV_HEIGHT = 0.72`). Move any bottom
  equations, axes, or takeaway text upward enough that they do not overlap.

Development render command:

```powershell
cd projects/phd_confirmation
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
$env:IMAGEIO_FFMPEG_EXE = "C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim -ql scenario0_why_nonlinear.py WhyNonlinearWaves
```

Current final PhD confirmation output:

- Combined video: `projects/phd_confirmation/media/videos/phd_confirmation_full_1080p60.mp4`
- Quality: `1080p60`
- Duration: `00:05:05.08`
- Merge list: `projects/phd_confirmation/concat_high_quality.txt`

Current calibrated scenario durations:

- S0 `WhyNonlinearWaves`: `52.20`
- S1 `BoundHarmonicsIntro`: `42.60`
- S2 `WhyExactInteractionsAreExpensive`: `39.58`
- S3 `TheVWAIdea`: `87.93`
- S4 `HigherOrderVWA`: `53.67`
- S5 `SurfaceKinematicsVWA`: `30.00`

If the animation timing changes, render a low-quality preview, measure the real duration
with ffmpeg, update `SCENARIO*_SECONDS`, then rerender the high-quality scenario. Use
`--disable_caching` when only the navigation timing constant changed, otherwise Manim may
reuse cached partial movies.
