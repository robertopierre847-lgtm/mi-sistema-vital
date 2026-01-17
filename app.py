from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Plus Ultra Roma</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --azul-claro: #e3f2fd;
            --azul-fuerte: #1976d2;
            --blanco: #ffffff;
        }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, var(--blanco) 0%, var(--azul-claro) 100%);
            display: flex; flex-direction: column; align-items: center; padding: 20px; min-height: 100vh;
        }
        .card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(12px); border-radius: 25px; padding: 25px;
            width: 100%; max-width: 420px; margin-bottom: 25px;
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.1);
            text-align: center; border: 1px solid rgba(255,255,255,0.5);
            transition: 0.3s ease;
        }
        .card:hover { transform: translateY(-8px); }
        h2 { color: var(--azul-fuerte); font-weight: 700; }
        .btn {
            background: var(--azul-fuerte); color: white; border: none;
            padding: 15px; border-radius: 15px; width: 100%;
            cursor: pointer; font-weight: 700; margin-bottom: 10px;
            transition: 0.3s; box-shadow: 0 4px 15px rgba(25, 118, 210, 0.2);
        }
        .btn:hover { background: #1565c0; transform: scale(1.02); }
        .btn-mute { background: #6c757d; font-size: 0.8em; width: auto; padding: 8px 15px; border-radius: 50px; }
        .btn-success { background: #28a745 !important; }
        .btn-danger { background: #dc3545 !important; }
        .ia-box { text-align: left; background: white; padding: 15px; border-radius: 15px; border-left: 5px solid var(--azul-fuerte); font-size: 14px; }
        #karma-bubble { position: fixed; top: 20px; left: 20px; background: var(--azul-fuerte); color: white; padding: 10px 20px; border-radius: 50px; font-weight: bold; z-index: 1000; }
    </style>
</head>
<body>
    <div id="karma-bubble">PODER: <span id="kVal">0</span>%</div>
    
    <button class="btn btn-mute" id="muteBtn" onclick="toggleMute()">🔊 VOZ: ACTIVA</button>

    <div class="card">
        <h2>Explorador Imperial 🏛️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:12px; border-radius:12px; border:2px solid var(--azul-fuerte); margin-bottom:10px; box-sizing: border-box;" placeholder="¿Qué investigaremos hoy, joven?">
        <button class="btn" onclick="consultarIA()">¡IR MÁS ALLÁ! ¡PLUS ULTRA!</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <button id="btnLeer" class="btn" style="display:none; background:#bbdefb; color:#0d47a1; margin-top:10px;" onclick="leerTexto()">🔊 ESCUCHAR ANÁLISIS</button>
        <img id="iaImg" style="width:100%; border-radius:15px; margin-top:15px; display:none;">
    </div>

    <div class="card">
        <h2>Trivia Romana ⚔️</h2>
        <p id="qText" style="font-weight: 700; font-size: 1.1em; color: #333;"></p>
        <div id="optionsContainer"></div>
        <button class="btn" id="nextBtn" style="display:none; background:#1976d2;" onclick="siguientePregunta()">¡SIGUIENTE PRUEBA!</button>
    </div>

    <script>
        let karma = 0;
        let pActual = 0;
        let textoLeido = "";
        let mutear = false;

        const preguntas = [
            { q: "¿Quién fue el primer emperador de Roma?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"] },
            { q: "¿Cómo se llama la formación que imitaba una tortuga?", a: "Testudo", ops: ["Testudo", "Escudo", "Legión"] },
            { q: "¿Qué estructura transportaba agua a la ciudad?", a: "Acueducto", ops: ["Puente", "Acueducto", "Túnel"] }
        ];

        function hablar(msj) {
            if (mutear) return;
            window.speechSynthesis.cancel(); // Detener cualquier voz previa
            const utter = new SpeechSynthesisUtterance(msj);
            utter.lang = 'es-ES';
            utter.pitch = 0.8; // Voz más grave como All Might
            utter.rate = 0.85; // Un poco más lento para sonar imponente
            window.speechSynthesis.speak(utter);
        }

        function toggleMute() {
            mutear = !mutear;
            document.getElementById('muteBtn').innerText = mutear ? "🔇 VOZ: SILENCIO" : "🔊 VOZ: ACTIVA";
            if(mutear) window.speechSynthesis.cancel();
        }

        function cargarPregunta() {
            const data = preguntas[pActual];
            document.getElementById('qText').innerText = data.q;
            const container = document.getElementById('optionsContainer');
            container.innerHTML = "";
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
            btns.forEach(b => b.disabled = true);
            if(op === preguntas[pActual].a) {
                elemento.classList.add('btn-success');
                hablar("¡JA JA JA! ¡Excelente joven! ¡Respuesta correcta! ¡No olvides sonreír, porque yo estoy aquí!");
                karma += 33;
            } else {
                elemento.classList.add('btn-danger');
                hablar("¡No te desanimes, joven! ¡Incluso los héroes fallan! La respuesta era " + preguntas[pActual].a + ". ¡Levántate y ve más allá!");
            }
            document.getElementById('kVal').innerText = karma;
            document.getElementById('nextBtn').style.display = "block";
        }

        async function consultarIA() {
            const t = document.getElementById('iaInput').value;
            const resDiv = document.getElementById('iaRes');
            const img = document.getElementById('iaImg');
            resDiv.style.display = "block";
            resDiv.innerHTML = "¡Analizando con el corazón de un héroe!... 🏛️";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                if(d.extract) {
                    resDiv.innerHTML = d.extract;
                    textoLeido = d.extract;
                    document.getElementById('btnLeer').style.display = "block";
                    if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = "block"; }
                }
            } catch(e) { resDiv.innerHTML = "¡Hubo un error, pero un héroe nunca se rinde!"; }
        }

        function leerTexto() { hablar("¡Escucha con atención este análisis histórico! " + textoLeido); }
        function siguientePregunta() { pActual = (pActual + 1) % preguntas.length; cargarPregunta(); }

        window.onload = () => {
            cargarPregunta();
            // Saludo inicial de All Might
            setTimeout(() => hablar("¡Ya estoy aquí para enseñarte historia!"), 1000);
        };
    </script>
</body>
</html>
