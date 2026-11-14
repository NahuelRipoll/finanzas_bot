import json
import os


def registrar_movimiento(tipo: str, monto: float, descripcion: str, categoria: str):
    print("HERRAMIENTA EJECUTADA: registrar_movimiento")
    movimiento = {
        "tipo": tipo,
        "monto": monto,
        "descripcion": descripcion,
        "categoria": categoria
    }
    
    guardar_movimiento(movimiento)

    return {
        "exito": True,
        "movimiento": movimiento
    }


#resultado = registrar_movimiento("gasto", 2000, "Botella de agua", "Alimentos y Bebidas")
#print(resultado)




def cargar_movimientos():
    if not os.path.exists("movimientos.json"):
        return []

    with open("movimientos.json", "r", encoding="utf-8") as archivo:
        movimientos = json.load(archivo)

    if isinstance(movimientos, dict):
        return [movimientos]

    return movimientos


def guardar_movimiento(movimiento):
    movimientos = cargar_movimientos()

    movimientos.append(movimiento)

    with open("movimientos.json", "w", encoding="utf-8") as archivo:
        json.dump(movimientos, archivo, indent=4, ensure_ascii=False)

    return True
        

datos = cargar_movimientos()



def consultar_resumen():
    print("HERRAMIENTA EJECUTADA: consultar_resumen")
    movimientos = cargar_movimientos()

    total_gastos = 0
    total_ingresos = 0

    for movimiento in movimientos:
        if movimiento["tipo"] == "gasto":
            total_gastos += movimiento["monto"]

        elif movimiento["tipo"] == "ingreso":
            total_ingresos += movimiento["monto"]

    saldo = total_ingresos - total_gastos

    return {
        "total_gastos": total_gastos,
        "total_ingresos": total_ingresos,
        "saldo": saldo
    }
    
    
if __name__ == "__main__":
    resultado = consultar_resumen()
    print(resultado)
    
    
    pass