from flask import Flask, request, jsonify, render_template_string
from groq import Groq
import os

app = Flask(__name__)

# ================= CONFIG =================
# Recuerda configurar tu API KEY en Render o ponerla aquí directamente
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

# ================= MEMORIA =================
memory = {}

def get_memory(uid):
    if uid not in memory:
        memory[uid] = []
    return memory[uid]

# ================= IA CORE =================
def ade_ai(uid, msg, mode):
    hist = get_memory(uid)

    if not hist:
        hist.append({
            "role":"system",
            "content":f"Eres ADE, una IA femenina, dulce y profesional. Estás en modo {mode}. Usa emojis, sé muy amable y ayuda al usuario a relajarse. Si el usuario quiere jugar, ayúdalo con el juego de adivinar el número."
        })

    hist.append({"role":"user","content":msg})

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=hist[-15:]
    )

    res = chat.choices[0].message.content
    hist.append({"role":"assistant","content":res})
    return res

# ================= API =================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    uid = data.get("user_id","user1")
    msg = data.get("msg","")
    mode = data.get("mode","Normal")
    res = ade_ai(uid,msg,mode)
    return jsonify({"response":res})

# ================= WEB =================
@app.route("/")
def home():
    return render_template_string(APP_HTML)

# ================= UI (DISEÑO SATISFACTORIO) =================
APP_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>ADE ✨ Aura</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
:root {
    --bg: #eef2f3;
    --glass: rgba(255, 255, 255, 0.7);
    --accent: #8e9eab;
    --text: #4a4a4a;
    --glow: #a1c4fd;
}

*{box-sizing:border-box; font-family: 'Quicksand', sans-serif;}

body{
    margin:0;
    height:100vh;
    background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

/* ===== GLASS CARD ===== */
.glass {
    width: 90%;
    max-width: 450px;
    height: 85vh;
    background: var(--glass);
    backdrop-filter: blur(20px);
    border-radius: 40px;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    padding: 25px;
    animation: fadeIn 1.5s ease-out;
}

@keyframes fadeIn { from {opacity: 0; transform: translateY(20px);} to {opacity: 1; transform: translateY(0);} }

.header {
    text-align: center;
    color: #5d6d7e;
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 15px;
    letter-spacing: 1px;
}

/* ===== GAME AREA ===== */
.game-box {
    background: rgba(255,255,255,0.4);
    border-radius: 20px;
    padding: 10px;
    margin-bottom: 10px;
    text-align: center;
    font-size: 13px;
    color: #707b7c;
    border: 1px dashed #abc;
}

/* ===== CHAT ===== */
#chat {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    margin-bottom: 15px;
    border-radius: 20px;
    scrollbar-width: none;
}
#chat::-webkit-scrollbar { display: none; }

.msg { margin: 10px 0; padding: 12px 18px; border-radius: 20px; max-width: 85%; line-height: 1.4; }
.user { background: #fff; color: #444; align-self: flex-end; margin-left: auto; border-bottom-right-radius: 5px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
.ai { background: #d4e6f1; color: #2e4053; border-bottom-left-radius: 5px; }

/* ===== INPUT ===== */
.input-area { display: flex; gap: 10px; background: white; padding: 10px; border-radius: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
input { flex: 1; border: none; outline: none; padding: 10px 15px; font-size: 16px; background: transparent; }
button { background: #a1c4fd; border: none; padding: 12px 20px; border-radius: 25px; color: white; font-weight: bold; cursor: pointer; transition: 0.3s; }
button:hover { background: #8ab4f8; transform: scale(1.05); }

</style>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700&display=swap" rel="stylesheet">
</head>

<body>

<div class="glass">
    <div class="header">ADE ✨ AURA</div>
    
    <div class="game-box" id="game-status">
        🎮 <b>Minijuego:</b> Adivina el número (1-100). <br>
        Di "Empezar juego" para jugar con ADE.
    </div>

    <div id="chat">
        <div class="msg ai">Hola... respira profundo. Estoy aquí para lo que necesites hoy. ✨</div>
    </div>

    <div class="input-area">
        <input id="input" placeholder="Escribe un mensaje o juega..." autocomplete="off">
        <button onclick="send()">Enviar</button>
    </div>
</div>

<script>
let numeroSecreto = Math.floor(Math.random() * 100) + 1;
let jugando = false;

async function send() {
    const input = document.getElementById("input");
    const chat = document.getElementById("chat");
    const text = input.value.trim();
    if (!text) return;

    // Mostrar mensaje usuario
    chat.innerHTML += `<div class="msg user">${text}</div>`;
    input.value = "";
    chat.scrollTop = chat.scrollHeight;

    // Lógica local del juego para hacerlo más rápido
    if (text.toLowerCase().includes("empezar juego")) {
        jugando = true;
        numeroSecreto = Math.floor(Math.random() * 100) + 1;
        const resp = "¡Claro! He pensado un número entre el 1 y el 100. ¿Cuál crees que es?";
        addAIRes(resp);
        return;
    }

    if (jugando && !isNaN(text)) {
        const num = parseInt(text);
        if (num === numeroSecreto) {
            jugando = false;
            addAIRes("¡Felicidades! 🎉 Lo adivinaste. ¿Quieres jugar otra vez?");
        } else if (num < numeroSecreto) {
            addAIRes("Es un poquito más alto... intenta de nuevo. ⬆️");
        } else {
            addAIRes("Es un poquito más bajo... intenta de nuevo. ⬇️");
        }
        return;
    }

    // Respuesta de la IA normal
    const res = await fetch("/api/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({msg: text, user_id: "user1", mode: "Relajación"})
    });

    const data = await res.json();
    addAIRes(data.response);
}

function addAIRes(text) {
    const chat = document.getElementById("chat");
    chat.innerHTML += `<div class="msg ai">${text}</div>`;
    chat.scrollTop = chat.scrollHeight;
    speak(text);
}

function speak(text) {
    window.speechSynthesis.cancel(); // Detener voz anterior
    let msg = new SpeechSynthesisUtterance(text);
    msg.lang = "es-ES";
    msg.rate = 0.9; // Más calmada
    msg.pitch = 1.2; // Más femenina
    window.speechSynthesis.speak(msg);
}

document.getElementById("input").addEventListener("keydown", e => {
    if (e.key === "Enter") send();
});
</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
