import tempfile
import unittest
from pathlib import Path

from vid2text.pipeline import resolve_output_path


class PipelineTests(unittest.TestCase):
    def test_resolve_output_path_uses_default_directory(self) -> None:
        output_path = resolve_output_path(
            input_path=Path("sample.mp4"),
            explicit_output=None,
            output_dir=Path("outputs"),
        )
        self.assertEqual(output_path, Path("outputs/sample.txt"))

    def test_resolve_output_path_prefers_explicit_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            explicit_output = Path(temp_dir) / "custom" / "transcript.txt"
            output_path = resolve_output_path(
                input_path=Path("sample.mp4"),
                explicit_output=explicit_output,
                output_dir=Path(temp_dir) / "outputs",
            )
            self.assertEqual(output_path, explicit_output.resolve())


if __name__ == "__main__":
    unittest.main()
