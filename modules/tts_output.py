import subprocess
import os

class TTSEngine:
    def __init__(self, voice="en_US-kristin-medium"):
        self.voice = voice
        self.piper_exe = os.path.abspath("bin/piper.exe")

    def say(self, text):
        try:
            model_path = os.path.abspath(f"voices/{self.voice}.onnx")
            subprocess.run(
                [self.piper_exe, "--model", model_path, "--output_file", "temp.wav"],
                input=text.encode("utf-8"), check=True
            )
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "temp.wav"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"[TTS Error] {e}")
