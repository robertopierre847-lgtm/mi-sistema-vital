from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# ================= BUSCADOR WIKIPEDIA =================
def buscar_wikipedia(query):
    url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
    r = requests.get(url)

    if r.status_code != 200:
        return None, None

    data = r.json()
    texto = data.get("extract", "No se encontró información.")
    imagen = None

    if "thumbnail" in data:
        imagen = data["thumbnail"]["source"]

    return texto, imagen

# ================= RUTA PRINCIPAL =================
@app.route("/", methods=["GET", "POST"])
def inicio():
    resultado = ""
    imagen = ""

    if request.method == "POST":
        busqueda = request.form.get("buscar", "").strip()
        if busqueda:
            texto, img = buscar_wikipedia(busqueda)
            if texto:
                resultado = texto
                imagen = img
            else:
                resultado = "No se encontró información."

    return render_template_string(HTML, resultado=resultado, imagen=imagen)

# ================= HTML =================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Buscador Inteligente</title>
<style>
body{
    font-family: Arial;
    background: linear-gradient(135deg,#e6f2ff,#ffffff);
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}
.card{
    background:rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    padding:20px;
    width:90%;
    max-width:500px;
    border-radius:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.1);
}
h1{
    text-align:center;
    color:#0055aa;
}
input{
    width:100%;
    padding:10px;
    border-radius:10px;
    border:1px solid #ccc;
    margin-bottom:10px;
}
button{
    width:100%;
    padding:10px;
    background:#0055aa;
    color:white;
    border:none;
    border-radius:10px;
    font-size:16px;
}
.resultado{
    margin-top:15px;
    color:#333;
}
img{
    max-width:100%;
    border-radius:15px;
    margin-top:10px;
}
.relax{
    margin-top:15px;
    font-size:14px;
    color:#555;
    text-align:center;
}
</style>
</head>
<body>

<div class="card">
<h1>🔍 Buscador Relax</h1>

<form method="post">
<input name="buscar" placeholder="Busca algo (historia, ciencia...)">
<button>Buscar</button>
</form>

{% if resultado %}
<div class="resultado">{{resultado}}</div>
{% endif %}

{% if imagen %}
<img src="{{imagen}}">
{% endif %}

<div class="relax">
Respira profundo 🌿<br>
Este espacio es para aprender con calma
</div>
</div>

</body>
</html>
"""

# ❗ NO app.run() ❗
# Render usa gunicorn
