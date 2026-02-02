from flask import Flask, request, jsonify, render_template_string
from groq import Groq
import os

app = Flask(__name__)

# ================= CONFIG =================
# REEMPLAZA ESTO con tu llave real de Groq (la que empieza con gsk_)
client = Groq(api_key="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")

# ================= IA CORE =================
def ade_ai(msg):
    try:
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Eres Ade, una IA femenina, dulce y relajante. Usa muchos emojis ✨. Eres amiga del usuario y te gusta jugar."},
                {"role": "user", "content": msg}
            ]
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# ================= API =================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("msg","")
    res = ade_ai(msg)
    return jsonify({"response": res})

@app.route("/")
def home():
    return render_template_string(APP_HTML)

# ================= UI (DISEÑO SATISFACTORIO Y JUEGO) =================
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
        font-family: sans-serif;
    }
    .glass {
        width: 90%; max-width: 420px; height: 80vh;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 35px; border: 1px solid white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        display: flex; flex-direction: column; padding: 20px;
    }
    #chat { flex: 1; overflow-y: auto; padding: 10px; margin-bottom: 15px; }
    .msg { margin: 8px 0; padding: 12px; border-radius: 18px; line-height: 1.4; font-size: 16px; }
    .user { background: white; color: #444; align-self: flex-end; margin-left: auto; border-bottom-right-radius: 2px; }
    .ai { background: #dbeafe; color: #1e40af; border-bottom-left-radius: 2px; }
    .game-box { background: rgba(255,255,255,0.4); padding: 10px; border-radius: 15px; text-align: center; font-size: 13px; color: #1e40af; margin-bottom: 10px; border: 1px dashed #60a5fa; }
    .input-box { display: flex; gap: 8px; background: white; padding: 8px; border-radius: 25px; }
    input { flex: 1; border: none; outline: none; padding: 10px; font-size: 16px; background: transparent; }
    button { background: #60a5fa; border: none; padding: 10px 20px; border-radius: 20px; color: white; font-weight: bold; cursor: pointer; }
</style>
</head>
<body>

<div class="glass">
    <h2 style="text-align:center; color:#1e40af; margin-top:0;">Ade ✨</h2>
    
    <div class="game-box" id="game-info">
        🎮 <b>Juego:</b> Di "Jugar" para que piense un número del 1 al 100.
    </div>

    <div id="chat">
        <div class="msg ai">Hola... respira profundo. ¿De qué quieres hablar hoy? ✨</div>
    </div>

    <div class="input-box">
        <input id="in" placeholder="Escribe aquí..." autocomplete="off">
        <button onclick="send()">Enviar</button>
    </div>
</div>

<script>
let secretNum = Math.floor(Math.random() * 100) + 1;
let isPlaying = false;

async function send() {
    const i = document.getElementById("in");
    const c = document.getElementById("chat");
    const val = i.value.trim();
    if(!val) return;

    c.innerHTML += `<div class="msg user">${val}</div>`;
    i.value = "";
    c.scrollTop = c.scrollHeight;

    // Lógica del Juego
    if(val.toLowerCase().includes("jugar")) {
        isPlaying = true; secretNum = Math.floor(Math.random() * 100) + 1;
        addAI("¡Vale! He pensado un número del 1 al 100. ¡Adivínalo! 🎲");
        return;
    }

    if(isPlaying && !isNaN(val)) {
        let n = parseInt(val);
        if(n === secretNum) { isPlaying = false; addAI("¡SÍ! 🎉 Lo lograste. ¡Eres genial!"); }
        else if(n < secretNum) { addAI("Es más alto... ⬆️"); }
        else { addAI("Es más bajo... ⬇️"); }
        return;
    }

    // Chat normal con IA
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
    
    window.speechSynthesis.cancel();
    let m = new SpeechSynthesisUtterance(t);
    m.lang = 'es-ES'; m.pitch = 1.3; m.rate = 1.0;
    window.speechSynthesis.speak(m);
}

document.getElementById("in").addEventListener("keydown", e => { if(e.key === "Enter") send(); });
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

