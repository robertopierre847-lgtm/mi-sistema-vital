from flask import Flask, request, render_template_string, jsonify
import requests, os

app = Flask(__name__)

TMDB_API_KEY = "TU_API_KEY_AQUI"  # <-- Pon tu API Key aquí

# =========================
# 🌐 BUSCADOR TMDB
# =========================
def buscar_tmdb(query):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&language=es-ES&query={query}&page=1&include_adult=false"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    results = []
    for item in data.get("results", [])[:10]:  # top 10 resultados
        # Portada
        poster = f"https://image.tmdb.org/t/p/w300{item.get('poster_path')}" if item.get("poster_path") else ""
        # Trailer
        trailer_url = ""
        # Obtener videos para cada película/anime
        if item.get("media_type") in ["movie", "tv"]:
            vid = requests.get(f"https://api.themoviedb.org/3/{item['media_type']}/{item['id']}/videos?api_key={TMDB_API_KEY}&language=es-ES")
            if vid.status_code == 200:
                vids = vid.json().get("results", [])
                for v in vids:
                    if v["type"] == "Trailer" and v["site"] == "YouTube":
                        trailer_url = f"https://www.youtube.com/embed/{v['key']}"
                        break
        results.append({
            "titulo": item.get("title") or item.get("name"),
            "descripcion": item.get("overview","No hay descripción"),
            "poster": poster,
            "trailer": trailer_url
        })
    return results

# =========================
# 🌐 RUTAS
# =========================
@app.route("/")
def inicio():
    return render_template_string(HTML)

@app.route("/buscar")
def buscar():
    q = request.args.get("q","")
    if not q: return jsonify([])
    res = buscar_tmdb(q)
    return jsonify(res or [])

# =========================
# 🎨 HTML + ESTILO
# =========================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🎬 Cine y Anime - Flotante</title>
<style>
body{
    margin:0; padding:0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg,#e6f4ff,#ffffff);
}
.container{
    padding:15px;
}
input{
    width:70%; padding:10px; border-radius:10px; border:1px solid #aad;
}
button{
    padding:10px 15px; border:none; border-radius:10px;
    background:#0077ff; color:white; margin-left:5px;
    cursor:pointer; transition:0.3s;
}
button:hover{transform:scale(1.05);}
.cards{
    display:flex; overflow-x:auto; gap:15px; padding-top:15px;
}
.card{
    min-width:200px; background:rgba(255,255,255,0.8);
    backdrop-filter:blur(10px); border-radius:15px;
    padding:10px; flex-shrink:0; transition:transform 0.3s;
}
.card:hover{transform:translateY(-10px);}
.card img{width:100%; border-radius:10px;}
iframe{width:100%; height:150px; border:none; margin-top:5px;}
</style>
</head>
<body>
<div class="container">
<h2>🎬 Buscador de Películas y Anime</h2>
<input id="q" placeholder="Escribe el título...">
<button onclick="buscar()">Buscar</button>

<div class="cards" id="resultados"></div>
</div>

<script>
function buscar(){
    let q = document.getElementById("q").value;
    if(!q) return;
    fetch("/buscar?q="+encodeURIComponent(q))
    .then(r=>r.json())
    .then(data=>{
        let cont = document.getElementById("resultados");
        cont.innerHTML="";
        data.forEach(item=>{
            let c = document.createElement("div");
            c.className="card";
            let poster = item.poster ? `<img src='${item.poster}'>` : "";
            let trailer = item.trailer ? `<iframe src='${item.trailer}' allowfullscreen></iframe>` : "";
            c.innerHTML = `<h3>${item.titulo}</h3>${poster}<p>${item.descripcion}</p>${trailer}`;
            cont.appendChild(c);
        });
    });
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
    app.run(host="0.0.0.0", port=port, debug=True)
