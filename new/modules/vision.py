import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

class VisionModule:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def describe_frame(self, frame):
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        inputs = self.processor(image, return_tensors="pt")
        out = self.model.generate(**inputs)
        return self.processor.decode(out[0], skip_special_tokens=True)