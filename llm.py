import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are Jarvis, a smart and friendly personal AI voice assistant.
Keep responses SHORT, 1-3 sentences. No markdown, no bullets, no emojis.
Sound natural like a helpful friend. Always be concise."""

history = [{"role": "system", "content": SYSTEM_PROMPT}]


def chat(user_message):
    global history
    history.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=history,
        max_tokens=150
    )
    reply = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": reply})
    return reply


def clear_memory():
    global history
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Memory cleared.")
