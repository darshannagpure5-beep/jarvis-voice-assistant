import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

def listen():
    """
    Records from mic and returns text.
    Returns None if nothing was heard.
    """
    with sr.Microphone() as source:
        print("\n🎙️  Listening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("⏱️  No speech detected.")
            return None

    print("⚙️  Processing speech...")

    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"🗣️  You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❓ Couldn't understand. Try again.")
        return None
    except sr.RequestError:
        print("❌ Internet error. Check connection.")
        return None
