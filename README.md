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
