from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Plus Ultra</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
            display: flex; flex-direction: column; align-items: center; padding: 20px; min-height: 100vh;
        }
        .card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px); border-radius: 25px; padding: 25px;
            width: 100%; max-width: 400px; margin-bottom: 25px;
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.1); text-align: center;
            border: 1px solid rgba(255,255,255,0.6);
        }
        h2 { color: #1976d2; margin-bottom: 15px; }
        .btn {
            background: #1976d2; color: white; border: none; padding: 15px;
            border-radius: 15px; width: 100%; cursor: pointer; font-weight: 700;
            margin-bottom: 10px; transition: 0.3s;
        }
        .btn-success { background: #28a745 !important; transform: scale(1.05); }
        .btn-error { background: #dc3545 !important; animation: shake 0.3s; }
        @keyframes shake { 0%, 100% {transform: translateX(0);} 25% {transform: translateX(-5px);} 75% {transform: translateX(5px);} }
        .ia-box { text-align: left; background: white; padding: 15px; border-radius: 15px; border-left: 5px solid #1976d2; font-size: 14px; margin-top: 15px; }
        #karma-bubble { position: fixed; top: 20px; left: 20px; background: #1976d2; color: white; padding: 10px 20px; border-radius: 50px; font-weight: bold; }
        .img-ia { width: 100%; border-radius: 15px; margin-top: 15px; display: none; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div id="karma-bubble">PODER: <span id="kVal">0</span>%</div>
    <button class="btn" style="width:auto; background:#6c757d; font-size:0.8em;" onclick="toggleMute()" id="mBtn">🔊 VOZ: ACTIVA</button>

    <div class="card">
        <h2>Buscador Romano 🏛️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:12px; border-radius:12px; border:1px solid #1976d2; box-sizing:border-box;" placeholder="¿Qué investigamos, joven?">
        <button class="btn" style="margin-top:10px;" onclick="consultarIA()">¡BUSCAR CON PODER!</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <img id="iaImg" class="img-ia" src="">
        <button id="btnLeer" class="btn" style="display:none; background:#bbdefb; color:#0d47a1; margin-top:10px;" onclick="leerTexto()">🔊 ESCUCHAR ANÁLISIS</button>
    </div>

    <div class="card">
        <h2>Trivia All Might ⚔️</h2>
        <p id="qText" style="font-weight: 700; font-size: 1.1em;"></p>
        <div id="optionsContainer"></div>
        <button class="btn" id="nextBtn" style="display:none; background:#28a745;" onclick="siguientePregunta()">¡SIGUIENTE RETO!</button>
    </div>

    <script>
        let karma = 0; let pActual = 0; let textoLeido = ""; let mutear = false;
        const preguntas = [
            { q: "¿Quién fue el primer emperador de Roma?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"] },
            { q: "¿Qué estructura transportaba agua?", a: "Acueducto", ops: ["Coliseo", "Acueducto", "Foro"] },
            { q: "¿Cómo se llama la formación de tortuga?", a: "Testudo", ops: ["Legión", "Testudo", "Falange"] }
        ];

        function hablar(msj) {
            if (mutear) return;
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(msj);
            utter.lang = 'es-ES'; utter.pitch = 0.7; utter.rate = 0.85;
            window.speechSynthesis.speak(utter);
        }

        function toggleMute() {
            mutear = !mutear;
            document.getElementById('mBtn').innerText = mutear ? "🔇 VOZ: SILENCIO" : "🔊 VOZ: ACTIVA";
        }

        function cargarPregunta() {
            const d = preguntas[pActual];
            document.getElementById('qText').innerText = d.q;
            const c = document.getElementById('optionsContainer');
            c.innerHTML = ""; document.getElementById('nextBtn').style.display = "none";
            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn'; b.innerText = o;
                b.onclick = (e) => {
                    const btns = document.querySelectorAll('#optionsContainer .btn');
                    if(o === d.a) {
                        e.target.classList.add('btn-success');
                        hablar("¡JA JA JA! ¡Respuesta correcta, joven! ¡PLUS ULTRA!");
                        karma += 30; document.getElementById('kVal').innerText = karma;
                        document.getElementById('nextBtn').style.display = "block";
                        btns.forEach(btn => { if(btn !== e.target) btn.disabled = true; });
                    } else {
                        e.target.classList.add('btn-error');
                        hablar("¡No te rindas! ¡Incluso los héroes cometen errores! ¡Prueba de nuevo!");
                        setTimeout(() => e.target.classList.remove('btn-error'), 500);
                    }
                };
                c.appendChild(b);
            });
        }

        async function consultarIA() {
            const t = document.getElementById('iaInput').value;
            const res = document.getElementById('iaRes');
            const img = document.getElementById('iaImg');
            res.style.display = "block"; res.innerHTML = "¡Buscando con justicia!...";
            img.style.display = "none";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                if(d.extract) {
                    res.innerHTML = d.extract; textoLeido = d.extract;
                    document.getElementById('btnLeer').style.display = "block";
                    if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = "block"; }
                }
            } catch(e) { res.innerHTML = "¡Error! Pero un héroe nunca retrocede."; }
        }

        function leerTexto() { hablar("¡Escucha joven! " + textoLeido); }
        function siguientePregunta() { pActual = (pActual + 1) % preguntas.length; cargarPregunta(); }
        window.onload = () => { cargarPregunta(); setTimeout(() => hablar("¡Ya estoy aquí para enseñarte historia!"), 1000); };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
