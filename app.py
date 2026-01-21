from flask import Flask, request, render_template_string
import json, os, random

app = Flask(__name__)

# ================== MEMORIA ==================
ARCHIVO = "mentiscope_memoria.json"

if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        historial = json.load(f)
else:
    historial = []

# ================== LÓGICA 474 ==================
PALABRAS_SOSPECHOSAS = [
    "creo", "tal vez", "no recuerdo", "más o menos",
    "supongo", "quizás", "nunca", "siempre"
]

PREGUNTAS_SEGUIMIENTO = [
    "¿Puedes dar más detalles?",
    "¿Cuándo ocurrió exactamente?",
    "¿Alguien más puede confirmarlo?",
    "¿Por qué estás seguro de eso?",
    "¿Cambiarías algo de tu respuesta?"
]

def analizar_frase(texto):
    texto_l = texto.lower()
    puntos = 50

    if len(texto) < 15:
        puntos -= 15
    if len(texto) > 120:
        puntos -= 10

    sospechas = [p for p in PALABRAS_SOSPECHOSAS if p in texto_l]
    puntos -= len(sospechas) * 5

    if "porque" in texto_l or "ya que" in texto_l:
        puntos += 10

    if puntos >= 70:
        estado = "🟢 PROBABLEMENTE VERDAD"
        mood = "calm"
    elif puntos >= 45:
        estado = "🟡 DUDOSO"
        mood = "think"
    else:
        estado = "🔴 PROBABLEMENTE MENTIRA"
        mood = "alert"

    return {
        "puntos": max(0, min(100, puntos)),
        "estado": estado,
        "sospechas": sospechas,
        "pregunta": random.choice(PREGUNTAS_SEGUIMIENTO),
        "mood": mood
    }

# ================== RUTA ==================
@app.route("/", methods=["GET", "POST"])
def inicio():
    resultado = None

    if request.method == "POST":
        frase = request.form.get("frase", "").strip()
        if frase:
            resultado = analizar_frase(frase)
            historial.append({
                "frase": frase,
                "resultado": resultado["estado"],
                "puntos": resultado["puntos"]
            })
            with open(ARCHIVO, "w", encoding="utf-8") as f:
                json.dump(historial, f, ensure_ascii=False, indent=2)

    return render_template_string(HTML, resultado=resultado, historial=historial[-5:])

# ================== HTML ==================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MENTISCOPE 474</title>

<style>
body{
    background: linear-gradient(135deg,#e6f4ff,#ffffff);
    font-family: Arial;
    padding: 20px;
}

.card{
    background: rgba(255,255,255,0.85);
    border-radius: 18px;
    padding: 20px;
    max-width: 520px;
    margin: auto;
    box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    animation: fade 0.6s ease;
}

h1{
    text-align:center;
    color:#0077ff;
}

textarea{
    width:100%;
    padding:12px;
    border-radius:12px;
    border:1px solid #aac;
    resize:none;
}

button{
    width:100%;
    padding:14px;
    margin-top:10px;
    border:none;
    border-radius:14px;
    background:#0077ff;
    color:white;
    font-size:16px;
}

.res{
    margin-top:15px;
    padding:14px;
    border-radius:14px;
    background:#f1f8ff;
    animation: slide 0.5s ease;
}

.bar{
    height:12px;
    background:#ddd;
    border-radius:10px;
    overflow:hidden;
    margin:8px 0;
}
.fill{
    height:100%;
    background:linear-gradient(90deg,#00c6ff,#0072ff);
    width:0%;
    transition:width 0.8s ease;
}

.inspector{
    text-align:center;
    font-size:60px;
    margin-bottom:10px;
}

@keyframes fade{
    from{opacity:0;transform:scale(0.95)}
    to{opacity:1;transform:scale(1)}
}
@keyframes slide{
    from{opacity:0;transform:translateY(10px)}
    to{opacity:1;transform:translateY(0)}
}
</style>
</head>

<body>

<div class="card">
<h1>🧠 MENTISCOPE 474</h1>

<form method="post">
<textarea name="frase" rows="4" placeholder="Escribe tu afirmación..."></textarea>
<button>Analizar</button>
</form>

{% if resultado %}
<div class="res">

<div class="inspector">
{% if resultado.mood == "calm" %}🕵️‍♂️
{% elif resultado.mood == "think" %}🤔
{% else %}🚨{% endif %}
</div>

<b>{{resultado.estado}}</b><br>

<div class="bar">
  <div class="fill" style="width:{{resultado.puntos}}%"></div>
</div>

<b>Puntuación lógica:</b> {{resultado.puntos}} / 100<br>

{% if resultado.sospechas %}
<b>Palabras sospechosas:</b> {{resultado.sospechas}}<br>
{% endif %}

<b>Pregunta:</b> {{resultado.pregunta}}

</div>
{% endif %}

<hr>
<small>Últimos análisis:</small>
<ul>
{% for h in historial %}
<li>{{h.frase}} → {{h.resultado}}</li>
{% endfor %}
</ul>

</div>
</body>
</html>
"""

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
