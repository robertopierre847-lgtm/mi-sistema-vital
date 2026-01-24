from flask import Flask, request, render_template_string, jsonify
import requests
import os
import random

app = Flask(__name__)

# =========================
# WIKIPEDIA API & PERSONALIDAD
# =========================
def buscar_wikipedia(q):
    try:
        # Buscamos en Wikipedia en español
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{q.replace(' ', '_')}"
        headers = {'User-Agent': 'NoviaVirtualBot/1.0'}
        r = requests.get(url, headers=headers, timeout=5)
        
        if r.status_code != 200:
            return None
        
        d = r.json()
        
        # Lista de frases para dar personalidad
        intros = [
            f"¡Claro que sí! Estuve investigando sobre {q} para ti: ",
            f"Cariño, aquí encontré lo que buscabas sobre {q}: ",
            f"Me encanta que me preguntes cosas, mira lo que encontré sobre {q}: ",
            f"Escucha, amor, esto es lo que dice Wikipedia sobre {q}: "
        ]
        
        texto_original = d.get("extract", "No encontré nada específico.")
        # Combinamos el intro de "novia virtual" con el dato de Wikipedia
        texto_personalizado = random.choice(intros) + texto_original
        
        return {
            "titulo": d.get("title", ""),
            "texto": texto_personalizado,
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
        return jsonify({"error":"Amor, escribe algo para que pueda buscarlo por ti."})
    
    wiki = buscar_wikipedia(q)
    if wiki:
        return jsonify(wiki)
    
    return jsonify({"error":"Lo siento mucho, no encontré información sobre eso en Wikipedia."})

# =========================
# FRONTEND
# =========================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mi IA Virtual</title>
<style>
body{
    margin:0;
    font-family:Arial, sans-serif;
    background:linear-gradient(135deg,#ffe3f2,#ffffff);
    padding:20px;
}
.container{max-width:700px;margin:auto;}
.card{
    background:white;
    border-radius:18px;
    padding:15px;
    margin-top:15px;
    box-shadow:0 10px 25px rgba(0,0,0,0.05);
    transition:0.3s;
}
input{
    width:70%;
    padding:12px;
    border-radius:12px;
    border:1px solid #ffadd2;
    outline:none;
}
button{
    padding:12px 16px;
    border:none;
    border-radius:12px;
    background:#ff4da6;
    color:white;
    cursor:pointer;
    font-weight:bold;
}
img{
    max-width:100%;
    border-radius:14px;
    margin-top:10px;
    display:block;
}
.letra{
    display:inline-block;
    margin:6px;
    padding:12px 15px;
    background:#ff4da6;
    color:white;
    border-radius:10px;
    font-weight:bold;
    cursor:pointer;
}
h2, h3 { color: #d63384; }
</style>
</head>

<body>
<div class="container">

<div class="card">
<h2>Tu Asistente Virtual</h2>
<p>Pregúntame lo que quieras, estaré feliz de ayudarte.</p>
<input id="q" placeholder="¿Qué quieres saber hoy?">
<button onclick="buscar()">Preguntar</button>
</div>

<div id="resultado"></div>

<div class="card">
<h2>Juego: Busca Sonas</h2>
<button onclick="cargarJuego()">Jugar conmigo</button>
<p id="pista"></p>
<div id="letras"></div>
<p id="respuesta"></p>
</div>

</div>

<script>
function buscar(){
    let q = document.getElementById("q").value;
    if(!q){alert("Escribe algo, amor");return;}
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
        document.getElementById('pista').innerText = "Ordena las letras para mí:";
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
            alert("¡Lo lograste! Sabía que eras muy inteligente.");
        }else{
            alert("Casi... la palabra era: "+palabraReal);
        }
        seleccion="";
    }
}
</script>

</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
        
