from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
import os
import cv2
from PyQt5.QtGui import QImage, QPixmap

# Load CLIP model & processor (once globally to avoid reloading each time)
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def describe_image(image_path):
    if not os.path.exists(image_path):
        return "[Vision] Error: Image path does not exist."

    image = Image.open(image_path).convert("RGB")
    prompts = [
        "a photo of a dog", "a photo of a cat", "a man", "a woman",
        "a scenic landscape", "a robot", "a cartoon", "a selfie",
        "something sad", "something happy", "an indoor scene", "an outdoor scene"
    ]

    inputs = clip_processor(text=prompts, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    best_match_idx = torch.argmax(probs).item()
    return f"[Vision] Most likely: {prompts[best_match_idx]}"

class VisionModule:
    def describe(self, image_path):
        return describe_image(image_path)

    def get_frame_qpixmap(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return QPixmap()
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(qt_image)
