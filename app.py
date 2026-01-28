from flask import Flask, request, jsonify, render_template_string
from groq import Groq
import os

app = Flask(__name__)

# ================= CONFIG =================
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
            "content":f"Eres ADE, una IA femenina, profesional, moderna, inteligente. Estás en modo {mode}. Responde de forma clara, útil, amigable y visual."
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

# ================= UI =================
APP_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>ADE PRO IA</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
*{box-sizing:border-box;font-family:'Segoe UI',Arial;}
body{
    margin:0;
    height:100vh;
    background:radial-gradient(circle at top,#0f2027,#000);
    overflow:hidden;
}

/* ===== LOADER ===== */
#loader{
    position:fixed;
    inset:0;
    background:linear-gradient(135deg,#000,#0f2027,#000);
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    color:white;
    z-index:999;
}
.loader-core{
    width:120px;height:120px;
    border-radius:50%;
    border:6px solid rgba(255,255,255,0.1);
    border-top:6px solid #00f5ff;
    animation:spin 1.2s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}
#loader h2{margin-top:20px;letter-spacing:2px}

/* ===== LAYOUT ===== */
#app{display:flex;height:100vh;}

/* SIDEBAR */
.sidebar{
    width:80px;
    background:rgba(0,0,0,0.6);
    backdrop-filter:blur(15px);
    display:flex;
    flex-direction:column;
    align-items:center;
    padding:10px 0;
    gap:15px;
}
.side-btn{
    width:50px;height:50px;
    border-radius:15px;
    background:rgba(255,255,255,0.1);
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    cursor:pointer;
    transition:.3s;
}
.side-btn:hover{background:#00f5ff;color:black;}

/* MAIN */
.main{
    flex:1;
    display:flex;
    justify-content:center;
    align-items:center;
}

/* GLASS */
.glass{
    width:480px;
    height:720px;
    background:linear-gradient(145deg,rgba(255,255,255,0.18),rgba(255,255,255,0.05));
    backdrop-filter:blur(25px);
    border-radius:30px;
    box-shadow:0 0 40px rgba(0,255,255,0.2), inset 0 0 20px rgba(255,255,255,0.08);
    padding:15px;
    display:flex;
    flex-direction:column;
    color:white;
}

/* HEADER */
.header{
    text-align:center;
    font-weight:bold;
    letter-spacing:2px;
}

/* MODES */
.modes{
    display:flex;
    justify-content:space-around;
    margin:10px 0;
}
.mode{
    padding:6px 12px;
    border-radius:10px;
    background:rgba(0,0,0,0.3);
    cursor:pointer;
    font-size:12px;
}
.mode.active{background:#00f5ff;color:black;font-weight:bold;}

/* CHAT */
#chat{
    flex:1;
    background:rgba(0,0,0,0.35);
    border-radius:15px;
    padding:10px;
    overflow-y:auto;
    font-size:14px;
}
.user{color:#00f5ff;margin:5px 0;}
.ai{color:white;margin:5px 0;}

/* INPUT */
.input-box{
    display:flex;
    gap:6px;
    margin-top:10px;
}
input{
    flex:1;
    padding:12px;
    border-radius:12px;
    border:none;
    outline:none;
}
button{
    padding:12px 16px;
    border-radius:12px;
    border:none;
    background:#00f5ff;
    font-weight:bold;
    cursor:pointer;
}
</style>
</head>

<body>

<!-- LOADER -->
<div id="loader">
    <div class="loader-core"></div>
    <h2>INICIALIZANDO ADE SYSTEM</h2>
</div>

<!-- APP -->
<div id="app" style="display:none;">
    <div class="sidebar">
        <div class="side-btn">🎓</div>
        <div class="side-btn">🎨</div>
        <div class="side-btn">💻</div>
        <div class="side-btn">🎮</div>
        <div class="side-btn">📚</div>
        <div class="side-btn">⚙️</div>
    </div>

    <div class="main">
        <div class="glass">
            <div class="header">ADE PRO IA</div>

            <div class="modes">
                <div class="mode active" onclick="setMode('Normal')">Normal</div>
                <div class="mode" onclick="setMode('Estudio')">Estudio</div>
                <div class="mode" onclick="setMode('Creativo')">Creativo</div>
                <div class="mode" onclick="setMode('Programación')">Code</div>
                <div class="mode" onclick="setMode('Gamer')">Gamer</div>
            </div>

            <div id="chat">
                <div class="ai"><b>ADE:</b> Sistema iniciado ✅ ¿Qué quieres hacer hoy?</div>
            </div>

            <div class="input-box">
                <input id="input" placeholder="Escribe aquí...">
                <button onclick="send()">Enviar</button>
            </div>
        </div>
    </div>
</div>

<script>
let MODE="Normal";

/* LOADER */
setTimeout(()=>{
    document.getElementById("loader").style.display="none";
    document.getElementById("app").style.display="flex";
},2500);

/* MODES */
function setMode(m){
    MODE=m;
    document.querySelectorAll(".mode").forEach(x=>x.classList.remove("active"));
    event.target.classList.add("active");
}

/* CHAT */
async function send(){
    const input=document.getElementById("input");
    const chat=document.getElementById("chat");
    const text=input.value;
    if(!text) return;

    chat.innerHTML+=`<div class="user"><b>Tú:</b> ${text}</div>`;
    input.value="";

    const res=await fetch("/api/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({msg:text,user_id:"user1",mode:MODE})
    });

    const data=await res.json();
    chat.innerHTML+=`<div class="ai"><b>ADE:</b> ${data.response}</div>`;
    chat.scrollTop=chat.scrollHeight;

    speak(data.response);
}

/* VOZ */
function speak(text){
    let msg=new SpeechSynthesisUtterance(text);
    msg.lang="es-ES";
    msg.rate=1;
    msg.pitch=1.15;
    speechSynthesis.speak(msg);
}

/* ENTER */
document.getElementById("input").addEventListener("keydown",e=>{
    if(e.key==="Enter") send();
});
</script>

</body>
</html>
"""

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
