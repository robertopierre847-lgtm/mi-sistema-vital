from flask import Flask, request, render_template_string, jsonify
import requests
import os
import random

app = Flask(__name__)

# =========================
# WIKIPEDIA APIs
# =========================

def wiki_summary(q):
    url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{q}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        d = r.json()
        return {
            "tipo": "Wikipedia",
            "titulo": d.get("title",""),
            "texto": d.get("extract",""),
            "img": d.get("thumbnail",{}).get("source","")
        }
    except:
        return None

def wiki_search(q):
    url = "https://es.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        resultados = data.get("query",{}).get("search",[])
        if not resultados:
            return None
        titulo = resultados[0]["title"]
        return wiki_summary(titulo.replace(" ","_"))
    except:
        return None

# =========================
# MOTOR LOGICO
# =========================

def responder_pregunta(q):
    ql = q.lower()

    if ql.startswith("quien es"):
        tema = ql.replace("quien es","").strip()
        return wiki_search(tema)

    if ql.startswith("que es"):
        tema = ql.replace("que es","").strip()
        return wiki_search(tema)

    if ql.startswith("que significa"):
        tema = ql.replace("que significa","").strip()
        return wiki_search(tema)

    if ql.startswith("donde esta"):
        tema = ql.replace("donde esta","").strip()
        return wiki_search(tema)

    if ql.startswith("cuando fue"):
        tema = ql.replace("cuando fue","").strip()
        return wiki_search(tema)

    return None

# =========================
# JUEGO
# =========================

PALABRAS = [
    "SISTEMA","MENTE","LOGICA","NUCLEO","ENERGIA",
    "INTELIGENCIA","PODER","SABER","EVOLUCION","CONTROL"
]

@app.route("/juego")
def juego():
    palabra = random.choice(PALABRAS)
    letras = list(palabra)
    random.shuffle(letras)
    return jsonify({"palabra": palabra, "mezcla": letras})

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
        return jsonify({"error":"Escribe algo"})

    q_clean = q.replace(" ","_")

    # 1. Intentar resumen directo
    direct = wiki_summary(q_clean)
    if direct and direct["texto"]:
        return jsonify(direct)

    # 2. Motor lógico
    logica = responder_pregunta(q)
    if logica:
        return jsonify(logica)

    # 3. Búsqueda inteligente
    search = wiki_search(q)
    if search:
        return jsonify(search)

    return jsonify({"error":"No se encontró información"})

# =========================
# FRONTEND
# =========================

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MENTISCOPE 474 PRO</title>

<style>
body{
margin:0;
font-family:Arial;
background:linear-gradient(135deg,#e6f3ff,#ffffff);
padding:20px;
}
.container{max-width:750px;margin:auto;}
.card{
background:white;
border-radius:18px;
padding:18px;
margin-top:15px;
box-shadow:0 10px 25px rgba(0,0,0,0.1);
transition:0.3s;
}
.card:hover{transform:translateY(-6px);}
h2{color:#005eff;}
input{
width:70%;
padding:12px;
border-radius:12px;
border:1px solid #aac;
outline:none;
}
button{
padding:12px 16px;
border:none;
border-radius:12px;
background:#005eff;
color:white;
cursor:pointer;
}
img{
max-width:100%;
border-radius:14px;
margin-top:10px;
}
.title{font-weight:bold;color:#003c99;}
.type{font-size:12px;color:#666;}
.letra{
display:inline-block;
margin:6px;
padding:12px 15px;
background:#005eff;
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
<h2>Sistema Inteligente PRO</h2>
<input id="q" placeholder="Pregunta o busca cualquier cosa">
<button onclick="buscar()">Buscar</button>
</div>

<div id="resultado"></div>

<div class="card">
<h2>Busca Sonas PRO</h2>
<button onclick="cargarJuego()">Iniciar</button>
<p id="pista"></p>
<div id="letras"></div>
<p id="respuesta"></p>
</div>

</div>

<script>
function buscar(){
let q=document.getElementById("q").value;
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
c.innerHTML=`
<div class="type">${d.tipo}</div>
<div class="title">${d.titulo}</div>
${d.img?`<img src="${d.img}">`:""}
<p>${d.texto}</p>`;
res.appendChild(c);
});
}

let palabraReal="";
let seleccion="";

function cargarJuego(){
fetch("/juego").then(r=>r.json()).then(d=>{
palabraReal=d.palabra;
seleccion="";
document.getElementById("pista").innerText="Ordena las letras:";
let l=document.getElementById("letras");
l.innerHTML="";
d.mezcla.forEach(le=>{
let s=document.createElement("span");
s.className="letra";
s.innerText=le;
s.onclick=()=>seleccionar(le);
l.appendChild(s);
});
document.getElementById("respuesta").innerText="";
});
}

function seleccionar(le){
seleccion+=le;
document.getElementById("respuesta").innerText=seleccion;
if(seleccion.length===palabraReal.length){
if(seleccion===palabraReal){
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
