from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Edición Imperial</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; font-family: 'Quicksand', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
            display: flex; flex-direction: column; align-items: center; padding: 20px;
        }
        .card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.4);
            border-radius: 25px; padding: 25px; width: 100%; max-width: 420px;
            margin-bottom: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.05);
            text-align: center;
        }
        h2 { color: #1976d2; margin-top: 0; }
        input {
            width: 100%; padding: 12px; margin: 10px 0; border-radius: 15px;
            border: 2px solid #bbdefb; outline: none; box-sizing: border-box;
        }
        .btn {
            background: #1976d2; color: white; border: none; padding: 14px;
            border-radius: 15px; width: 100%; cursor: pointer; font-weight: 600;
        }
        .ia-box {
            text-align: left; background: white; padding: 15px; border-radius: 15px;
            margin-top: 15px; border-left: 5px solid #64b5f6; font-size: 14px;
        }
        .img-ia { width: 100%; border-radius: 15px; margin-top: 10px; display: none; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        /* Burbuja de Karma */
        #karma-bubble {
            position: fixed; top: 20px; right: 20px; width: 60px; height: 60px;
            background: #1976d2; color: white; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; font-size: 20px; box-shadow: 0 5px 15px rgba(25,118,210,0.4);
            z-index: 1000; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
    </style>
</head>
<body>

    <div id="karma-bubble" title="Tu Karma Vital">0</div>

    <div class="card">
        <h2>Asistente de IA Cariñosa ❤️</h2>
        <p>¿Qué quieres ver, mi cielo? Busca castillos, catapultas o lo que desees.</p>
        <input type="text" id="iaInput" placeholder="Busca un tema aquí...">
        <button class="btn" onclick="iaChat()">Consultar a mi IA</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <img id="iaImg" class="img-ia" src="" alt="Imagen de consulta">
    </div>

    <div class="card" style="border-top: 5px solid #ffca28;">
        <h2>Secretos del Imperio Romano 🏛️</h2>
        <p style="font-size: 0.9em; text-align: left;">
            Los romanos guardaban comida en <b>sal</b>, usaban <b>miel</b> como conservante y tenían pozos de <b>nieve</b> para el verano.
        </p>
        <button class="btn" style="background:#ffca28; color:#333;" onclick="subirKarma(10)">Aprender más (+10 Karma)</button>
    </div>

    <div class="card">
        <h2>Desafío Mental Pro</h2>
        <input type="number" id="guessInput" placeholder="¿Cuál es el número?">
        <button class="btn" onclick="jugar()">Adivinar</button>
        <p id="msgJuego"></p>
    </div>

    <script>
        let karma = 0;
        function subirKarma(pts) {
            karma += pts;
            const b = document.getElementById('karma-bubble');
            b.innerText = karma;
            b.style.transform = "scale(1.3)";
            setTimeout(() => b.style.transform = "scale(1)", 300);
        }

        async function iaChat() {
            let q = document.getElementById('iaInput').value;
            let resDiv = document.getElementById('iaRes');
            let img = document.getElementById('iaImg');
            resDiv.style.display = "block";
            resDiv.innerHTML = "Buscando para ti, mi tesoro... ✨";
            img.style.display = "none";

            try {
                const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${q}`);
                const data = await res.json();
                if(data.extract) {
                    resDiv.innerHTML = `<b>Mi amor, aquí tienes:</b><br>${data.extract}`;
                    if(data.originalimage) {
                        img.src = data.originalimage.source;
                        img.style.display = "block";
                    }
                    subirKarma(5);
                } else {
                    resDiv.innerHTML = "Lo siento, corazón. No encontré una imagen real de eso. ¿Probamos con 'Castillo' o 'Catapulta'?";
                }
            } catch {
                resDiv.innerHTML = "Hubo un pequeño error, mi vida.";
            }
        }

        let secreto = Math.floor(Math.random() * 100) + 1;
        function jugar() {
            let g = document.getElementById('guessInput').value;
            let m = document.getElementById('msgJuego');
            if(g == secreto) {
                m.innerText = "¡ADIVINASTE! 🎉 (+20 Karma)";
                subirKarma(20);
                secreto = Math.floor(Math.random() * 100) + 1;
            } else {
                m.innerText = g < secreto ? "Más alto, cariño ⬆️" : "Más bajo, cielo ⬇️";
            }
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
    
