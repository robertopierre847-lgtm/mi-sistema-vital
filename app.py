import os
import requests
import random
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ================= DATOS DE LOS JUEGOS =================
preguntas_familia = [
    {"q": "¿Quién es el hijo de tu hermano?", "a": "sobrino"},
    {"q": "¿Cómo se llama la madre de tu padre?", "a": "abuela"},
    {"q": "¿Qué es para ti el hijo de tu tío?", "a": "primo"},
    {"q": "¿Cómo se llama el padre de tu esposa?", "a": "suegro"}
]

juego_sonidos = [
    {"s": "🔊 🎶 'Do-Re-Mi...'", "o": ["Piano", "Guitarra", "Tambor"], "a": "Piano"},
    {"s": "🔊 🦁 '¡Grrr-aaaaa!'", "o": ["Tigre", "León", "Oso"], "a": "León"},
    {"s": "🔊 ⚡ '¡Boom! ¡Crack!'", "o": ["Trueno", "Fuego", "Explosión"], "a": "Trueno"},
    {"s": "🔊 🌊 'Swoosh...'", "o": ["Viento", "Olas del mar", "Lluvia"], "a": "Olas del mar"}
]

# Estado global simple
estado = {"modo": "chat", "nivel_f": 1, "nivel_s": 1, "r_correcta": ""}

def wiki_search(query):
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        res = requests.get(url, headers={'User-Agent': 'AdeOS/3.0'}).json()
        return res.get("extract", "No encontré nada sobre eso... 🔍"), res.get("thumbnail", {}).get("source", "")
    except:
        return "Error de conexión.", ""

# ================= INTERFAZ WEB =================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade Vital OS 💎</title>
    <style>
        body {
            margin: 0; height: 100vh;
            background: linear-gradient(135deg, #021b79, #0575e6);
            font-family: 'Segoe UI', sans-serif;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            overflow: hidden; color: white;
        }

        .os-window {
            width: 90%; max-width: 420px; height: 75vh;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 30px;
            display: flex; flex-direction: column;
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
            animation: float 5s ease-in-out infinite;
        }

        @keyframes float { 0%,100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }

        #screen { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; scrollbar-width: none; }
        
        .bubble { padding: 12px; border-radius: 15px; font-size: 0.9rem; max-width: 80%; }
        .ade { background: rgba(255,255,255,0.15); align-self: flex-start; }
        .user { background: #00d2ff; color: #001; align-self: flex-end; font-weight: bold; }

        .game-panel {
            padding: 15px; background: rgba(0,0,0,0.3);
            border-bottom-left-radius: 30px; border-bottom-right-radius: 30px;
            display: flex; justify-content: center; gap: 10px;
        }

        .btn-game {
            background: rgba(255,255,255,0.2); border: 1px solid white;
            color: white; padding: 8px 15px; border-radius: 12px;
            cursor: pointer; font-size: 0.8rem; transition: 0.3s;
        }

        .btn-game:hover { background: white; color: #021b79; }

        .options-container { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px; }
        .opt-btn { background: #00d2ff; border: none; padding: 8px; border-radius: 8px; cursor: pointer; color: #001; font-weight: bold; flex: 1; }

        .input-box { display: flex; padding: 15px; gap: 10px; }
        input { flex: 1; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); border-radius: 15px; padding: 10px; color: white; outline: none; }
    </style>
</head>
<body>

<div class="os-window">
    <div style="padding: 15px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1);">Ade OS Vital 💎</div>
    <div id="screen">
        <div class="bubble ade">¡Hola! Soy tu sistema inteligente.<br><br>Escribe cualquier cosa para buscar en Wikipedia o selecciona un juego abajo.</div>
    </div>

    <div id="options" class="options-container" style="padding: 0 20px; display:none;"></div>

    <div class="input-box">
        <input type="text" id="userInput" placeholder="Escribe o responde aquí..." onkeypress="if(event.key==='Enter') send()">
        <button onclick="send()" style="background:#00d2ff; border:none; border-radius:50%; width:40px; height:40px; cursor:pointer;">➤</button>
    </div>

    <div class="game-panel">
        <button class="btn-game" onclick="startGame('familia')">👨‍👩‍👦 Juego Familia</button>
        <button class="btn-game" onclick="startGame('sonidos')">🔊 Juego Sonidos</button>
    </div>
</div>

<script>
    async function send(overrideMsg = null) {
        const input = document.getElementById("userInput");
        const msg = overrideMsg || input.value.trim();
        if(!msg) return;

        const screen = document.getElementById("screen");
        screen.innerHTML += `<div class="bubble user">${msg}</div>`;
        input.value = "";
        document.getElementById("options").style.display = "none";

        const res = await fetch("/api/ade", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({msg: msg})
        });
        const data = await res.json();

        let html = `<div class="bubble ade">`;
        if(data.nivel) html += `<b style="color:#ffea00;">NIVEL ${data.nivel}</b><br>`;
        html += data.text;
        if(data.img) html += `<br><img src="${data.img}" style="width:100%; border-radius:10px; margin-top:10px;">`;
        html += `</div>`;
        
        screen.innerHTML += html;

        if(data.options) {
            const optDiv = document.getElementById("options");
            optDiv.innerHTML = "";
            optDiv.style.display = "flex";
            data.options.forEach(o => {
                optDiv.innerHTML += `<button class="opt-btn" onclick="send('${o}')">${o}</button>`;
            });
        }
        screen.scrollTop = screen.scrollHeight;
    }

    function startGame(tipo) {
        send(tipo === 'familia' ? "INICIAR_FAMILIA" : "INICIAR_SONIDOS");
    }
</script>
</body>
</html>
"""

# ================= LÓGICA DEL SERVIDOR =================
@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/ade", methods=["POST"])
def api():
    msg = request.json.get("msg", "").strip()
    
    # Iniciar Juego Familia
    if msg == "INICIAR_FAMILIA":
        estado["modo"] = "familia"
        estado["nivel_f"] = 1
        q = random.choice(preguntas_familia)
        estado["r_correcta"] = q["a"]
        return jsonify({"text": f"¡Reto Familia nivel 1!<br>{q['q']}", "nivel": 1})

    # Iniciar Juego Sonidos
    if msg == "INICIAR_SONIDOS":
        estado["modo"] = "sonidos"
        estado["nivel_s"] = 1
        q = random.choice(juego_sonidos)
        estado["r_correcta"] = q["a"]
        return jsonify({"text": f"Adivina el sonido:<br><b>{q['s']}</b>", "nivel": 1, "options": q["o"]})

    # Lógica de Respuesta de Juegos
    if estado["modo"] == "familia" and msg.lower() == estado["r_correcta"].lower():
        estado["nivel_f"] += 1
        q = random.choice(preguntas_familia)
        estado["r_correcta"] = q["a"]
        return jsonify({"text": f"✅ ¡Correcto!<br>{q['q']}", "nivel": estado["nivel_f"]})

    if estado["modo"] == "sonidos" and msg == estado["r_correcta"]:
        estado["nivel_s"] += 1
        if estado["nivel_s"] > 55: return jsonify({"text": "🏆 ¡Ganaste el juego de sonidos!"})
        q = random.choice(juego_sonidos)
        estado["r_correcta"] = q["a"]
        return jsonify({"text": f"✅ ¡Increíble!<br>Siguiente sonido:<br><b>{q['s']}</b>", "nivel": estado["nivel_s"], "options": q["o"]})

    # SI NO ES JUEGO, ES BUSCADOR AUTOMÁTICO
    info, img = wiki_search(msg)
    estado["modo"] = "chat"
    return jsonify({"text": info, "img": img})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
