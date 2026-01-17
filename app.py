from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Edición Símbolo de la Paz</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --azul-hero: #0056b3;
            --amarillo-all: #ffcc00;
            --rojo-all: #ff0000;
        }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
            display: flex; flex-direction: column; align-items: center; padding: 20px;
        }
        .card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 25px; padding: 25px; width: 100%; max-width: 420px;
            margin-bottom: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            text-align: center; border: 3px solid var(--azul-hero);
            transition: 0.3s;
        }
        .card:hover { transform: translateY(-5px); }
        h2 { color: var(--rojo-all); font-weight: 700; text-transform: uppercase; }
        .btn {
            background: var(--azul-hero); color: white; border: none;
            padding: 14px; border-radius: 15px; width: 100%;
            cursor: pointer; font-weight: 700; margin-bottom: 10px;
        }
        .btn-mute { background: #6c757d; font-size: 0.8em; width: auto; padding: 10px 20px; }
        .btn-success { background: #28a745 !important; }
        .btn-danger { background: var(--rojo-all) !important; }
        .ia-box { text-align: left; background: #fffbe6; padding: 15px; border-radius: 15px; border-left: 5px solid var(--amarillo-all); }
        #karma-bubble { position: fixed; top: 15px; left: 15px; background: var(--amarillo-all); color: #000; padding: 10px 20px; border-radius: 50px; font-weight: bold; }
    </style>
</head>
<body>
    <div id="karma-bubble">PODER: <span id="kVal">0</span>%</div>
    
    <button class="btn btn-mute" id="muteBtn" onclick="toggleMute()">🔊 Voz: ACTIVA</button>

    <div class="card">
        <h2>Buscador de la Justicia 🏛️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:12px; border-radius:12px; border:2px solid var(--azul-hero); margin-bottom:10px;" placeholder="¿Qué quieres investigar, joven?">
        <button class="btn" onclick="consultarIA()">¡IR MÁS ALLÁ! (PLUS ULTRA)</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <button id="btnLeer" class="btn" style="display:none; background:var(--amarillo-all); color:#000; margin-top:10px;" onclick="leerTexto()">🔊 ESCUCHAR ANÁLISIS</button>
        <img id="iaImg" style="width:100%; border-radius:15px; margin-top:15px; display:none;">
    </div>

    <div class="card">
        <h2>Trivia Imperial: ¡Responde con Valor! ⚔️</h2>
        <p id="qText" style="font-weight: 700; font-size: 1.1em;"></p>
        <div id="optionsContainer"></div>
        <p id="feedback" style="font-weight: bold; margin-top: 10px;"></p>
        <button class="btn" id="nextBtn" style="display:none; background:var(--rojo-all);" onclick="siguientePregunta()">¡SIGUIENTE RETO!</button>
    </div>

    <script>
        let karma = 0;
        let pActual = 0;
        let textoLeido = "";
        let mutear = false;

        const preguntas = [
            { q: "¿Quién fue el primer emperador de Roma?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"] },
            { q: "¿Qué estructura llevaba agua a las ciudades?", a: "Acueducto", ops: ["Acueducto", "Puente", "Coliseo"] },
            { q: "¿Cómo se llama la formación de tortuga?", a: "Testudo", ops: ["Testudo", "Escudo", "Legión"] }
        ];

        function toggleMute() {
            mutear = !mutear;
            document.getElementById('muteBtn').innerText = mutear ? "🔇 Voz: SILENCIO" : "🔊 Voz: ACTIVA";
            if(mutear) window.speechSynthesis.cancel();
        }

        function hablar(msj) {
            if (mutear) return;
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(msj);
            utter.lang = 'es-ES';
            utter.pitch = 1; // Tono normal
            utter.rate = 0.9; // Un poco más lento para que suene imponente
            synth.speak(utter);
        }

        function cargarPregunta() {
            const data = preguntas[pActual];
            document.getElementById('qText').innerText = data.q;
            const container = document.getElementById('optionsContainer');
            container.innerHTML = "";
            document.getElementById('feedback').innerText = "";
            document.getElementById('nextBtn').style.display = "none";

            data.ops.forEach(op => {
                const b = document.createElement('button');
                b.className = 'btn';
                b.innerText = op;
                b.onclick = (e) => verificar(op, e.target);
                container.appendChild(b);
            });
        }

        function verificar(op, elemento) {
            const btns = document.querySelectorAll('#optionsContainer .btn');
            btns.forEach(btn => btn.disabled = true);

            if(op === preguntas[pActual].a) {
                elemento.classList.add('btn-success');
                hablar("¡Excelente joven! ¡Respuesta correcta! ¡Sigue así, PLUS ULTRA!");
                karma += 20;
            } else {
                elemento.classList.add('btn-danger');
                hablar("¡No te rindas! La respuesta era " + preguntas[pActual].a + ". ¡Levántate y brilla de nuevo!");
            }
            document.getElementById('kVal').innerText = karma;
            document.getElementById('nextBtn').style.display = "block";
        }

        async function consultarIA() {
            const t = document.getElementById('iaInput').value;
            const resDiv = document.getElementById('iaRes');
            const img = document.getElementById('iaImg');
            resDiv.style.display = "block";
            resDiv.innerHTML = "¡Analizando la historia con justicia!... 🏛️";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                if(d.extract) {
                    resDiv.innerHTML = d.extract;
                    textoLeido = d.extract;
                    document.getElementById('btnLeer').style.display = "block";
                    if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = "block"; }
                }
            } catch(e) { resDiv.innerHTML = "¡Un héroe nunca se rinde, pero hubo un error de conexión!"; }
        }

        function leerTexto() { hablar(textoLeido); }
        function siguientePregunta() { pActual = (pActual + 1) % preguntas.length; cargarPregunta(); }

        window.onload = cargarPregunta;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
