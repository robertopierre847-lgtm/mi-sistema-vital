from flask import Flask, request, jsonify, render_template_string
import requests
import random
import os

app = Flask(__name__)

# ================= RESPUESTAS SIMPLES =================
def responder(msg):
    msg = msg.lower()

    if "hola" in msg:
        return "Hola 😊 ¿Cómo estás?"
    elif "como estas" in msg:
        return "Estoy muy bien ✨ gracias por preguntar"
    elif "tu nombre" in msg:
        return "Soy Ade 💎 tu asistente"
    elif "gracias" in msg:
        return "De nada 😊"
    else:
        return "No entendí bien 🤔 intenta buscar o jugar"

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

# ================= JUEGO =================
preguntas = [
    {"q": "¿Cuántos días tiene una semana?", "a": "7"},
    {"q": "¿Color del cielo?", "a": "azul"},
    {"q": "¿Cuánto es 10+5?", "a": "15"},
    {"q": "¿Capital de Francia?", "a": "paris"}
]

nivel = 0

# ================= API =================
@app.route("/api/chat", methods=["POST"])
def chat():
    global nivel
    data = request.json
    msg = data.get("msg","").lower()

    # WIKIPEDIA
    if msg.startswith("buscar"):
        query = msg.replace("buscar","").strip()
        texto, img = buscar_wikipedia(query)
        return jsonify({"response": texto, "img": img})

    # JUEGO
    if "jugar" in msg:
        nivel = 0
        return jsonify({"response": f"🎮 Nivel 1\n{preguntas[nivel]['q']}"})

    if nivel < len(preguntas) and msg == preguntas[nivel]["a"]:
        nivel += 1
        if nivel >= len(preguntas):
            return jsonify({"response": "🏆 Ganaste todos los niveles!"})
        return jsonify({"response": f"✅ Correcto\nNivel {nivel+1}\n{preguntas[nivel]['q']}"})

    # RESPUESTA SIMPLE
    return jsonify({"response": responder(msg)})

# ================= HTML =================
@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Ade 💎</title>

<style>
body{
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background: linear-gradient(135deg,#6dd5ed,#2193b0);
    font-family:sans-serif;
}

.glass{
    width:90%;
    max-width:420px;
    height:90vh;
    backdrop-filter: blur(20px);
    background: rgba(255,255,255,0.3);
    border-radius:30px;
    padding:20px;
    display:flex;
    flex-direction:column;
}

#chat{
    flex:1;
    overflow:auto;
}

.msg{
    padding:10px;
    margin:10px;
    border-radius:15px;
}

.user{
    background:white;
    text-align:right;
}

.ai{
    background:rgba(0,150,255,0.3);
}

img{
    max-width:100%;
    border-radius:10px;
}

.bar{
    display:flex;
}

input{
    flex:1;
    padding:10px;
    border:none;
    border-radius:20px;
}

button{
    background:#00aaff;
    border:none;
    color:white;
    padding:10px;
    border-radius:20px;
}
</style>
</head>

<body>

<div class="glass">
<h2>Ade 💎</h2>

<div id="chat"></div>

<div class="bar">
<input id="txt" placeholder="Escribe...">
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
}
</script>

</body>
</html>
""")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
