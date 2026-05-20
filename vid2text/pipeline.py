"""Core transcription pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class TranscriptionOptions:
    input_path: Path
    output_path: Path
    model_name: str
    language: str
    include_timestamps: bool = True


@dataclass(slots=True)
class TranscriptionArtifact:
    transcript_text: str
    output_path: Path
