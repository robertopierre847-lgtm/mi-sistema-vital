import os, requests, random
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Base de datos de "Dominicanismos"
diccionario_rd = {
    "klk": "Saludo común, acortamiento de '¿Qué es lo que hay?'.",
    "vaina": "Cosa, objeto o situación (se usa para todo).",
    "manso": "Estar tranquilo o en paz.",
    "concho": "Transporte público colectivo.",
    "heavy": "Algo que está muy bien o excelente."
}

def wiki_search(query):
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        res = requests.get(url, headers={'User-Agent': 'AdeOS/4.0'}).json()
        return res.get("extract", "No encontré info, intenta otra palabra."), res.get("thumbnail", {}).get("source", "")
    except: return "Error de red.", ""

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade Vital OS Pro 💎</title>
    <style>
        :root { --bg: #021b79; --glass: rgba(255, 255, 255, 0.1); --accent: #00d2ff; }
        body { 
            margin:0; height:100vh; background: var(--bg); font-family: 'Segoe UI', sans-serif;
            display:flex; align-items:center; justify-content:center; color: white; transition: 0.5s;
        }
        .os-window {
            width:90%; max-width:450px; height:85vh; background: var(--glass);
            backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.2);
            border-radius:30px; display:flex; flex-direction:column; box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }
        #screen { flex:1; padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:10px; }
        .bubble { padding:12px; border-radius:15px; font-size:0.9rem; max-width:85%; background:rgba(255,255,255,0.1); }
        .user { align-self:flex-end; background: var(--accent); color:#001; font-weight:bold; }
        
        .dock { padding:10px; background:rgba(0,0,0,0.3); display:grid; grid-template-columns: repeat(3, 1fr); gap:5px; border-radius:0 0 30px 30px; }
        .btn { background:rgba(255,255,255,0.1); border:none; color:white; padding:8px; border-radius:10px; cursor:pointer; font-size:0.7rem; }
        .btn:hover { background: var(--accent); color:black; }
        
        .input-box { display:flex; padding:15px; gap:10px; }
        input { flex:1; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.3); border-radius:15px; padding:10px; color:white; outline:none; }
        #pomodoro { text-align:center; color:#ffea00; font-weight:bold; font-size:1.2rem; display:none; }
    </style>
</head>
<body>

<div class="os-window">
    <div style="padding:15px; text-align:center;">Ade Vital OS Pro 💎</div>
    <div id="pomodoro">25:00</div>
    <div id="screen">
        <div class="bubble">SISTEMA LISTO. 🚀<br>Usa el buscador o los módulos del panel inferior.</div>
    </div>

    <div class="input-box">
        <input type="text" id="in" placeholder="Pregúntame algo..." onkeypress="if(event.key==='Enter') send()">
        <button onclick="send()" style="border-radius:50%; width:40px; border:none; background:var(--accent);">➤</button>
    </div>

    <div class="dock">
        <button class="btn" onclick="startPomodoro()">⏳ Pomodoro</button>
        <button class="btn" onclick="rdWiki()">🇩🇴 RD Dic</button>
        <button class="btn" onclick="setTheme('#05350c', '#28e041')">🌿 Estudio</button>
        <button class="btn" onclick="setTheme('#021b79', '#00d2ff')">💎 Vital</button>
        <button class="btn" onclick="saludAlert()">💧 Salud</button>
        <button class="btn" onclick="hablar('Iniciando sistema vital')">🔊 Voz</button>
    </div>
</div>

<script>
    const screen = document.getElementById("screen");

    function hablar(texto) {
        const msg = new SpeechSynthesisUtterance(texto);
        msg.lang = 'es-ES';
        window.speechSynthesis.speak(msg);
    }

    async function send(customMsg = null) {
        const input = document.getElementById("in");
        const val = customMsg || input.value.trim();
        if(!val) return;
        
        screen.innerHTML += `<div class="bubble user">${val}</div>`;
        input.value = "";

        const res = await fetch("/api/ade", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({msg: val})
        });
        const data = await res.json();

        let html = `<div class="bubble"><b>Ade:</b><br>${data.text}</div>`;
        if(data.img) html += `<img src="${data.img}" style="width:100%; border-radius:15px; margin-top:10px;">`;
        
        screen.innerHTML += html;
        hablar(data.text.split('<')[0]); // Habla solo el texto plano
        screen.scrollTop = screen.scrollHeight;
    }

    function startPomodoro() {
        document.getElementById("pomodoro").style.display = "block";
        let time = 25 * 60;
        const timer = setInterval(() => {
            let min = Math.floor(time / 60);
            let sec = time % 60;
            document.getElementById("pomodoro").innerText = `${min}:${sec < 10 ? '0'+sec : sec}`;
            if(time <= 0) { clearInterval(timer); hablar("Tiempo terminado, descansa."); }
            time--;
        }, 1000);
    }

    function setTheme(bg, accent) {
        document.documentElement.style.setProperty('--bg', bg);
        document.documentElement.style.setProperty('--accent', accent);
    }

    function saludAlert() {
        send("Dame un consejo de salud");
    }

    function rdWiki() {
        send("Diccionario Dominicano");
    }
</script>
</body>
</html>
""")

@app.route("/api/ade", methods=["POST"])
def api():
    msg = request.json.get("msg", "").lower()
    
    # 2. Cultura Dominicana
    if "diccionario dominicano" in msg:
        return jsonify({"text": "Escribe una palabra (klk, vaina, manso) para explicarte."})
    if msg in diccionario_rd:
        return jsonify({"text": f"🇩🇴 <b>{msg.upper()}:</b> {diccionario_rd[msg]}"})

    # 3. Salud Vital
    if "salud" in msg or "consejo" in msg:
        tips = ["Bebe 2 litros de agua hoy.", "Estira tu espalda cada 30 minutos.", "Descansa la vista de la pantalla."]
        return jsonify({"text": f"💡 <b>Tip Vital:</b> {random.choice(tips)}"})

    # 1. Buscador automático
    txt, img = wiki_search(msg)
    return jsonify({"text": txt, "img": img})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
