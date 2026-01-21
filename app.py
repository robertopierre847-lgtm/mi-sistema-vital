from flask import Flask, request, render_template_string, jsonify
import json, os

app = Flask(__name__)

# =========================
# 📂 GUARDADO
# =========================
ARCHIVO = "progreso.json"

def cargar():
    if os.path.exists(ARCHIVO):
        return json.load(open(ARCHIVO, "r", encoding="utf-8"))
    return {"nivel": 1, "puntos": 0, "vida": 100}

def guardar(data):
    json.dump(data, open(ARCHIVO, "w", encoding="utf-8"), ensure_ascii=False)

estado = cargar()

# =========================
# 🧩 PREGUNTAS (30)
# =========================
preguntas = [
    {"p":"Si ayudas a alguien sin esperar nada, ¿qué demuestras?",
     "o":["Interés","Empatía","Miedo"], "r":1},
    {"p":"Decir la verdad aunque cueste es señal de…",
     "o":["Debilidad","Valentía","Problemas"], "r":1},
]

# rellenar hasta 30
while len(preguntas) < 30:
    preguntas.append(preguntas[-1])

# =========================
# 🌐 RUTAS
# =========================
@app.route("/")
def inicio():
    return render_template_string(HTML)

@app.route("/estado")
def ver_estado():
    return jsonify(estado)

@app.route("/responder", methods=["POST"])
def responder():
    global estado
    data = request.json
    nivel = estado["nivel"] - 1
    correcta = preguntas[nivel]["r"]

    if data["op"] == correcta:
        estado["puntos"] += 5
        if estado["nivel"] == 30:
            estado["vida"] -= 10
        else:
            estado["nivel"] += 1
        ok = True
    else:
        estado["puntos"] -= 2
        if estado["nivel"] == 30:
            estado["vida"] += 5
        ok = False

    if estado["vida"] < 0: estado["vida"] = 0
    if estado["vida"] > 100: estado["vida"] = 100

    guardar(estado)
    return jsonify({"ok": ok, "estado": estado})

# =========================
# 🎨 HTML + CSS + JS
# =========================
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MENTISCOPE 474</title>
<style>
body{
margin:0;font-family:Arial;
background:linear-gradient(135deg,#e6f4ff,#fff);
}
.card{
max-width:420px;margin:20px auto;
background:rgba(255,255,255,.75);
backdrop-filter:blur(10px);
border-radius:20px;padding:20px;
box-shadow:0 10px 30px rgba(0,0,0,.1);
}
h1{text-align:center;color:#0077ff}
button{
width:100%;padding:12px;margin-top:10px;
border:none;border-radius:14px;
background:#0077ff;color:white;font-size:16px;
}
button:hover{transform:scale(1.03)}
.personaje{
width:60px;height:60px;border-radius:50%;
background:#0077ff;margin:auto;
box-shadow:0 0 15px #0077ff;
}
.gigante{
width:100px;height:100px;border-radius:20px;
background:#444;margin:auto;
transition:.3s;
}
.vibrar{animation:vib .2s}
@keyframes vib{
0%{transform:translateX(-5px)}
50%{transform:translateX(5px)}
}
.barra{
height:15px;background:#ddd;border-radius:10px;
overflow:hidden;margin-top:10px;
}
.vida{
height:100%;background:red;width:100%;
transition:.4s;
}
</style>
</head>
<body>

<div class="card">
<h1>🧠 MENTISCOPE 474</h1>

<div class="personaje"></div>
<p id="nivel"></p>
<p id="pregunta"></p>
<div id="ops"></div>

<div id="boss" style="display:none">
<div class="gigante" id="gig"></div>
<div class="barra"><div class="vida" id="vida"></div></div>
</div>

<p id="msg"></p>
</div>

<script>
let estado;

function cargar(){
fetch("/estado").then(r=>r.json()).then(d=>{
estado=d;
document.getElementById("nivel").innerText="Nivel "+estado.nivel;
if(estado.nivel==30){
document.getElementById("boss").style.display="block";
document.getElementById("vida").style.width=estado.vida+"%";
}
mostrar();
});
}

function mostrar(){
let p={{ preguntas|tojson }}[estado.nivel-1];
pregunta.innerText=p.p;
ops.innerHTML="";
p.o.forEach((t,i)=>{
let b=document.createElement("button");
b.innerText=t;
b.onclick=()=>responder(i);
ops.appendChild(b);
});
}

function responder(i){
fetch("/responder",{method:"POST",
headers:{'Content-Type':'application/json'},
body:JSON.stringify({op:i})})
.then(r=>r.json()).then(d=>{
estado=d.estado;
msg.innerText=d.ok?"✔ Correcto":"❌ Incorrecto";
if(estado.nivel==30){
vida.style.width=estado.vida+"%";
gig.classList.add("vibrar");
setTimeout(()=>gig.classList.remove("vibrar"),200);
}
cargar();
});
}

cargar();
</script>
</body>
</html>
"""

# =========================
# ▶ RUN (RENDER)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
