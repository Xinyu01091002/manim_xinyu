# Manim Project Guidelines

## Animation Workflow

Before writing any code, create an `outline.md` in the project folder.

## Presentation Style

Use restrained animation language for presentation work:

- Text should enter quietly. Prefer `FadeIn`, `Write`, or direct `add`.
- Avoid decorative text motion that does not help understanding.
- Reserve richer animation for conceptual visualizations: waves, transforms, mappings,
  kernels, probes, arrows, and phase relationships.
- Labels, titles, subtitles, and takeaway text should not distract from the main visual.
- Recurrent UI elements such as navigation bars should be stable and efficient: build them
  once and update small state changes instead of rebuilding text every frame.

### Narrative Structure

Every animation should follow this structure:

- **Qi / Setup** - pose the question or context. Why should the viewer watch this?
- **Cheng / Build** - establish foundational concepts, lay the groundwork.
- **Zhuan / Turn** - the core insight or transformation, the reason the animation exists.
- **He / Resolution** - close the loop, answer the opening question, give the viewer a clear takeaway.

### Map Narrative To Scenes

Each narrative beat maps to one or more Manim `Scene` classes. One Scene = one idea.

```text
outline.md          ->    scenes in code
----------------------------------------------
Qi: pose problem    ->    TitleScene / IntroScene
Cheng: build ideas  ->    ConceptScene / SetupScene
Zhuan: core insight ->    DemoScene / TransformScene
He: wrap up         ->    SummaryScene / OutroScene
```

### Within Each Scene

- Introduce one element at a time.
- Use `self.wait()` before important transitions - give the viewer time to process.
- Use `LaggedStart` for related elements appearing together, not all at once.

## Project Structure

```text
projects/
└── <project-name>/
    ├── outline.md      <- start here, before any code
    ├── main.py
    └── manim.cfg
```

## Environment

- Manim Community v0.19.0 (Anaconda)
- Manim executable: `C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim`
- TeX path for `MathTex`: `C:\texlive\2023\bin\windows`
- ffmpeg for stitching:
  `C:\Users\spet5947\AppData\Local\anaconda3\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe`
- Smoke test a scene without rendering: `manim --dry_run <script>.py <SceneName>`
- To update skills from upstream: `git subtree pull --prefix=skills upstream main --squash`

## PhD Confirmation Current Output

- Combined high-quality video:
  `projects/phd_confirmation/media/videos/phd_confirmation_full_1080p60.mp4`
- Quality: `1080p60`
- Duration: `00:05:05.08`
- Navigation: use `bottom_progress_nav` from
  `projects/phd_confirmation/presentation_nav.py`
- Merge list: `projects/phd_confirmation/concat_high_quality.txt`
