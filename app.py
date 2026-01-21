from flask import Flask, request, jsonify, render_template_string
import os, json

app = Flask(__name__)

# ================== ESTADO ==================
ARCHIVO = "mentiscope_save.json"

if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        estado = json.load(f)
else:
    estado = {
        "nivel": 1,
        "vida_gigante": 300,
        "finalizado": False
    }

def guardar():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(estado, f)

# ================== PREGUNTAS ==================
preguntas = []
for i in range(1, 31):
    preguntas.append({
        "p": f"Nivel {i}: ¿Qué decisión demuestra mayor control emocional?",
        "o": [
            "Pensar antes de actuar",
            "Responder con rabia",
            "Echar la culpa",
            "Ignorar el problema"
        ],
        "c": 0
    })

# ================== RANKING ==================
def calcular_rango():
    vida = estado["vida_gigante"]
    if vida <= 0:
        return "🟢 RANGO S – Lógica excelente"
    elif vida <= 50:
        return "🔵 RANGO A – Muy buen razonamiento"
    elif vida <= 120:
        return "🟡 RANGO B – Buen trabajo"
    elif vida <= 200:
        return "🟠 RANGO C – Respuestas impulsivas"
    else:
        return "🔴 RANGO D – Necesitas reflexionar más"

# ================== API ==================
@app.route("/estado")
def get_estado():
    return jsonify(estado)

@app.route("/pregunta")
def get_pregunta():
    return jsonify(preguntas[estado["nivel"] - 1])

@app.route("/responder", methods=["POST"])
def responder():
    data = request.json
    correcta = data["correcta"]

    if estado["nivel"] < 30:
        if correcta:
            estado["nivel"] += 1
    else:
        # JEFE FINAL
        if correcta:
            estado["vida_gigante"] -= 30
        else:
            estado["vida_gigante"] += 20

        estado["vida_gigante"] = max(0, min(300, estado["vida_gigante"]))

        if estado["vida_gigante"] == 0:
            estado["finalizado"] = True

    guardar()
    return jsonify(estado)

@app.route("/rango")
def rango():
    return jsonify({"rango": calcular_rango()})

# ================== HTML ==================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MENTISCOPE 474</title>

<style>
body{
background:linear-gradient(135deg,#eef6ff,#ffffff);
font-family:Arial;
padding:20px;
}
.card{
max-width:500px;
margin:auto;
background:white;
border-radius:18px;
padding:20px;
box-shadow:0 15px 35px rgba(0,0,0,.15);
animation:fade .8s;
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
background:#0066ff;
color:white;
font-size:16px;
}
#gigante{
font-size:60px;
text-align:center;
animation:shake .8s infinite alternate;
}
@keyframes shake{
from{transform:translateX(-3px);}
to{transform:translateX(3px);}
}
.bar{
height:18px;
background:#ddd;
border-radius:10px;
overflow:hidden;
}
.fill{
height:100%;
background:#ff4444;
transition:.4s;
}
.rango{
margin-top:15px;
padding:12px;
border-radius:10px;
background:#f1f7ff;
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
resultado.innerHTML='<div class="rango">'+d.rango+'</div>';
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
