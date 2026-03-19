from flask import Flask, request, jsonify, render_template_string
import requests
from groq import Groq
import os
import random

app = Flask(__name__)

# ================= CONFIG =================
client = Groq(api_key="TU_API_KEY_GROQ_AQUI")

# ================= IA =================
def ade_ai(msg):
    try:
        chat = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Eres Ade ✨, una IA dulce, relajante, inteligente. Hablas bonito, claro y usas emojis suaves."},
                {"role": "user", "content": msg}
            ]
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error IA: {str(e)}"

# ================= WIKIPEDIA =================
def buscar_wikipedia(query):
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{query}"
        res = requests.get(url).json()

        texto = res.get("extract", "No encontré información 😢")
        imagen = res.get("thumbnail", {}).get("source", "")

        return texto, imagen
    except:
        return "Error buscando en Wikipedia", ""

# ================= JUEGO TRIVIA =================
preguntas = [
    {"q": "¿Cuántos días tiene una semana?", "a": "7"},
    {"q": "¿Qué planeta es el más grande?", "a": "jupiter"},
    {"q": "¿Color del cielo?", "a": "azul"},
    {"q": "¿Cuánto es 5+5?", "a": "10"},
]

nivel = 0

@app.route("/api/chat", methods=["POST"])
def chat():
    global nivel
    data = request.json
    msg = data.get("msg","").lower()

    # ===== MODO WIKIPEDIA =====
    if msg.startswith("buscar"):
        query = msg.replace("buscar","").strip()
        texto, img = buscar_wikipedia(query)
        return jsonify({"response": texto, "img": img})

    # ===== MODO JUEGO =====
    if "jugar" in msg:
        nivel = 0
        return jsonify({"response": f"🎮 Nivel 1\n{preguntas[nivel]['q']}"})

    if msg in [p["a"] for p in preguntas]:
        if msg == preguntas[nivel]["a"]:
            nivel += 1
            if nivel >= len(preguntas):
                return jsonify({"response": "🏆 ¡Ganaste todos los niveles!"})
            return jsonify({"response": f"✅ Correcto!\nNivel {nivel+1}\n{preguntas[nivel]['q']}"})

    # ===== IA NORMAL =====
    res = ade_ai(msg)
    return jsonify({"response": res})


# ================= FRONTEND =================
@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Ade Crystal ✨</title>

<style>
body{
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background: linear-gradient(135deg,#74ebd5,#ACB6E5);
    font-family:sans-serif;
}

.glass{
    width:95%;
    max-width:420px;
    height:90vh;
    backdrop-filter: blur(25px);
    background: rgba(255,255,255,0.25);
    border-radius:30px;
    padding:20px;
    display:flex;
    flex-direction:column;
    box-shadow:0 0 40px rgba(0,0,0,0.2);
}

#chat{
    flex:1;
    overflow:auto;
}

.msg{
    padding:12px;
    margin:10px;
    border-radius:15px;
}

.user{
    background:white;
    text-align:right;
}

.ai{
    background:rgba(0,150,255,0.2);
}

img{
    max-width:100%;
    border-radius:10px;
    margin-top:5px;
}

input{
    flex:1;
    border:none;
    padding:10px;
    border-radius:20px;
}

button{
    background:#00aaff;
    color:white;
    border:none;
    padding:10px;
    border-radius:20px;
}

.bar{
    display:flex;
}
</style>
</head>

<body>

<div class="glass">
<h2>Ade 💎</h2>

<div id="chat"></div>

<div class="bar">
<input id="txt" placeholder="Habla o escribe...">
<button onclick="send()">Enviar</button>
</div>

</div>

<script>
async function send(){
    let input=document.getElementById("txt");
    let val=input.value;
    if(!val) return;

    let chat=document.getElementById("chat");
    chat.innerHTML+=`<div class="msg user">${val}</div>`;

    input.value="";

    let res=await fetch("/api/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({msg:val})
    });

    let data=await res.json();

    let html=`<div class="msg ai">${data.response}`;

    if(data.img){
        html+=`<br><img src="${data.img}">`;
    }

    html+=`</div>`;
    chat.innerHTML+=html;

    chat.scrollTop=chat.scrollHeight;

    // VOZ
    let speech=new SpeechSynthesisUtterance(data.response);
    speech.lang="es-ES";
    speech.rate=0.9;
    speech.pitch=1.2;
    speechSynthesis.speak(speech);
}
</script>

</body>
</html>
""")

if __name__ == "__main__":
    app.run(debug=True)
