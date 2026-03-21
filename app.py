import os
import requests
import random
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ================= CONFIGURACIÓN DEL JUEGO =================
# Banco de preguntas para llegar a los niveles altos
banco_familia = [
    {"q": "¿Cómo se le dice al padre de tu padre?", "a": "abuelo"},
    {"q": "¿Qué es para ti la hija de tu tía?", "a": "prima"},
    {"q": "¿Quién es el esposo de tu madre (que no es tu padre)?", "a": "padrastro"},
    {"q": "¿Cómo se llama el hermano de tu madre?", "a": "tio"},
    {"q": "¿La madre de tu esposa es tu...?", "a": "suegra"},
    {"q": "¿El hijo de tu hijo es tu...?", "a": "nieto"},
    {"q": "¿Cómo se llama la hermana de tu padre?", "a": "tia"},
    {"q": "¿Qué parentesco tienes con el hijo de tu hermano?", "a": "sobrino"}
]

# Estado temporal (Se reinicia si el servidor de Render duerme)
user_data = {"nivel": 1, "pregunta_actual": None}

# ================= FUNCIONES DE APOYO =================
def get_wiki(query):
    try:
        # User-agent es necesario para que Wikipedia no bloquee la petición
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        headers = {'User-Agent': 'AdeOS/1.0'}
        res = requests.get(url, headers=headers).json()
        
        texto = res.get("extract", "No encontré información específica sobre eso. 🧐")
        img = res.get("thumbnail", {}).get("source", "")
        return texto, img
    except:
        return "Hubo un error al conectar con la base de datos de Wikipedia. 🌐", ""

# ================= INTERFAZ (HTML/CSS) =================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade OS 💎</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            background: #0f0c29;
            background: linear-gradient(to bottom, #24243e, #302b63, #0f0c29);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }

        /* Efecto de Cristal Flotante */
        .os-container {
            width: 90%;
            max-width: 450px;
            height: 85vh;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 30px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        .header {
            padding: 20px;
            text-align: center;
            font-weight: bold;
            font-size: 1.2rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            text-shadow: 0 0 10px #00d2ff;
        }

        #display {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .msg {
            padding: 12px 16px;
            border-radius: 15px;
            max-width: 80%;
            font-size: 0.9rem;
            line-height: 1.4;
        }

        .ade { background: rgba(0, 150, 255, 0.2); align-self: flex-start; border-bottom-left-radius: 2px; }
        .user { background: rgba(255, 255, 255, 0.9); color: #1a1a1a; align-self: flex-end; border-bottom-right-radius: 2px; }

        .wiki-img { width: 100%; border-radius: 10px; margin-top: 8px; }

        .controls {
            padding: 20px;
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 12px;
            border-radius: 15px;
            color: white;
            outline: none;
        }

        button {
            background: #00d2ff;
            border: none;
            padding: 10px 20px;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        .level-tag {
            background: #ff007a;
            padding: 2px 8px;
            border-radius: 5px;
            font-size: 0.7rem;
            margin-bottom: 5px;
            display: inline-block;
        }
    </style>
</head>
<body>

<div class="os-container">
    <div class="header">Ade System 💎</div>
    <div id="display">
        <div class="msg ade">Hola, soy Ade. <br><br>Puedes usar:<br>1. <b>buscar [tema]</b> para Wikipedia.<br>2. <b>jugar</b> para iniciar el reto de 666 niveles.</div>
    </div>
    <div class="controls">
        <input type="text" id="in" placeholder="Escribe aquí..." onkeypress="if(event.key==='Enter') exec()">
        <button onclick="exec()">Ok</button>
    </div>
</div>

<script>
    async function exec() {
        const input = document.getElementById("in");
        const display = document.getElementById("display");
        const val = input.value.trim();
        if(!val) return;

        display.innerHTML += `<div class="msg user">${val}</div>`;
        input.value = "";

        const res = await fetch("/api/ade", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({msg: val})
        });
        const data = await res.json();

        let html = `<div class="msg ade">`;
        if(data.nivel) html += `<span class="level-tag">NIVEL ${data.nivel}/666</span><br>`;
        html += data.text;
        if(data.img) html += `<br><img class="wiki-img" src="${data.img}">`;
        html += `</div>`;

        display.innerHTML += html;
        display.scrollTop = display.scrollHeight;
    }
</script>
</body>
</html>
"""

# ================= LÓGICA DEL SERVIDOR =================
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/ade", methods=["POST"])
def api():
    msg = request.json.get("msg", "").lower().strip()
    
    # BUSCADOR WIKIPEDIA
    if msg.startswith("buscar"):
        query = msg.replace("buscar", "").strip()
        texto, imagen = get_wiki(query)
        return jsonify({"text": texto, "img": imagen})

    # LÓGICA DEL JUEGO
    if "jugar" in msg:
        user_data["nivel"] = 1
        q = random.choice(banco_familia)
        user_data["pregunta_actual"] = q
        return jsonify({"text": f"¡Reto iniciado! Nivel 1:<br><b>{q['q']}</b>", "nivel": 1})

    # VERIFICAR RESPUESTA DEL JUEGO
    if user_data["pregunta_actual"] and msg == user_data["pregunta_actual"]["a"]:
        user_data["nivel"] += 1
        if user_data["nivel"] > 666:
            return jsonify({"text": "¡HAS COMPLETADO LOS 666 NIVELES! Eres un genio. 🏆"})
        
        q = random.choice(banco_familia)
        user_data["pregunta_actual"] = q
        return jsonify({
            "text": f"✅ ¡Correcto! Siguiente nivel:<br><b>{q['q']}</b>", 
            "nivel": user_data["nivel"]
        })

    # RESPUESTA POR DEFECTO
    return jsonify({"text": "No entiendo ese comando. Prueba con 'buscar' o 'jugar'."})

# ================= ARRANQUE PARA RENDER =================
if __name__ == "__main__":
    # Importante: Render usa la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
