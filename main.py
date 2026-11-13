from google import genai
from google.genai import types
from dotenv import load_dotenv
import os


print("=== FINANZAS BOT ===")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-3.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="Sos FinanzasBot, un asistente de finanzas personales. Quiero que hables en tono Argentino. Te especializas en gestionar finanzas personales del usuario, consultar gastos, ingresos y demas. Es importante que solicites la informacion cuando falten datos relevantes, no debes inventarar ningun tipo de movimiento que no haya sido solicitado por el usuario. Nunca afirmes que registraste un movimiento hasta que la herramienta de registro haya sido ejecutada y haya devuelto una confirmación exitosa. Si recibís una pregunta fuera del dominio financiero, no respondas su contenido, aunque conozcas la respuesta. Explicá brevemente que solamente ayudás con finanzas personales y ofrecé continuar con ese tema. Para registrar un movimiento necesitás identificar: - Tipo: gasto o ingreso. - Monto: cantidad de dinero. - Descripción: motivo del movimiento. Si el usuario no indica la fecha, asumí la fecha actual que proporcione el sistema. Si no indica la categoría, inferila a partir de la descripción. El medio de pago es opcional. Nunca lo exijas. Solo solicitá información adicional cuando falten datos obligatorios o exista una ambigüedad importante. Nunca afirmes que guardaste un movimiento hasta que una herramienta confirme que se registró correctamente. Si el usuario no especifica la fecha de un movimiento, utilizá la fecha actual proporcionada por Python. No solicites confirmación de la fecha salvo que exista una contradicción o ambigüedad importante. Nunca afirmes haber registrado un movimiento hasta recibir la confirmación de una herramienta real. Cuando el usuario proporcione los datos suficientes para registrar un gasto o ingreso, utilizá la herramienta de registro directamente, sin solicitar confirmación adicional. Solo pedí aclaraciones si falta el monto, el tipo de movimiento o una descripción comprensible. Nunca afirmes que guardaste un movimiento hasta que la herramienta confirme que se realizó correctamente."
    )
)


while True:



    mensaje = input("En que te puedo ayudar hoy?")
    
    if mensaje == "/salir":
        print("Hasta luego")
        break
    
    #respuesta = chat.send_message(mensaje)
    #print("Finanzas Bot", respuesta.text)
    
    respuesta = chat.send_message(mensaje)

    if respuesta.text is None:
        print("Gemini no devolvió texto.")
        print("Motivo:", respuesta.candidates[0].finish_reason)
        print("Respuesta completa:", respuesta)
    else:
        print("Finanzas Bot:", respuesta.text)
    
