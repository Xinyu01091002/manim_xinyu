# manim

Personal collection of Manim animation scripts.

## Structure

- `projects/` - individual animation projects
- `skills/` - Manim best practice guides for AI coding assistants, sourced from
  [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill)

## Running a project

```bash
cd projects/<project-name>
manim -pql <script>.py <SceneName>
```

## Animation Style

For presentation animations in this repo, keep text motion restrained. Prefer
simple `FadeIn`, `Write`, or static placement for titles, labels, equations, and
takeaways. Save richer animation for visual mechanisms that help understanding:
wave evolution, transforms, phase matching, probes, kernel comparisons, arrows,
and diagrams. Avoid decorative text entrances that pull attention away from the
scientific content.

Recurring UI, especially presentation navigation, should be built once and
updated through small state changes. Do not rebuild text-heavy navigation with
`always_redraw`.

## Known Local Windows Environment

On this machine, the working ManimCE install is:

- Manim executable: `C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim`
- Python for helper scripts: `C:\Users\spet5947\AppData\Local\anaconda3\python.exe`
- TeX/LaTeX path required by Manim `MathTex`: `C:\texlive\2023\bin\windows`
- ffmpeg used for video stitching: `C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe`

Important:

- The default `python` / `py` in the shell may point to other Python installs
  without Manim.
- If `manim` is not on `PATH`, prefer calling the executable above directly
  instead of guessing which Python environment is active.
- If `MathTex` fails with `FileNotFoundError` for `latex.exe`, prepend the TeX
  Live path in the current PowerShell session:

```powershell
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
```

- For stitched-video workflows, set `IMAGEIO_FFMPEG_EXE` to the ffmpeg path
  above.

Notes:

- Run Manim from the project directory so media output is written to that
  project's own `media/` folder.
- For active development in this repo, low quality is the default unless a
  higher-quality render is explicitly needed.

## PhD Confirmation Project

Project-specific notes live in [projects/phd_confirmation/README.md](projects/phd_confirmation/README.md).

Current final output:

- Combined high-quality video:
  `projects/phd_confirmation/media/videos/phd_confirmation_full_1080p60.mp4`
- Quality: `1080p60`
- Duration: `00:05:05.08`

The presentation uses the optimized two-tier `bottom_progress_nav` from
`projects/phd_confirmation/presentation_nav.py`:

- Row 1: whole-talk progress across `S0`-`S5`
- Row 2: active subscenario progress
- Scenario timing constants should be calibrated against rendered video duration
  after major edits

Current high-quality render and merge workflow:

```powershell
cd projects/phd_confirmation
$env:PATH = "C:\texlive\2023\bin\windows;$env:PATH"
$env:IMAGEIO_FFMPEG_EXE = "C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
$manim = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim"

& $manim -qh scenario0_why_nonlinear.py WhyNonlinearWaves
& $manim -qh scenario1_bound_harmonics.py BoundHarmonicsIntro
& $manim -qh scenario2_exact_interactions.py WhyExactInteractionsAreExpensive
& $manim -qh scenario3_vwa_structure.py TheVWAIdea
& $manim -qh scenario4_higher_order_vwa.py HigherOrderVWA
& $manim -qh scenario5_surface_kinematics.py SurfaceKinematicsVWA

& $env:IMAGEIO_FFMPEG_EXE -y -f concat -safe 0 -i concat_high_quality.txt -c copy media/videos/phd_confirmation_full_1080p60.mp4
```

## Creamer Transform Project

For `projects/creamer_transform/`, the current workflow is:

```bash
cd projects/creamer_transform
manim -ql scenario0_what_is_creamer.py WhatIsCreamer
manim -ql scenario1_why_h3_removable.py WhyH3Removable
manim -ql scenario2_how_to_absorb_h3.py HowToAbsorbH3
manim -ql scenario3_1d_remapping.py OneDDeepWaterRemapping
```

This project is a staged visualization of the Creamer transform:

- `scenario0`: what Creamer is trying to improve
- `scenario1`: why deep water singles out `H_3`
- `scenario2`: how the canonical transform absorbs `H_3`
- `scenario3`: why the 1D deep-water limit becomes a horizontal remapping
