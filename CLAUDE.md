# Manim Project Guidelines

## Animation Workflow

Before writing any code, create an `outline.md` in the project folder.

### Narrative structure (起承转合)

Every animation should follow this structure:

- **起 (Setup)** — pose the question or context. Why should the viewer watch this?
- **承 (Build)** — establish foundational concepts, lay the groundwork
- **转 (Turn)** — the core insight or transformation, the reason the animation exists
- **合 (Resolution)** — close the loop, answer the opening question, give the viewer a clear takeaway

### Map narrative to Scenes

Each narrative beat maps to one or more Manim `Scene` classes. One Scene = one idea.

```
outline.md          →    scenes in code
----------------------------------------------
起: pose problem    →    TitleScene / IntroScene
承: build concepts  →    ConceptScene / SetupScene
转: core insight    →    DemoScene / TransformScene
合: wrap up         →    SummaryScene / OutroScene
```

### Within each Scene

- Introduce one element at a time
- Use `self.wait()` before important transitions — give the viewer time to process
- Use `LaggedStart` for related elements appearing together, not all at once

## Project Structure

```
projects/
└── <project-name>/
    ├── outline.md      ← start here, before any code
    ├── main.py
    └── manim.cfg
```

## Environment

- Manim Community v0.19.0 (Anaconda)
- FFmpeg not on bash PATH — install via `conda install -c conda-forge ffmpeg` to enable video output
- Smoke test a scene without rendering: `manim --dry_run <script>.py <SceneName>`
- To update skills from upstream: `git subtree pull --prefix=skills upstream main --squash`
