import os, requests, random
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- BANCO DE DATOS ---
preguntas_f = [
    {"q": "¿Hijo de mi hermano?", "a": "sobrino"},
    {"q": "¿Padre de mi padre?", "a": "abuelo"},
    {"q": "¿Hermana de mi madre?", "a": "tia"}
]
sonidos_f = [
    {"s": "🔊 '¡Miau!'", "o": ["Perro", "Gato", "Vaca"], "a": "Gato"},
    {"s": "🔊 '¡Ring Ring!'", "o": ["Timbre", "Reloj", "Teléfono"], "a": "Teléfono"}
]

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade Vital OS 💎</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <style>
        :root { --accent: #007bff; --glass: rgba(255, 255, 255, 0.7); --text: #333; }
        body { 
            margin:0; height:100vh; background: #e0e5ec;
            background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', sans-serif; display:flex; justify-content:center; align-items:center;
            color: var(--text); transition: 0.5s;
        }

        /* DISEÑO BLANCO CRISTALINO */
        .glass-card {
            width:90%; max-width:420px; height:85vh; 
            background: var(--glass);
            backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.4);
            border-radius:30px; display:flex; flex-direction:column;
            box-shadow: 20px 20px 60px #bebebe, -20px -20px 60px #ffffff;
            animation: fadeIn 1s; overflow:hidden;
        }

        #screen { flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:15px; }
        .msg { padding:12px; border-radius:15px; font-size:0.9rem; max-width:85%; animation: zoomIn 0.3s; }
        .ade { background: white; align-self: flex-start; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
        .user { background: var(--accent); color: white; align-self: flex-end; }

        .wiki-img { width: 100%; border-radius: 15px; margin-top: 10px; border: 3px solid white; }

        .input-area { padding:15px; display:flex; gap:10px; background: rgba(255,255,255,0.3); }
        input { flex:1; border:none; border-radius:20px; padding:12px; outline:none; background:white; }

        /* SELECTOR DE COLORES */
        .color-bar { display:flex; justify-content:center; gap:10px; padding:10px; background:white; }
        .dot { width:20px; height:20px; border-radius:50%; cursor:pointer; border:2px solid white; }

        .btn-game { flex:1; padding:10px; border:none; border-radius:12px; cursor:pointer; font-weight:bold; transition: 0.3s; }
    </style>
</head>
<body>

<div class="glass-card">
    <div class="color-bar">
        <div class="dot" style="background:#007bff" onclick="changeColor('#007bff', 'rgba(255,255,255,0.7)')"></div>
        <div class="dot" style="background:#ffcc00" onclick="changeColor('#ffcc00', 'rgba(255,250,230,0.8)')"></div>
        <div class="dot" style="background:#2ecc71" onclick="changeColor('#2ecc71', 'rgba(235,255,240,0.8)')"></div>
        <div class="dot" style="background:#e74c3c" onclick="changeColor('#e74c3c', 'rgba(255,235,235,0.8)')"></div>
    </div>

    <div id="screen">
        <div class="msg ade"><b>¡Hola! Soy Ade.</b> 💎<br>Usa el buscador para Wikipedia o elige un juego abajo.</div>
    </div>

    <div id="game-ui" style="display:none; padding:10px; background:rgba(255,255,255,0.5);">
        <div id="opciones" style="display:flex; gap:5px;"></div>
    </div>

    <div class="input-area">
        <input type="text" id="userInput" placeholder="Escribe un tema o respuesta..." onkeypress="if(event.key==='Enter') send()">
        <button onclick="send()" style="border:none; background:var(--accent); color:white; width:40px; height:40px; border-radius:50%; cursor:pointer;">➤</button>
    </div>

    <div style="display:flex; gap:5px; padding:10px;">
        <button class="btn-game" style="background:#eee" onclick="startGame('familia')">👨‍👩‍👦 Familia</button>
        <button class="btn-game" style="background:#eee" onclick="startGame('sonido')">🔊 Sonidos</button>
    </div>
</div>

<script>
    function changeColor(accent, glass) {
        document.documentElement.style.setProperty('--accent', accent);
        document.documentElement.style.setProperty('--glass', glass);
    }

    async function send(custom = null) {
        const input = document.getElementById("userInput");
        const val = custom || input.value.trim();
        if(!val) return;
        
        document.getElementById("screen").innerHTML += `<div class="msg user">${val}</div>`;
        input.value = "";
        document.getElementById("game-ui").style.display = "none";

        const res = await fetch("/api/ade", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({msg: val})
        });
        const data = await res.json();
        
        let html = `<div class="msg ade">`;
        if(data.lvl) html += `<b style="color:var(--accent)">NIVEL ${data.lvl}</b><br>`;
        html += data.text;
        if(data.img) html += `<br><img src="${data.img}" class="wiki-img">`;
        html += `</div>`;
        
        document.getElementById("screen").innerHTML += html;
        
        if(data.opts) {
            const ui = document.getElementById("game-ui");
            const optBox = document.getElementById("opciones");
            ui.style.display = "block";
            optBox.innerHTML = "";
            data.opts.forEach(o => {
                optBox.innerHTML += `<button onclick="send('${o}')" style="flex:1; padding:10px; border-radius:10px; border:none; background:var(--accent); color:white; cursor:pointer;">${o}</button>`;
            });
        }
        document.getElementById("screen").scrollTop = document.getElementById("screen").scrollHeight;
    }

    function startGame(t) { send(t === 'familia' ? "JUGAR_FAMILIA" : "JUGAR_SONIDO"); }
</script>
</body>
</html>
""")

@app.route("/api/ade", methods=["POST"])
def api():
    msg = request.json.get("msg", "").strip()
    
    # Lógica de Juegos
    if msg == "JUGAR_FAMILIA":
        q = random.choice(preguntas_f)
        return jsonify({"text": f"Nivel Familia:<br><b>{q['q']}</b>", "lvl": 1})
    if msg == "JUGAR_SONIDO":
        q = random.choice(sonidos_f)
        return jsonify({"text": f"Adivina:<br><b>{q['s']}</b>", "lvl": 1, "opts": q["o"]})

    # Buscador Wikipedia (Con imágenes corregidas)
    try:
        # Usamos el API de Wikipedia con un User-Agent claro
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{msg.replace(' ', '_')}"
        headers = {'User-Agent': 'AdeVitalBot/1.0 (https://ade-os.onrender.com; ade@example.com)'}
        res = requests.get(url, headers=headers).json()
        return jsonify({
            "text": res.get("extract", "No encontré información sobre eso."),
            "img": res.get("thumbnail", {}).get("source", "") # Esto trae la imagen real
        })
    except:
        return jsonify({"text": "Error al conectar con la enciclopedia."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
        
