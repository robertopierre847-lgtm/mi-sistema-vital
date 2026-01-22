from flask import Flask, request, render_template_string, jsonify
import requests, os

app = Flask(__name__)

# =========================
# 🌐 FUNCIONES
# =========================
def buscar_wiki(q):
    """Busca un término en Wikipedia y devuelve título, extracto e imagen."""
    url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{q}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        d = r.json()
        return {
            "titulo": d.get("title",""),
            "texto": d.get("extract","No se encontró información."),
            "img": d.get("thumbnail",{}).get("source",""),
            "url": d.get("content_urls",{}).get("desktop",{}).get("page","")
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
    return jsonify(r if r else {})

# =========================
# 🎨 HTML + ANIMACIONES
# =========================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🎬 Cine & Anime Explorer</title>
<style>
/* ---------------------- ESTILOS GENERALES ---------------------- */
body {
    margin:0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg,#ffffff,#e0f0ff);
    overflow-x: hidden;
}
h1 {
    text-align:center;
    color:#0077ff;
    animation: tituloAnim 2s ease-in-out infinite alternate;
}
@keyframes tituloAnim {
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
}
/* ---------------------- CARD FLOTANTE ---------------------- */
.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    padding: 15px;
    margin: 20px auto;
    max-width: 400px;
    transition: transform 0.3s, box-shadow 0.3s;
    animation: flotar 3s ease-in-out infinite;
}
.card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 25px 50px rgba(0,0,0,0.2);
}
@keyframes flotar {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
/* ---------------------- BUSCADOR ---------------------- */
input {
    width: calc(100% - 24px);
    padding:10px;
    border-radius: 10px;
    border:1px solid #aad;
    margin-bottom:10px;
}
button {
    width:100%;
    padding:12px;
    margin-top:10px;
    border:none;
    border-radius:12px;
    background:#0077ff;
    color:white;
    font-size:16px;
    cursor:pointer;
    transition: transform 0.2s;
}
button:hover { transform: scale(1.05); }
img {
    width: 100%;
    border-radius: 12px;
    margin-bottom: 10px;
    transition: transform 0.3s;
}
img:hover { transform: scale(1.03); }
/* ---------------------- CARRUSEL ---------------------- */
.carousel {
    display: flex;
    overflow-x: auto;
    scroll-behavior: smooth;
    padding-bottom: 10px;
}
.carousel::-webkit-scrollbar {
    height: 8px;
}
.carousel::-webkit-scrollbar-thumb {
    background: #0077ff;
    border-radius: 4px;
}
.carousel-item {
    min-width: 120px;
    margin-right: 10px;
    border-radius: 12px;
    cursor: pointer;
    transition: transform 0.3s;
}
.carousel-item:hover {
    transform: scale(1.1);
}
/* ---------------------- MODAL TRAILER ---------------------- */
#trailerModal {
    display:none;
    position:fixed;
    top:0; left:0;
    width:100%; height:100%;
    background:rgba(0,0,0,0.85);
    justify-content:center; align-items:center;
    z-index:1000;
}
#trailerModal iframe {
    width:80%; height:60%;
    border-radius:12px;
}
#closeModal {
    position:absolute; top:20px; right:20px;
    background:#0077ff; color:white; border:none; padding:10px; border-radius:8px;
    cursor:pointer;
}
#closeModal:hover { transform: scale(1.1); }
</style>
</head>
<body>
<h1>🎬 Cine & Anime Explorer</h1>

<!-- BUSCADOR -->
<div class="card" id="buscador">
<input id="q" placeholder="Busca tu anime o película...">
<button onclick="buscar()">Buscar</button>
<h3 id="t"></h3>
<img id="img" src="">
<p id="txt"></p>
<a id="wikiLink" href="" target="_blank"></a>
</div>

<!-- CARRUSEL -->
<div class="card">
<h3>Portadas Destacadas</h3>
<div class="carousel" id="carousel">
<!-- Miniaturas generadas por JS -->
</div>
</div>

<!-- MODAL TRAILER -->
<div id="trailerModal">
<button id="closeModal" onclick="cerrarModal()">Cerrar</button>
<iframe id="trailer" src="" frameborder="0" allowfullscreen></iframe>
</div>

<!-- MINI ALL MIGHT -->
<img src="https://i.imgur.com/6i9I3Zp.png" style="width:60px; position:fixed; bottom:20px; right:20px; animation:flotar 3s ease-in-out infinite;" alt="Mini All Might">

<script>
const portadas = ["Naruto","Attack on Titan","One Piece","Your Name","Spirited Away","Demon Slayer"];

function cargarCarrusel() {
    const carousel = document.getElementById("carousel");
    portadas.forEach(p => {
        const imgEl = document.createElement("img");
        imgEl.className="carousel-item";
        imgEl.src = "https://source.unsplash.com/160x240/?" + encodeURIComponent(p);
        imgEl.alt = p;
        imgEl.onclick = ()=>abrirModal(p);
        carousel.appendChild(imgEl);
    });
}

function buscar(){
    const qVal = document.getElementById("q").value;
    if(!qVal) return;

    fetch("/buscar?q="+encodeURIComponent(qVal))
    .then(r=>r.json())
    .then(d=>{
        t.innerText = d.titulo || "No encontrado";
        txt.innerText = d.texto || "No hay información disponible.";
        img.src = d.img || "";
        wikiLink.href = d.url || "#";
        wikiLink.innerText = d.url ? "Ir a Wikipedia" : "";
        // Trailer en modal
        document.getElementById("trailer").src = "https://www.youtube.com/embed?listType=search&list=" + encodeURIComponent(qVal+" trailer");
        document.getElementById("trailerModal").style.display="flex";
    });
}

function abrirModal(pelicula) {
    document.getElementById("trailer").src = "https://www.youtube.com/embed?listType=search&list=" + encodeURIComponent(pelicula+" trailer");
    document.getElementById("trailerModal").style.display="flex";
}

function cerrarModal() {
    document.getElementById("trailerModal").style.display="none";
    document.getElementById("trailer").src = "";
}

// Inicializar carrusel al cargar
cargarCarrusel();
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
