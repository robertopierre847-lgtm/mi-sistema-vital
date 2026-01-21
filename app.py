from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Buscador Vital</title>

<style>
*{box-sizing:border-box}
body{
    margin:0;
    min-height:100vh;
    background:linear-gradient(135deg,#e0f2ff,#f7fbff);
    font-family:system-ui, sans-serif;
    display:flex;
    justify-content:center;
    align-items:center;
}

.app{
    width:95%;
    max-width:420px;
    padding:20px;
    border-radius:22px;
    background:rgba(255,255,255,0.45);
    backdrop-filter:blur(18px);
    box-shadow:0 20px 40px rgba(0,100,255,.15);
    animation:fadeIn .8s ease;
}

@keyframes fadeIn{
    from{opacity:0;transform:translateY(20px)}
    to{opacity:1;transform:none}
}

h1{
    text-align:center;
    color:#1e88e5;
    margin-bottom:10px;
}

p.relax{
    text-align:center;
    font-size:13px;
    color:#555;
    margin-bottom:15px;
}

.search-box{
    display:flex;
    gap:8px;
}

input{
    flex:1;
    padding:12px;
    border-radius:14px;
    border:1px solid #cfe7ff;
    background:rgba(255,255,255,.7);
    font-size:16px;
}

button{
    padding:12px 16px;
    border:none;
    border-radius:14px;
    background:#1e88e5;
    color:white;
    font-size:15px;
    cursor:pointer;
    transition:.2s;
}
button:active{transform:scale(.95)}

#sugerencias{
    margin-top:6px;
}

.sug{
    padding:8px;
    border-radius:10px;
    background:rgba(30,136,229,.08);
    margin-bottom:4px;
    cursor:pointer;
    animation:fadeIn .3s ease;
}

.resultado{
    margin-top:15px;
    font-size:14px;
    color:#333;
    line-height:1.5;
    animation:fadeIn .4s ease;
}

img{
    width:100%;
    border-radius:14px;
    margin-top:10px;
}

/* mini juego */
.juego{
    margin-top:20px;
    padding:15px;
    border-radius:16px;
    background:rgba(30,136,229,.08);
    text-align:center;
}

.word{
    font-weight:bold;
    font-size:18px;
    color:#1e88e5;
}

.puntos{
    margin-top:6px;
    font-size:14px;
}
</style>
</head>

<body>
<div class="app">

<h1>🌤️ Buscador Vital</h1>
<p class="relax">Respira profundo. Aprende algo nuevo.</p>

<div class="search-box">
<input id="q" placeholder="Buscar en Wikipedia...">
<button onclick="buscar()">Buscar</button>
</div>

<div id="sugerencias"></div>
<div id="res" class="resultado"></div>

<div class="juego">
<p>🧠 Juego de palabras</p>
<div class="word" id="palabra"></div>
<input id="resp" placeholder="Escribe la palabra">
<button onclick="verificar()">Probar</button>
<div class="puntos">Puntos: <span id="pts">0</span></div>
</div>

</div>

<script>
let puntos = 0;
const palabras = ["calma","mente","respirar","paz","energia","equilibrio"];

function nuevaPalabra(){
    document.getElementById("palabra").innerText =
        palabras[Math.floor(Math.random()*palabras.length)];
}
nuevaPalabra();

function verificar(){
    let r = document.getElementById("resp").value.toLowerCase();
    let p = document.getElementById("palabra").innerText;
    if(r === p){
        puntos++;
        document.getElementById("pts").innerText = puntos;
        nuevaPalabra();
    }
    document.getElementById("resp").value="";
}

/* BUSCADOR WIKIPEDIA */
const input = document.getElementById("q");
input.addEventListener("input", async ()=>{
    let v = input.value;
    if(v.length < 2){ document.getElementById("sugerencias").innerHTML=""; return; }
    let r = await fetch(
      "https://es.wikipedia.org/w/api.php?action=opensearch&origin=*&search="+v
    );
    let d = await r.json();
    let s = document.getElementById("sugerencias");
    s.innerHTML="";
    d[1].slice(0,5).forEach(t=>{
        let div=document.createElement("div");
        div.className="sug";
        div.innerText=t;
        div.onclick=()=>{ input.value=t; buscar(); s.innerHTML=""; };
        s.appendChild(div);
    });
});

async function buscar(){
    let q = input.value;
    let res = document.getElementById("res");
    res.innerHTML="⏳ Buscando...";
    let r = await fetch(
      "https://es.wikipedia.org/api/rest_v1/page/summary/"+q
    );
    let d = await r.json();
    res.innerHTML = "<b>"+d.title+"</b><p>"+(d.extract||"")+"</p>";
    if(d.thumbnail){
        res.innerHTML += "<img src='"+d.thumbnail.source+"'>";
    }
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
