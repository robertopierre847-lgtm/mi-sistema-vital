from flask import Flask, request, jsonify, render_template_string
import os, json

app = Flask(__name__)

# ================== ARCHIVO ==================
ARCHIVO = "estado.json"

# ================== CARGAR ESTADO ==================
def cargar_estado():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {
            "nivel": 1,
            "vida_gigante": 300,
            "finalizado": False
        }

# ================== GUARDAR ESTADO ==================
def guardar_estado(estado):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(estado, f)
    except:
        pass  # evita error 500

estado = cargar_estado()

# ================== PREGUNTAS ==================
preguntas = []
for i in range(1, 31):
    preguntas.append({
        "p": f"Nivel {i}: ¿Qué acción demuestra mayor inteligencia emocional?",
        "o": [
            "Pensar antes de actuar",
            "Gritar",
            "Culpar a otros",
            "Ignorar el problema"
        ],
        "c": 0
    })

# ================== RANGO ==================
def calcular_rango(vida):
    if vida <= 0:
        return "🟢 RANGO S – Mente lógica superior"
    elif vida <= 60:
        return "🔵 RANGO A – Muy buen criterio"
    elif vida <= 140:
        return "🟡 RANGO B – Buen razonamiento"
    elif vida <= 220:
        return "🟠 RANGO C – Impulsivo"
    else:
        return "🔴 RANGO D – Necesita mejorar"

# ================== API ==================
@app.route("/estado")
def api_estado():
    return jsonify(estado)

@app.route("/pregunta")
def api_pregunta():
    return jsonify(preguntas[estado["nivel"] - 1])

@app.route("/responder", methods=["POST"])
def responder():
    data = request.json
    correcta = data.get("correcta", False)

    if estado["nivel"] < 30:
        if correcta:
            estado["nivel"] += 1
    else:
        # JEFE FINAL
        if correcta:
            estado["vida_gigante"] -= 25
        else:
            estado["vida_gigante"] += 15

        estado["vida_gigante"] = max(0, min(300, estado["vida_gigante"]))

        if estado["vida_gigante"] == 0:
            estado["finalizado"] = True

    guardar_estado(estado)
    return jsonify(estado)

@app.route("/rango")
def rango():
    return jsonify({"rango": calcular_rango(estado["vida_gigante"])})

# ================== HTML ==================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>MENTISCOPE 474</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body{
background:linear-gradient(135deg,#eaf4ff,#ffffff);
font-family:Arial;
padding:20px;
}
.card{
max-width:520px;
margin:auto;
background:white;
padding:20px;
border-radius:18px;
box-shadow:0 15px 30px rgba(0,0,0,.15);
animation:fade .6s;
}
@keyframes fade{
from{opacity:0;transform:translateY(20px);}
to{opacity:1;}
}
button{
width:100%;
padding:12px;
margin:6px 0;
border:none;
border-radius:12px;
background:#0077ff;
color:white;
font-size:16px;
}
.bar{
height:16px;
background:#ddd;
border-radius:10px;
overflow:hidden;
}
.fill{
height:100%;
background:#ff4444;
transition:.4s;
}
#gigante{
font-size:64px;
text-align:center;
}
.result{
margin-top:15px;
padding:12px;
background:#f1f7ff;
border-radius:12px;
font-weight:bold;
text-align:center;
}
</style>
</head>

<body>
<div class="card">
<h1>🧠 MENTISCOPE 474</h1>

<p id="nivel"></p>
<p id="pregunta"></p>
<div id="ops"></div>

<div id="final" style="display:none;">
<h2>👹 JEFE FINAL</h2>
<div id="gigante">🗿</div>
<div class="bar"><div class="fill" id="vida"></div></div>
</div>

<div id="resultado"></div>
</div>

<script>
const nivel=document.getElementById("nivel");
const pregunta=document.getElementById("pregunta");
const ops=document.getElementById("ops");
const vida=document.getElementById("vida");
const final=document.getElementById("final");
const resultado=document.getElementById("resultado");

function cargar(){
fetch("/estado").then(r=>r.json()).then(e=>{
nivel.innerText="Nivel "+e.nivel;
if(e.nivel==30){
final.style.display="block";
vida.style.width=(e.vida_gigante/300*100)+"%";
}
if(e.finalizado){
fetch("/rango").then(r=>r.json()).then(d=>{
resultado.innerHTML='<div class="result">'+d.rango+'</div>';
});
}
});

fetch("/pregunta").then(r=>r.json()).then(p=>{
pregunta.innerText=p.p;
ops.innerHTML="";
p.o.forEach((t,i)=>{
let b=document.createElement("button");
b.innerText=t;
b.onclick=()=>responder(i==p.c);
ops.appendChild(b);
});
});
}

function responder(c){
fetch("/responder",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({correcta:c})
}).then(()=>cargar());
}

cargar();
</script>
</body>
</html>
"""

# ================== RUN ==================
@app.route("/")
def inicio():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
