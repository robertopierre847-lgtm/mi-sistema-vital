from flask import Flask, request, render_template_string, jsonify
import requests, random, os

app = Flask(__name__)

# =========================
# 🌍 BUSCADOR WIKIPEDIA
# =========================
def buscar_wiki(q):
    url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + q
    r = requests.get(url)
    if r.status_code != 200:
        return None
    d = r.json()
    return {
        "titulo": d.get("title",""),
        "texto": d.get("extract","No se encontró información."),
        "img": d.get("thumbnail",{}).get("source","")
    }

# =========================
# 🧩 JUEGO DE DECISIONES
# =========================
niveles = [
    {
        "pregunta": "Ves a alguien triste en la escuela ¿qué haces?",
        "opciones": {
            "A": ("Lo ignoras", -1),
            "B": ("Lo escuchas", +2),
            "C": ("Pides ayuda a un adulto", +1)
        }
    },
    {
        "pregunta": "Tienes un examen y no estudiaste",
        "opciones": {
            "A": ("Copiar", -2),
            "B": ("Ser honesto", +2),
            "C": ("Intentar lo que sepas", +1)
        }
    }
]

estado_juego = {"nivel": 0, "puntos": 0}

def opinion_ia(puntos):
    if puntos >= 3:
        return "Buena decisión 👍 estás actuando con madurez."
    elif puntos >= 1:
        return "Vas bien, pero piensa más tus acciones 🤔"
    else:
        return "Cuidado, esas decisiones pueden traerte problemas ⚠️"

# =========================
# 🌙 FRASES RELAJANTES
# =========================
frases = [
    "Respira profundo 🌬️",
    "Todo pasa, esto también",
    "Estás haciendo lo mejor que puedes",
    "Un paso a la vez 💙"
]

# =========================
# 🌐 RUTAS
# =========================
@app.route("/")
def inicio():
    return render_template_string(HTML)

@app.route("/buscar")
def buscar():
    q = request.args.get("q","")
    r = buscar_wiki(q)
    return jsonify(r if r else {})

@app.route("/juego", methods=["POST"])
def juego():
    op = request.json["op"]
    nivel = niveles[estado_juego["nivel"]]
    puntos = nivel["opciones"][op][1]
    estado_juego["puntos"] += puntos
    estado_juego["nivel"] = (estado_juego["nivel"] + 1) % len(niveles)
    return jsonify({
        "puntos": estado_juego["puntos"],
        "opinion": opinion_ia(estado_juego["puntos"]),
        "siguiente": niveles[estado_juego["nivel"]]
    })

@app.route("/relax")
def relax():
    return jsonify({"frase": random.choice(frases)})

# =========================
# 🎨 HTML + ANIMACIONES
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{
background:linear-gradient(135deg,#e3f2fd,#ffffff);
font-family:Arial;
padding:15px;
}
.card{
background:rgba(255,255,255,0.6);
backdrop-filter:blur(10px);
border-radius:15px;
padding:15px;
margin-bottom:15px;
animation:fade 0.6s;
}
button{
background:#2196f3;
color:white;
border:none;
padding:10px;
border-radius:10px;
margin:5px;
transition:transform 0.2s;
}
button:hover{transform:scale(1.05);}
img{max-width:100%;border-radius:10px;}
@keyframes fade{from{opacity:0}to{opacity:1}}
</style>
</head>
<body>

<h2>🔍 Buscador Inteligente</h2>
<div class="card">
<input id="q"><button onclick="buscar()">Buscar</button>
<h3 id="t"></h3>
<img id="img">
<p id="txt"></p>
</div>

<h2>🧩 Juego de Decisiones</h2>
<div class="card">
<p id="preg"></p>
<div id="ops"></div>
<p id="res"></p>
</div>

<h2>🌙 Relajación</h2>
<div class="card">
<button onclick="relax()">Respirar</button>
<p id="fr"></p>
</div>

<p>💪 Mini All Might te apoya</p>

<script>
let nivel = null;

function buscar(){
fetch("/buscar?q="+q.value)
.then(r=>r.json())
.then(d=>{
t.innerText=d.titulo;
txt.innerText=d.texto;
img.src=d.img || "";
});
}

function cargarJuego(d){
preg.innerText=d.pregunta;
ops.innerHTML="";
for(let k in d.opciones){
let b=document.createElement("button");
b.innerText=k;
b.onclick=()=>jugar(k);
ops.appendChild(b);
}
}

function jugar(o){
fetch("/juego",{method:"POST",headers:{'Content-Type':'application/json'},
body:JSON.stringify({op:o})})
.then(r=>r.json())
.then(d=>{
res.innerText=d.opinion+" | Puntos: "+d.puntos;
cargarJuego(d.siguiente);
});
}

function relax(){
fetch("/relax").then(r=>r.json()).then(d=>fr.innerText=d.frase);
}

fetch("/juego",{method:"POST",headers:{'Content-Type':'application/json'},
body:JSON.stringify({op:"A"})}).then(r=>r.json()).then(d=>cargarJuego(d.siguiente));
</script>

</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
