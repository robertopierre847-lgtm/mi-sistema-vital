from flask import Flask, request, render_template_string, jsonify
import requests, os, random

app = Flask(__name__)

# =========================
# 🌍 BUSCADOR PELÍCULAS / ANIME
# =========================
def buscar_wiki(q):
    try:
        url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + q
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        d = r.json()
        return {
            "titulo": d.get("title",""),
            "texto": d.get("extract","No se encontró información."),
            "img": d.get("thumbnail",{}).get("source","")
        }
    except:
        return {"titulo":"Error al buscar", "texto":"No se pudo obtener información.","img":""}

# =========================
# 🌙 FRASES MOTIVADORAS
# =========================
frases = [
    "Disfruta tu película favorita 🎬",
    "Sumérgete en el anime 🌟",
    "Respira y relájate 💙",
    "Un momento para ti mismo 🍿"
]

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
    return jsonify(r if r else {})

@app.route("/relax")
def relax():
    return jsonify({"frase": random.choice(frases)})

# =========================
# 🎨 HTML + DISEÑO CRISTAL
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🎬 Cine & Anime</title>
<style>
body{
    background: linear-gradient(135deg,#e3f2fd,#ffffff);
    font-family: Arial;
    padding:15px;
}
.card{
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
    border-radius:15px;
    padding:15px;
    margin-bottom:15px;
    animation:fade 0.6s;
}
button{
    background:#2196f3;
    color:white;
    border:none;
    padding:10px;
    border-radius:10px;
    margin:5px 0;
    transition:transform 0.2s;
    width:100%;
    font-size:16px;
}
button:hover{transform:scale(1.05);}
img{max-width:100%;border-radius:10px;margin-top:10px;}
input{width:100%;padding:10px;border-radius:8px;border:1px solid #aad;margin-bottom:5px;}
@keyframes fade{from{opacity:0}to{opacity:1}}
h1,h2{color:#0077ff;text-align:center;}
</style>
</head>
<body>

<h1>🎬 Cine & Anime</h1>

<div class="card">
<h2>🔍 Buscador</h2>
<input id="q" placeholder="Ej: Naruto, One Piece, Avengers...">
<button onclick="buscar()">Buscar</button>
<h3 id="t"></h3>
<img id="img">
<p id="txt"></p>
</div>

<div class="card">
<h2>🌙 Relajación</h2>
<button onclick="relax()">Inspiración</button>
<p id="fr"></p>
</div>

<script>
function buscar(){
    const query = document.getElementById('q').value;
    if(!query) return;
    fetch("/buscar?q="+encodeURIComponent(query))
    .then(r=>r.json())
    .then(d=>{
        document.getElementById('t').innerText=d.titulo;
        document.getElementById('txt').innerText=d.texto;
        document.getElementById('img').src=d.img || "";
    })
    .catch(()=>{alert("Error al buscar");});
}

function relax(){
    fetch("/relax").then(r=>r.json()).then(d=>document.getElementById('fr').innerText=d.frase);
}
</script>

</body>
</html>
"""

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
