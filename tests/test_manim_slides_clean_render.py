import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import manim_slides_clean_render as clean_render


class ManimSlidesCleanRenderTests(unittest.TestCase):
    def test_ensure_safe_path_accepts_project_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            target = root / "slides" / "Example.json"

            self.assertEqual(
                clean_render.ensure_safe_path(target, root),
                target.resolve(),
            )

    def test_ensure_safe_path_rejects_outside_root(self):
        with tempfile.TemporaryDirectory() as root_tmp, tempfile.TemporaryDirectory() as outside_tmp:
            root = Path(root_tmp).resolve()
            outside = Path(outside_tmp) / "Example.json"

            with self.assertRaises(ValueError):
                clean_render.ensure_safe_path(outside, root)

    def test_collects_slide_json_and_files_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            slide_json = root / "slides" / "BasicExample.json"
            slide_files = root / "slides" / "files" / "BasicExample"
            slide_files.mkdir(parents=True)
            slide_json.parent.mkdir(parents=True, exist_ok=True)
            slide_json.write_text("{}", encoding="utf-8")

            targets = clean_render.collect_cleanup_targets(root, "example.py", ["BasicExample"])

            self.assertIn(slide_json.resolve(), targets)
            self.assertIn(slide_files.resolve(), targets)

    def test_collects_scene_video_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            video = root / ".manim_media" / "videos" / "example" / "480p15" / "BasicExample.mp4"
            other = root / ".manim_media" / "videos" / "example" / "480p15" / "OtherScene.mp4"
            video.parent.mkdir(parents=True)
            video.write_bytes(b"video")
            other.write_bytes(b"other")

            targets = clean_render.collect_cleanup_targets(root, "example.py", ["BasicExample"])

            self.assertIn(video.resolve(), targets)
            self.assertNotIn(other.resolve(), targets)

    def test_collects_scene_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            image = root / ".manim_media" / "images" / "example" / "BasicExample.png"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"image")

            targets = clean_render.collect_cleanup_targets(root, "example.py", ["BasicExample"])

            self.assertIn(image.resolve(), targets)

    def test_dry_run_does_not_delete_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            slide_json = root / "slides" / "BasicExample.json"
            slide_json.parent.mkdir(parents=True)
            slide_json.write_text("{}", encoding="utf-8")

            with mock.patch.object(clean_render, "find_project_root", return_value=root):
                with contextlib.redirect_stdout(io.StringIO()):
                    exit_code = clean_render.main(["example.py", "BasicExample", "--dry-run"])

            self.assertEqual(exit_code, 0)
            self.assertTrue(slide_json.exists())

    def test_rejects_configured_cleanup_path_outside_root(self):
        with tempfile.TemporaryDirectory() as root_tmp, tempfile.TemporaryDirectory() as outside_tmp:
            root = Path(root_tmp).resolve()
            outside_slides = Path(outside_tmp).resolve()
            target = outside_slides / "BasicExample.json"
            target.write_text("{}", encoding="utf-8")

            with self.assertRaises(ValueError):
                clean_render.collect_cleanup_targets(
                    root,
                    "example.py",
                    ["BasicExample"],
                    slides_dir=outside_slides,
                )

    def test_multiple_scenes_are_handled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            first = root / "slides" / "FirstScene.json"
            second = root / "slides" / "SecondScene.json"
            first.parent.mkdir(parents=True)
            first.write_text("{}", encoding="utf-8")
            second.write_text("{}", encoding="utf-8")

            targets = clean_render.collect_cleanup_targets(
                root,
                "example.py",
                ["FirstScene", "SecondScene"],
            )

            self.assertIn(first.resolve(), targets)
            self.assertIn(second.resolve(), targets)


if __name__ == "__main__":
    unittest.main()
