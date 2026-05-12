---
name: manim-slides-clean-render
description: Use when working on Manim Slides scenes and the user asks to render, rerender, clean stale MP4/media/slide assets, manage generated files, or keep iterative Manim output organized.
---

# Manim Slides Clean-Render Workflow

Use this skill for iterative Manim Slides development.

## Default Behavior

1. Identify the Manim Python file and scene name(s).
2. Prefer the repository script:
   `python tools/manim_slides_clean_render.py <file.py> <SceneName> -q l`
3. Use `.manim_media/` as the default development media directory.
4. Clean only scene-specific generated assets:
   - `slides/<Scene>.json`
   - `slides/files/<Scene>/`
   - matching scene outputs under `.manim_media/videos/<file_stem>/**/`
   - matching scene images under `.manim_media/images/<file_stem>/**/`
5. Use `--dry-run` before broad cleanup.
6. Use `--flush-cache` during iterative work.
7. Use `--disable-caching` only when stale cache behavior is suspected.
8. Do not delete outside the repository root unless the user explicitly requests it and passes `--allow-outside-project`.

## Common Commands

Dry run:
`python tools/manim_slides_clean_render.py example.py BasicExample --dry-run`

Iterative low-quality render:
`python tools/manim_slides_clean_render.py example.py BasicExample -q l`

Clean without rendering:
`python tools/manim_slides_clean_render.py example.py BasicExample --clean-only`

Render and present:
`python tools/manim_slides_clean_render.py example.py BasicExample -q l --present`

Final high-quality render:
`python tools/manim_slides_clean_render.py example.py BasicExample -q h`

## Safety Notes

- On Windows, deletion may fail when generated files are open in a presenter window, media player, browser, PowerPoint, or file previewer. Tell the user to close those programs and rerun the command.
- Never use broad shell commands such as `rm -rf media slides` unless the user explicitly requests a full project cleanup and the path has been verified.
- Prefer Python path handling over shell globs for deletion.
