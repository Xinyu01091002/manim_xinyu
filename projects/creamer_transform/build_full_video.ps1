param(
    [string]$OutputPath = "media\\videos\\CreamerTransform_full_720p.mp4",
    [switch]$RenderMissing
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$manim = "C:\Users\spet5947\AppData\Local\anaconda3\Scripts\manim"
$condaPython = "C:\Users\spet5947\AppData\Local\anaconda3\python.exe"

function Resolve-FfmpegExe {
    $ffmpegCommand = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if ($ffmpegCommand) {
        return $ffmpegCommand.Source
    }

    if (-not (Test-Path $condaPython)) {
        throw "Could not find $condaPython. Install ffmpeg or update the script's Python path."
    }

    $ffmpegSource = (& $condaPython -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())").Trim()
    if (-not $ffmpegSource) {
        throw "Could not resolve an ffmpeg executable. Try: $condaPython -m pip install imageio-ffmpeg"
    }

    $toolDir = Join-Path $projectRoot ".tools"
    $ffmpegExe = Join-Path $toolDir "ffmpeg.exe"
    New-Item -ItemType Directory -Force $toolDir | Out-Null

    $shouldCopy = -not (Test-Path $ffmpegExe)
    if (-not $shouldCopy) {
        $sourceInfo = Get-Item $ffmpegSource
        $localInfo = Get-Item $ffmpegExe
        $shouldCopy = $sourceInfo.Length -ne $localInfo.Length
    }

    if ($shouldCopy) {
        Copy-Item $ffmpegSource $ffmpegExe -Force
    }

    return $ffmpegExe
}

function Invoke-SceneRender {
    param(
        [string]$ScriptPath,
        [string]$SceneName
    )

    if (-not (Test-Path $manim)) {
        throw "Could not find manim at $manim"
    }

    Write-Host "Rendering $SceneName at 720p30..."
    & $manim $ScriptPath $SceneName
}

$ffmpegExe = Resolve-FfmpegExe
$env:PATH = "$(Split-Path -Parent $ffmpegExe);$env:PATH"

$scenes = @(
    [pscustomobject]@{
        Label = "scenario0"
        Script = "scenario0_what_is_creamer.py"
        Scene = "WhatIsCreamer"
        Preferred = "media\\videos\\scenario0_what_is_creamer\\720p30\\WhatIsCreamer.mp4"
        HighFallback = "media\\videos\\scenario0_what_is_creamer\\1080p60\\WhatIsCreamer.mp4"
        LowFallback = "media\\videos\\scenario0_what_is_creamer\\480p15\\WhatIsCreamer.mp4"
    }
    [pscustomobject]@{
        Label = "scenario1"
        Script = "scenario1_why_h3_removable.py"
        Scene = "WhyH3Removable"
        Preferred = "media\\videos\\scenario1_why_h3_removable\\720p30\\WhyH3Removable.mp4"
        HighFallback = "media\\videos\\scenario1_why_h3_removable\\1080p60\\WhyH3Removable.mp4"
        LowFallback = "media\\videos\\scenario1_why_h3_removable\\480p15\\WhyH3Removable.mp4"
    }
    [pscustomobject]@{
        Label = "scenario2"
        Script = "scenario2_how_to_absorb_h3.py"
        Scene = "HowToAbsorbH3"
        Preferred = "media\\videos\\scenario2_how_to_absorb_h3\\720p30\\HowToAbsorbH3.mp4"
        HighFallback = $null
        LowFallback = "media\\videos\\scenario2_how_to_absorb_h3\\480p15\\HowToAbsorbH3.mp4"
    }
    [pscustomobject]@{
        Label = "scenario3"
        Script = "scenario3_1d_remapping.py"
        Scene = "OneDDeepWaterRemapping"
        Preferred = "media\\videos\\scenario3_1d_remapping\\720p30\\OneDDeepWaterRemapping.mp4"
        HighFallback = $null
        LowFallback = "media\\videos\\scenario3_1d_remapping\\480p15\\OneDDeepWaterRemapping.mp4"
    }
)

if ($RenderMissing) {
    foreach ($scene in $scenes) {
        $hasPreferred = Test-Path $scene.Preferred
        $hasHighFallback = $scene.HighFallback -and (Test-Path $scene.HighFallback)
        if (-not ($hasPreferred -or $hasHighFallback)) {
            Invoke-SceneRender -ScriptPath $scene.Script -SceneName $scene.Scene
        }
    }
}

$selectedSources = @()
foreach ($scene in $scenes) {
    $candidates = @($scene.Preferred, $scene.HighFallback, $scene.LowFallback) | Where-Object { $_ }
    $source = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $source) {
        throw "No render found for $($scene.Label). Consider running .\\build_full_video.ps1 -RenderMissing"
    }

    $resolvedSource = (Resolve-Path $source).Path
    $selectedSources += $resolvedSource
    Write-Host "Using $($scene.Label): $resolvedSource"
}

$outputAbsolute = if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $OutputPath
} else {
    Join-Path $projectRoot $OutputPath
}

$outputDirectory = Split-Path -Parent $outputAbsolute
if ($outputDirectory) {
    New-Item -ItemType Directory -Force $outputDirectory | Out-Null
}

$filterParts = @()
for ($index = 0; $index -lt $selectedSources.Count; $index++) {
    $filterParts += "[$($index):v]fps=30,scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[v$($index)]"
}

$concatInputs = (0..($selectedSources.Count - 1) | ForEach-Object { "[v$_]" }) -join ""
$filterGraph = ($filterParts -join "; ") + "; $concatInputs" + "concat=n=$($selectedSources.Count):v=1:a=0[v]"

$ffmpegArgs = @()
foreach ($source in $selectedSources) {
    $ffmpegArgs += "-i"
    $ffmpegArgs += $source
}

$ffmpegArgs += "-filter_complex"
$ffmpegArgs += $filterGraph
$ffmpegArgs += "-map"
$ffmpegArgs += "[v]"
$ffmpegArgs += "-c:v"
$ffmpegArgs += "libx264"
$ffmpegArgs += "-preset"
$ffmpegArgs += "medium"
$ffmpegArgs += "-crf"
$ffmpegArgs += "18"
$ffmpegArgs += "-pix_fmt"
$ffmpegArgs += "yuv420p"
$ffmpegArgs += "-movflags"
$ffmpegArgs += "+faststart"
$ffmpegArgs += "-y"
$ffmpegArgs += $outputAbsolute

Write-Host "Writing stitched video to $outputAbsolute"
& $ffmpegExe @ffmpegArgs
if ($LASTEXITCODE -ne 0) {
    throw "ffmpeg failed with exit code $LASTEXITCODE"
}

Write-Host "Done: $outputAbsolute"
