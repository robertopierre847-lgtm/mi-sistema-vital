import os, requests, random
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- BANCO DE DATOS MEJORADO ---
preguntas_familia = [
    {"q": "¿Quién es el hermano de tu padre?", "a": "tio"},
    {"q": "¿La hija de tu tía es tu...?", "a": "prima"},
    {"q": "¿El padre de tu abuelo es tu...?", "a": "bisabuelo"},
    {"q": "¿Cómo se le dice al esposo de tu madre que no es tu padre?", "a": "padrastro"}
]

sonidos_juego = [
    {"s": "🔊 '¡Guau Guau!'", "o": ["Perro", "Lobo", "Zorro"], "a": "Perro"},
    {"s": "🔊 '¡Muuuu!'", "o": ["Oveja", "Vaca", "Cabra"], "a": "Vaca"},
    {"s": "🔊 '¡Oink Oink!'", "o": ["Cerdo", "Pato", "Pollo"], "a": "Cerdo"}
]

# --- INTERFAZ PROFESIONAL ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ade Vital OS 💎</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <style>
        :root { --accent: #00d2ff; --glass: rgba(255, 255, 255, 0.8); }
        
        body { 
            margin:0; height:100vh; overflow:hidden;
            font-family: 'Segoe UI', sans-serif;
            background: #e0e5ec;
            display: flex; align-items: center; justify-content: center;
            perspective: 1000px;
        }

        /* EFECTO PARALLAX DE FONDO */
        #bg-parallax {
            position: absolute; width: 110%; height: 110%;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            z-index: -1; transition: transform 0.1s ease-out;
        }

        .os-container {
            width: 90%; max-width: 450px; height: 85vh;
            background: var(--glass);
            backdrop-filter: blur(15px);
            border-radius: 30px; border: 1px solid white;
            box-shadow: 20px 20px 60px #bebebe, -20px -20px 60px #ffffff;
            display: flex; flex-direction: column; overflow: hidden;
            animation: fadeInDown 1s;
        }

        #screen { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        
        .msg { padding: 12px; border-radius: 15px; font-size: 0.9rem; max-width: 80%; line-height: 1.4; }
        .ade { background: white; align-self: flex-start; box-shadow: 2px 5px 15px rgba(0,0,0,0.05); animation: backInLeft 0.5s; }
        .user { background: var(--accent); color: white; align-self: flex-end; animation: backInRight 0.5s; }

        /* CONTROLES TIPO HOVER ANIMATION */
        .dock { padding: 15px; background: rgba(255,255,255,0.4); display: flex; gap: 10px; border-top: 1px solid #ddd; }
        .btn-vital { 
            flex: 1; border: none; padding: 10px; border-radius: 12px; 
            cursor: pointer; font-weight: bold; transition: all 0.3s;
            background: white; color: #555;
        }
        .btn-vital:hover { transform: translateY(-3px) scale(1.05); box-shadow: 0 5px 15px rgba(0,0,0,0.1); color: var(--accent); }

        .input-box { display: flex; padding: 15px; gap: 10px; background: white; }
        input { flex: 1; border: 1px solid #eee; padding: 10px; border-radius: 10px; outline: none; }
        
        .color-picker { position: absolute; top: 20px; right: 20px; display: flex; gap: 5px; }
        .dot { width: 15px; height: 15px; border-radius: 50%; cursor: pointer; border: 2px solid white; }
    </style>
</head>
<body>

<div id="bg-parallax"></div>

<div class="color-picker">
    <div class="dot" style="background:#00d2ff" onclick="setTheme('#00d2ff')"></div>
    <div class="dot" style="background:#ff4757" onclick="setTheme('#ff4757')"></div>
    <div class="dot" style="background:#2ed573" onclick="setTheme('#2ed573')"></div>
    <div class="dot" style="background:#ffa502" onclick="setTheme('#ffa502')"></div>
</div>

<div class="os-container">
    <div style="padding:15px; text-align:center; font-weight:bold; color:#666;">ADE VITAL OS 💎</div>
    <div id="screen">
        <div class="msg ade">¡Bienvenido! He integrado efectos de <b>Parallax</b> y <b>Hover Animations</b>.<br><br>Escribe para buscar en Wikipedia o presiona un juego.</div>
    </div>

    <div id="game-options" style="padding:10px; display:none; background:rgba(0,0,0,0.05); text-align:center;"></div>

    <div class="input-box">
        <input type="text" id="userInput" placeholder="Pregunta o responde..." onkeypress="if(event.key==='Enter') send()">
        <button onclick="send()" style="background:var(--accent); color:white; border:none; border-radius:50%; width:40px; height:40px; cursor:pointer;">➤</button>
    </div>

    <div class="dock">
        <button class="btn-vital" onclick="startJuego('familia')">👨‍👩‍👦 Familia</button>
        <button class="btn-vital" onclick="startJuego('sonidos')">🔊 Sonidos</button>
    </div>
</div>

<script>
    // EFECTO PARALLAX
    document.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth / 2 - e.pageX) / 25;
        const y = (window.innerHeight / 2 - e.pageY) / 25;
        document.getElementById('bg-parallax').style.transform = `rotateY(${x}deg) rotateX(${y}deg)`;
    });

    let modo = "chat";
    let respuestaCorrecta = "";

    function setTheme(color) { document.documentElement.style.setProperty('--accent', color); }

    async function send(customMsg = null) {
        const input = document.getElementById("userInput");
        const msg = customMsg || input.value.trim();
        if(!msg) return;

        addMsg("user", msg);
        input.value = "";
        document.getElementById("game-options").style.display = "none";

        const res = await fetch("/api/ade", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({msg: msg, modo: modo, r_correcta: respuestaCorrecta})
        });
        const data = await res.json();

        addMsg("ade", data.text);
        if(data.img) addMsg("ade", `<img src="${data.img}" style="width:100%; border-radius:10px; margin-top:10px;">`);
        
        // Actualizar lógica del juego
        if(data.modo_actual) modo = data.modo_actual;
        if(data.r_correcta) respuestaCorrecta = data.r_correcta;

        if(data.opts) {
            const optDiv = document.getElementById("game-options");
            optDiv.style.display = "block";
            optDiv.innerHTML = "";
            data.opts.forEach(o => {
                optDiv.innerHTML += `<button onclick="send('${o}')" style="margin:5px; padding:8px; border-radius:8px; border:none; background:var(--accent); color:white; cursor:pointer;">${o}</button>`;
            });
        }
    }

    function addMsg(tipo, texto) {
        const screen = document.getElementById("screen");
        screen.innerHTML += `<div class="msg ${tipo}">${texto}</div>`;
        screen.scrollTop = screen.scrollHeight;
    }

    function startJuego(tipo) {
        modo = "chat"; // Reset para forzar el inicio
        send(tipo === 'familia' ? "INICIAR_FAMILIA" : "INICIAR_SONIDOS");
    }
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/ade", methods=["POST"])
def api():
    data = request.json
    msg = data.get("msg", "").lower().strip()
    modo_cliente = data.get("modo")
    r_correcta = data.get("r_correcta", "").lower()

    # --- LÓGICA DEL JUEGO (ARREGLADA) ---
    
    # 1. Iniciar juegos
    if msg == "iniciar_familia":
        q = random.choice(preguntas_familia)
        return jsonify({"text": f"<b>Juego Familia Nivel 1</b><br>{q['q']}", "modo_actual": "juego_familia", "r_correcta": q['a']})

    if msg == "iniciar_sonidos":
        q = random.choice(sonidos_juego)
        return jsonify({"text": f"<b>Adivina el Sonido</b><br>{q['s']}", "modo_actual": "juego_sonidos", "r_correcta": q['a'], "opts": q['o']})

    # 2. Validar respuestas si estamos en modo juego
    if modo_cliente == "juego_familia":
        if msg == r_correcta:
            q = random.choice(preguntas_familia)
            return jsonify({"text": f"✅ ¡Correcto! Siguiente:<br>{q['q']}", "modo_actual": "juego_familia", "r_correcta": q['a']})
        else:
            return jsonify({"text": "❌ Incorrecto. ¡Sigue intentando!", "modo_actual": "juego_familia", "r_correcta": r_correcta})

    if modo_cliente == "juego_sonidos":
        if msg == r_correcta:
            q = random.choice(sonidos_juego)
            return jsonify({"text": f"✅ ¡Excelente!<br>{q['s']}", "modo_actual": "juego_sonidos", "r_correcta": q['a'], "opts": q['o']})
        else:
            return jsonify({"text": f"❌ ¡Oh no! Inténtalo otra vez.", "modo_actual": "juego_sonidos", "r_correcta": r_correcta, "opts": ["Reintentar"]})

    # 3. Si no es juego, es WIKIPEDIA
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{msg.replace(' ', '_')}"
        headers = {'User-Agent': 'AdeVitalOS/1.0'}
        res = requests.get(url, headers=headers).json()
        return jsonify({
            "text": res.get("extract", "No encontré información sobre eso."),
            "img": res.get("thumbnail", {}).get("source", ""),
            "modo_actual": "chat"
        })
    except:
        return jsonify({"text": "Error de conexión con la enciclopedia.", "modo_actual": "chat"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
