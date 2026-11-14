
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from movimientos import registrar_movimiento, consultar_resumen


# Cargar la API Key de Gemini
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Falta GEMINI_API_KEY en el archivo .env")

client = genai.Client(api_key=API_KEY)


# Instrucciones del agente
system_instruction = """
Sos FinanzasBot, un asistente de finanzas personales.

Respondé en español argentino, de manera clara y amigable.

Tu función es ayudar al usuario a:
- Registrar gastos.
- Registrar ingresos.
- Consultar el resumen de sus finanzas.

Reglas:
- No inventes movimientos ni montos.
- Usá registrar_movimiento para guardar gastos e ingresos.
- Usá consultar_resumen para obtener los totales reales.
- No afirmes que registraste algo si la herramienta no se ejecutó.
- Si faltan datos importantes, preguntá antes de registrar.
- Si el usuario pregunta algo ajeno a las finanzas,
  explicá amablemente que sos un asistente financiero.
"""


# Crear una conversación con Gemini
def crear_chat(historial=None):
    return client.chats.create(
        model="gemini-3.5-flash",
        history=historial or [],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[
                registrar_movimiento,
                consultar_resumen
            ]
        )
    )
