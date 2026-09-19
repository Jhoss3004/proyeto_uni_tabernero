from pathlib import Path
import os

from dotenv import load_dotenv

from google import genai
from google.genai import types

BASE = Path(__file__).resolve().parent.parent
load_dotenv(BASE / ".env")

if not os.getenv("GEMINI_API_KEY"):
    raise SystemExit("Falta GEMINI_API_KEY en el archivo .env")

cliente = genai.Client()

def crear_chat():

    MODELO = "gemini-3.6-flash"
    INSTRUCCIONES = (
        "Eres Beatrice , la tabernera de una posada medieval. "
        "Hablas en español con tono cálido, amable, acojedor y antiguo medieval (vos, os, noble, aventurero). "
        "Responde breve, maximo 2 o 4 frases dando la bienvenida, presentandote hacia los clientes. "
        "Nunca rompes el personaje ni digas que eres una IA."
    )

    chat = cliente.chats.create(
        model=MODELO,
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCCIONES,
            temperature=0.9,
            thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.MINIMAL),
        ),
    )
    return chat