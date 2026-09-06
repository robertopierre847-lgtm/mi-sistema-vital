import os
import random
import unicodedata
from urllib.parse import quote

import requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# ============================================================
# ADE VITAL 2.0 - IA EDUCATIVA EN UNA ESFERA
# ============================================================

PREGUNTAS = [
    {"q": "¿Cuál es el planeta más grande del sistema solar?", "a": "jupiter", "opts": ["Júpiter", "Marte", "Venus"]},
    {"q": "¿Cuántos lados tiene un hexágono?", "a": "6", "opts": ["5", "6", "8"]},
    {"q": "¿Quién escribió Don Quijote de la Mancha?", "a": "miguel de cervantes", "opts": ["Miguel de Cervantes", "Gabriel García Márquez", "Pablo Neruda"]},
    {"q": "¿Qué gas necesitan principalmente las plantas para realizar la fotosíntesis?", "a": "dioxido de carbono", "opts": ["Oxígeno", "Dióxido de carbono", "Helio"]},
]

SONIDOS = [
    {"s": "🐶 ¡Guau, guau!", "a": "perro", "opts": ["Perro", "Gato", "Vaca"]},
    {"s": "🐄 ¡Muuuu!", "a": "vaca", "opts": ["Caballo", "Vaca", "Oveja"]},
    {"s": "🐱 ¡Miauuu!", "a": "gato", "opts": ["Gato", "Perro", "León"]},
]

def normalizar(texto):
    texto = unicodedata.normalize("NFD", str(texto).lower().strip())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")

HTML = r"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ADE VITAL 2.0</title>
<style>
*{box-sizing:border-box}
:root{
 --accent:#00d9ff;--accent2:#7b2cff;--bg:#050817;
 --glass:rgba(7,13,35,.72);--text:#eafaff
}
body{
 margin:0;min-height:100vh;color:var(--text);
 font-family:Segoe UI,Arial,sans-serif;background:var(--bg);
 overflow-x:hidden;transition:background .5s;
}
#universe{position:fixed;inset:0;z-index:-5;overflow:hidden}
.stars{
 position:absolute;inset:-20%;
 background-image:
 radial-gradient(circle at 20% 30%,rgba(0,220,255,.55) 0 1px,transparent 2px),
 radial-gradient(circle at 70% 20%,rgba(255,255,255,.8) 0 1px,transparent 2px),
 radial-gradient(circle at 45% 80%,rgba(150,80,255,.7) 0 1px,transparent 2px);
 background-size:90px 90px,130px 130px,170px 170px;
 animation:drift 25s linear infinite;
}
.nebula{
 position:absolute;width:60vw;height:60vw;border-radius:50%;
 background:radial-gradient(circle,rgba(92,42,255,.28),rgba(0,210,255,.08),transparent 70%);
 filter:blur(25px);left:-10%;top:5%;animation:float 8s ease-in-out infinite;
}
.nebula.two{left:auto;right:-15%;top:35%;background:radial-gradient(circle,rgba(0,240,210,.2),rgba(100,30,255,.1),transparent 70%);animation-delay:-4s}
.floating{position:absolute;font-size:26px;opacity:.25;animation:float 7s ease-in-out infinite}
.f1{left:12%;top:20%}.f2{right:14%;top:17%;animation-delay:-2s}.f3{left:7%;bottom:20%;animation-delay:-4s}.f4{right:8%;bottom:16%;animation-delay:-1s}
@keyframes drift{to{transform:translate(70px,40px)}}
@keyframes float{50%{transform:translateY(-25px) rotate(8deg)}}
.app{
 width:min(1400px,96vw);min-height:94vh;margin:3vh auto;
 display:grid;grid-template-columns:220px 1fr 240px;gap:14px;
}
.panel,.topbar,.bottom,.chat,.hero{
 background:var(--glass);border:1px solid rgba(0,217,255,.25);
 box-shadow:0 0 35px rgba(0,180,255,.08),inset 0 0 30px rgba(255,255,255,.02);
 backdrop-filter:blur(18px);border-radius:22px;
}
.sidebar{padding:18px;display:flex;flex-direction:column;gap:10px}
.logo{font-size:22px;font-weight:900;color:var(--accent);text-shadow:0 0 15px var(--accent)}
.tag{font-size:10px;letter-spacing:3px;opacity:.65;margin-bottom:18px}
.nav{
 padding:13px;border:1px solid transparent;border-radius:13px;
 color:#cfe9f5;background:transparent;text-align:left;cursor:pointer;font-size:14px;
 transition:.25s
}
.nav:hover,.nav.active{border-color:var(--accent);background:rgba(0,217,255,.1);transform:translateX(4px);color:white}
.profile{margin-top:auto;padding:14px;border-radius:16px;background:rgba(255,255,255,.04)}
.level{height:7px;border-radius:20px;background:#18243c;overflow:hidden;margin-top:8px}
.level i{display:block;width:72%;height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));box-shadow:0 0 12px var(--accent)}
.main{display:flex;flex-direction:column;gap:14px}
.topbar{height:58px;padding:0 18px;display:flex;align-items:center;justify-content:space-between}
.clock{font-weight:800;color:var(--accent)}
.quote{font-size:12px;opacity:.8}
.hero{flex:1;min-height:520px;position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden}
.hero:before{
 content:"";position:absolute;width:500px;height:500px;border-radius:50%;
 background:radial-gradient(circle,rgba(0,217,255,.12),transparent 62%);
 animation:pulse 3s ease-in-out infinite
}
@keyframes pulse{50%{transform:scale(1.12);opacity:.7}}
.orb{
 width:245px;height:245px;border-radius:50%;position:relative;z-index:2;
 display:flex;align-items:center;justify-content:center;
 background:radial-gradient(circle at 35% 30%,#263b72 0,#090f29 42%,#02040d 75%);
 border:2px solid var(--accent);
 box-shadow:0 0 25px var(--accent),0 0 80px rgba(0,217,255,.35),inset 0 0 45px rgba(0,217,255,.25);
 animation:orb 4s ease-in-out infinite
}
.orb:after,.orb:before{
 content:"";position:absolute;inset:-25px;border:2px solid var(--accent);
 border-radius:50%;opacity:.5;transform:rotateX(70deg) rotateZ(20deg);
 animation:ring 4s linear infinite
}
.orb:after{inset:-45px;opacity:.22;animation-duration:7s;transform:rotateX(72deg) rotateZ(-35deg)}
@keyframes orb{50%{transform:translateY(-8px) scale(1.025)}}
@keyframes ring{to{transform:rotateX(70deg) rotateZ(380deg)}}
.face{font-size:58px;color:var(--accent);text-shadow:0 0 20px var(--accent)}
.ade-name{font-size:32px;font-weight:900;letter-spacing:6px;color:white;text-shadow:0 0 18px var(--accent);margin-top:20px}
.status{color:var(--accent);font-size:12px;letter-spacing:2px;margin-top:7px}
.quick{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:25px;z-index:3}
.quick button,.send{
 border:1px solid var(--accent);background:rgba(0,217,255,.08);color:white;
 padding:9px 13px;border-radius:999px;cursor:pointer
}
.quick button:hover{background:rgba(0,217,255,.2);box-shadow:0 0 15px rgba(0,217,255,.25)}
.chat{padding:10px;display:flex;gap:10px}
#input{flex:1;background:rgba(0,0,0,.3);border:1px solid #203b55;color:white;border-radius:13px;padding:14px;outline:none}
.send{width:52px;background:var(--accent);color:#001018;font-weight:900}
.messages{position:absolute;left:18px;bottom:18px;width:min(370px,70%);z-index:4}
.msg{padding:12px 15px;border-radius:15px;margin-top:8px;font-size:13px;line-height:1.4;background:rgba(2,8,20,.85);border:1px solid rgba(0,217,255,.2)}
.msg.user{border-color:var(--accent);text-align:right}
.right{padding:16px;display:flex;flex-direction:column;gap:12px}
.section-title{font-weight:800;color:var(--accent);font-size:14px}
.theme{padding:10px;border-radius:13px;border:1px solid #23425b;background:rgba(255,255,255,.03);cursor:pointer}
.theme:hover{border-color:var(--accent);transform:scale(1.02)}
.theme b{display:block}.theme span{font-size:11px;opacity:.6}
.card{padding:13px;border-radius:15px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07)}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.stat{text-align:center;padding:10px;border-radius:12px;background:rgba(0,217,255,.05)}
.stat strong{display:block;font-size:20px;color:var(--accent)}
.bottom{padding:12px;display:grid;grid-template-columns:repeat(5,1fr);gap:8px}
.mode{
 padding:12px 5px;border:1px solid transparent;background:transparent;color:white;border-radius:13px;cursor:pointer
}
.mode:hover{border-color:var(--accent);background:rgba(0,217,255,.08)}
.game-options{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:12px;z-index:5}
.game-options button{padding:10px 14px;border:1px solid var(--accent);border-radius:12px;background:#07182a;color:white;cursor:pointer}
@media(max-width:950px){.app{grid-template-columns:1fr}.sidebar,.right{display:none}.hero{min-height:560px}.bottom{grid-template-columns:repeat(5,1fr)}}
@media(max-width:550px){.app{width:100%;margin:0;min-height:100vh}.topbar{border-radius:0}.hero{border-radius:0;min-height:560px}.orb{width:190px;height:190px}.face{font-size:45px}.ade-name{font-size:25px}.bottom{border-radius:0}.mode{font-size:11px}.messages{width:85%}}
</style>
</head>
<body>
<div id="universe">
 <div class="stars"></div><div class="nebula"></div><div class="nebula two"></div>
 <div class="floating f1">✦</div><div class="floating f2">◈</div><div class="floating f3">✧</div><div class="floating f4">⬡</div>
</div>

<div class="app">
 <aside class="panel sidebar">
   <div class="logo">✦ ADE VITAL</div>
   <div class="tag">TU MENTE, SIN LÍMITES</div>
   <button class="nav active" onclick="home()">⌂ Inicio</button>
   <button class="nav" onclick="focusInput()">◉ Chat IA</button>
   <button class="nav" onclick="startGame('trivia')">🎮 Juegos</button>
   <button class="nav" onclick="lab()">⚗ Laboratorio</button>
   <button class="nav" onclick="explore()">◎ Explorar</button>
   <button class="nav" onclick="wiki()">▣ Biblioteca</button>
   <button class="nav" onclick="progress()">▥ Progreso</button>
   <div class="profile">
     <b>👤 Estudiante</b><br><small>Nivel 12 · 2,450 XP</small>
     <div class="level"><i></i></div>
   </div>
 </aside>

 <main class="main">
   <div class="topbar">
     <div class="clock" id="clock">--:--</div>
     <div class="quote">“El conocimiento abre nuevos mundos.”</div>
     <div>⚡ <b id="xp">2450</b> XP</div>
   </div>

   <section class="hero">
     <div class="orb" id="orb"><div class="face">◡‿◡</div></div>
     <div class="ade-name">ADE</div>
     <div class="status" id="status">● SISTEMA EDUCATIVO ACTIVO</div>
     <div class="quick">
       <button onclick="ask('¿Qué es la gravedad?')">¿Qué es la gravedad?</button>
       <button onclick="ask('Dame un resumen de historia')">Resumen de historia</button>
       <button onclick="startGame('trivia')">Desafío escolar</button>
     </div>
     <div class="game-options" id="options"></div>
     <div class="messages" id="messages">
       <div class="msg"><b>Hola, soy ADE.</b> 🤖<br>Pregunta, estudia, juega o explora. Mi universo educativo está listo.</div>
     </div>
   </section>

   <div class="chat">
     <input id="input" placeholder="Escribe tu pregunta o elige una misión..." onkeydown="if(event.key==='Enter')send()">
     <button class="send" onclick="send()">➤</button>
   </div>

   <div class="bottom">
     <button class="mode" onclick="startGame('trivia')">🎮<br>Juegos</button>
     <button class="mode" onclick="lab()">🧪<br>Laboratorio</button>
     <button class="mode" onclick="explore()">🌎<br>Explorar</button>
     <button class="mode" onclick="wiki()">📚<br>Biblioteca</button>
     <button class="mode" onclick="progress()">🏆<br>Progreso</button>
   </div>
 </main>

 <aside class="panel right">
   <div class="section-title">🌌 FONDOS DISPONIBLES</div>
   <div class="theme" onclick="theme('space')"><b>🌌 Cosmos</b><span>Nebulosas y estrellas</span></div>
   <div class="theme" onclick="theme('nature')"><b>🌿 Naturaleza</b><span>Modo explorador</span></div>
   <div class="theme" onclick="theme('ocean')"><b>🌊 Océano</b><span>Profundidades</span></div>
   <div class="theme" onclick="theme('science')"><b>🧬 Ciencia</b><span>Moléculas y energía</span></div>
   <div class="theme" onclick="theme('history')"><b>🏛 Historia</b><span>Civilizaciones</span></div>
   <div class="theme" onclick="theme('cyber')"><b>💠 Cyber</b><span>Ciudad digital</span></div>
   <div class="section-title" style="margin-top:8px">📊 HOY</div>
   <div class="stats">
     <div class="stat"><strong id="score">0</strong><small>Puntos</small></div>
     <div class="stat"><strong id="answers">0</strong><small>Acertadas</small></div>
   </div>
   <div class="card">🔥 <b>Racha</b><br><small>¡Sigue aprendiendo!</small></div>
   <div class="card">💡 <b>Misión</b><br><small>Responde 3 desafíos educativos.</small></div>
 </aside>
</div>

<script>
let mode="chat", correct="", score=0, answers=0;

function clock(){
 const d=new Date();
 document.getElementById("clock").textContent=d.toLocaleTimeString("es-DO",{hour:"2-digit",minute:"2-digit"});
}
setInterval(clock,1000);clock();

function add(type,text){
 const box=document.getElementById("messages");
 const div=document.createElement("div");
 div.className="msg "+type;
 div.textContent=text;
 box.appendChild(div);
 while(box.children.length>4) box.removeChild(box.firstChild);
}

function focusInput(){document.getElementById("input").focus()}
function ask(t){document.getElementById("input").value=t;send()}
function setStatus(t){document.getElementById("status").textContent="● "+t}

async function send(custom=null){
 const input=document.getElementById("input");
 const msg=(custom??input.value).trim();
 if(!msg)return;
 add("user",msg); input.value="";
 document.getElementById("options").innerHTML="";
 setStatus("ADE ESTÁ PENSANDO...");
 document.getElementById("orb").style.filter="brightness(1.5)";

 try{
  const r=await fetch("/api/ade",{
   method:"POST",headers:{"Content-Type":"application/json"},
   body:JSON.stringify({msg,mode,correct})
  });
  const data=await r.json();
  add("ade",data.text);
  mode=data.mode||"chat"; correct=data.correct||"";
  if(data.options){
   const box=document.getElementById("options");
   data.options.forEach(o=>{
    const b=document.createElement("button");
    b.textContent=o;b.onclick=()=>send(o);box.appendChild(b);
   });
  }
  if(data.correct_answer){score+=10;answers++;document.getElementById("score").textContent=score;document.getElementById("answers").textContent=answers}
 }catch(e){add("ade","No pude conectar con mi núcleo. Intenta de nuevo.");}
 setStatus("SISTEMA EDUCATIVO ACTIVO");
 document.getElementById("orb").style.filter="";
}

function startGame(kind){
 if(kind==="trivia")send("INICIAR_TRIVIA");
 else send("INICIAR_SONIDOS");
}
function theme(t){
 const u=document.getElementById("universe");
 if(t==="nature")u.style.background="linear-gradient(135deg,#082015,#174d35)";
 else if(t==="ocean")u.style.background="linear-gradient(135deg,#031c32,#07556b)";
 else if(t==="science")u.style.background="linear-gradient(135deg,#16072e,#073f52)";
 else if(t==="history")u.style.background="linear-gradient(135deg,#21150a,#4c2b0e)";
 else if(t==="cyber")u.style.background="linear-gradient(135deg,#160026,#071d3f)";
 else u.style.background="radial-gradient(circle at 50% 30%,#14235c,#050817 65%)";
}
function home(){add("ade","🏠 Estás en Inicio. La esfera ADE está lista para ayudarte.");}
function lab(){add("ade","🧪 LABORATORIO: próximamente podrás explorar experimentos, simulaciones y fenómenos científicos.");}
function explore(){add("ade","🌎 EXPLORAR: elige un tema como espacio, animales, geografía, historia o tecnología y pregúntame sobre él.");}
function wiki(){ask("¿Qué información educativa interesante puedes encontrar en Wikipedia?");}
function progress(){add("ade","🏆 PROGRESO: Nivel 12 · 2,450 XP · Sigue completando desafíos para subir de nivel.");}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/ade", methods=["POST"])
def api():
    data = request.get_json(silent=True) or {}
    msg = str(data.get("msg", "")).strip()
    msg_n = normalizar(msg)
    mode = data.get("mode", "chat")
    correct = normalizar(data.get("correct", ""))

    if msg_n == "iniciar_trivia":
        q = random.choice(PREGUNTAS)
        return jsonify({"text": "🎮 DESAFÍO ESCOLAR\n\n" + q["q"], "mode": "trivia", "correct": q["a"], "options": q["opts"]})

    if msg_n == "iniciar_sonidos":
        q = random.choice(SONIDOS)
        return jsonify({"text": "🔊 ADIVINA EL SONIDO\n\n" + q["s"], "mode": "sounds", "correct": q["a"], "options": q["opts"]})

    if mode in ("trivia", "sounds"):
        if msg_n == correct:
            if mode == "trivia":
                q = random.choice(PREGUNTAS)
                return jsonify({"text": "✅ ¡Excelente! +10 XP\n\nSiguiente desafío:\n" + q["q"], "mode": "trivia", "correct": q["a"], "options": q["opts"], "correct_answer": True})
            q = random.choice(SONIDOS)
            return jsonify({"text": "✅ ¡Correcto! +10 XP\n\nNuevo sonido:\n" + q["s"], "mode": "sounds", "correct": q["a"], "options": q["opts"], "correct_answer": True})
        return jsonify({"text": "❌ Todavía no. Prueba otra opción.", "mode": mode, "correct": correct})

    if not msg:
        return jsonify({"text": "Escribe algo y comenzaré a ayudarte.", "mode": "chat"})

    # Wikipedia: fuente externa para respuestas educativas.
    try:
        title = quote(msg.replace(" ", "_"), safe="")
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{title}"
        res = requests.get(
            url,
            headers={"User-Agent": "AdeVital/2.0 educational project"},
            timeout=8
        )
        if res.status_code == 200:
            data_w = res.json()
            extract = data_w.get("extract")
            if extract:
                return jsonify({
                    "text": "📚 Según Wikipedia:\n\n" + extract,
                    "mode": "chat"
                })
    except requests.RequestException:
        pass

    return jsonify({
        "text": "🤖 No encontré una entrada exacta en Wikipedia. Prueba con un concepto más específico, por ejemplo: \"Sistema Solar\", \"fotosíntesis\" o \"Revolución Francesa\".",
        "mode": "chat"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

