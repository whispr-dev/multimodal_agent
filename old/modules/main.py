import time
from modules import vision, audio_input, emotion, memory, llm_core, tts_output

def main():
    print("[fren-agent] starting up...")
    mem = memory.MemoryEngine()
    llm = llm_core.LLMEngine()
    tts = tts_output.TTSEngine()

    print("[fren-agent] loading input modules...")
    vision.start_capture()
    audio_input.start_audio_stream()

def closeEvent(self, event):
    self.memory.save()
    self.log("[FrenAgent] Memory saved.")
    event.accept()

    try:
        while True:
            frame_data = vision.capture_frame()
            scene_desc = vision.describe_frame(frame_data)
            speech_text = audio_input.transcribe()
            mood = emotion.detect_tone(speech_text)

            context = mem.query_recent(scene_desc + " " + speech_text + " " + mood)
            reply = llm.respond(context, scene_desc, speech_text, mood)
            tts.say(reply)
            mem.store(scene_desc, speech_text, mood, reply)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[fren-agent] shutting down...")

if __name__ == "__main__":
    main()