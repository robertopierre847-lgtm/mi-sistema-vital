from flask import Flask, render_template_string, request
import requests
import json
import os

app = Flask(__name__)

ARCHIVO = "datos.json"

if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w") as f:
        json.dump({
            "puntos": 0,
            "nivel": 1,
            "indice": 0
        }, f)

def cargar():
    return json.load(open(ARCHIVO))

def guardar(data):
    json.dump(data, open(ARCHIVO, "w"))

# ===== PREGUNTAS DEL JUEGO =====
preguntas = [
    {
        "p": "Ves a alguien triste en la calle. ¿Qué haces?",
        "o": {
            "Ignorar": 0,
            "Pensar cómo ayudar": 10,
            "Burlarte": -10
        }
    },
    {
        "p": "Cometes un error importante. ¿Reaccionas cómo?",
        "o": {
            "Aceptar y aprender": 15,
            "Culpar a otros": -5,
            "Rendirme": -10
        }
    },
    {
        "p": "Tienes tiempo libre. ¿Qué eliges?",
        "o": {
            "Aprender algo nuevo": 20,
            "Dormir todo el día": 5,
            "Perder tiempo sin pensar": -5
        }
    }
]

@app.route("/", methods=["GET", "POST"])
def inicio():
    datos = cargar()
    resultado = ""
    imagen = ""

    if request.method == "POST":
        # BUSCADOR WIKIPEDIA
        if "buscar" in request.form:
            q = request.form.get("buscar")
            url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{q}"
            r = requests.get(url)
            if r.status_code == 200:
                d = r.json()
                resultado = d.get("extract", "No se encontró información.")
                if "thumbnail" in d:
                    imagen = d["thumbnail"]["source"]
            else:
                resultado = "No se pudo buscar."

        # JUEGO
        if "opcion" in request.form:
            idx = datos["indice"]
            if idx < len(preguntas):
                puntos = preguntas[idx]["o"].get(request.form["opcion"], 0)
                datos["puntos"] += puntos
                datos["indice"] += 1
                if datos["puntos"] >= datos["nivel"] * 30:
                    datos["nivel"] += 1
                guardar(datos)

    return render_template_string(HTML,
        datos=datos,
        preguntas=preguntas,
        resultado=resultado,
        imagen=imagen
    )

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IA Mental</title>
<style>
body{
    font-family: Arial;
    background: linear-gradient(135deg,#eaf6ff,#ffffff);
    margin:0;padding:10px;
}
.card{
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(8px);
    border-radius:15px;
    padding:15px;
    margin-bottom:15px;
    box-shadow:0 4px 10px rgba(0,0,0,0.1);
}
button{
    width:100%;
    padding:10px;
    margin-top:8px;
    border:none;
    border-radius:10px;
    background:#2196f3;
    color:white;
    font-size:16px;
}
input{
    width:100%;
    padding:10px;
    border-radius:10px;
    border:1px solid #ccc;
}
img{
    width:100%;
    border-radius:10px;
}
</style>
</head>
<body>

<div class="card">
<h2>🔎 Buscador mental (Wikipedia)</h2>
<form method="post">
<input name="buscar" placeholder="Buscar algo...">
<button>Buscar</button>
</form>
{% if resultado %}
<p>{{resultado}}</p>
{% if imagen %}
<img src="{{imagen}}">
{% endif %}
{% endif %}
</div>

<div class="card">
<h2>🧠 Juego de decisiones</h2>
<p>Nivel: {{datos.nivel}} | Puntos: {{datos.puntos}}</p>

{% if datos.indice < preguntas|length %}
<p><b>{{preguntas[datos.indice].p}}</b></p>
<form method="post">
{% for op in preguntas[datos.indice].o.keys() %}
<button name="opcion" value="{{op}}">{{op}}</button>
{% endfor %}
</form>
{% else %}
<p>🎉 Juego terminado</p>
<p>Recompensa: mejor criterio y autocontrol</p>
{% endif %}
</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
