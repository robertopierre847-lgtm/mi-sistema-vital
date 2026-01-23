from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ==========================
# CONFIG
# ==========================
WIKIPEDIA_API = "https://es.wikipedia.org/api/rest_v1/page/summary/"

# ==========================
# NÚCLEO
# ==========================
CORE = {
    "nombre": "MENTISCOPE 474",
    "estado": "ACTIVO",
    "nivel": "EVOLUCIÓN",
    "sistema": "VIVO",
    "modo": "NORMAL",
    "version": "PRO",
}

# ==========================
# RESPUESTAS BASE (IA SIMPLE)
# ==========================
BASE_CONOCIMIENTO = {
    "quien eres": "Soy el núcleo del sistema MENTISCOPE 474, un sistema inteligente en evolución.",
    "que es el nucleo": "El núcleo es el cerebro del sistema. Controla niveles, búsquedas y evolución.",
    "modo dios": "Modo DIOS es el nivel máximo de control del sistema.",
    "que es mentiscope": "MENTISCOPE 474 es un sistema de inteligencia artificial experimental.",
    "vida": "La vida es el proceso biológico que distingue a los seres vivos.",
    "inteligencia artificial": "La IA es la simulación de inteligencia humana en máquinas."
}

# ==========================
# FUNCIONES
# ==========================
def buscar_wikipedia(query):
    try:
        url = WIKIPEDIA_API + query.replace(" ", "%20")
        r = requests.get(url, timeout=5)

        if r.status_code == 200:
            data = r.json()
            return {
                "titulo": data.get("title", "Sin título"),
                "descripcion": data.get("description", ""),
                "resumen": data.get("extract", ""),
                "imagen": data.get("thumbnail", {}).get("source", None),
                "fuente": "Wikipedia"
            }
        else:
            return None
    except:
        return None

# ==========================
# RUTAS
# ==========================
@app.route("/")
def home():
    return jsonify({
        "sistema": CORE,
        "mensaje": "MENTISCOPE 474 ACTIVO - Buscador inteligente conectado a Wikipedia",
        "uso": {
            "buscar": "/buscar?q=palabra",
            "preguntar": "/preguntar (POST)",
            "core": "/core",
            "niveles": "/niveles",
            "activar": "/activar/<nivel>"
        }
    })

@app.route("/core")
def core():
    return jsonify(CORE)

@app.route("/niveles")
def niveles():
    return jsonify({
        "niveles": [
            "BASE",
            "ALFA",
            "BETA",
            "OMEGA",
            "DIOS",
            "EVOLUCIÓN"
        ]
    })

@app.route("/activar/<nivel>")
def activar_nivel(nivel):
    CORE["modo"] = nivel.upper()
    return jsonify({
        "mensaje": f"Nivel {nivel.upper()} ACTIVADO",
        "core": CORE
    })

# ==========================
# BUSCADOR INTELIGENTE
# ==========================
@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").lower().strip()

    if not q:
        return jsonify({"error": "Escribe algo para buscar"}), 400

    # 1) Buscar en base interna
    for clave in BASE_CONOCIMIENTO:
        if clave in q:
            return jsonify({
                "tipo": "IA_INTERNA",
                "pregunta": q,
                "respuesta": BASE_CONOCIMIENTO[clave],
                "nivel": CORE["modo"]
            })

    # 2) Buscar en Wikipedia
    wiki = buscar_wikipedia(q)

    if wiki:
        return jsonify({
            "tipo": "WIKIPEDIA",
            "busqueda": q,
            "titulo": wiki["titulo"],
            "descripcion": wiki["descripcion"],
            "resumen": wiki["resumen"],
            "imagen": wiki["imagen"],
            "fuente": wiki["fuente"]
        })

    # 3) Respuesta por defecto
    return jsonify({
        "tipo": "IA",
        "respuesta": "No tengo información exacta, pero estoy evolucionando..."
    })

# ==========================
# API DE PREGUNTAS
# ==========================
@app.route("/preguntar", methods=["POST"])
def preguntar():
    data = request.json
    pregunta = data.get("pregunta", "").lower()

    if not pregunta:
        return jsonify({"error": "Pregunta vacía"}), 400

    for clave in BASE_CONOCIMIENTO:
        if clave in pregunta:
            return jsonify({
                "tipo": "IA_INTERNA",
                "pregunta": pregunta,
                "respuesta": BASE_CONOCIMIENTO[clave]
            })

    wiki = buscar_wikipedia(pregunta)

    if wiki:
        return jsonify({
            "tipo": "WIKIPEDIA",
            "pregunta": pregunta,
            "titulo": wiki["titulo"],
            "resumen": wiki["resumen"],
            "imagen": wiki["imagen"]
        })

    return jsonify({
        "tipo": "IA",
        "respuesta": "Estoy aprendiendo... aún no tengo esa información."
    })

# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
