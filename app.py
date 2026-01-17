from flask import Flask, render_template_string

app = Flask(__name__)

# Diseño Blanco y Azul con efecto de Cristal
diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Imperio Romano: Edición All Might</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
            display: flex; flex-direction: column; align-items: center; padding: 20px; min-height: 100vh;
        }
        .card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px); border-radius: 20px; padding: 25px;
            width: 100%; max-width: 400px; margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(25, 118, 210, 0.1); text-align: center;
            border: 1px solid rgba(255,255,255,0.5);
        }
        h2 { color: #1976d2; font-weight: 700; }
        .btn {
            background: #1976d2; color: white; border: none; padding: 15px;
            border-radius: 12px; width: 100%; cursor: pointer; font-weight: 700;
            margin-bottom: 10px; transition: 0.3s;
        }
        .btn:active { transform: scale(0.95); }
        .btn-mute { background: #6c757d; font-size: 0.8em; width: auto; padding: 8px 15px; border-radius: 50px; }
        .ia-box { text-align: left; background: white; padding: 15px; border-radius: 12px; border-left: 5px solid #1976d2; font-size: 14px; margin-top: 10px; }
        #karma-bubble { position: fixed; top: 20px; left: 20px; background: #1976d2; color: white; padding: 10px 18px; border-radius: 50px; font-weight: bold; }
    </style>
</head>
<body>
    <div id="karma-bubble">PODER: <span id="kVal">0</span>%</div>
    <button class="btn btn-mute" id="muteBtn" onclick="toggleMute()">🔊 VOZ: ACTIVA</button>

    <div class="card">
        <h2>Buscador Romano 🏛️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:12px; border-radius:10px; border:1px solid #1976d2; box-sizing:border-box;" placeholder="¿Qué investigaremos, joven?">
        <button class="btn" style="margin-top:10px;" onclick="consultarIA()">¡PLUS ULTRA!</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <button id="btnLeer" class="btn" style="display:none; background:#bbdefb; color:#0d47a1; margin-top:10px;" onclick="leerTexto()">🔊 ESCUCHAR</button>
    </div>

    <div class="card">
        <h2>Trivia Imperial ⚔️</h2>
        <p id="qText" style="font-weight: 700;"></p>
        <div id="optionsContainer"></div>
        <button class="btn" id="nextBtn" style="display:none;" onclick="siguientePregunta()">¡SIGUIENTE!</button>
    </div>

    <script>
        let karma = 0; let pActual = 0; let textoLeido = ""; let mutear = false;
        const preguntas = [
            { q: "¿Quién fue el primer emperador?", a: "Augusto", ops: ["César", "Augusto", "Nerón"] },
            { q: "¿Formación tipo tortuga?", a: "Testudo", ops: ["Testudo", "Legión", "Falange"] }
        ];

        function hablar(msj) {
            if (mutear) return;
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(msj);
            utter.lang = 'es-ES'; utter.pitch = 0.7; utter.rate = 0.8;
            window.speechSynthesis.speak(utter);
        }

        function toggleMute() {
            mutear = !mutear;
            document.getElementById('muteBtn').innerText = mutear ? "🔇 VOZ: SILENCIO" : "🔊 VOZ: ACTIVA";
            if(mutear) window.speechSynthesis.cancel();
        }

        function cargarPregunta() {
            const d = preguntas[pActual];
            document.getElementById('qText').innerText = d.q;
            const c = document.getElementById('optionsContainer');
            c.innerHTML = ""; document.getElementById('nextBtn').style.display = "none";
            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn'; b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) {
                        hablar("¡JA JA JA! ¡Correcto joven! ¡Sigue así!");
                        karma += 50; document.getElementById('kVal').innerText = karma;
                        document.getElementById('nextBtn').style.display = "block";
                    } else {
                        hablar("¡No te rindas! ¡Inténtalo de nuevo con valor!");
                    }
                };
                c.appendChild(b);
            });
        }

        async function consultarIA() {
            const t = document.getElementById('iaInput').value;
            const res = document.getElementById('iaRes');
            res.style.display = "block"; res.innerHTML = "¡Buscando con justicia!...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                if(d.extract) {
                    res.innerHTML = d.extract; textoLeido = d.extract;
                    document.getElementById('btnLeer').style.display = "block";
                }
            } catch(e) { res.innerHTML = "¡Error! Pero un héroe no se rinde."; }
        }

        function leerTexto() { hablar("¡Escucha joven! " + textoLeido); }
        function siguientePregunta() { pActual = (pActual + 1) % preguntas.length; cargarPregunta(); }
        window.onload = () => { cargarPregunta(); setTimeout(() => hablar("¡Ya estoy aquí!"), 1000); };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
