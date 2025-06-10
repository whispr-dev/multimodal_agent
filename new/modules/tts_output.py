import subprocess

class TTSEngine:
    def __init__(self, voice="en_US-kristin-medium"):
        self.voice = voice

    def say(self, text):
        try:
            subprocess.run(
                ["piper", "--model", f"voices/{self.voice}.onnx", "--output_file", "temp.wav"],
                input=text.encode("utf-8"), check=True
            )
            subprocess.run(["ffplay", "-nodisp", "-autoexit", "temp.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"[TTS Error] {e}")