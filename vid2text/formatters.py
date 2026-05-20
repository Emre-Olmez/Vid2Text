"""Formatting helpers for transcript output."""

from __future__ import annotations

from typing import Iterable


def format_timestamp(seconds: float) -> str:
    """Return a human-readable [MM:SS] timestamp."""

    total_seconds = max(int(seconds), 0)
    minutes, remaining_seconds = divmod(total_seconds, 60)
    return f"[{minutes:02}:{remaining_seconds:02}]"


def build_transcript_text(segments: Iterable[dict], include_timestamps: bool = True) -> str:
    """Build the plain-text transcript from Whisper segments."""

    lines = []
    for segment in segments:
        text = str(segment.get("text", "")).strip()
        if not text:
            continue

        if include_timestamps:
            lines.append(f"{format_timestamp(float(segment.get('start', 0.0)))} {text}")
        else:
            lines.append(text)

    return "\n".join(lines)
