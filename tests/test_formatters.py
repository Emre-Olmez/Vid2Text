import unittest

from vid2text.formatters import build_transcript_text, format_timestamp


class FormatterTests(unittest.TestCase):
    def test_format_timestamp_rounds_down_to_whole_seconds(self) -> None:
        self.assertEqual(format_timestamp(125.9), "[02:05]")

    def test_build_transcript_text_with_timestamps(self) -> None:
        transcript = build_transcript_text(
            [
                {"start": 0, "text": "Merhaba"},
                {"start": 65, "text": "dunya"},
            ]
        )
        self.assertEqual(transcript, "[00:00] Merhaba\n[01:05] dunya")

    def test_build_transcript_text_without_timestamps(self) -> None:
        transcript = build_transcript_text(
            [
                {"start": 0, "text": "Merhaba"},
                {"start": 65, "text": "dunya"},
            ],
            include_timestamps=False,
        )
        self.assertEqual(transcript, "Merhaba\ndunya")


if __name__ == "__main__":
    unittest.main()
