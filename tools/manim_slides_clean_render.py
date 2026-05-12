#!/usr/bin/env python3
"""Clean scene-specific Manim Slides artifacts before rendering."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence


GENERATED_MEDIA_EXTENSIONS = (".mp4", ".mov", ".webm", ".gif", ".png")


def find_project_root(start: Path | None = None) -> Path:
    """Return the git repository root, falling back to the current directory."""
    cwd = Path.cwd() if start is None else Path(start)
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return cwd.resolve()

    root = result.stdout.strip()
    return Path(root).resolve() if root else cwd.resolve()


def resolve_configured_path(path: str | Path, project_root: Path) -> Path:
    """Resolve a configured path relative to the project root when needed."""
    raw = Path(path)
    if raw.is_absolute():
        return raw.resolve()
    return (project_root / raw).resolve()


def ensure_safe_path(path: Path, project_root: Path, allow_outside_project: bool = False) -> Path:
    """Return path if it is safe to delete, otherwise raise ValueError."""
    resolved = path.resolve()
    root = project_root.resolve()
    if not allow_outside_project and not (resolved == root or resolved.is_relative_to(root)):
        raise ValueError(f"refusing to delete outside repository root: {resolved}")
    return resolved


def _dedupe_existing(paths: Iterable[Path]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved.exists() and resolved not in seen:
            seen.add(resolved)
            result.append(resolved)
    return result


def _matching_scene_outputs(base: Path, scene: str) -> Iterable[Path]:
    if not base.exists():
        return []
    matches: list[Path] = []
    for ext in GENERATED_MEDIA_EXTENSIONS:
        matches.extend(base.rglob(f"{scene}{ext}"))
    return matches


def _scene_partial_dirs(video_base: Path, scene: str) -> Iterable[Path]:
    if not video_base.exists():
        return []
    matches: list[Path] = []
    for partial_root in video_base.rglob("partial_movie_files"):
        scene_dir = partial_root / scene
        if scene_dir.is_dir():
            matches.append(scene_dir)
    return matches


def _all_partial_roots(video_base: Path) -> Iterable[Path]:
    if not video_base.exists():
        return []
    return [path for path in video_base.rglob("partial_movie_files") if path.is_dir()]


def collect_cleanup_targets(
    project_root: Path,
    input_file: str | Path,
    scenes: Sequence[str],
    media_dir: str | Path = ".manim_media",
    slides_dir: str | Path = "slides",
    *,
    clean_partials: bool = False,
    clean_all_partials: bool = False,
    allow_outside_project: bool = False,
) -> list[Path]:
    """Collect existing scene-specific generated artifacts to remove."""
    root = project_root.resolve()
    input_stem = Path(input_file).stem
    media_root = resolve_configured_path(media_dir, root)
    slides_root = resolve_configured_path(slides_dir, root)
    video_base = media_root / "videos" / input_stem
    image_base = media_root / "images" / input_stem

    candidates: list[Path] = []
    for scene in scenes:
        candidates.extend(
            [
                slides_root / f"{scene}.json",
                slides_root / "files" / scene,
            ]
        )
        candidates.extend(_matching_scene_outputs(video_base, scene))
        candidates.extend(_matching_scene_outputs(image_base, scene))
        if clean_partials:
            candidates.extend(_scene_partial_dirs(video_base, scene))

    if clean_all_partials:
        candidates.extend(_all_partial_roots(video_base))

    safe = [
        ensure_safe_path(path, root, allow_outside_project=allow_outside_project)
        for path in _dedupe_existing(candidates)
    ]
    safe.sort(key=lambda p: (len(p.parts), str(p).lower()))
    return safe


def remove_target(path: Path) -> None:
    """Remove a file or directory."""
    try:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    except PermissionError as exc:
        raise PermissionError(
            f"Could not remove locked generated artifact: {path}\n"
            "Close manim-slides present, video players, PowerPoint, browsers, "
            "or file previewers, then rerun the command."
        ) from exc


def build_render_command(
    input_file: str,
    scenes: Sequence[str],
    quality: str,
    media_dir: str,
    *,
    flush_cache: bool = True,
    disable_caching: bool = False,
    extra_args: Sequence[str] = (),
) -> list[str]:
    """Build the manim-slides render command."""
    cmd = [
        "manim-slides",
        "render",
        "-q",
        quality,
        "--media_dir",
        media_dir,
    ]
    if flush_cache:
        cmd.append("--flush_cache")
    if disable_caching:
        cmd.append("--disable_caching")
    cmd.extend([input_file, *scenes, *extra_args])
    return cmd


def build_present_command(scenes: Sequence[str]) -> list[str]:
    """Build the manim-slides present command."""
    return ["manim-slides", "present", *scenes]


def parse_args(argv: Sequence[str] | None = None) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        description="Clean scene-specific Manim/manim-slides artifacts before rendering.",
    )
    parser.add_argument("input_file", help="Manim Python file, e.g. example.py")
    parser.add_argument("scenes", nargs="+", help="One or more scene class names")
    parser.add_argument("-q", "--quality", choices=["l", "m", "h", "p", "k"], default="l")
    parser.add_argument("--media-dir", default=".manim_media")
    parser.add_argument("--slides-dir", default="slides")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--clean-only", action="store_true")
    parser.add_argument("--present", action="store_true")
    parser.add_argument("--flush-cache", dest="flush_cache", action="store_true", default=True)
    parser.add_argument("--no-flush-cache", dest="flush_cache", action="store_false")
    parser.add_argument("--disable-caching", action="store_true")
    parser.add_argument(
        "--clean-partials",
        action="store_true",
        help="Remove scene-specific partial_movie_files/<Scene>/ directories when found.",
    )
    parser.add_argument(
        "--clean-all-partials",
        action="store_true",
        help=(
            "Remove every partial_movie_files directory for this input file under the "
            "configured media directory. Use --dry-run first for unusual cleanup."
        ),
    )
    parser.add_argument(
        "--allow-outside-project",
        action="store_true",
        help="Allow configured cleanup paths outside the detected repository root.",
    )
    return parser.parse_known_args(argv)


def _print_command(label: str, command: Sequence[str]) -> None:
    print(f"{label}:")
    print("  " + subprocess.list2cmdline(list(command)))


def main(argv: Sequence[str] | None = None) -> int:
    args, extra_args = parse_args(argv)
    project_root = find_project_root()

    try:
        cleanup_targets = collect_cleanup_targets(
            project_root,
            args.input_file,
            args.scenes,
            args.media_dir,
            args.slides_dir,
            clean_partials=args.clean_partials,
            clean_all_partials=args.clean_all_partials,
            allow_outside_project=args.allow_outside_project,
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if cleanup_targets:
        print("Cleanup targets:")
        for target in cleanup_targets:
            print(f"  {target}")
    else:
        print("Cleanup targets: none")

    render_command = build_render_command(
        args.input_file,
        args.scenes,
        args.quality,
        args.media_dir,
        flush_cache=args.flush_cache,
        disable_caching=args.disable_caching,
        extra_args=extra_args,
    )

    if args.clean_only:
        print("Clean-only mode: render skipped.")
    else:
        _print_command("Render command", render_command)

    if args.present:
        _print_command("Present command", build_present_command(args.scenes))

    if args.dry_run:
        print("Dry run: no files removed and no commands executed.")
        return 0

    if not args.clean_only and shutil.which("manim-slides") is None:
        print(
            "error: manim-slides was not found on PATH. Install it or activate the "
            "environment that provides manim-slides.",
            file=sys.stderr,
        )
        return 127

    for target in cleanup_targets:
        try:
            remove_target(target)
        except PermissionError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        except OSError as exc:
            print(f"error: failed to remove {target}: {exc}", file=sys.stderr)
            return 1

    if args.clean_only:
        return 0

    render_result = subprocess.run(render_command)
    if render_result.returncode != 0:
        return render_result.returncode

    if args.present:
        present_result = subprocess.run(build_present_command(args.scenes))
        return present_result.returncode

    return render_result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
