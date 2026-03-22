import os, requests, random
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

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
        :root { --accent: #00d2ff; --bg: #050a15; }
        body { 
            margin:0; height:100vh; background: var(--bg); color: white;
            font-family: 'Segoe UI', sans-serif; display:flex; justify-content:center; align-items:center;
            overflow: hidden;
        }

        .glass {
            width:90%; max-width:420px; height:85vh; 
            background: rgba(10, 20, 40, 0.6);
            backdrop-filter: blur(20px); border: 2px solid rgba(0, 210, 255, 0.3);
            border-radius:35px; display:flex; flex-direction:column; overflow:hidden;
            box-shadow: 0 0 50px rgba(0, 210, 255, 0.2);
            animation: backInDown 1s ease-out;
        }

        #screen { flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:15px; scrollbar-width: none; }

        /* Estilo de Mensajes */
        .msg { padding:14px; border-radius:20px; font-size:0.9rem; max-width:85%; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        
        .ade { 
            background: rgba(255, 255, 255, 0.1); align-self: flex-start; 
            border-left: 5px solid var(--accent);
            animation: backInLeft 0.6s; 
        }

        .user { 
            background: linear-gradient(45deg, #00d2ff, #3a7bd5); color: white; 
            align-self: flex-end; border-bottom-right-radius: 2px;
            animation: backInRight 0.5s;
        }

        /* Estilo de la Mascota del Sistema (Avatar) */
        .avatar-container {
            text-align: center; padding: 10px 0;
            border-bottom: 1px solid rgba(0, 210, 255, 0.2);
        }
        .ade-avatar {
            width: 60px; height: 60px;
            background: radial-gradient(circle, #fff 0%, var(--accent) 50%, #001 100%);
            border-radius: 50%; display: inline-block;
            box-shadow: 0 0 20px var(--accent);
            /* Animación de flotación constante */
            animation: floatAvatar 3s ease-in-out infinite;
        }
        @keyframes floatAvatar {
            0%, 100% { transform: translateY(0) scale(1); box-shadow: 0 0 20px var(--accent); }
            50% { transform: translateY(-10px) scale(1.05); box-shadow: 0 0 35px var(--accent); }
        }

        .input-area { padding:15px; display:flex; gap:10px; background: rgba(0,0,0,0.4); }
        input { flex:1; background:transparent; border: 1px solid var(--accent); border-radius:20px; padding:12px; color:white; outline:none; }
        
        .btn-gamer {
            background: rgba(255,255,255,0.05); border: 1px solid var(--accent);
            color: white; padding: 10px; border-radius: 15px; cursor: pointer;
            font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;
            transition: 0.3s; width: 100%;
        }
        .btn-gamer:hover { background: var(--accent); color: black; transform: scale(1.05); box-shadow: 0 0 15px var(--accent); }
    </style>
</head>
<body>

<div class="glass">
    <div class="avatar-container">
        <div class="ade-avatar"></div>
        <div style="font-size: 0.8rem; color: var(--accent); margin-top: 5px;">ADE VITAL</div>
    </div>

    <div id="screen">
        <div class="msg ade">Módulos vitales cargados. 👋<br>Soy Ade, tu guía. Usa el buscador o los modos inferiores.</div>
    </div>
    
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Escribe un comando..." onkeypress="if(event.key==='Enter') process()">
        <button onclick="process()" style="background:var(--accent); border:none; width:40px; height:40px; border-radius:50%; cursor:pointer;">➤</button>
    </div>

    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; padding:15px; background:rgba(0,0,0,0.2);">
        <button class="btn-gamer" onclick="process('MODO_ESTUDIO')">📚 Modo Estudio</button>
        <button class="btn-gamer" onclick="process('SALUD')">💧 Tip Salud</button>
    </div>
</div>

<script>
    async function process(override = null) {
        const input = document.getElementById("userInput");
        const val = override || input.value.trim();
        if(!val) return;

        const screen = document.getElementById("screen");
        screen.innerHTML += `<div class="msg user animate__animated animate__backInRight">${val}</div>`;
        input.value = "";

        // Voz de usuario (opcional para feedback)
        // hablar(val); 

        const res = await fetch("/api/ade", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({msg: val})
        });
        const data = await res.json();
        
        screen.innerHTML += `<div class="msg ade animate__animated animate__backInLeft">${data.text}</div>`;
        screen.scrollTop = screen.scrollHeight;
        
        // Voz del sistema Ade
        const u = new SpeechSynthesisUtterance(data.text);
        u.lang = 'es-ES';
        window.speechSynthesis.speak(u);
    }
</script>
</body>
</html>
""")

@app.route("/api/ade", methods=["POST"])
def api():
    msg = request.json.get("msg", "").lower()
    
    if "estudio" in msg:
        return jsonify({"text": "⏳ Modo Pomodoro iniciado. Concéntrate 25 minutos. ¡Tú puedes!"})
    
    if "salud" in msg:
        tips = ["Bebe un vaso de agua.", "Estira las piernas.", "Parpadea seguido."]
        return jsonify({"text": f"💧 Tip Vital: {random.choice(tips)}"})

    # Buscador Wikipedia
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{msg.replace(' ', '_')}"
        res = requests.get(url, headers={'User-Agent': 'AdeOS/7.0'}).json()
        return jsonify({"text": res.get("extract", "No encontré info en la base de datos.")})
    except:
        return jsonify({"text": "Error de conexión con el satélite vital."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
