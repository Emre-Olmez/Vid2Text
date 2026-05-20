# Vid2Text

Vid2Text converts Turkish speech from video or audio files into timestamped text.

The original repository contained a single Python script. This rebuild keeps the
same goal while reorganizing the project into a maintainable application with:

- a modular transcription pipeline,
- a drag-and-drop interface,
- a command-line entry point, and
- cleaner output handling.

## Planned structure

```text
vid2text/
  cli.py
  config.py
  formatters.py
  pipeline.py
  ui.py
app.py
Vid2Text.py
requirements.txt
```

## Status

The professional rebuild is in progress on feature branches. See the final
merged branch history for the completed implementation.
