"""Backward-compatible interactive launcher."""

from __future__ import annotations

from pathlib import Path

from vid2text.pipeline import TranscriptionOptions, run_transcription


def main() -> int:
    input_path = input("Lutfen video veya ses dosyasinin yolunu girin: ").strip()
    if not input_path:
        print("Hata: Dosya yolu bos birakilamaz.")
        return 1

    try:
        artifact = run_transcription(TranscriptionOptions(input_path=Path(input_path)))
    except Exception as exc:
        print(f"Hata: {exc}")
        return 1

    print(f"Transcription saved to {artifact.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
