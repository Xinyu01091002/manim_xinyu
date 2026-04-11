# Manim Presentation Project

## Files
- `presentation.py`: includes `Deck` (for manim-slides) and standalone scenes.
- `manim.cfg`: default render config.
- `render.ps1`: helper script for one scene.

## 1) Normal Manim Preview (works now)
```powershell
cd c:\Research\manim\presentation_project
"c:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim" presentation.py Deck
```

## 2) Use Manim-Slides (interactive presentation)
### Install
Your current environment has `PIP_NO_INDEX=1`, so pip cannot fetch packages.
In the same terminal, run:
```powershell
$env:PIP_NO_INDEX="0"
"c:\Users\spet5947\AppData\Local\anaconda3\Scripts\pip" install manim-slides
```

### Render + Present
```powershell
"c:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim" presentation.py Deck
"c:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim-slides" Deck
```

If `manim-slides Deck` does not work in your version, run:
```powershell
"c:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim-slides" present Deck
```

## Slide Controls (typical)
- Next: Right Arrow / Space
- Previous: Left Arrow
- Quit: `q`
