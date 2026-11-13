import json


def registrar_movimiento(tipo, monto, descripcion, categoria):
    movimiento = {
        "tipo": tipo,
        "monto": monto,
        "descripcion": descripcion,
        "categoria": categoria
    }

    return movimiento


resultado = registrar_movimiento("gasto", 2000, "Botella de agua", "Alimentos y Bebidas")
print(resultado)


def guardar_movimiento(movimiento):
    with open("movimientos.json", "w", encoding="utf-8") as archivo:
        json.dump(movimiento, archivo, indent=4, ensure_ascii=False)
        
        
        
guardar_movimiento(resultado)