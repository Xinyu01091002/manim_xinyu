# Manim Slides Clean-Render Workflow

Use `tools/manim_slides_clean_render.py` for iterative Manim Slides work. It
removes scene-specific generated assets before rendering so stale MP4, slide
JSON, and slide asset directories do not accumulate.

The default development media directory is `.manim_media/`, keeping iterative
outputs away from Manim's default `media/` directory.

## Active Manim Skills

Repo-local skills live under `.agents/skills/` so Codex can discover them as
default guidance for this workspace:

- `manim-composer`: plan educational Manim narratives before writing scenes.
- `manimce-best-practices`: apply Manim Community Edition patterns when files
  import `from manim import *` or use the `manim` CLI.
- `manim-slides-html`: build, adapt, export, and verify browser-facing
  Manim Slides decks.
- `manim-slides-clean-render`: clean stale Manim Slides assets before
  iterative renders.
- `manimgl-best-practices`: use only for ManimGL / 3Blue1Brown-style projects
  that import `from manimlib import *`.

For browser-controlled slide decks, combine `manim-slides-html` with
`manim-slides-clean-render`: use the clean-render helper for scene-specific
rerenders, then rebuild or export the HTML deck.

## Common Commands

Default iterative render:

```powershell
python tools/manim_slides_clean_render.py example.py BasicExample -q l
```

Dry run:

```powershell
python tools/manim_slides_clean_render.py example.py BasicExample --dry-run
```

Clean without rendering:

```powershell
python tools/manim_slides_clean_render.py example.py BasicExample --clean-only
```

Final/high-quality render:

```powershell
python tools/manim_slides_clean_render.py example.py BasicExample -q h
```

Present after render:

```powershell
python tools/manim_slides_clean_render.py example.py BasicExample -q l --present
```

Forward extra Manim/manim-slides render flags after the normal arguments:

```powershell
python tools/manim_slides_clean_render.py example.py BasicExample -q l -- --renderer=opengl
```

## What Gets Cleaned

For each scene, the script removes only matching generated assets:

- `slides/<Scene>.json`
- `slides/files/<Scene>/`
- final scene outputs under `.manim_media/videos/<file_stem>/**/`
- matching scene images under `.manim_media/images/<file_stem>/**/`

Partial movie cache cleanup is intentionally conservative. Use
`--clean-partials` to remove exact `partial_movie_files/<Scene>/` directories
when they can be identified. Use `--clean-all-partials` only for broader
input-file cache cleanup, and run `--dry-run` first.

## Safety Notes

The script resolves deletion targets to absolute paths and refuses to delete
outside the detected repository root unless `--allow-outside-project` is passed.

On Windows, deletion may fail if generated files are open in `manim-slides
present`, a media player, PowerPoint, browser, or file previewer. Close those
programs and rerun the command.

`--flush-cache` is enabled by default for iterative development. Use
`--disable-caching` only when stale Manim cache behavior is suspected.
