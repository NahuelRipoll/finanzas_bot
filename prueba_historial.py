import json

historial = []

historial.append({
    "rol": "usuario",
    "mensaje": "Hola, soy Nahuel"
})

historial.append({
    "rol": "asistente",
    "mensaje": "¡Hola, Nahuel!"
})

historial.append({
    "rol": "usuario",
    "mensaje": "Quiero consultar mis gastos"
})


with open("historial.json", "w", encoding="utf-8") as archivo:
    json.dump(historial, archivo, indent=4, ensure_ascii=False)

print("Historial guardado correctamente")

with open("historial.json", "r", encoding="utf-8") as archivo:
    historial_recuperado = json.load(archivo)

print("Historial recuperado:")
print(historial_recuperado)