import json
from google.genai import types


def guardar_historial(chat):
    historial = chat.get_history()

    datos = [
        mensaje.model_dump(mode="json", exclude_none=True)
        for mensaje in historial
    ]

    with open("historial.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    return True


def cargar_historial():
    try:
        with open("historial.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        return [
            types.Content.model_validate(mensaje)
            for mensaje in datos
        ]

    except FileNotFoundError:
        return []