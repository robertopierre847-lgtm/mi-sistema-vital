from flask import Flask, request, jsonify, render_template_string
from groq import Groq
import os

app = Flask(__name__)

# ================= CONFIGURACIÓN =================
# 1. Pega aquí tu llave de Groq (la que empieza con gsk_)
client = Groq(api_key="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")

# 2. Pega aquí tu llave de Hugging Face (la que empieza con hf_)
# (Nota: Se usa para funciones avanzadas de imagen/voz en el futuro)
HF_TOKEN = "TU_LLAVE_DE_HUGGING_FACE_AQUI"

# ================= CEREBRO DE ADE =================
def ade_ai(msg):
    try:
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Eres Ade, una IA femenina muy dulce, relajante y profesional. Usa emojis ✨ y trata al usuario con mucho cariño. Si quiere jugar, ayúdalo."},
                {"role": "user", "content": msg}
            ]
        )
        return chat.choices[0].message.content
    except Exception as e:
        # Esto te dirá en pantalla si tu llave sigue mal
        return f"Error de conexión (Verifica tus llaves): {str(e)}"

# ================= RUTAS =================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    res = ade_ai(data.get("msg",""))
    return jsonify({"response": res})

@app.route("/")
def home():
    return render_template_string(APP_HTML)

# ================= DISEÑO SATISFACTORIO (HTML/CSS) =================
APP_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ade ✨ Aura</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0; height: 100vh;
            background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
            display: flex; justify-content: center; align-items: center;
            font-family: 'Quicksand', sans-serif;
        }
        .glass {
            width: 90%; max-width: 420px; height: 85vh;
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(20px);
            border-radius: 40px; border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            display: flex; flex-direction: column; padding: 25px;
        }
        #chat { flex: 1; overflow-y: auto; padding: 10px; scrollbar-width: none; }
        #chat::-webkit-scrollbar { display: none; }
        .msg { margin: 10px 0; padding: 15px; border-radius: 20px; font-size: 16px; max-width: 85%; line-height: 1.4; }
        .user { background: white; color: #444; align-self: flex-end; margin-left: auto; border-bottom-right-radius: 5px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .ai { background: #d4e6f1; color: #2e4053; border-bottom-left-radius: 5px; }
        .game-info { background: rgba(255,255,255,0.4); padding: 10px; border-radius: 15px; text-align: center; font-size: 13px; color: #5d6d7e; margin-bottom: 10px; border: 1px dashed #abc; }
        .input-area { display: flex; gap: 10px; background: white; padding: 10px; border-radius: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
        input { flex: 1; border: none; outline: none; padding: 10px; font-size: 16px; background: transparent; }
        button { background: #a1c4fd; border: none; padding: 12px 20px; border-radius: 25px; color: white; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #8ab4f8; transform: scale(1.05); }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
</head>
<body>

<div class="glass">
    <h2 style="text-align:center; color:#5d6d7e; margin-bottom:10px;">Ade ✨</h2>
    
    <div class="game-info" id="game-status">
        🎮 <b>Juego:</b> Di "Jugar" para empezar a adivinar el número del 1 al 100.
    </div>

    <div id="chat">
        <div class="msg ai">Hola... respira profundo. Estoy aquí para acompañarte. ¿De qué quieres hablar hoy? ✨</div>
    </div>

    <div class="input-area">
        <input id="in" placeholder="Escribe un mensaje..." autocomplete="off">
        <button onclick="send()">Enviar</button>
    </div>
</div>

<script>
let secretNum = Math.floor(Math.random() * 100) + 1;
let playing = false;

async function send() {
    const i = document.getElementById("in");
    const c = document.getElementById("chat");
    const val = i.value.trim();
    if(!val) return;

    c.innerHTML += `<div class="msg user">${val}</div>`;
    i.value = "";
    c.scrollTop = c.scrollHeight;

    // Lógica rápida del Juego
    if(val.toLowerCase().includes("jugar")) {
        playing = true; secretNum = Math.floor(Math.random() * 100) + 1;
        addAI("¡Qué divertido! He pensado un número del 1 al 100. ¡Dime cuál crees que es! 🎲");
        return;
    }

    if(playing && !isNaN(val)) {
        let n = parseInt(val);
        if(n === secretNum) { playing = false; addAI("¡SÍ! 🎉 ¡Lo adivinaste! Eres increíble. ¿Quieres jugar otra vez?"); }
        else if(n < secretNum) { addAI("Es un poquito más alto... ⬆️"); }
        else { addAI("Es un poquito más bajo... ⬇️"); }
        return;
    }

    // Respuesta de la IA
    const r = await fetch("/api/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({msg: val})
    });
    const data = await r.json();
    addAI(data.response);
}

function addAI(t) {
    const c = document.getElementById("chat");
    c.innerHTML += `<div class="msg ai">${t}</div>`;
    c.scrollTop = c.scrollHeight;
    
    // Voz Femenina y Satisfactoria
    window.speechSynthesis.cancel();
    let m = new SpeechSynthesisUtterance(t);
    m.lang = 'es-ES'; m.pitch = 1.3; m.rate = 0.95;
    window.speechSynthesis.speak(m);
}

document.getElementById("in").addEventListener("keydown", e => { if(e.key === "Enter") send(); });
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))￼Enter
