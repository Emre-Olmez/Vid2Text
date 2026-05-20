"""Gradio user interface for Vid2Text."""

from __future__ import annotations

from pathlib import Path

import gradio as gr

from .config import DEFAULT_LANGUAGE, DEFAULT_MODEL, SUPPORTED_EXTENSIONS, WHISPER_MODELS
from .pipeline import TranscriptionOptions, run_transcription

APP_CSS = """
:root {
    --surface: #f5efe6;
    --surface-strong: #fffaf4;
    --ink: #1f2933;
    --accent: #c26d3b;
    --accent-strong: #8f3f1f;
    --line: rgba(31, 41, 51, 0.12);
}

body {
    background:
        radial-gradient(circle at top left, rgba(194, 109, 59, 0.20), transparent 32%),
        linear-gradient(135deg, #f7f0e5 0%, #efe3d2 100%);
}

.app-shell {
    max-width: 1180px;
    margin: 0 auto;
    padding: 18px 0 32px;
}

.hero {
    background: linear-gradient(135deg, rgba(31, 41, 51, 0.96), rgba(64, 32, 20, 0.94));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 28px;
    padding: 28px;
    color: #fff8f1;
    box-shadow: 0 24px 60px rgba(31, 41, 51, 0.22);
}

.hero h1 {
    margin: 0;
    font-size: 2.4rem;
}

.hero p {
    margin: 12px 0 0;
    max-width: 760px;
    line-height: 1.6;
}

.info-strip {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-top: 18px;
}

.info-card {
    background: rgba(255, 248, 241, 0.08);
    border: 1px solid rgba(255, 248, 241, 0.15);
    border-radius: 20px;
    padding: 14px 16px;
}

.panel {
    background: rgba(255, 250, 244, 0.92);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 18px;
    box-shadow: 0 16px 36px rgba(31, 41, 51, 0.08);
}

.panel h3 {
    margin-top: 0;
    color: var(--ink);
}

.supported-types {
    color: #52606d;
    font-size: 0.95rem;
    line-height: 1.5;
}

.status-box {
    min-height: 96px;
}
"""

READY_MESSAGE = "Hazir. Bir dosya biraktiginizda transkripsiyon burada gorunecek."


def transcribe_uploaded_file(
    file_path: str | None,
    model_name: str,
    language: str,
    include_timestamps: bool,
) -> tuple[str, str, str]:
    """Handle the uploaded media file and return the UI outputs."""

    if not file_path:
        raise gr.Error("Lutfen once bir video veya ses dosyasi secin.")

    try:
        artifact = run_transcription(
            TranscriptionOptions(
                input_path=Path(file_path),
                model_name=model_name,
                language=language.strip() or DEFAULT_LANGUAGE,
                include_timestamps=include_timestamps,
            )
        )
    except Exception as exc:
        raise gr.Error(f"Transkripsiyon basarisiz oldu: {exc}") from exc

    status_message = (
        "Transkripsiyon tamamlandi.\n\n"
        f"Cikti dosyasi: `{artifact.output_path.name}`\n\n"
        f"Kayit konumu: `{artifact.output_path}`"
    )
    return status_message, artifact.transcript_text, str(artifact.output_path)


def reset_form() -> tuple[None, str, bool, str, str, None]:
    """Restore the UI to its default state."""

    return None, DEFAULT_LANGUAGE, True, READY_MESSAGE, "", None


def build_interface() -> gr.Blocks:
    """Construct the drag-and-drop application UI."""

    supported_types = ", ".join(sorted(SUPPORTED_EXTENSIONS))

    with gr.Blocks(
        title="Vid2Text",
        theme=gr.themes.Soft(
            primary_hue="orange",
            secondary_hue="amber",
            neutral_hue="stone",
        ),
        css=APP_CSS,
    ) as demo:
        with gr.Column(elem_classes=["app-shell"]):
            gr.HTML(
                """
                <section class="hero">
                    <h1>Vid2Text</h1>
                    <p>
                        Video veya ses dosyanizi surukleyip birakin, Whisper ile
                        otomatik olarak metne cevirelim. Orijinal projenin ayni
                        islevini korur, ama artik daha duzenli, gorunur ve
                        kullanimi rahat bir arayuzle gelir.
                    </p>
                    <div class="info-strip">
                        <div class="info-card"><strong>1.</strong> Dosya yukle</div>
                        <div class="info-card"><strong>2.</strong> Model ve dil sec</div>
                        <div class="info-card"><strong>3.</strong> Metni indir</div>
                    </div>
                </section>
                """
            )

            with gr.Row(equal_height=True):
                with gr.Column(scale=5, elem_classes=["panel"]):
                    gr.HTML("<h3>Kaynak Dosya</h3>")
                    file_input = gr.File(
                        label="Dosyayi surukleyip birakin veya secin",
                        type="filepath",
                        file_types=sorted(SUPPORTED_EXTENSIONS),
                    )
                    gr.HTML(
                        f"<div class='supported-types'>Desteklenen turler: {supported_types}</div>"
                    )

                    with gr.Row():
                        model_input = gr.Dropdown(
                            label="Whisper modeli",
                            choices=list(WHISPER_MODELS),
                            value=DEFAULT_MODEL,
                        )
                        language_input = gr.Textbox(
                            label="Dil kodu",
                            value=DEFAULT_LANGUAGE,
                            placeholder="tr",
                        )

                    include_timestamps = gr.Checkbox(
                        label="Zaman damgalarini ekle",
                        value=True,
                    )

                    with gr.Row():
                        transcribe_button = gr.Button(
                            "Transkripsiyonu Baslat",
                            variant="primary",
                        )
                        clear_button = gr.Button("Formu Temizle")

                with gr.Column(scale=6, elem_classes=["panel"]):
                    gr.HTML("<h3>Sonuc</h3>")
                    status_output = gr.Markdown(
                        value=READY_MESSAGE,
                        elem_classes=["status-box"],
                    )
                    transcript_output = gr.Textbox(
                        label="Transkript",
                        lines=18,
                        max_lines=24,
                        show_copy_button=True,
                    )
                    download_output = gr.File(label="Indirilebilir cikti")

            transcribe_button.click(
                fn=transcribe_uploaded_file,
                inputs=[file_input, model_input, language_input, include_timestamps],
                outputs=[status_output, transcript_output, download_output],
            )

            clear_button.click(
                fn=reset_form,
                outputs=[
                    file_input,
                    language_input,
                    include_timestamps,
                    status_output,
                    transcript_output,
                    download_output,
                ],
            )

    return demo


def launch() -> None:
    """Launch the local Gradio interface."""

    build_interface().launch()
