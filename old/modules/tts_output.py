# modules/tts_output.py
import subprocess
import tempfile
import os

def speak_text(text, model_path, output_path="output.wav"):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as f:
        f.write(text)
        input_path = f.name

    try:
        subprocess.run([
            "C:\\piper\\piper.exe",
            "--model", model_path,
            "--output_file", output_path
        ], stdin=open(input_path, 'r'), check=True)

        subprocess.run([
            "ffplay", "-nodisp", "-autoexit", output_path
        ], check=True)
    finally:
        os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

class TTSEngine:
    def __init__(self):
        # Init your model or TTS engine here
        pass

    def speak_text(self, text):
        print(f"[tts] Speaking: {text}")
        # Actual TTS implementation goes here

    def say(self, text):
        self.speak_text(text)

