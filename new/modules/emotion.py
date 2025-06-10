def detect_tone(text=""):
    lowered = text.lower()
    if any(word in lowered for word in ["hate", "angry", "sucks"]):
        return "[emotion: angry]"
    elif any(word in lowered for word in ["love", "great", "awesome"]):
        return "[emotion: happy]"
    elif any(word in lowered for word in ["scared", "worried", "afraid"]):
        return "[emotion: fearful]"
    elif any(word in lowered for word in ["meh", "ok", "whatever"]):
        return "[emotion: neutral]"
    elif any(word in lowered for word in ["cry", "sad", "lonely"]):
        return "[emotion: sad]"
    return "[emotion: calm]"