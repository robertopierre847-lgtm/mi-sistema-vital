from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Buscador Inteligente</title>

<style>
body{
    margin:0;
    font-family:Arial;
    background:linear-gradient(135deg,#e6f2ff,#ffffff);
    color:#003366;
}

.contenedor{
    max-width:900px;
    margin:40px auto;
    padding:30px;
    background:rgba(255,255,255,0.7);
    backdrop-filter:blur(12px);
    border-radius:20px;
    box-shadow:0 0 30px rgba(0,0,0,0.1);
}

h1{text-align:center}

input{
    width:100%;
    padding:15px;
    border-radius:15px;
    border:1px solid #99ccff;
    font-size:16px;
}

button{
    margin-top:15px;
    padding:15px;
    width:100%;
    border:none;
    border-radius:15px;
    background:#3399ff;
    color:white;
    font-size:16px;
    cursor:pointer;
}

.resultado{
    margin-top:25px;
    background:white;
    padding:20px;
    border-radius:15px;
}

img{
    max-width:100%;
    border-radius:15px;
    margin-bottom:15px;
}

.relax{
    margin-top:30px;
    text-align:center;
    opacity:0.8;
}
</style>

</head>
<body>

<div class="contenedor">
    <h1>🔍 Buscador Inteligente</h1>

    <form method="post">
        <input name="busqueda" placeholder="Busca ciencia, historia, animales...">
        <button>Buscar</button>
    </form>

    {% if texto %}
    <div class="resultado">
        {% if imagen %}
            <img src="{{imagen}}">
        {% endif %}
        <p>{{texto}}</p>
    </div>
    {% endif %}

    <div class="relax">
        🌿 Respira  
        💙 Mantén la calma  
        🌊 La información fluye
    </div>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def inicio():
    texto = ""
    imagen = ""

    if request.method == "POST":
        q = request.form.get("busqueda","").strip()
        if q:
            url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + q.replace(" ","_")
            r = requests.get(url)

            if r.status_code == 200:
                data = r.json()
                texto = data.get("extract","No encontré información.")
                if "thumbnail" in data:
                    imagen = data["thumbnail"].get("source","")
            else:
                texto = "No se pudo encontrar información 😌"

    return render_template_string(HTML, texto=texto, imagen=imagen)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
