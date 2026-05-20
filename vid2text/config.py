"""Application configuration values."""

from pathlib import Path

DEFAULT_MODEL = "base"
DEFAULT_LANGUAGE = "tr"
DEFAULT_OUTPUT_DIR = Path("outputs")
DEFAULT_TEMP_DIR = Path("temp")

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
    ".m4v",
}

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
}

SUPPORTED_EXTENSIONS = VIDEO_EXTENSIONS | AUDIO_EXTENSIONS
WHISPER_MODELS = ("tiny", "base", "small", "medium", "large")
