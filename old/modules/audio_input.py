import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
import torch

def record_audio(duration=5, sample_rate=16000):
    print(f"[Audio] Recording for {duration} seconds...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, sample_rate, audio)
    return temp_file.name

from transformers import AutoModelForCausalLM, AutoTokenizer

class LLMEngine:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype=torch.float16)
        self.model.eval()

    def respond(self, context, vision_desc, speech, mood):
        prompt = f"[Vision]: {vision_desc}\n[Speech]: {speech}\n[Mood]: {mood}\n[Memory]: {context}\nResponse:"
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        out = self.model.generate(input_ids, max_length=512)
        return self.tokenizer.decode(out[0], skip_special_tokens=True)
