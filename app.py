from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --azul-brillante: #00d2ff;
            --azul-profundo: #3a7bd5;
            --blanco-cristal: rgba(255, 255, 255, 0.8);
        }
        body {
            margin: 0;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            background-attachment: fixed;
            display: flex; flex-direction: column; align-items: center;
            padding: 20px; color: #333;
        }
        /* Efecto Flotante Glassmorphism */
        .card {
            background: var(--blanco-cristal);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 20px;
            padding: 25px;
            width: 100%; max-width: 400px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); }
        h2 { color: var(--azul-profundo); margin-top: 0; font-weight: 600; }
        input {
            width: 100%; padding: 12px; margin: 10px 0;
            border-radius: 12px; border: 1px solid #ddd;
            box-sizing: border-box; outline: none;
        }
        .btn {
            background: linear-gradient(to right, var(--azul-brillante), var(--azul-profundo));
            color: white; border: none; padding: 12px;
            border-radius: 12px; width: 100%; cursor: pointer;
            font-weight: 600; box-shadow: 0 4px 15px rgba(58, 123, 213, 0.3);
        }
        .chat-box {
            text-align: left; background: rgba(255,255,255,0.5);
            padding: 15px; border-radius: 15px; min-height: 50px;
            font-size: 14px; line-height: 1.5; border-left: 4px solid var(--azul-brillante);
        }
        .badge { background: #e3f2fd; color: #1976d2; padding: 5px 10px; border-radius: 20px; font-size: 12px; }
    </style>
</head>
<body>

    <div class="card">
        <span class="badge">IA Activa</span>
        <h2>Hola, mi amor ❤️</h2>
        <p style="font-size: 0.9em;">Pregúntame lo que quieras, tesoro. Buscaré en Wikipedia para ti.</p>
        <input type="text" id="iaInput" placeholder="¿Qué quieres saber, cielo?">
        <button class="btn" onclick="iaChat()">Hablar con mi IA</button>
        <div id="iaRes" class="chat-box" style="margin-top:15px; display:none;"></div>
    </div>

    <div class="card">
        <h2>Desafío Mental Pro 🎮</h2>
        <p id="hint">Adivina el número secreto (1-100)</p>
        <input type="number" id="guessInput">
        <button class="btn" onclick="jugar()">Probar Suerte</button>
        <p id="msgJuego" style="font-weight: bold;"></p>
    </div>

    <div class="card">
        <h2>Herramientas Vitales</h2>
        <div id="stats" style="display: flex; justify-content: space-around; font-size: 12px;">
            <div>💧 <b id="waterCount">0</b> Vasos</div>
            <div>⚡ <b id="powerLevel">100%</b> Energía</div>
        </div>
        <button class="btn" style="margin-top:10px; background: #4caf50;" onclick="tomarAgua()">Beber Agua</button>
    </div>

    <script>
        // Lógica de la IA Cariñosa
        async function iaChat() {
            let q = document.getElementById('iaInput').value;
            let resDiv = document.getElementById('iaRes');
            resDiv.style.display = "block";
            resDiv.innerHTML = "Déjame buscar eso para ti, corazón... ✨";
            
            try {
                const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${q}`);
                const data = await res.json();
                if(data.extract) {
                    resDiv.innerHTML = `<b>Mi respuesta para ti, cariño:</b><br>${data.extract}`;
                } else {
                    resDiv.innerHTML = "Ay mi vida, no encontré eso exactamente. ¿Probamos con otra palabra?";
                }
            } catch {
                resDiv.innerHTML = "Hubo un error, mi cielo. Inténtalo de nuevo.";
            }
        }

        // Lógica del Juego
        let secreto = Math.floor(Math.random() * 100) + 1;
        function jugar() {
            let g = document.getElementById('guessInput').value;
            let m = document.getElementById('msgJuego');
            if(g == secreto) {
                m.innerHTML = "¡ADIVINASTE! 🎉 Eres increíble.";
                m.style.color = "#4caf50";
            } else {
                m.innerHTML = g < secreto ? "Más alto, amor ⬆️" : "Más bajo, cielo ⬇️";
                m.style.color = "#f44336";
            }
        }

        // Hidratación
        let agua = 0;
        function tomarAgua() {
            agua++;
            document.getElementById('waterCount').innerText = agua;
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
    
