import threading

import pyttsx3

from google.genai import errors

class TabernaModelo:
    BIENVENIDA = "Bienvenido a mi taberna. ¿En qué os puedo ayudar, noble aventurero?"
    PENSANDO = "La tabernera juega con su cabello mientras piensa...."

    def __init__(self, chat):
        self.chat = chat
        self._detener_voz = threading.Event()

    def preguntar(self, texto):
        try:
            respuesta = self.chat.send_message(texto)
            return respuesta.text or "La tabernera os observa en silencio..."
        except errors.APIError as e:
            return f"(Error {e.code}: {e.message})"
        except Exception as e:
            return f"(Error de conexion: {e})"

    def hablar(self, texto):
        self._detener_voz.clear()
        motor = pyttsx3.Engine()
        motor.setProperty("rate", 200)

        def on_word(name, location, length):
            if self._detener_voz.is_set():
                motor.stop()

        motor.connect("started-word", on_word)
        motor.say(texto)
        motor.runAndWait()

    def detener_voz(self):
        self._detener_voz.set()