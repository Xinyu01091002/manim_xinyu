---
name: manim-slides-html
description: Build, adapt, render, export, and verify HTML presentations made from Manim Community Edition scenes using manim-slides. Use when Codex is asked to create an HTML-style Manim presentation, convert Manim scenes into presenter-controlled slides, export one-file/offline HTML decks, rebuild linked browser previews, troubleshoot manim-slides render/convert workflows, or update repo-specific PhD confirmation slide decks.
---

# Manim Slides HTML

## Overview

Use this skill for ManimCE presentations whose delivery target is a browser HTML deck rather than a stitched video. Prefer the existing `projects/phd_confirmation` workflow for mature decks and use `projects/presentation_project` only as a small smoke-test/prototype.

For scene authoring details, combine this skill with `manimce-best-practices`. For narrative planning before implementation, combine it with `manim-composer`.

## Workflow

1. Identify the deck mode:
   - **One-file offline HTML** for portable sharing.
   - **Linked preview HTML** for local iteration against generated slide MP4s.
   - **Narrated preview HTML** only when audio/subtitle helpers are explicitly part of the task.
2. Use `manim_slides.Slide` with a fallback to `Scene` so source remains renderable when `manim-slides` is absent.
3. Convert explanatory waits into presenter-controlled pauses with a small helper that calls `next_slide(loop=False)`.
4. Keep video scenes and slide scenes separate. In this repo, `scenario*_*.py` is the calibrated video path and `slides_s*_*.py` is the presenter-controlled path.
5. For iterative scene work, prefer `tools/manim_slides_clean_render.py` so stale scene-specific media and slide assets are removed before render. Use raw `manim-slides render` only when the clean-render wrapper is not appropriate.
6. Render with the local Anaconda `manim-slides.exe`, then export or rebuild HTML.
7. Verify by rendering a small representative deck or the changed slide deck, then check that expected HTML/JSON/MP4 outputs exist.

## Repo Rules

- Preserve the restrained scientific presentation style from the repo `AGENTS.md`: quiet text motion, stable layouts, and animation effort spent on visual mechanisms.
- Prefer a LaTeX-style academic visual language for Manim slide decks: CMU/Computer Modern-style serif typography, equation-led composition, high-contrast mathematical notation, and restrained color accents. Use `MathTex`/`Tex` for formulas and prefer plain serif text over dashboard/card-like UI styling unless the user asks for a different look.
- Design each slide around one conceptual move and reveal it progressively. Do not show every equation, conclusion, and interpretation at once when a step-by-step reveal would make the logic clearer. Avoid unexplained helper symbols or placeholder variables in teaching slides; prefer the real physical/mathematical quantities already established in the lecture. Use animation to show how one expression becomes another, how a phase locks, or how a mean/set-down/subharmonic component emerges.
- In `projects/phd_confirmation`, use `presentation_nav.py` and drive navigation explicitly at slide pauses. Do not use elapsed-time navigation updaters in presenter-controlled slide scenes.
- Keep generated `media/`, `slides/`, exported HTML, and asset folders out of source control unless the repo explicitly tracks a specific artifact.
- Keep iterative development media in `.manim_media/` by default and clean only scene-specific generated assets unless the user asks for broader cleanup.
- Do not rely on `manim-slides present` as the primary review path on this machine; the documented reliable path is HTML export and browser review.
- Set TeX and ffmpeg environment variables before rendering scenes that use `MathTex` or video export.

## Commands

Read [references/workflow.md](references/workflow.md) for exact local PowerShell commands, render/export recipes, linked-preview details, and verification checklists.
