from flask import Flask, request, render_template_string, jsonify import requests, os, random

app = Flask(name)

=========================

🔍 APIs

=========================

🔹 Anime API (Jikan - MyAnimeList)

def buscar_anime(q): url = f"https://api.jikan.moe/v4/anime?q={q}&limit=1" r = requests.get(url) if r.status_code != 200: return None data = r.json().get("data", []) if not data: return None a = data[0] return { "tipo": "Anime", "titulo": a.get("title", ""), "texto": a.get("synopsis", "Sin descripción disponible."), "img": a.get("images", {}).get("jpg", {}).get("large_image_url", "") }

🔹 Wikipedia Español

def buscar_wikipedia(q): url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{q}" r = requests.get(url) if r.status_code != 200: return None d = r.json() return { "tipo": "Información", "titulo": d.get("title", ""), "texto": d.get("extract", "No se encontró información."), "img": d.get("thumbnail", {}).get("source", "") }

=========================

🎮 JUEGO: BUSCA SONAS

=========================

PALABRAS = ["ANIME","AZUL","BLANCO","FLASK","JUEGO","BUSCADOR","WIKI","DRAGON","NARUTO","ROMA"]

@app.route("/juego") def juego(): palabra = random.choice(PALABRAS) letras = list(palabra) random.shuffle(letras) return jsonify({"palabra": palabra, "mezcla": letras})

=========================

🌐 Rutas

=========================

@app.route("/") def home(): return render_template_string(HTML)

@app.route("/buscar") def buscar(): q = request.args.get("q","" ).strip() if not q: return jsonify({"error":"Escribe algo para buscar"})

anime = buscar_anime(q)
if anime:
    return jsonify(anime)

wiki = buscar_wikipedia(q)
if wiki:
    return jsonify(wiki)

return jsonify({"error":"No se encontró nada relacionado"})

=========================

🎨 FRONTEND

=========================

HTML = """

<!DOCTYPE html><html lang="es">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Buscador Inteligente</title>
<style>
body{margin:0;font-family:Arial;background:linear-gradient(135deg,#e3f2ff,#ffffff);padding:20px;}
.container{max-width:650px;margin:auto;}
.card{background:white;border-radius:18px;padding:15px;margin-top:15px;box-shadow:0 10px 25px rgba(0,0,0,0.1);transition:0.3s;}
.card:hover{transform:translateY(-6px);} 
input{width:70%;padding:12px;border-radius:12px;border:1px solid #aad;outline:none;}
button{padding:12px 16px;border:none;border-radius:12px;background:#007bff;color:white;cursor:pointer;}
button:hover{opacity:0.9;} 
img{max-width:100%;border-radius:14px;margin-top:10px;}
.title{font-weight:bold;color:#0056b3;}
.type{font-size:12px;color:#666;}
.letra{display:inline-block;margin:6px;padding:12px 15px;background:#007bff;color:white;border-radius:10px;font-weight:bold;cursor:pointer;}
</style>
</head><body>
<div class="container">
    <div class="card">
        <h2>🔍 Buscador Inteligente</h2>
        <input id="q" placeholder="Busca anime, películas, preguntas, novelas...">
        <button onclick="buscar()">Buscar</button>
    </div><div id="resultado"></div>

<div class="card">
    <h2>🎮 Juego: El Busca Sonas</h2>
    <button onclick="cargarJuego()">Iniciar juego</button>
    <p id="pista"></p>
    <div id="letras"></div>
    <p id="respuesta"></p>
</div>

</div><script>
function buscar(){
    let q = document.getElementById("q").value;
    if(!q){alert("Escribe algo");return;}
    fetch("/buscar?q="+encodeURIComponent(q))
    .then(r=>r.json())
    .then(d=>{
        let res=document.getElementById("resultado");
        res.innerHTML="";
        if(d.error){res.innerHTML="<div class='card'>❌ "+d.error+"</div>";return;}
        let c=document.createElement("div");
        c.className="card";
        c.innerHTML = `
            <div class="type">${d.tipo}</div>
            <div class="title">${d.titulo}</div>
            ${d.img ? `<img src="${d.img}">` : ""}
            <p>${d.texto}</p>`;
        res.appendChild(c);
    });
}

let palabraReal = "";

function cargarJuego(){
    fetch('/juego').then(r=>r.json()).then(d=>{
        palabraReal = d.palabra;
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

let seleccion="";
function seleccionar(le){
    seleccion += le;
    document.getElementById('respuesta').innerText = seleccion;
    if(seleccion.length === palabraReal.length){
        if(seleccion === palabraReal){
            alert('✅ Correcto: '+palabraReal);
        }else{
            alert('❌ Incorrecto. Era: '+palabraReal);
        }
        seleccion="";
    }
}
</script></body>
</html>
"""=========================

▶ RUN

=========================

if name == "main": port = int(os.environ.get("PORT", 5000)) app.run(host="0.0.0.0", port=port)
