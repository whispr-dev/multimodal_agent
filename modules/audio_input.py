import queue
import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
import librosa
from faster_whisper import WhisperModel
from modules.emotion import detect_tone

class AudioInput:
    def __init__(self, model_name="tiny.en"):
        self.audio_queue = queue.Queue()
        self.transcribed_text = ""
        self.mood = "[emotion: unknown]"
        self.model = WhisperModel(model_name, compute_type="int8")
        self.running = False
        self.device_index = None
        self.device_samplerate = 16000

    def _select_working_input_device(self):
        print("\n\n=== AUDIO INPUT DEVICE CHECK ===")
        for i, device in enumerate(sd.query_devices()):
            if device["max_input_channels"] < 1:
                continue
            name = device["name"].lower()
            if any(x in name for x in ["mapper", "loopback", "wdm-ks"]):
                continue
            for rate in [16000, 22050, 44100, 48000]:
                try:
                    sd.check_input_settings(device=i, samplerate=rate)
                    print(f"✅ Device {i} '{device['name']}' supports {rate} Hz")
                    self.device_index = i
                    self.device_samplerate = rate
                    return
                except Exception:
                    pass
        print("❌ No working mic input found — fallback will fail.")
        raise RuntimeError("No suitable microphone input device detected.")

    def _audio_callback(self, indata, frames, time, status):
        self.audio_queue.put(indata.copy())

    def _listen_loop(self):
        buffer = np.zeros((0,), dtype=np.float32)
        chunk_size_target = 32000  # 2 seconds worth of samples at 16kHz

        while self.running:
            chunk = self.audio_queue.get()

            # Flatten and normalize
            if chunk.ndim > 1:
                chunk = chunk[:, 0]
            chunk = chunk.astype(np.float32)
            peak = np.max(np.abs(chunk))
            if peak > 0:
                chunk /= peak

            buffer = np.concatenate((buffer, chunk))

            # If not enough audio yet, keep buffering
            if len(buffer) < chunk_size_target:
                continue

            try:
                print(f"[AudioInput] running transcription on {len(buffer)} samples")
                segments, _ = self.model.transcribe(buffer, beam_size=1)
                segments = list(segments)
                print(f"[AudioInput] segments: {segments}")
                full = " ".join(seg.text for seg in segments)
                print(f"[AudioInput] full: '{full}'")

                if full.strip():
                    print(f"[Audio Transcript] {full.strip()}")
                    self.transcribed_text = full.strip()
                    self.mood = detect_tone(full)
                else:
                    print("[AudioInput] silence or no transcribable audio.")
                    sf.write("last_chunk.wav", buffer, 16000)

            except Exception as e:
                print(f"[AudioInput Error] {e}")
                try:
                    sf.write("error_chunk.wav", buffer, 16000)
                except:
                    pass

            # clear buffer after each attempt
            buffer = np.zeros((0,), dtype=np.float32)

    def start_stream(self):
        self._select_working_input_device()
        print(f"[AudioInput] using device {self.device_index} at {self.device_samplerate} Hz")

        self.running = True
        self.stream = sd.InputStream(
            samplerate=self.device_samplerate,
            channels=1,
            dtype='float32',
            device=self.device_index,
            callback=self._audio_callback
        )
        self.stream.start()
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def stop_stream(self):
        self.running = False
        try:
            self.stream.stop()
        except Exception:
            pass

    def get_transcription(self):
        return self.transcribed_text

    def get_mood(self):
        return self.mood
