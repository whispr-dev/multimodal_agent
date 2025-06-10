from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLMEngine:
    def __init__(self, model_name="microsoft/phi-2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
        self.model.eval()

    def respond(self, context, vision_desc, speech, mood):
        prompt = (
            f"[Vision]: {vision_desc}\\n"
            f"[Speech]: {speech}\\n"
            f"[Mood]: {mood}\\n"
            f"[Memory]: {context}\\n"
            "Response:"
        )
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        out = self.model.generate(input_ids, max_length=512)
        return self.tokenizer.decode(out[0], skip_special_tokens=True)