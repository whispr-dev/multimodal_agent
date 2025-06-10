import queue
import threading
import sounddevice as sd
from faster_whisper import WhisperModel
from modules.emotion import detect_tone

class AudioInput:
    def __init__(self, model_name="base.en"):
        self.audio_queue = queue.Queue()
        self.transcribed_text = ""
        self.mood = "[emotion: unknown]"
        self.model = WhisperModel(model_name, compute_type="int8")
        self.running = False

    def _audio_callback(self, indata, frames, time, status):
        self.audio_queue.put(indata.copy())

    def _listen_loop(self):
        while self.running:
            audio_chunk = self.audio_queue.get()
            segments, _ = self.model.transcribe(audio_chunk[:, 0], beam_size=1)
            full = " ".join([seg.text for seg in segments])
            if full.strip():
                self.transcribed_text = full.strip()
                self.mood = detect_tone(full)

    def start_stream(self):
        self.running = True
        self.stream = sd.InputStream(samplerate=16000, channels=1, callback=self._audio_callback)
        self.stream.start()
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def stop_stream(self):
        self.running = False
        self.stream.stop()

    def get_transcription(self):
        return self.transcribed_text

    def get_mood(self):
        return self.mood