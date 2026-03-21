import os
import requests
import random
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ================= LÓGICA DEL JUEGO (666 NIVELES) =================
# Banco de datos expandible para la familia y cultura
preguntas_familia = [
    {"q": "¿Quién es el hijo de tu hermano?", "a": "sobrino", "cat": "Familia"},
    {"q": "¿Cómo se llama la madre de tu padre?", "a": "abuela", "cat": "Familia"},
    {"q": "¿Qué es para ti el hijo de tu tío?", "a": "primo", "cat": "Familia"},
    {"q": "¿Cómo se le llama al esposo de tu hija?", "a": "yerno", "cat": "Familia"},
    {"q": "¿Quién es la hermana de tu madre?", "a": "tia", "cat": "Familia"},
    {"q": "¿El hijo de tu padrastro que no es tu hermano es tu...?", "a": "hermanastro", "cat": "Familia"},
    {"q": "¿Cómo se llama el padre de tu esposa?", "a": "suegro", "cat": "Familia"}
]

# Estado del sistema
estado = {"nivel": 1, "esperando_respuesta": False, "r_correcta": ""}

# ================= CONEXIÓN REAL A WIKIPEDIA =================
def buscar_en_wikipedia(query):
    try:
        # API oficial de Wikipedia en español
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        headers = {'User-Agent': 'AdeOS/2.0 (SistemaVital; contacto@ejemplo.com)'}
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            texto = data.get("extract", "No hay resumen disponible.")
            imagen = data.get("thumbnail", {}).get("source", "")
            return texto, imagen
        else:
            return "No encontré nada en Wikipedia sobre ese tema. Prueba con otra palabra.", ""
    except Exception as e:
        return f"Error de conexión con Wikipedia: {str(e)}", ""

# ================= INTERFAZ DE USUARIO (CRISTAL AZUL) =================
HTML_UI = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade Vital OS 💎</title>
    <style>
        :root {
            --azul-cristal: rgba(10, 40, 95, 0.4);
            --borde-neon: rgba(0, 210, 255, 0.5);
        }

        body {
            margin: 0;
            height: 100vh;
            background: url('https://wallpaperaccess.com/full/1155013.jpg') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', sans-serif;
            overflow: hidden;
        }

        /* Efecto Flotante y Cristalizado */
        .window {
            width: 400px;
            height: 600px;
            background: var(--azul-cristal);
            backdrop-filter: blur(25px) saturate(150%);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid var(--borde-neon);
            border-radius: 40px;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.6);
            display: flex;
            flex-direction: column;
            animation: floating 5s ease-in-out infinite;
            position: relative;
        }

        @keyframes floating {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        .header {
            padding: 25px;
            text-align: center;
            color: #00d2ff;
            font-size: 1.5rem;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(0, 210, 255, 0.8);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        #chat {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
            scrollbar-width: none;
        }

        .bubble {
            padding: 12px 18px;
            border-radius: 20px;
            font-size: 0.95rem;
            line-height: 1.4;
            max-width: 85%;
            color: white;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn { from { opacity:0; transform: scale(0.8); } }

        .ade { background: rgba(255, 255, 255, 0.15); align-self: flex-start; border-bottom-left-radius: 2px; }
        .user { background: #00d2ff; color: #002; align-self: flex-end; border-bottom-right-radius: 2px; font-weight: 500; }

        .wiki-img { width: 100%; border-radius: 15px; margin-top: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }

        .input-area {
            padding: 20px;
            background: rgba(0,0,0,0.2);
            display: flex;
            gap: 10px;
            border-bottom-left-radius: 40px;
            border-bottom-right-radius: 40px;
        }

        input {
            flex: 1;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(0, 210, 255, 0.3);
            border-radius: 20px;
            padding: 12px;
            color: white;
            outline: none;
        }

        button {
            background: #00d2ff;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
        }

        button:hover { filter: brightness(1.2); transform: scale(1.05); }

        .level-tag { color: #ff007a; font-weight: bold; font-size: 0.8rem; }
    </style>
</head>
<body>

<div class="window">
    <div class="header">Ade Vital OS 💎</div>
    <div id="chat">
        <div class="bubble ade">Sistema en línea. 🌐<br><br>• Escribe <b>"buscar [algo]"</b> para usar Wikipedia.<br>• Escribe <b>"jugar"</b> para el reto de la familia.</div>
    </div>
    <div class="input-area">
        <input type="text" id="msgIn" placeholder="Comando..." onkeypress="if(event.key==='Enter') enviar()">
        <button onclick="enviar()">➤</button>
    </div>
</div>

<script>
    async function enviar() {
        const input = document.getElementById("msgIn");
        const chat = document.getElementById("chat");
        const texto = input.value.trim();
        if(!texto) return;

        chat.innerHTML += `<div class="bubble user">${texto}</div>`;
        input.value = "";

        const res = await fetch("/api/v1/ade", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({msg: texto})
        });
        const data = await res.json();

        let aiHtml = `<div class="bubble ade">`;
        if(data.nivel) aiHtml += `<span class="level-tag">NIVEL ${data.nivel}/666</span><br>`;
        aiHtml += data.response;
        if(data.img) aiHtml += `<br><img class="wiki-img" src="${data.img}">`;
        aiHtml += `</div>`;

        chat.innerHTML += aiHtml;
        chat.scrollTop = chat.scrollHeight;
    }
</script>
</body>
</html>
"""

# ================= ENDPOINTS DE LA API =================
@app.route("/")
def home():
    return render_template_string(HTML_UI)

@app.route("/api/v1/ade", methods=["POST"])
def process_logic():
    data = request.json
    raw_msg = data.get("msg", "").lower().strip()
    
    # BUSCADOR WIKIPEDIA
    if raw_msg.startswith("buscar"):
        tema = raw_msg.replace("buscar", "").strip()
        info, img = buscar_en_wikipedia(tema)
        estado["esperando_respuesta"] = False
        return jsonify({"response": info, "img": img})

    # LÓGICA DEL JUEGO
    if "jugar" in raw_msg:
        pregunta = random.choice(preguntas_familia)
        estado["nivel"] = 1
        estado["esperando_respuesta"] = True
        estado["r_correcta"] = pregunta["a"]
        return jsonify({"response": f"¡Reto nivel 1 iniciado!<br>{pregunta['q']}", "nivel": 1})

    # VALIDAR RESPUESTA DEL JUEGO
    if estado["esperando_respuesta"]:
        if raw_msg == estado["r_correcta"]:
            estado["nivel"] += 1
            if estado["nivel"] > 666:
                estado["esperando_respuesta"] = False
                return jsonify({"response": "🏆 ¡HAS COMPLETADO LOS 666 NIVELES! Eres el maestro de la familia."})
            
            siguiente = random.choice(preguntas_familia)
            estado["r_correcta"] = siguiente["a"]
            return jsonify({"response": f"✨ ¡Correcto!<br>Siguiente pregunta:<br>{siguiente['q']}", "nivel": estado["nivel"]})
        else:
            return jsonify({"response": "❌ Respuesta incorrecta. Inténtalo de nuevo o escribe 'buscar' para investigar.", "nivel": estado["nivel"]})

    return jsonify({"response": "No reconozco ese comando. Usa 'buscar [tema]' o 'jugar'."})

if __name__ == "__main__":
    # Configuración para Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
