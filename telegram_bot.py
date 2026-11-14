
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram.request import HTTPXRequest

from agente import crear_chat


# Cargar variables del .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Crear una conversación con Gemini
chat = crear_chat()


# Comando /start
async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy FinanzasBot 💰\n\n"
        "Podés registrar gastos, ingresos y consultar tu saldo.\n\n"
        "Ejemplos:\n"
        "• Gasté $2.350 en papa\n"
        "• Cobré $50.000 por un trabajo\n"
        "• ¿Cuánto dinero tengo disponible?"
    )


# Responder mensajes con Gemini
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text

    print("Mensaje recibido:", mensaje)

    try:
        # Gemini interpreta el mensaje y puede ejecutar herramientas
        respuesta = await asyncio.to_thread(
            chat.send_message,
            mensaje
        )

        await update.message.reply_text(
            respuesta.text or "No pude generar una respuesta."
        )

    except Exception as error:
        print("Error con Gemini:", error)

        if "429" in str(error):
            texto_error = (
                "⚠️ Alcanzamos el límite de solicitudes de Gemini. "
                "Probá más tarde."
            )
        else:
            texto_error = (
                "⚠️ Ocurrió un error al procesar tu mensaje."
            )

        await update.message.reply_text(texto_error)


# Iniciar el bot
def main():
    if not TOKEN:
        raise ValueError(
            "Falta TELEGRAM_BOT_TOKEN en el archivo .env"
        )

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30
    )

    updates_request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30
    )

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(request)
        .get_updates_request(updates_request)
        .build()
    )

    app.add_handler(CommandHandler("start", iniciar))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            responder
        )
    )

    print("FinanzasBot + Gemini funcionando en Telegram...")

    app.run_polling()


if __name__ == "__main__":
    main()
