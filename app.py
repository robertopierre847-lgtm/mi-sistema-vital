from flask import Flask, request, render_template_string
import random, json, os, time

app = Flask(__name__)

# ===============================
# 🧠 ARCHIVO DE MEMORIA
# ===============================
ARCHIVO = "mentiscope_memoria.json"

if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        HISTORIAL = json.load(f)
else:
    HISTORIAL = []

# ===============================
# 🧩 CASOS PSICOLÓGICOS AVANZADOS
# ===============================
CASOS = [
    {
        "caso": "Dijiste que llegaste tarde porque había tráfico, pero nadie más llegó tarde.",
        "claves": ["porque", "tráfico"],
        "riesgo": 15
    },
    {
        "caso": "Afirmas que olvidaste algo importante, pero recuerdas muchos detalles.",
        "claves": ["olvidé", "no recuerdo"],
        "riesgo": 20
    },
    {
        "caso": "Dices que siempre actúas bien, incluso cuando nadie te observa.",
        "claves": ["siempre", "nunca"],
        "riesgo": 25
    },
    {
        "caso": "Cambias ligeramente tu historia cuando te hacen la misma pregunta.",
        "claves": ["tal vez", "creo"],
        "riesgo": 30
    }
]

PALABRAS_SOSPECHOSAS = [
    "creo", "tal vez", "quizás", "supongo",
    "no recuerdo", "más o menos", "siempre", "nunca"
]

PREGUNTAS_PRESION = [
    "¿Responderías igual si alguien pudiera comprobarlo?",
    "¿Qué parte de tu historia cambiarías ahora?",
    "¿Por qué esta respuesta te parece segura?",
    "¿Qué pasaría si estuvieras equivocado?",
    "¿Alguien más confirmaría esto sin dudar?"
]

# ===============================
# 🔍 LÓGICA 474 AVANZADA
# ===============================
def analizar_mente(texto):
    texto_l = texto.lower()
    puntuacion = 74  # base 474 reducida
    alertas = []

    # Longitud
    if len(texto) < 20:
        puntuacion -= 15
        alertas.append("respuesta breve")
    if len(texto) > 160:
        puntuacion -= 10
        alertas.append("exceso de detalle")

    # Palabras sospechosas
    for p in PALABRAS_SOSPECHOSAS:
        if p in texto_l:
            puntuacion -= 6
            alertas.append(p)

    # Seguridad aparente
    if "porque" in texto_l or "ya que" in texto_l:
        puntuacion += 8

    # Casos mentales
    caso = random.choice(CASOS)
    for c in caso["claves"]:
        if c in texto_l:
            puntuacion -= caso["riesgo"]

    # Estado final
    if puntuacion >= 80:
        estado = "🟢 COHERENCIA ALTA"
    elif puntuacion >= 55:
        estado = "🟡 INESTABILIDAD DETECTADA"
    else:
        estado = "🔴 NARRATIVA COMPROMETIDA"

    return {
        "puntos": max(0, min(100, puntuacion)),
        "estado": estado,
        "alertas": list(set(alertas)),
        "caso": caso["caso"],
        "pregunta": random.choice(PREGUNTAS_PRESION)
    }

# ===============================
# 🌐 RUTA PRINCIPAL
# ===============================
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        frase = request.form.get("frase", "").strip()

        if frase:
            resultado = analizar_mente(frase)

            HISTORIAL.append({
                "frase": frase,
                "estado": resultado["estado"],
                "puntos": resultado["puntos"],
                "time": int(time.time())
            })

            with open(ARCHIVO, "w", encoding="utf-8") as f:
                json.dump(HISTORIAL, f, ensure_ascii=False, indent=2)

    return render_template_string(HTML, resultado=resultado, historial=HISTORIAL[-5:])

# ===============================
# 🎨 HTML NOIR PSICOLÓGICO
# ===============================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MENTISCOPE 474</title>
<style>
body{
    background:#0b0e13;
    color:#e6e9ef;
    font-family:Arial, sans-serif;
}
.card{
    max-width:480px;
    margin:40px auto;
    padding:20px;
    background:#1c2330;
    border-radius:18px;
    box-shadow:0 0 40px rgba(0,0,0,0.6);
    animation:fade 0.8s;
}
h1{
    text-align:center;
    color:#4da3ff;
}
textarea{
    width:100%;
    padding:12px;
    border-radius:12px;
    border:none;
    background:#0f2a44;
    color:white;
}
button{
    width:100%;
    margin-top:12px;
    padding:14px;
    background:#4da3ff;
    border:none;
    border-radius:14px;
    font-size:16px;
    color:black;
    cursor:pointer;
    transition:transform 0.2s;
}
button:hover{transform:scale(1.03);}
.res{
    margin-top:18px;
    padding:15px;
    background:#0f2a44;
    border-radius:12px;
    animation:fade 0.6s;
}
small{color:#9aa4b2;}
.bar{
    height:10px;
    background:#111;
    border-radius:8px;
    overflow:hidden;
    margin:6px 0;
}
.fill{
    height:100%;
    background:#4da3ff;
}
@keyframes fade{from{opacity:0;transform:translateY(10px)}to{opacity:1}}
</style>
</head>
<body>

<div class="card">
<h1>🧠 MENTISCOPE 474</h1>
<small>Inspector 474 activo</small>

<form method="post">
<textarea name="frase" rows="4" placeholder="Expón tu afirmación con cuidado..."></textarea>
<button>ANALIZAR</button>
</form>

{% if resultado %}
<div class="res">
<b>Veredicto:</b> {{resultado.estado}}<br>
<b>Coherencia mental:</b>
<div class="bar"><div class="fill" style="width:{{resultado.puntos}}%"></div></div>

<small>Caso activo:</small><br>
<i>{{resultado.caso}}</i><br><br>

{% if resultado.alertas %}
<b>Indicadores:</b> {{resultado.alertas}}<br>
{% endif %}

<b>Pregunta 474:</b><br>
{{resultado.pregunta}}
</div>
{% endif %}

<hr>
<small>Últimos registros</small>
<ul>
{% for h in historial %}
<li>{{h.frase[:40]}}… → {{h.estado}}</li>
{% endfor %}
</ul>

</div>
</body>
</html>
"""

# ===============================
# 🚀 RUN (RENDER SAFE)
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
