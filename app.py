from flask import Flask, request, render_template_string, jsonify
import requests, random, os

app = Flask(__name__)

# =========================
# 🌐 FRASES CURIOSAS
# =========================
frases = [
    "La creatividad es inteligencia divirtiéndose. 🎨",
    "Cada error te acerca más al éxito. 🚀",
    "Aprender es descubrir cosas que no sabías que sabías. 💡",
    "El conocimiento es el pasaporte hacia tu futuro. 🌟",
    "Pequeños pasos crean grandes cambios. 👣"
]

# =========================
# 🔍 BUSCADOR WIKIPEDIA
# =========================
def buscar_wiki(q):
    url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + q
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        d = r.json()
        return {
            "titulo": d.get("title",""),
            "texto": d.get("extract","No se encontró información."),
            "img": d.get("thumbnail",{}).get("source","")
        }
    except:
        return None

# =========================
# 🌐 RUTAS
# =========================
@app.route("/")
def inicio():
    return render_template_string(HTML)

@app.route("/buscar")
def buscar():
    q = request.args.get("q","")
    r = buscar_wiki(q)
    frase = random.choice(frases)
    return jsonify(r if r else {}, {"frase": frase})

# =========================
# 🎨 HTML + DISEÑO
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Explora y Aprende</title>
<style>
body{
    margin:0; padding:20px;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg,#e6f4ff,#ffffff);
}
.card{
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
h1{
    text-align:center;
    color:#0077ff;
}
input{
    width: 70%;
    padding:10px;
    border-radius:10px;
    border:1px solid #aad;
    margin-right:5px;
}
button{
    padding:10px 15px;
    border:none;
    border-radius:10px;
    background:#0077ff;
    color:white;
    cursor:pointer;
    transition: transform 0.2s;
}
button:hover{
    transform: scale(1.05);
}
img{
    max-width:100%;
    border-radius:10px;
    margin-top:10px;
}
#resultado{
    margin-top:15px;
}
.frase{
    font-style: italic;
    color:#004bb5;
    margin-top:10px;
}
</style>
</head>
<body>

<h1>🔎 Explora y Aprende</h1>

<div class="card">
    <input id="q" placeholder="Escribe un tema...">
    <button onclick="buscar()">Buscar</button>
    <div id="resultado">
        <h2 id="titulo"></h2>
        <p id="texto"></p>
        <img id="img">
        <p class="frase" id="frase"></p>
    </div>
</div>

<script>
function buscar(){
    let query = document.getElementById("q").value;
    if(!query) return;
    fetch("/buscar?q="+encodeURIComponent(query))
    .then(r=>r.json())
    .then(data=>{
        let info = data[0];
        let frase = data[1].frase;
        if(info.titulo){
            document.getElementById("titulo").innerText = info.titulo;
            document.getElementById("texto").innerText = info.texto;
            document.getElementById("img").src = info.img || "";
            document.getElementById("frase").innerText = frase;
        } else {
            document.getElementById("titulo").innerText = "No se encontró información";
            document.getElementById("texto").innerText = "";
            document.getElementById("img").src = "";
            document.getElementById("frase").innerText = frase;
        }
    });
}
</script>

</body>
</html>
"""

# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
