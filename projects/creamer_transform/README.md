# Creamer Transform Project

This project is for building Manim visualizations of the Creamer transform, with the main emphasis on the original 1989 deep-water construction and a secondary finite-depth outlook.

Current status:

- project scaffold created
- narrative outline drafted in [outline.md](/c:/Research/manim/projects/creamer_transform/outline.md:1)
- first four scenes implemented and rendered in preview form

Implemented scenes:

- [scenario0_what_is_creamer.py](/c:/Research/manim/projects/creamer_transform/scenario0_what_is_creamer.py:1)
  Introductory scene: what Creamer is trying to improve, why the story starts from `H = H_2 + H_3 + H_4 + ...`, and why shape-function / DNO thinking differs from a Stokes expansion around the flat `z=0`.
- [scenario1_why_h3_removable.py](/c:/Research/manim/projects/creamer_transform/scenario1_why_h3_removable.py:1)
  Explains why `H_3` is the first nonlinear target and why deep water makes it removable.
- [scenario2_how_to_absorb_h3.py](/c:/Research/manim/projects/creamer_transform/scenario2_how_to_absorb_h3.py:1)
  Introduces the Poisson bracket, the `lambda`-flow viewpoint, and the cubic cancellation logic behind `K = H_2 + O(4)`.
- [scenario3_1d_remapping.py](/c:/Research/manim/projects/creamer_transform/scenario3_1d_remapping.py:1)
  Shows how the 1D deep-water case becomes a geometric horizontal remapping.

Current narrative map:

1. `scenario0`: what the transform is trying to improve
2. `scenario1`: why deep water singles out `H_3`
3. `scenario2`: how the canonical transform absorbs `H_3`
4. `scenario3`: why the 1D deep-water limit becomes visually readable

Planned next scenes:

- `scenario4`: reconstruction and bound harmonics
- `scenario5`: long-short-wave physical meaning
- finite-depth contrast and research-outlook closing scenes

Planned focus:

- what Creamer is doing in Hamiltonian terms
- why deep water is special
- how the 1D remapping picture creates bound harmonics during reconstruction
- what becomes nontrivial in finite depth

Local Windows environment for this repo:

- Preferred Manim executable on this machine:
  `C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim`
- Matching Python for helper scripts:
  `C:\Users\spet5947\AppData\Local\anaconda3\python.exe`
- The default shell `python` / `py` may point to other installs that do not have Manim.
- TeX rendering works when `C:\texlive\2023\bin\windows` is on `PATH`.
- `build_full_video.ps1` uses the same Anaconda Python and can resolve `ffmpeg` from `imageio-ffmpeg` if needed.

If `manim` is not on `PATH`, call it explicitly:

```powershell
& "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim" scenario0_what_is_creamer.py WhatIsCreamer
```

Suggested render pattern once scene files exist:

```powershell
cd c:\Research\manim\projects\creamer_transform
manim -ql <script>.py <SceneName>
```

Current preview renders:

```powershell
cd c:\Research\manim\projects\creamer_transform
manim -ql scenario0_what_is_creamer.py WhatIsCreamer
manim -ql scenario1_why_h3_removable.py WhyH3Removable
manim -ql scenario2_how_to_absorb_h3.py HowToAbsorbH3
manim -ql scenario3_1d_remapping.py OneDDeepWaterRemapping
```

Build a stitched 720p video:

```powershell
cd c:\Research\manim\projects\creamer_transform
.\build_full_video.ps1 -RenderMissing
```

This selects the best available render for each implemented scene, renders missing low-resolution-only scenes to `720p30` when needed, and writes `media/videos/CreamerTransform_full_720p.mp4`.

High-quality renders:

```powershell
cd c:\Research\manim\projects\creamer_transform
manim -qh scenario0_what_is_creamer.py WhatIsCreamer
manim -qh scenario1_why_h3_removable.py WhyH3Removable
```

Notes:

- Run Manim from this project directory so outputs stay under this project's own `media/` tree.
- If `build_full_video.ps1` cannot find `ffmpeg`, install it into the same Anaconda environment with `C:\Users\spet5947\AppData\Local\anaconda3\python.exe -m pip install imageio-ffmpeg`.
- During iteration, rendering one scene at a time is preferred. Manim will reuse cache for unchanged animations.
