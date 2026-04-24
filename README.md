# manim

Personal collection of Manim animation scripts.

## Structure

- `projects/` — individual animation projects
- `skills/` — Manim best practice guides for AI coding assistants (sourced from [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill))

## Running a project

```bash
cd projects/<project-name>
manim -pql <script>.py <SceneName>
```

## Known Local Windows Environment

On this machine, the working ManimCE install is:

- Manim executable: `C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim`
- Python for helper scripts: `C:\Users\spet5947\AppData\Local\anaconda3\python.exe`
- TeX path to keep on `PATH`: `C:\texlive\2023\bin\windows`

Important:
- The default `python` / `py` in the shell may point to other Python installs without Manim.
- If `manim` is not on `PATH`, prefer calling the executable above directly instead of guessing which Python environment is active.
- For stitched-video workflows that need `ffmpeg`, install `imageio-ffmpeg` into the same Anaconda Python if necessary.

Notes:
- Run Manim from the project directory so media output is written to that project's own `media/` folder.
- For active development in this repo, low quality is the default unless a higher-quality render is explicitly needed.

## Skills

The `skills/` directory contains best practice rule files for ManimCE and ManimGL.
These are automatically picked up by AI coding assistants to provide better Manim-specific guidance.

## Current project note

For `projects/phd_confirmation/`, the current workflow is:

```bash
cd projects/phd_confirmation
manim -ql scenario0_why_nonlinear.py WhyNonlinearWaves
manim -qh scenario0_why_nonlinear.py WhyNonlinearWaves
```

This keeps the render outputs under `projects/phd_confirmation/media/` and matches the current presentation workflow.

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
