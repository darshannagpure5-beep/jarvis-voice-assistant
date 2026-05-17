import speech_recognition as sr

recognizer = sr.Recognizer()

print("Microphone is ready ....")

with sr.Microphone() as source:
    print("try saying something, listening in process....")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio = recognizer.listen(source, timeout=10)

print("Processing...")

try:
    text = recognizer.recognize_google(audio, language="en-IN")
    print(f"\nyou said: {text}")
except sr.UnknownValueError:
    print("didn't understand say again!")
except sr.RequestError:
    print("Check your internet")
