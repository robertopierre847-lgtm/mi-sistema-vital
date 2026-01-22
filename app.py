from flask import Flask, request, render_template_string, jsonify
import requests, random, os

app = Flask(__name__)

# =========================
# 🌐 APIs
# =========================

# Wikipedia resumen
def buscar_wiki(q):
    url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + q
    r = requests.get(url)
    if r.status_code != 200:
        return None
    d = r.json()
    return {
        "titulo": d.get("title", ""),
        "texto": d.get("extract", "No se encontró información."),
        "img": d.get("thumbnail", {}).get("source", "")
    }

# AniList API (GraphQL) para anime
def buscar_anime(q):
    url = "https://graphql.anilist.co"
    query = '''
    query ($search: String) {
      Media(search: $search, type: ANIME) {
        title { romaji }
        description(asHtml: false)
        coverImage { large }
      }
    }
    '''
    variables = {"search": q}
    r = requests.post(url, json={'query': query, 'variables': variables})
    if r.status_code != 200:
        return None
    d = r.json().get("data", {}).get("Media", {})
    if not d:
        return None
    return {
        "titulo": d["title"]["romaji"],
        "texto": d.get("description", "Sin descripción."),
        "img": d.get("coverImage", {}).get("large", "")
    }

# =========================
# 🖥️ Rutas
# =========================
@app.route("/")
def inicio():
    return render_template_string(HTML)

@app.route("/buscar")
def buscar():
    q = request.args.get("q","").strip()
    if not q:
        return jsonify({"error":"No hay búsqueda"})
    
    # Primero buscamos anime
    anime = buscar_anime(q)
    if anime:
        anime["tipo"] = "Anime"
        return jsonify(anime)
    
    # Después Wikipedia
    wiki = buscar_wiki(q)
    if wiki:
        wiki["tipo"] = "General / Película / Serie"
        return jsonify(wiki)
    
    return jsonify({"error":"No se encontró información"})

# =========================
# 🎨 HTML + Animaciones
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Buscador Animado</title>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#e6f4ff,#ffffff);padding:15px;}
.card{background:rgba(255,255,255,0.8);backdrop-filter:blur(8px);border-radius:15px;padding:15px;margin:10px 0;box-shadow:0 8px 20px rgba(0,0,0,0.1);transition:transform 0.3s;}
.card:hover{transform:translateY(-5px);}
button{background:#0077ff;color:white;border:none;padding:10px 15px;border-radius:12px;cursor:pointer;transition:0.2s;}
button:hover{transform:scale(1.05);}
input{padding:10px;width:70%;border-radius:12px;border:1px solid #aad;}
img{max-width:100%;border-radius:12px;margin-top:10px;}
</style>
</head>
<body>

<h2>🎬 Buscador de Anime y Películas</h2>
<div class="card">
<input id="q" placeholder="Escribe anime, película o pregunta...">
<button onclick="buscar()">Buscar</button>
</div>

<div id="resultado"></div>

<script>
function buscar(){
    let q = document.getElementById("q").value;
    if(!q) return alert("Escribe algo para buscar!");
    fetch("/buscar?q="+encodeURIComponent(q))
    .then(r=>r.json())
    .then(d=>{
        let res=document.getElementById("resultado");
        res.innerHTML="";
        if(d.error){res.innerHTML="<div class='card'><b>"+d.error+"</b></div>";return;}
        let card=document.createElement("div");
        card.className="card";
        card.innerHTML="<h3>"+d.titulo+" ("+d.tipo+")</h3>";
        if(d.img) card.innerHTML+="<img src='"+d.img+"'>";
        card.innerHTML+="<p>"+d.texto+"</p>";
        res.appendChild(card);
    });
}
</script>

</body>
</html>
"""

# =========================
# 🔹 RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
