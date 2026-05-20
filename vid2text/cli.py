"""Command-line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import DEFAULT_LANGUAGE, DEFAULT_MODEL, WHISPER_MODELS
from .pipeline import TranscriptionOptions, run_transcription


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert video or audio files into timestamped Turkish text.",
    )
    parser.add_argument("input_path", help="Path to the source media file.")
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output transcript path. Defaults to outputs/<file-name>.txt.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=WHISPER_MODELS,
        help="Whisper model to use.",
    )
    parser.add_argument(
        "--language",
        default=DEFAULT_LANGUAGE,
        help="Whisper language code. Defaults to Turkish (tr).",
    )
    parser.add_argument(
        "--no-timestamps",
        action="store_true",
        help="Write plain text without [MM:SS] timestamps.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    options = TranscriptionOptions(
        input_path=Path(args.input_path),
        output_path=Path(args.output) if args.output else None,
        model_name=args.model,
        language=args.language,
        include_timestamps=not args.no_timestamps,
    )

    try:
        artifact = run_transcription(options)
    except Exception as exc:
        print(f"Transcription failed: {exc}", file=sys.stderr)
        return 1

    print(f"Transcript saved to {artifact.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
