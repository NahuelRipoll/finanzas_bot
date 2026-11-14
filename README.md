# FinanzasBot 💰

**FinanzasBot** es un agente de inteligencia artificial desarrollado en **Python** que permite registrar gastos e ingresos personales mediante lenguaje natural y consultar un resumen financiero desde la consola.

El proyecto utiliza la **API de Gemini** para interpretar los mensajes y **Function Calling** para ejecutar funciones reales de Python. Los movimientos se guardan en un archivo JSON, y el historial de conversación se conserva entre ejecuciones.

> **Estado del proyecto:** versión de consola. La integración con Telegram es una posible mejora futura y no forma parte de esta versión.

## Funcionalidades

- Conversar en español argentino con un asistente especializado en finanzas personales.
- Registrar gastos e ingresos mediante mensajes como `Gasté $3.780 en empanadas` o `Cobré $1.000.000 de sueldo`.
- Inferir una categoría cuando el usuario no la especifica.
- Consultar ingresos, gastos y saldo a partir de los movimientos realmente guardados.
- Mantener el contexto durante la conversación y recuperar el historial al reiniciar el programa.
- Reiniciar el contexto conversacional con `/limpiar` sin borrar los movimientos financieros.
- Salir con `/salir`.
- Mostrar mensajes de error cuando la API no responde o alcanza su cuota.

## Tecnologías

- **Python 3.12** (versión utilizada durante el desarrollo).
- **Google Gen AI SDK (`google-genai`)** para interactuar con Gemini.
- **`python-dotenv`** para cargar la clave de API desde un archivo `.env`.
- **JSON** para almacenar movimientos e historial de conversación.

## Estructura del proyecto

```text
finanzas-bot/
├── main.py               # Configuración de Gemini e interfaz de consola
├── movimientos.py        # Registro y resumen de movimientos financieros
├── historial.py          # Guardado y recuperación del historial de Gemini
├── movimientos.json      # Datos financieros (se genera al guardar movimientos)
├── historial.json        # Historial conversacional (se genera al guardarlo)
├── requirements.txt      # Dependencias externas
├── README.md             # Documentación del proyecto
├── .gitignore            # Archivos excluidos de Git
└── .env                  # Clave privada de Gemini (NO subir a GitHub)
```

Los archivos `prueba_historial.py` y otros scripts de prueba pueden conservarse localmente, pero no son necesarios para ejecutar el agente.

## Instalación

### 1. Obtener el proyecto

Cloná el repositorio o descargá el código y abrí una terminal en su carpeta.

### 2. Crear y activar un entorno virtual

En **Windows (PowerShell)**:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, podés habilitarla temporalmente para esa terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar la API de Gemini

Creá un archivo `.env` en la raíz del proyecto:

```dotenv
GEMINI_API_KEY=tu_clave_de_api
```

Podés obtener una clave desde [Google AI Studio](https://aistudio.google.com/apikey). **No publiques tu clave de API.**

Comprobá que `.gitignore` incluya, como mínimo:

```gitignore
.env
venv/
__pycache__/
```

### 5. Ejecutar FinanzasBot

```powershell
python main.py
```

## Ejemplos de uso

```text
=== FINANZAS BOT ===
Comandos disponibles: /salir y /limpiar

¿En qué te puedo ayudar hoy? Gasté $3.780 en empanadas
HERRAMIENTA EJECUTADA: registrar_movimiento
Finanzas Bot: ¡Listo! Registré el gasto de $3.780 en empanadas.

¿En qué te puedo ayudar hoy? Cobré $1.000.000 de sueldo
Finanzas Bot: Registré tu ingreso de $1.000.000.

¿En qué te puedo ayudar hoy? ¿Cuánto gasté en total?
HERRAMIENTA EJECUTADA: consultar_resumen
Finanzas Bot: ...

¿En qué te puedo ayudar hoy? /salir
Finanzas Bot: ¡Hasta luego!
```

*Ejemplo ilustrativo: los mensajes exactos de Gemini y los totales dependen de los movimientos guardados.*

## Herramientas del agente (Function Calling)

### `registrar_movimiento(tipo, monto, descripcion, categoria)`

Recibe los datos identificados por Gemini, construye un movimiento y lo guarda mediante la lógica de `movimientos.py`. La función devuelve un resultado que permite confirmar la operación.

### `consultar_resumen()`

Lee los movimientos almacenados, suma los importes según su tipo y devuelve:

- `total_gastos`
- `total_ingresos`
- `saldo` (ingresos menos gastos)

Gemini decide cuándo solicitar estas herramientas según el mensaje del usuario. La ejecución de las funciones y el acceso al archivo JSON ocurren en Python.

## Persistencia

El proyecto utiliza dos archivos independientes:

- **`movimientos.json`:** almacena los ingresos y gastos registrados. No se borra al usar `/limpiar`.
- **`historial.json`:** almacena el historial de conversación de Gemini, incluidas las estructuras necesarias para conservar el contexto. Se recupera al iniciar el programa y se reinicia con `/limpiar`.

**Importante:** la persistencia de movimientos financieros y la persistencia de la conversación son funcionalidades distintas.

## Comandos

| Comando | Acción |
|---|---|
| `/salir` | Cierra el programa. |
| `/limpiar` | Reinicia el historial conversacional sin eliminar los movimientos financieros. |

## Limitaciones y mejoras futuras

- Requiere conexión a Internet y una clave válida de la API de Gemini.
- La cuota gratuita de Gemini puede producir un error **429 (`RESOURCE_EXHAUSTED`)**; en ese caso hay que esperar a que se restablezca la cuota o utilizar otra configuración disponible.
- La versión actual es de consola; **no** incluye todavía un bot de Telegram.
- Los movimientos actualmente guardan tipo, monto, descripción y categoría. **No se registra todavía una fecha estructurada ni un medio de pago**.
- El saldo calculado representa ingresos menos gastos **registrados en el archivo**, no necesariamente el saldo bancario real.
- La implementación usa archivos JSON locales; no está pensada todavía para múltiples usuarios concurrentes.

Posibles mejoras: integración con Telegram, fechas y filtros por período, edición o eliminación de movimientos, almacenamiento en SQLite y un proveedor alternativo de IA.

## Pruebas sugeridas para la demostración

1. Registrar un gasto en lenguaje natural y comprobar que aparece en `movimientos.json`.
2. Registrar un ingreso y consultar el saldo actualizado.
3. Cerrar el programa, volver a iniciarlo y verificar que se recupera el contexto conversacional.
4. Ejecutar `/limpiar` y comprobar que se reinicia la conversación sin borrar los movimientos.
5. Mostrar la ejecución de las dos herramientas mediante los mensajes de depuración.

## Autoría y finalidad

Proyecto académico desarrollado para la materia **Sistemas Inteligentes**, como práctica de agentes conversacionales, uso de APIs, Function Calling y persistencia de datos.
