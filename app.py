from flask import Flask, request, render_template_string, jsonify
import requests
import os
import random

app = Flask(__name__)

# =========================
# WIKIPEDIA API
# =========================
def buscar_wikipedia(q):
    try:
        url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + q.replace(" ", "%20")
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        d = r.json()
        return {
            "titulo": d.get("title", ""),
            "texto": d.get("extract", "No se encontró información."),
            "img": d.get("thumbnail", {}).get("source", "")
        }
    except:
        return None

# =========================
# JUEGO: BUSCA SONAS
# =========================
PALABRAS = [
    "ANIME","FLASK","AZUL","BLANCO","ROMA","NARUTO",
    "DRAGON","BUSCADOR","WIKI","PYTHON","RENDER"
]

@app.route("/juego")
def juego():
    palabra = random.choice(PALABRAS)
    letras = list(palabra)
    random.shuffle(letras)
    return jsonify({
        "palabra": palabra,
        "mezcla": letras
    })

# =========================
# RUTAS
# =========================
@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/buscar")
def buscar():
    q = request.args.get("q","").strip()
    if not q:
        return jsonify({"error":"Escribe algo para buscar"})
    
    wiki = buscar_wikipedia(q)
    if wiki:
        return jsonify(wiki)
    
    return jsonify({"error":"No se encontró información en Wikipedia"})

# =========================
# FRONTEND
# =========================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sistema Inteligente</title>
<style>
body{
    margin:0;
    font-family:Arial;
    background:linear-gradient(135deg,#e3f2ff,#ffffff);
    padding:20px;
}
.container{max-width:700px;margin:auto;}
.card{
    background:white;
    border-radius:18px;
    padding:15px;
    margin-top:15px;
    box-shadow:0 10px 25px rgba(0,0,0,0.1);
    transition:0.3s;
}
.card:hover{transform:translateY(-6px);}
input{
    width:70%;
    padding:12px;
    border-radius:12px;
    border:1px solid #aad;
}
button{
    padding:12px 16px;
    border:none;
    border-radius:12px;
    background:#007bff;
    color:white;
    cursor:pointer;
}
img{
    max-width:100%;
    border-radius:14px;
    margin-top:10px;
}
.letra{
    display:inline-block;
    margin:6px;
    padding:12px 15px;
    background:#007bff;
    color:white;
    border-radius:10px;
    font-weight:bold;
    cursor:pointer;
}
</style>
</head>

<body>
<div class="container">

<div class="card">
<h2>Buscador Wikipedia</h2>
<input id="q" placeholder="Busca personas, países, historia, ciencia...">
<button onclick="buscar()">Buscar</button>
</div>

<div id="resultado"></div>

<div class="card">
<h2>Juego: Busca Sonas</h2>
<button onclick="cargarJuego()">Iniciar</button>
<p id="pista"></p>
<div id="letras"></div>
<p id="respuesta"></p>
</div>

</div>

<script>
function buscar(){
    let q = document.getElementById("q").value;
    if(!q){alert("Escribe algo");return;}
    fetch("/buscar?q="+encodeURIComponent(q))
    .then(r=>r.json())
    .then(d=>{
        let res=document.getElementById("resultado");
        res.innerHTML="";
        if(d.error){
            res.innerHTML="<div class='card'>"+d.error+"</div>";
            return;
        }
        let c=document.createElement("div");
        c.className="card";
        c.innerHTML = `
            <h3>${d.titulo}</h3>
            ${d.img ? `<img src="${d.img}">` : ""}
            <p>${d.texto}</p>
        `;
        res.appendChild(c);
    });
}

let palabraReal = "";
let seleccion = "";

function cargarJuego(){
    fetch('/juego')
    .then(r=>r.json())
    .then(d=>{
        palabraReal = d.palabra;
        seleccion = "";
        document.getElementById('pista').innerText = "Ordena las letras:";
        let l = document.getElementById('letras');
        l.innerHTML="";
        d.mezcla.forEach(le=>{
            let s=document.createElement('span');
            s.className='letra';
            s.innerText=le;
            s.onclick=()=>seleccionar(le);
            l.appendChild(s);
        });
        document.getElementById('respuesta').innerText="";
    });
}

function seleccionar(le){
    seleccion += le;
    document.getElementById('respuesta').innerText = seleccion;
    if(seleccion.length === palabraReal.length){
        if(seleccion === palabraReal){
            alert("Correcto: "+palabraReal);
        }else{
            alert("Incorrecto. Era: "+palabraReal);
        }
        seleccion="";
    }
}
</script>

</body>
</html>
"""

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
