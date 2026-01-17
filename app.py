from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital Maestro</title>
    <style>
        :root { --azul: #00a8ff; }
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: #f0f2f5; padding: 20px; }
        .panel { background: white; padding: 20px; border-radius: 20px; width: 100%; max-width: 400px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; }
        .btn { background: var(--azul); color: white; border: none; padding: 10px; border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold; margin-top: 10px; }
        input { width: 90%; padding: 10px; margin-bottom: 10px; border-radius: 10px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="panel">
        <h2>Núcleo Azul</h2>
        <input type="text" id="wikiIn" placeholder="Buscar en Wikipedia...">
        <button class="btn" onclick="buscar()">SCAN</button>
        <div id="resWiki" style="margin-top:10px; font-size: 14px;"></div>
    </div>

    <div class="panel">
        <h2>Desafío Mental</h2>
        <p>Adivina el número (1-100)</p>
        <input type="number" id="guessInput">
        <button class="btn" onclick="checkGuess()">ADIVINAR</button>
        <p id="guessMsg"></p>
        <button onclick="initGame()" style="font-size: 12px; background: none; border: none; color: gray;">Reiniciar</button>
    </div>

    <script>
        let secret;
        function initGame() { secret = Math.floor(Math.random() * 100) + 1; document.getElementById('guessMsg').innerText = "¡Suerte!"; }
        function checkGuess() {
            let g = document.getElementById('guessInput').value;
            let m = document.getElementById('guessMsg');
            if(g == secret) m.innerText = "¡ADIVINASTE! 🎉";
            else if(g < secret) m.innerText = "Más ALTO ⬆️";
            else m.innerText = "Más BAJO ⬇️";
        }
        async function buscar() {
            let q = document.getElementById('wikiIn').value;
            let r = document.getElementById('resWiki');
            r.innerText = "Buscando...";
            const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${q}`);
            const d = await res.json();
            r.innerText = d.extract || "No se encontró nada.";
        }
        window.onload = initGame;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
