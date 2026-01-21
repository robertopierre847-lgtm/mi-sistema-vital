from flask import Flask, request, render_template_string, jsonify
import requests, os

app = Flask(__name__)

# =========================
# 🟦 BUSCADOR EDUCATIVO
# =========================
def buscar_duckduckgo(q):
    """Obtiene resultados de DuckDuckGo instant answer API"""
    url = "https://api.duckduckgo.com/"
    params = {
        "q": q,
        "format": "json",
        "t": "mentiscope"
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return []
    d = r.json()
    results = []
    # Resultado principal
    if d.get("AbstractURL"):
        results.append({
            "titulo": d.get("Heading",""),
            "descripcion": d.get("AbstractText",""),
            "url": d.get("AbstractURL",""),
            "img": d.get("Image","")
        })
    # Otros relacionados
    for r in d.get("RelatedTopics", []):
        if "Text" in r and "FirstURL" in r:
            results.append({
                "titulo": r.get("Text",""),
                "descripcion": r.get("Text",""),
                "url": r.get("FirstURL",""),
                "img": r.get("Icon",{}).get("URL","")
            })
    return results

def buscar_wikipedia(q):
    """Complementa con Wikipedia"""
    url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{q}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    d = r.json()
    return {
        "titulo": d.get("title",""),
        "descripcion": d.get("extract",""),
        "url": f"https://es.wikipedia.org/wiki/{q}",
        "img": d.get("thumbnail",{}).get("source","")
    }

# =========================
# 🌐 RUTAS
# =========================
@app.route("/")
def inicio():
    return render_template_string(HTML)

@app.route("/buscar")
def buscar():
    q = request.args.get("q","")
    resultados = []
    if q:
        resultados.extend(buscar_duckduckgo(q))
        wiki = buscar_wikipedia(q)
        if wiki:
            resultados.insert(0,wiki)
    return jsonify(resultados)

# =========================
# 🎨 HTML + CSS + JS
# =========================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Buscador Escolar 🔍</title>
<style>
body{
    font-family: Arial;
    background: linear-gradient(135deg,#e6f4ff,#ffffff);
    margin:0;
    padding:20px;
}
h1{text-align:center;color:#0077ff;}
.card{
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    max-width: 600px;
    margin: 20px auto;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.card:hover{transform: translateY(-5px);}
input{
    width: 80%;
    padding: 10px;
    border-radius: 10px;
    border:1px solid #aad;
}
button{
    padding: 10px 15px;
    border:none;
    border-radius:10px;
    background:#0077ff;
    color:white;
    font-weight:bold;
    cursor:pointer;
}
.result{
    display:flex;
    flex-direction: column;
    margin-top: 15px;
    gap: 10px;
}
.result div{
    background: rgba(240,247,255,0.8);
    border-radius:10px;
    padding:10px;
    display:flex;
    gap:10px;
    align-items:center;
}
.result img{
    max-width:80px;
    border-radius:6px;
}
a{color:#0077ff;text-decoration:none;font-weight:bold;}
</style>
</head>
<body>
<h1>Buscador Escolar 🔍</h1>
<div class="card">
<input id="q" placeholder="Escribe tu búsqueda...">
<button onclick="buscar()">Buscar</button>
<div class="result" id="res"></div>
</div>

<script>
function buscar(){
    const query = document.getElementById("q").value;
    fetch("/buscar?q="+encodeURIComponent(query))
    .then(r=>r.json())
    .then(data=>{
        const res=document.getElementById("res");
        res.innerHTML="";
        if(data.length==0){
            res.innerHTML="<p>No se encontraron resultados.</p>";
            return;
        }
        data.forEach(d=>{
            const div=document.createElement("div");
            div.innerHTML = `
                ${d.img?'<img src="'+d.img+'">':''}
                <div>
                    <a href="${d.url}" target="_blank">${d.titulo}</a>
                    <p>${d.descripcion}</p>
                </div>
            `;
            res.appendChild(div);
        });
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
