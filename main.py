import time
from modules import vision, audio_input, emotion, memory, llm_core, tts_output

def main():
    print("[fren-agent] starting up...")
    mem = memory.MemoryEngine()
    llm = llm_core.LLMEngine()
    tts = tts_output.TTSEngine()
    vision_module = vision.VisionModule()
    audio_module = audio_input.AudioInput()

    audio_module.start_stream()

    try:
        while True:
            frame_data = vision_module.get_frame()
            scene_desc = vision_module.describe_frame(frame_data)
            speech_text = audio_module.get_transcription()
            mood = audio_module.get_mood()

            context = mem.query_recent(scene_desc + " " + speech_text + " " + mood)
            reply = llm.respond(context, scene_desc, speech_text, mood)
            tts.say(reply)
            mem.store(scene_desc, speech_text, mood, reply)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\\n[fren-agent] shutting down...")
        audio_module.stop_stream()
        mem.save()

    if frame_data is None or speech_text.strip() == "":
        continue

# if __name__ == "__main__":
#     main()