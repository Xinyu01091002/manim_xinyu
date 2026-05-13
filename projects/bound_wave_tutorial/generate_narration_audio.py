from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro


ROOT = Path(__file__).resolve().parent
SCRIPT_PATH = ROOT / "narration" / "draft_page_scripts.md"
AUDIO_DIR = ROOT / "narration" / "audio"
MODEL_PATH = ROOT / "narration" / "models" / "kokoro-v1.0.onnx"
VOICES_PATH = ROOT / "narration" / "models" / "voices-v1.0.bin"
PHD_MODEL_PATH = ROOT.parent / "phd_confirmation" / "narration" / "models" / "kokoro-v1.0.onnx"
PHD_VOICES_PATH = ROOT.parent / "phd_confirmation" / "narration" / "models" / "voices-v1.0.bin"

PAGE_HEADING = re.compile(r"^(?:##|###) Page (?P<number>\d+) - (?P<title>.+)$")


@dataclass(frozen=True)
class NarrationPage:
    number: int
    title: str
    text: str

    @property
    def audio_name(self) -> str:
        return f"{self.number:03d}.wav"

    @property
    def meta_name(self) -> str:
        return f"{self.number:03d}.json"


def parse_pages(path: Path) -> list[NarrationPage]:
    pages: list[NarrationPage] = []
    current_number: int | None = None
    current_title = ""
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_number, current_title, current_lines
        if current_number is None:
            return
        text = "\n".join(line for line in current_lines).strip()
        if not text:
            raise ValueError(f"Missing narration text for page {current_number}: {current_title}")
        pages.append(NarrationPage(current_number, current_title, text))
        current_number = None
        current_title = ""
        current_lines = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = PAGE_HEADING.match(raw_line.strip())
        if match:
            flush()
            current_number = int(match.group("number"))
            current_title = match.group("title")
            continue
        if current_number is not None:
            if raw_line.startswith("#"):
                continue
            current_lines.append(raw_line)

    flush()
    expected = list(range(len(pages)))
    actual = [page.number for page in pages]
    if actual != expected:
        raise ValueError(f"Expected contiguous page numbers {expected[:3]}...{expected[-3:]}, got {actual[:3]}...{actual[-3:]}")
    return pages


def text_hash(text: str, voice: str, speed: float) -> str:
    payload = json.dumps({"text": text, "voice": voice, "speed": speed, "speech_normalizer": 1}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def normalize_math_for_speech(text: str) -> str:
    replacements = {
        r"\eta": "eta",
        r"\theta": "theta",
        r"\omega": "omega",
        r"\kappa": "kappa",
        r"\boldsymbol": "",
        r"\rm": "",
        r"\widehat": "",
        r"\approx": " approximately ",
        r"\left": "",
        r"\right": "",
        r"\frac": " fraction ",
        r"\sum": " sum ",
        r"\mathcal": "",
        r"\{": " ",
        r"\}": " ",
    }
    spoken = text
    spoken = re.sub(r"`([^`]+)`", r"\1", spoken)
    spoken = re.sub(r"\\\((.*?)\\\)", lambda match: math_span_to_words(match.group(1)), spoken)
    spoken = re.sub(r"\\\[(.*?)\\\]", lambda match: math_span_to_words(match.group(1)), spoken, flags=re.DOTALL)
    for old, new in replacements.items():
        spoken = spoken.replace(old, new)
    spoken = re.sub(r"([A-Za-z])_([A-Za-z0-9]+)", r"\1 \2", spoken)
    spoken = re.sub(r"([A-Za-z])\^2", r"\1 squared", spoken)
    spoken = re.sub(r"([A-Za-z])\^3", r"\1 cubed", spoken)
    spoken = re.sub(r"([A-Za-z])\^5", r"\1 to the fifth", spoken)
    spoken = spoken.replace("_", " ")
    spoken = spoken.replace("^", " to the ")
    spoken = spoken.replace("{", " ").replace("}", " ")
    spoken = spoken.replace("\\", " ")
    spoken = re.sub(r"\s+", " ", spoken).strip()
    return spoken


def math_span_to_words(span: str) -> str:
    specific = {
        r"k_m": "k m",
        r"k_n": "k n",
        r"\theta_m+\theta_n": "theta m plus theta n",
        r"k_m+k_n": "k m plus k n",
        r"N_c^2": "N c squared",
        r"N_c^3": "N c cubed",
        r"N_c^5": "N c to the fifth",
        r"G(k_m,k_n)": "the full two-variable kernel",
        r"G_2(k)": "G two of k",
        r"G_2(k_m)": "G two at k m",
        r"G_2(k_n)": "G two at k n",
        r"\phi_s": "surface potential",
        r"u_s": "horizontal surface velocity",
        r"w_s": "vertical surface velocity",
        r"Q": "Q",
    }
    cleaned = span.strip()
    if cleaned in specific:
        return specific[cleaned]
    cleaned = re.sub(r"\\frac\{1\}\{2\}", "one half", cleaned)
    cleaned = cleaned.replace(r"\left", "").replace(r"\right", "")
    cleaned = cleaned.replace("(", " ").replace(")", " ")
    cleaned = cleaned.replace("[", " ").replace("]", " ")
    cleaned = cleaned.replace(",", " ")
    cleaned = cleaned.replace("+", " plus ")
    cleaned = cleaned.replace("-", " minus ")
    cleaned = re.sub(r"\\[a-zA-Z]+", lambda match: match.group(0).lstrip("\\"), cleaned)
    cleaned = re.sub(r"([A-Za-z])_([A-Za-z0-9]+)", r"\1 \2", cleaned)
    cleaned = re.sub(r"([A-Za-z])\^2", r"\1 squared", cleaned)
    cleaned = re.sub(r"([A-Za-z])\^3", r"\1 cubed", cleaned)
    cleaned = re.sub(r"([A-Za-z])\^5", r"\1 to the fifth", cleaned)
    cleaned = cleaned.replace("_", " ").replace("^", " to the ")
    cleaned = cleaned.replace("{", " ").replace("}", " ")
    return re.sub(r"\s+", " ", cleaned).strip()


def resolve_model_paths() -> tuple[Path, Path]:
    if MODEL_PATH.exists() and VOICES_PATH.exists():
        return MODEL_PATH, VOICES_PATH
    if PHD_MODEL_PATH.exists() and PHD_VOICES_PATH.exists():
        return PHD_MODEL_PATH, PHD_VOICES_PATH
    raise FileNotFoundError(
        "Missing Kokoro model files. Expected narration/models/ here or ../phd_confirmation/narration/models/."
    )


def generate_audio(page: NarrationPage, kokoro: Kokoro, voice: str, speed: float, force: bool) -> bool:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = AUDIO_DIR / page.audio_name
    meta_path = AUDIO_DIR / page.meta_name
    spoken_text = normalize_math_for_speech(page.text)
    digest = text_hash(spoken_text, voice, speed)

    if not force and audio_path.exists() and meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if meta.get("hash") == digest:
                return False
        except json.JSONDecodeError:
            pass

    samples, sample_rate = kokoro.create(spoken_text, voice=voice, speed=speed, lang="en-us")
    sf.write(audio_path, samples, sample_rate)
    meta_path.write_text(
        json.dumps(
            {
                "page": page.number,
                "title": page.title,
                "voice": voice,
                "speed": speed,
                "sample_rate": sample_rate,
                "hash": digest,
                "text": page.text,
                "spoken_text": spoken_text,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate per-page narration audio for the bound wave tutorial slides.")
    parser.add_argument("--voice", default="af_sarah")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Generate only the first N pages for testing.")
    args = parser.parse_args()

    pages = parse_pages(SCRIPT_PATH)
    if args.limit:
        pages = pages[: args.limit]

    model_path, voices_path = resolve_model_paths()
    kokoro = Kokoro(str(model_path), str(voices_path))
    generated = 0
    for page in pages:
        did_generate = generate_audio(page, kokoro, args.voice, args.speed, args.force)
        generated += int(did_generate)
        status = "generated" if did_generate else "cached"
        print(f"{status}: {page.number:03d} {page.title}")

    print(f"Done. Pages={len(pages)} generated={generated} cached={len(pages) - generated}")


if __name__ == "__main__":
    main()
