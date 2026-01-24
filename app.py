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
        # Usamos la API de sumario de Wikipedia en español
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{q.replace(' ', '_')}"
        headers = {'User-Agent': 'SistemaInteligenteBot/1.0'}
        r = requests.get(url, headers=headers, timeout=5)
        
        if r.status_code != 200:
            return None
        
        d = r.json()
        return {
            "titulo": d.get("title", ""),
            "texto": d.get("extract", "No se encontró información."),
            # Extraemos la URL de la imagen si existe
            "img": d.get("thumbnail", {}).get("source", "")
        }
    except Exception:
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
# FRONTEND (HTML + CSS + JS)
# =========================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sistema Inteligente</title>
<style>
body{
    margin:0;
    font-family: 'Segoe UI', Arial, sans-serif;
    background:linear-gradient(135deg,#e3f2ff,#ffffff);
    padding:20px;
    min-height: 100vh;
}
.container{max-width:700px;margin:auto;}
.card{
    background:white;
    border-radius:18px;
    padding:20px;
    margin-top:15px;
    box-shadow:0 10px 25px rgba(0,0,0,0.1);
    transition:0.3s;
}
.card:hover{transform:translateY(-3px);}
input{
    width:65%;
    padding:12px;
    border-radius:12px;
    border:1px solid #aad;
    outline: none;
}
button{
    padding:12px 20px;
    border:none;
    border-radius:12px;
    background:#007bff;
    color:white;
    cursor:pointer;
    font-weight: bold;
}
button:hover{ background:#0056b3; }
img{
    width:100%;
    max-height: 350px;
    object-fit: contain;
    border-radius:14px;
    margin: 15px 0;
    background: #f8f9fa;
}
.letra{
    display:inline-block;
    margin:6px;
    padding:12px 18px;
    background:#007bff;
    color:white;
    border-radius:10px;
    font-weight:bold;
    cursor:pointer;
    user-select: none;
}
.letra:active{ transform: scale(0.9); }
</style>
</head>

<body>
<div class="container">

    <div class="card">
        <h2>Buscador Wikipedia</h2>
        <div style="display:flex; gap:10px;">
            <input id="q" placeholder="Ej: Albert Einstein, México, Python...">
            <button onclick="buscar()">Buscar</button>
        </div>
    </div>

    <div id="resultado"></div>

    <div class="card">
        <h2>Juego: Busca Sonas</h2>
        <button onclick="cargarJuego()">Iniciar Juego</button>
        <p id="pista"></p>
        <div id="letras"></div>
        <p>Tu respuesta: <strong id="respuesta"></strong></p>
    </div>

</div>

<script>
function buscar(){
    let q = document.getElementById("q").value;
    if(!q){alert("Escribe algo");return;}
    
    let res = document.getElementById("resultado");
    res.innerHTML = "<div class='card'>Buscando...</div>";

    fetch("/buscar?q="+encodeURIComponent(q))
    .then(r=>r.json())
    .then(d=>{
        res.innerHTML="";
        if(d.error){
            res.innerHTML="<div class='card'>"+d.error+"</div>";
            return;
        }
        let c=document.createElement("div");
        c.className="card";
        c.innerHTML = `
            <h3>${d.titulo}</h3>
            ${d.img ? `<img src="${d.img}" alt="Imagen de Wikipedia">` : "<i>No hay imagen disponible</i>"}
            <p>${d.texto}</p>
        `;
        res.appendChild(c);
    })
    .catch(err => {
        res.innerHTML="<div class='card'>Error en la conexión</div>";
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
            s.onclick=()=>seleccionar(le, s);
            l.appendChild(s);
        });
        document.getElementById('respuesta').innerText="";
    });
}

function seleccionar(le, elemento){
    seleccion += le;
    document.getElementById('respuesta').innerText = seleccion;
    elemento.style.opacity = "0.5";
    elemento.style.pointerEvents = "none";

    if(seleccion.length === palabraReal.length){
        setTimeout(() => {
            if(seleccion === palabraReal){
                alert("¡Correcto! Es " + palabraReal);
            }else{
                alert("Incorrecto. La palabra era: " + palabraReal);
            }
            cargarJuego();
        }, 200);
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
    # Ajustado para Render u otros servicios de hosting
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
        
