"""
🤖 Jarvis — Voice AI Personal Assistant
----------------------------------------
Voice loop: You speak → STT → Claude → TTS → You hear

Wake word: "hey jarvis" (optional, can speak directly)
Exit: say "goodbye" or "exit" or Ctrl+C
"""

from reminders import parse_and_set_reminder, run_scheduler, set_speak
from llm import chat, clear_memory
from tts import speak
from stt import listen
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Check API key before starting
if not os.getenv("GROQ_API_KEY"):
    print("❌ ERROR: Groq_API_KEY not found in .env file!")
    print("   Create a .env file with: Groq_API_KEY=your_key_here")
    sys.exit(1)


# Pass speak function to reminders module
set_speak(speak)

# Exit words — saying any of these stops the assistant
EXIT_PHRASES = {"goodbye", "bye", "exit", "quit", "stop", "shut down"}

# Words to clear memory
CLEAR_PHRASES = {"clear memory", "forget everything", "reset", "start over"}


def main():
    print("=" * 50)
    print("🤖  JARVIS — Voice AI Assistant")
    print("=" * 50)
    print("📌  Say 'goodbye' to stop.")
    print("📌  Say 'clear memory' to reset conversation.")
    print("📌  Say 'remind me in X minutes to [task]' for reminders.")
    print("=" * 50)

    # Start background reminder scheduler
    run_scheduler()

    # Greet the user
    speak("Hello! I'm Jarvis, your personal AI assistant. How can I help you today?")

    while True:
        try:
            # Step 1: Listen
            user_input = listen()

            if not user_input:
                continue  # Nothing heard, loop again

            user_lower = user_input.lower().strip()

            # Step 2: Check for exit command
            if any(phrase in user_lower for phrase in EXIT_PHRASES):
                speak("Goodbye! Have a great day!")
                break

            # Step 3: Check for memory clear command
            if any(phrase in user_lower for phrase in CLEAR_PHRASES):
                clear_memory()
                speak("Memory cleared. We can start fresh now.")
                continue

            # Step 4: Check for reminder intent (before sending to Claude)
            reminder_response = parse_and_set_reminder(user_input)
            if reminder_response:
                speak(reminder_response)
                continue

            # Step 5: Send to Claude and get reply
            print("🧠 Thinking...")
            reply = chat(user_input)

            # Step 6: Speak the reply
            speak(reply)

        except KeyboardInterrupt:
            print("\n👋 Stopped by user.")
            speak("Shutting down. Goodbye!")
            break
        except Exception as e:
            print(f"⚠️  Unexpected error: {e}")
            speak("Sorry, something went wrong. Please try again.")


if __name__ == "__main__":
    main()
