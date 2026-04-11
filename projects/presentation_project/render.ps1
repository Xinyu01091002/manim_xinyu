# Render helper
# Usage:
#   .\render.ps1 TitleSlide
#   .\render.ps1 AgendaSlide
#   .\render.ps1 ResultsSlide

param(
    [Parameter(Mandatory=$true)]
    [string]$Scene
)

$manim = "c:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim"
& $manim "presentation.py" $Scene
