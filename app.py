from flask import Flask, request, jsonify, render_template_string
from groq import Groq
import os

# ==============================
# CONFIG
# ==============================
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY","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"))

# ==============================
# MEMORIA GLOBAL
# ==============================
memory_db = {}

def get_memory(user_id):
    if user_id not in memory_db:
        memory_db[user_id] = []
    return memory_db[user_id]

# ==============================
# IA CORE
# ==============================
def ade_ai(user_id, msg):
    history = get_memory(user_id)

    if not history:
        history.append({
            "role":"system",
            "content":"Eres ADE, una IA femenina, amable, inteligente, profesional, moderna, con personalidad adaptable. Usa emojis moderadamente. Sé clara, útil y cercana."
        })

    history.append({"role":"user","content":msg})

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=history[-15:]
    )

    res = chat.choices[0].message.content
    history.append({"role":"assistant","content":res})
    return res

# ==============================
# API
# ==============================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id","user1")
    msg = data.get("msg","")
    res = ade_ai(user_id,msg)
    return jsonify({"response":res})

# ==============================
# WEB
# ==============================
@app.route("/")
def home():
    return render_template_string(APP_HTML)

# ==============================
# HTML + CSS + JS
# ==============================
APP_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>ADE IA Platform</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body{
    margin:0;
    height:100vh;
    background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    display:flex;
    justify-content:center;
    align-items:center;
    font-family:Arial;
}

/* LOADER */
#loader{
    position:fixed;
    inset:0;
    background:black;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    color:white;
    z-index:999;
}
#loader img{
    width:160px;
    animation: float 2s ease-in-out infinite;
}
@keyframes float{
    0%{transform:translateY(0)}
    50%{transform:translateY(-15px)}
    100%{transform:translateY(0)}
}

/* APP */
.hidden{display:none;}

.glass{
    width:420px;
    height:640px;
    background:rgba(255,255,255,0.12);
    backdrop-filter:blur(15px);
    border-radius:25px;
    padding:15px;
    color:white;
    display:flex;
    flex-direction:column;
    box-shadow:0 8px 40px rgba(0,0,0,0.5);
}

h1{text-align:center;margin:5px 0;}

#chat{
    flex:1;
    overflow-y:auto;
    padding:10px;
    background:rgba(0,0,0,0.25);
    border-radius:15px;
    margin-bottom:10px;
    font-size:14px;
}

.msg-user{color:#00f5ff;}
.msg-ai{color:#ffffff;}

.input-box{
    display:flex;
    gap:6px;
}

input{
    flex:1;
    padding:12px;
    border-radius:10px;
    border:none;
    outline:none;
}

button{
    border-radius:10px;
    border:none;
    padding:12px 16px;
    background:#00f5ff;
    font-weight:bold;
    cursor:pointer;
}
</style>
</head>

<body>

<!-- LOADER -->
<div id="loader">
    <!-- Mini All Might (URL externa para Render) -->
    <img src="https://i.imgur.com/9QO4FQy.png">
    <p>Cargando sistema ADE...</p>
</div>

<!-- APP -->
<div id="app" class="hidden">
    <div class="glass">
        <h1>ADE 🤖</h1>
        <div id="chat">
            <p class="msg-ai"><b>Ade:</b> Hola 👋 Soy ADE, tu asistente inteligente. ¿En qué te ayudo hoy?</p>
        </div>
        <div class="input-box">
            <input id="input" placeholder="Habla con Ade...">
            <button onclick="send()">Enviar</button>
        </div>
    </div>
</div>

<script>
// LOADER
setTimeout(()=>{
    document.getElementById("loader").style.display="none";
    document.getElementById("app").classList.remove("hidden");
},2500);

// CHAT
async function send(){
    const input = document.getElementById("input");
    const chat = document.getElementById("chat");
    const text = input.value;
    if(!text) return;

    chat.innerHTML += `<p class="msg-user"><b>Tú:</b> ${text}</p>`;
    input.value="";

    const res = await fetch("/api/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({msg:text,user_id:"user1"})
    });

    const data = await res.json();
    chat.innerHTML += `<p class="msg-ai"><b>Ade:</b> ${data.response}</p>`;
    chat.scrollTop = chat.scrollHeight;

    speak(data.response);
}

// VOZ
function speak(text){
    let msg = new SpeechSynthesisUtterance(text);
    msg.lang="es-ES";
    msg.rate=1;
    msg.pitch=1.2;
    speechSynthesis.speak(msg);
}

// ENTER
document.getElementById("input").addEventListener("keydown",function(e){
    if(e.key==="Enter") send();
});
</script>

</body>
</html>
"""

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
