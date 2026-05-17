import pyttsx3
import threading
import os

_lock = threading.Lock()


def speak(text: str):
    print(f"🔊 Assistant: {text}")
    if os.environ.get("TTS_MUTED") == "1":
        return

    def _run():
        with _lock:
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 175)
                engine.setProperty("volume", 1.0)
                voices = engine.getProperty("voices")
                for voice in voices:
                    if "zira" in voice.name.lower() or "female" in voice.name.lower():
                        engine.setProperty("voice", voice.id)
                        break
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception:
                pass
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join(timeout=15)
