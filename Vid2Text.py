import moviepy.editor as mp
import whisper
import os

def extract_audio(video_path, audio_path="temp_audio.wav"):
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        return audio_path
    except Exception as e:
        print(f"Hata: Ses çıkarılırken bir sorun oluştu: {e}")
        return None

def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="tr", word_timestamps=True)
        return result["segments"]
    except Exception as e:
        print(f"Hata: Ses transkripsiyonu sırasında bir sorun oluştu: {e}")
        return None

def save_transcription(segments, output_file="transcription.txt"):
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for segment in segments:
                start_time = segment["start"]
                minutes = int(start_time // 60)
                seconds = int(start_time % 60)
                timestamp = f"[{minutes:02}:{seconds:02}]"
                text = segment["text"]
                f.write(f"{timestamp} {text}\n")
        print(f"Transcription saved to {output_file}")
    except Exception as e:
        print(f"Hata: Transkripsiyon dosyası kaydedilirken bir sorun oluştu: {e}")

def main():
    video_path = input("Lütfen video dosyasının adını girin (örn: video.mp4): ").strip()
    if not os.path.exists(video_path):
        print("Hata: Belirtilen dosya bulunamadı.")
        return
    
    audio_path = extract_audio(video_path)
    if audio_path is None:
        return
    
    try:
        segments = transcribe_audio(audio_path)
        if segments is not None:
            save_transcription(segments)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    main()