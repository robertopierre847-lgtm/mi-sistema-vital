from flask import Flask, render_template_string

app = Flask(__name__)

# --- DISEÑO INTEGRAL: NÚCLEO AZUL + HERRAMIENTAS VITALES + JUEGO ADIVINANZAS ---
diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital Maestro</title>
    <style>
        :root {
            --azul-electrico: #00a8ff;
            --blanco: #ffffff;
            --fondo-gris: #f5f7fa;
            --sombra-suave: rgba(0, 168, 255, 0.15);
        }
        * { box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
            font-family: 'Quicksand', sans-serif;
            display: flex; flex-direction: column; align-items: center;
            padding: 20px; margin: 0; min-height: 100vh;
        }
        .panel {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            padding: 25px; border-radius: 40px;
            width: 100%; max-width: 480px;
            margin-bottom: 25px; text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 15px 35px var(--sombra-suave);
            animation: flotar 5s ease-in-out infinite;
        }
        @keyframes flotar {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        h2 { 
            color: var(--azul-electrico); 
            font-size: 1rem; 
            letter-spacing: 2.5px; 
            text-transform: uppercase; 
            margin-bottom: 20px;
            font-weight: 600;
        }
        .btn { 
            background: var(--azul-electrico); 
            color: white; border: none; 
            padding: 12px 22px; border-radius: 20px; 
            cursor: pointer; font-weight: bold; 
            transition: 0.3s; margin: 5px;
            box-shadow: 0 4px 15px rgba(0, 168, 255, 0.3);
        }
        .btn:hover { transform: scale(1.05); filter: brightness(1.1); }
        input { 
            width: 90%; padding: 14px; border-radius: 18px; 
            border: 1.5px solid #e1f5fe; outline: none; 
            margin-bottom: 12px; font-family: inherit;
        }

        /* Estilos de módulos */
        #timerDisplay { font-size: 2.2rem; font-weight: 300; color: #2f3640; margin: 10px 0; }
        #waterDisplay { font-size: 1.8rem; margin: 15px 0; }
        .nota-item { 
            background: white; padding: 12px; border-radius: 18px; 
            margin-top: 10px; text-align: left; 
            border-left: 5px solid var(--azul-electrico);
            font-size: 0.9rem; box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        }
        #resWiki { font-size: 0.85rem; text-align: left; margin-top: 15px; color: #444; line-height: 1.4; }

        /* Estilos específicos para el juego de adivinanzas */
        #guessInput { width: 60%; margin-right: 5px; display: inline-block; }
        #guessBtn { width: 30%; display: inline-block; }
        #guessMessage { margin-top: 15px; font-weight: 500; color: #333; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;500;700&display=swap" rel="stylesheet">
</head>
<body>

    <div class="panel">
        <h2>Núcleo Azul</h2>
        <input type="text" id="wikiIn" placeholder="Investigar tema en la red...">
        <button class="btn" onclick="buscar()">SCAN</button>
        <div id="resWiki"></div>
    </div>

    <div class="panel">
        <h2>Hidratación Vital</h2>
        <div id="waterDisplay">💧 0 Vasos</div>
        <button class="btn" onclick="cambiarAgua(1)">+ Añadir</button>
        <button class="btn" onclick="cambiarAgua(-1)" style="background:#f1f2f6; color:#7f8c8d; box-shadow:none;">Quitar</button>
    </div>

    <div class="panel">
        <h2>Escáner de Enfoque</h2>
        <div id="timerDisplay">25:00</div>
        <button class="btn" onclick="toggleTimer()" id="btnTimer">Iniciar Ciclo</button>
        <button class="btn" onclick="resetTimer()" style="background:none; color:var(--azul-electrico); font-size:0.8rem; box-shadow:none;">Reiniciar</button>
    </div>

    <div class="panel">
        <h2>Desafío Mental</h2>
        <p>Adivina el número (entre 1 y 100).</p>
        <input type="number" id="guessInput" placeholder="Tu número" min="1" max="100">
        <button class="btn" id="guessBtn" onclick="checkGuess()">Adivinar</button>
        <p id="guessMessage"></p>
        <button class="btn" onclick="startGame()" style="background:#f1f2f6; color:#7f8c8d; box-shadow:none; font-size:0.8rem; margin-top:10px;">Nuevo Juego</button>
    </div>

    <div class="panel">
        <h2>Memo-Blue</h2>
        <input type="text" id="notaIn" placeholder="Escribe un recordatorio...">
        <button class="btn" onclick="addNota()">Guardar</button>
        <div id="listaNotas"></div>
    </div>

    <div class="panel">
        <h2>Misión del Momento</h2>
        <p id="misionTxt" style="font-style: italic; color: #57606f;">¿Qué haremos hoy?</p>
        <button class="btn" onclick="nuevaMision()">GENERAR</button>
    </div>

    <script>
        // --- LÓGICA BUSCADOR ---
        async function buscar() {
            const q = document.getElementById('wikiIn').value;
            const res = document.getElementById('resWiki');
            if(!q) return;
            res.innerHTML = "Sincronizando con el Núcleo...";
            try {
                const url = `https://es.wikipedia.org/api/rest_v1/page/summary/${q.trim().replace(/ /g, '_')}`;
                const r = await fetch(url);
                const d = await r.json();
                res.innerHTML = d.extract ? `<b>${d.title}:</b> ${d.extract}` : "No se encontraron datos específicos.";
            } catch(e) { res.innerHTML = "Error de conexión al Núcleo."; }
        }

        // --- LÓGICA HIDRATACIÓN ---
        let vasos = 0;
        function cambiarAgua(n) {
            vasos = Math.max(0, vasos + n);
            document.getElementById('waterDisplay').innerText = `💧 ${vasos} Vasos`;
        }

        // --- LÓGICA TIMER ---
        let timer;
        let running = false;
        let timeLeft = 25 * 60;
        function toggleTimer() {
            const btn = document.getElementById('btnTimer');
            if(running) {
                clearInterval(timer);
                btn.innerText = "Reanudar";
            } else {
                timer = setInterval(() => {
                    timeLeft--;
                    let min = Math.floor(timeLeft / 60);
                    let sec = timeLeft % 60;
                    document.getElementById('timerDisplay').innerText = `${min}:${sec < 10 ? '0' : ''}${sec}`;
                    if(timeLeft <= 0) { 
                        clearInterval(timer); 
                        alert("Ciclo de enfoque terminado. ¡Tómate un descanso!"); 
                        resetTimer();
                    }
                }, 1000);
                btn.innerText = "Pausar";
            }
            running = !running;
        }
        function resetTimer() {
            clearInterval(timer);
            running = false;
            timeLeft = 25 * 60;
            document.getElementById('timerDisplay').innerText = "25:00";
            document.getElementById('btnTimer').innerText = "Iniciar Ciclo";
        }

        // --- LÓGICA JUEGO ADIVINANZAS ---
        let randomNumber;
        let attempts = 0;
        function startGame() {
            randomNumber = Math.floor(Math.random() * 100) + 1; // Número entre 1 y 100
            attempts = 0;
            document.getElementById('guessMessage').innerText = "¡He pensado un número!";
            document.getElementById('guessInput').value = "";
            document.getElementById('guessInput').disabled = false;
            document.getElementById('guessBtn').disabled = false;
        }
        function checkGuess() {
            const guess = parseInt(document.getElementById('guessInput').value);
            const messageDisplay = document.getElementById('guessMessage');
            
            if (isNaN(guess) || guess < 1 || guess > 100) {
                messageDisplay.innerText = "Por favor, introduce un número válido entre 1 y 100.";
                return;
            }

            attempts++;
            if (guess === randomNumber) {
                messageDisplay.innerText = `¡Felicidades! Adivinaste el número ${randomNumber} en ${attempts} intentos.`;
                document.getElementById('guessInput').disabled = true;
                document.getElementById('guessBtn').disabled = true;
            } else if (guess < randomNumber) {
                messageDisplay.innerText = "Más alto.";
            } else {
                messageDisplay.innerText = "Más bajo.";
            }
        }
        // Iniciar el juego al cargar la página por primera vez
        document.addEventListener('DOMContentLoaded', startGame);


        // --- LÓGICA NOTAS ---
        function addNota() {
            const val = document.getElementById('notaIn').value;
            if(!val) return;
            const item = document.createElement('div');
            item.className = 'nota-item';
            item.innerText = "• " + val;
            document.getElementById('listaNotas').prepend(item);
            document.getElementById('notaIn').value = "";
        }

        // --- LÓGICA MISIONES ---
        function nuevaMision() {
            const m = [
                "Bebe un vaso de agua ahora mismo.",
                "Haz 5 minutos de estiramientos.",
                "Escribe una meta para mañana.",
                "Ordena un pequeño rincón de tu mesa.",
                "Respira profundamente durante 1 minuto.",
                "Aprende una palabra nueva hoy."
            ];
            document.getElementById('misionTxt').innerText = m[Math.floor(Math.random()*m.length)];
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
