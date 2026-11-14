from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from movimientos import registrar_movimiento, consultar_resumen
from historial import guardar_historial, cargar_historial

# 1. Configurar la API de Gemini
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("No se encontró GEMINI_API_KEY en el archivo .env")

client = genai.Client(api_key=api_key)


# 2. Instrucciones del asistente
system_instruction = """
Sos FinanzasBot, un asistente de finanzas personales.
Hablás en español argentino, con un tono amigable y claro.

Tu especialidad es registrar ingresos, gastos y consultar
el estado de las finanzas personales del usuario.

Para registrar movimientos:
- Identificá el tipo, monto y descripción.
- Inferí la categoría cuando no esté indicada.
- No exijas el medio de pago.
- Pedí aclaraciones solo cuando falten datos esenciales.
- No inventes movimientos.
- Cuando haya datos suficientes, ejecutá registrar_movimiento
  directamente, sin pedir confirmaciones innecesarias.
- Nunca afirmes que guardaste un movimiento hasta que
  la herramienta confirme que se realizó correctamente.

Para consultar saldos y totales:
- Utilizá siempre la herramienta consultar_resumen.
- No inventes importes ni saldos.

Si recibís preguntas fuera del dominio financiero,
rechazalas amablemente y redirigí la conversación
hacia las finanzas personales.
"""


# 3. Función para crear una conversación
def crear_chat(historial=None):
    return client.chats.create(
        model="gemini-3.5-flash",
        history=historial or [],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[registrar_movimiento, consultar_resumen],
        ),
    )


# 4. Crear el chat inicial
historial_anterior = cargar_historial()
chat = crear_chat(historial_anterior)

print("=== FINANZAS BOT ===")
print("Comandos disponibles: /salir y /limpiar")
""

# 5. Bucle principal
while True:

    mensaje = input("\n¿En qué te puedo ayudar hoy? ").strip()

    # Evitar mensajes vacíos
    if not mensaje:
        continue

    # Comando para salir
    if mensaje.lower() == "/salir":
        print("Finanzas Bot: ¡Hasta luego!")
        break

    # Comando para limpiar la conversación
    if mensaje.lower() == "/limpiar":
        chat = crear_chat()
        guardar_historial(chat)

        print("Finanzas Bot: Conversación reiniciada.")
        continue

    # Enviar mensaje a Gemini
    try:
        respuesta = chat.send_message(mensaje)
        guardar_historial(chat)

        if respuesta.text:
            print("Finanzas Bot:", respuesta.text)
        else:
            print("Finanzas Bot: No pude generar una respuesta. Intentá nuevamente.")

    except Exception as error:
        if "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error):
            print(
                "Finanzas Bot: Alcanzamos el límite de solicitudes "
                "de Gemini. Intentá más tarde."
            )
        else:
            print("Finanzas Bot: Ocurrió un error al procesar tu mensaje.")
            print("Detalle técnico:", error)
