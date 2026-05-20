"""Core transcription pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import (
    DEFAULT_LANGUAGE,
    DEFAULT_MODEL,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TEMP_DIR,
    SUPPORTED_EXTENSIONS,
    VIDEO_EXTENSIONS,
)
from .formatters import build_transcript_text


@dataclass(slots=True)
class TranscriptionOptions:
    input_path: Path
    output_path: Path | None = None
    model_name: str = DEFAULT_MODEL
    language: str = DEFAULT_LANGUAGE
    include_timestamps: bool = True
    output_dir: Path = DEFAULT_OUTPUT_DIR
    temp_dir: Path = DEFAULT_TEMP_DIR


@dataclass(slots=True)
class TranscriptionArtifact:
    transcript_text: str
    output_path: Path


def run_transcription(options: TranscriptionOptions) -> TranscriptionArtifact:
    """Transcribe the supplied media file and write the transcript to disk."""

    input_path = options.input_path.expanduser().resolve()
    validate_input_path(input_path)

    output_dir = options.output_dir.expanduser().resolve()
    temp_dir = options.temp_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    output_path = resolve_output_path(input_path, options.output_path, output_dir)
    audio_path, cleanup_required = prepare_audio_source(input_path, temp_dir)

    try:
        segments = transcribe_audio(
            audio_path=audio_path,
            model_name=options.model_name,
            language=options.language,
        )
        transcript_text = build_transcript_text(
            segments,
            include_timestamps=options.include_timestamps,
        )
        write_transcript(transcript_text, output_path)
        return TranscriptionArtifact(transcript_text=transcript_text, output_path=output_path)
    finally:
        if cleanup_required and audio_path.exists():
            audio_path.unlink()


def validate_input_path(input_path: Path) -> None:
    """Ensure the input exists and uses a supported media extension."""

    if not input_path.exists():
        raise FileNotFoundError(f"Input file was not found: {input_path}")

    if input_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Supported extensions: "
            + ", ".join(sorted(SUPPORTED_EXTENSIONS))
        )


def resolve_output_path(input_path: Path, explicit_output: Path | None, output_dir: Path) -> Path:
    """Resolve the final transcript path."""

    if explicit_output is not None:
        output_path = explicit_output.expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path

    return output_dir / f"{input_path.stem}.txt"


def prepare_audio_source(input_path: Path, temp_dir: Path) -> tuple[Path, bool]:
    """Return an audio file path, extracting audio first when the input is a video."""

    if input_path.suffix.lower() in VIDEO_EXTENSIONS:
        return extract_audio(input_path, temp_dir), True

    return input_path, False


def extract_audio(video_path: Path, temp_dir: Path) -> Path:
    """Extract PCM audio from the source video into the temporary workspace."""

    import moviepy.editor as moviepy

    audio_path = temp_dir / f"{video_path.stem}.wav"
    clip = moviepy.VideoFileClip(str(video_path))

    try:
        if clip.audio is None:
            raise ValueError(f"No audio stream found in video: {video_path.name}")

        clip.audio.write_audiofile(
            str(audio_path),
            codec="pcm_s16le",
            logger=None,
        )
        return audio_path
    finally:
        clip.close()


def transcribe_audio(audio_path: Path, model_name: str, language: str) -> list[dict]:
    """Run Whisper transcription and return the segment list."""

    import whisper

    model = whisper.load_model(model_name)
    result = model.transcribe(
        str(audio_path),
        language=language,
        word_timestamps=True,
    )
    return list(result.get("segments", []))


def write_transcript(transcript_text: str, output_path: Path) -> None:
    """Persist the transcript to disk."""

    output_path.write_text(transcript_text, encoding="utf-8")
