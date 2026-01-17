from flask import Flask, render_template_string

app = Flask(__name__)

# --- DISEÑO INTEGRAL: NÚCLEO AZUL + HERRAMIENTAS + JUEGO ADIVINANZAS ---
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
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            padding: 25px; border-radius: 35px;
            width: 100%; max-width: 450px;
            margin-bottom: 20px; text-align: center;
            box-shadow: 0 10px 30px var(--sombra-suave);
        }
        h2 { color: var(--azul-electrico); font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px; }
        .btn { 
            background: var(--azul-electrico); color: white; border: none; 
            padding: 12px 20px; border-radius: 20px; cursor: pointer; font-weight: bold; 
            transition: 0.3s; margin: 5px; width: 80%;
        }
        input { 
            width: 85%; padding: 12px; border-radius: 15px; 
            border: 1px solid #e1f5fe; outline: none; margin-bottom: 10px;
        }
        #guessMessage { margin: 10px; font-weight: bold; color: #2f3640; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
</head>
<body>

    <div class="panel">
        <h2>Núcleo Azul</h2>
        <input type="text" id="wikiIn" placeholder="Investigar tema...">
        <button class="btn" onclick="buscar()">SCAN</button>
        <div id="resWiki"></div>
    </div>

    <div class="panel">
        <h2>Desafío Mental</h2>
        <p>Adivina el número del 1 al 100</p>
        <input type="number" id="guessInput" placeholder="Tu número...">
        <button class="btn" onclick="checkGuess()">ADIVINAR</button>
        <p id="guessMessage">¡Suerte!</p>
        <button class="btn" onclick="startGame()" style="background:#f1f2f6; color:#7f8c8d;">Reiniciar Juego</button>
    </div>

    <div class="panel">
        <h2>Hidratación</h2>
        <div id="water">💧 0 Vasos</div>
        <button class="btn" onclick="addWater()">+ Añadir Vaso</button>
    </div>

    <script>
        // Lógica del Juego
        let numSecret;
        function startGame() {
            numSecret = Math.floor(Math.random() * 100) + 1;
            document.getElementById('guessMessage').innerText = "He pensado un número...";
        }
        function checkGuess() {
            let g = document.getElementById('guessInput').value;
            let m = document.getElementById('guessMessage');
            if(g == numSecret) m.innerText = "¡ADIVINASTE! 🎉";
            else if(g < numSecret) m.innerText = "Más ALTO ⬆️";
            else m.innerText = "Más BAJO ⬇️";
        }
        
        let v = 0;
        function addWater() { v++; document.getElementById('water').innerText = "💧 " + v + " Vasos"; }
        
        async function buscar() {
            let q = document.getElementById('wikiIn').value;
            let r = document.getElementById('resWiki');
            r.innerText = "Buscando...";
            const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${q}`);
            const data = await res.json();
            r.innerText = data.extract || "No encontré nada.";
        }
        window.onload = startGame;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
