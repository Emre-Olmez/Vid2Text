# Vid2Text

Vid2Text converts Turkish speech from video or audio files into text with optional
timestamps. The original repository was a single Python script; this rebuild keeps
the same core job but ships it as a cleaner application with a modular pipeline,
a drag-and-drop interface, and a reusable CLI.

## What it does

- accepts common video and audio formats,
- extracts audio automatically from video files,
- transcribes the media with OpenAI Whisper,
- writes a `.txt` transcript into the `outputs/` folder, and
- lets you review and download the result from a GUI.

## Project structure

```text
Vid2Text.py              Backward-compatible interactive launcher
app.py                   Gradio UI launcher
vid2text/
  __init__.py
  __main__.py            Package launcher
  cli.py                 Command-line interface
  config.py              Shared defaults and supported file types
  formatters.py          Transcript formatting helpers
  pipeline.py            Media extraction and Whisper orchestration
  ui.py                  Drag-and-drop interface
tests/
  test_formatters.py
  test_pipeline.py
requirements.txt
pyproject.toml
```

## Installation

1. Create and activate a virtual environment.
2. Install the project dependencies.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`moviepy` requires FFmpeg to be available on the machine. `openai-whisper` will
download the selected model the first time it is used.

## Running the app

Start the drag-and-drop interface:

```powershell
python app.py
```

Or launch the package directly:

```powershell
python -m vid2text
```

The interface supports drag and drop, model selection, language override, and
transcript download after processing.

## CLI usage

```powershell
python -m vid2text.cli .\ornek-video.mp4 --model base --language tr
```

Optional arguments:

- `-o, --output` to choose a custom transcript path
- `--no-timestamps` to write plain text only
- `--model` to switch Whisper model size
- `--language` to override the default `tr` language code

## Compatibility launcher

If you want the old prompt-driven behavior, run:

```powershell
python Vid2Text.py
```

## Verification

The lightweight verification that does not require Whisper or Gradio runtime
dependencies can be run with:

```powershell
python -m unittest discover -s tests -v
```
