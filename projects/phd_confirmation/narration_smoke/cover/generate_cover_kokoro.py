from __future__ import annotations

import argparse
import wave
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro


ROOT = Path(__file__).resolve().parents[2]
SMOKE_DIR = ROOT / "narration_smoke" / "cover"
SCRIPT_PATH = SMOKE_DIR / "cover_script.txt"
OUTPUT_PATH = SMOKE_DIR / "cover_kokoro.wav"
MODEL_PATH = SMOKE_DIR / "models" / "kokoro-v1.0.onnx"
VOICES_PATH = SMOKE_DIR / "models" / "voices-v1.0.bin"


def generate_cover_voice(script_path: Path, output_path: Path, voice: str) -> None:
    text = script_path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Script is empty: {script_path}")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Missing Kokoro ONNX model: {MODEL_PATH}")
    if not VOICES_PATH.exists():
        raise FileNotFoundError(f"Missing Kokoro voices file: {VOICES_PATH}")

    kokoro = Kokoro(str(MODEL_PATH), str(VOICES_PATH))
    samples, sample_rate = kokoro.create(text, voice=voice, speed=1.0, lang="en-us")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output_path, samples, sample_rate)


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav_file:
        return wav_file.getnframes() / float(wav_file.getframerate())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Kokoro ONNX TTS smoke-test voiceover for the PhD confirmation cover page.")
    parser.add_argument("--voice", default="af_sarah", help="Kokoro voice name, e.g. af_sarah.")
    parser.add_argument("--script", type=Path, default=SCRIPT_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    generate_cover_voice(args.script.resolve(), args.output.resolve(), args.voice)
    duration = wav_duration(args.output.resolve())
    print(f"Wrote {args.output.resolve()}")
    print(f"Duration: {duration:.2f}s")


if __name__ == "__main__":
    main()
