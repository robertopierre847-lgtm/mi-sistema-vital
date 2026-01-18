from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roma Plus Ultra</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --blanco: #ffffff; }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }

        /* ANIMACIÓN DE ENTRADA ÉPICA */
        #intro {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--azul); color: white; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: transform 1s ease-in-out;
        }
        .intro-cerrar { transform: translateY(-100%); }

        /* DISEÑO CRISTAL */
        .glass {
            background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px);
            border-radius: 25px; padding: 20px; width: 90%; max-width: 400px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center;
            animation: flotar 4s ease-in-out infinite;
        }
        @keyframes flotar { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }

        /* BUSCADOR E IMAGEN */
        #img-res { width: 100%; border-radius: 15px; margin-top: 15px; display: none; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .input-hero { width: 100%; padding: 12px; border-radius: 10px; border: 2px solid #ddd; box-sizing: border-box; }
        .btn-hero { background: var(--azul); color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: bold; margin-top: 10px; cursor: pointer; }

        /* ALL MIGHT MINI */
        #am-mini { position: fixed; bottom: 15px; right: 15px; width: 80px; z-index: 100; }
        .talk { position: fixed; bottom: 100px; right: 20px; background: white; padding: 10px; border-radius: 15px; border: 2px solid var(--azul); font-size: 12px; font-weight: bold; display: none; }
    </style>
</head>
<body>

    <div id="intro">
        <h1 style="font-size: 3em;">🏛️</h1>
        <h2>IMPERIO ROMANO</h2>
        <button class="btn-hero" style="width: 200px; background: gold; color: black;" onclick="entrar()">¡PLUS ULTRA!</button>
    </div>

    <div id="am-mini"><img src="https://i.imgur.com/vH9vIqy.png" style="width: 100%;"></div>
    <div class="talk" id="burbuja">¡YA ESTOY AQUÍ!</div>

    <div class="glass">
        <h2 style="color: var(--azul);">Buscador Imperial 🔍</h2>
        <input type="text" id="busqueda" class="input-hero" placeholder="Ej: Gladiador, Julio César...">
        <button class="btn-hero" onclick="buscar()">BUSCAR CON PODER</button>
        <div id="texto-res" style="margin-top: 15px; font-size: 14px; text-align: left;"></div>
        <img id="img-res" src="">
    </div>

    <div class="glass">
        <h2 style="color: var(--azul);">Trivia ⚔️</h2>
        <p id="pregunta" style="font-weight: bold;"></p>
        <div id="opciones"></div>
    </div>

    <script>
        function entrar() {
            document.getElementById('intro').classList.add('intro-cerrar');
            hablar("¡Bienvenido joven! ¡Hoy aprenderemos con el corazón!");
        }

        function hablar(msj) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(msj);
            u.lang = 'es-ES'; u.pitch = 0.7; u.rate = 0.9;
            window.speechSynthesis.speak(u);
            const b = document.getElementById('burbuja');
            b.innerText = msj; b.style.display = 'block';
            setTimeout(() => b.style.display = 'none', 4000);
        }

        async function buscar() {
            const t = document.getElementById('busqueda').value;
            const res = document.getElementById('texto-res');
            const img = document.getElementById('img-res');
            res.innerHTML = "Buscando en los archivos...";
            img.style.display = 'none';

            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                res.innerHTML = d.extract || "No encontré información, ¡intenta con otra palabra!";
                if(d.thumbnail) {
                    img.src = d.thumbnail.source;
                    img.style.display = 'block';
                }
                hablar("¡Aquí tienes los datos históricos, joven!");
            } catch(e) { res.innerHTML = "Error al conectar con el Senado."; }
        }

        const trivia = [{q:"¿Quién fundó Roma según la leyenda?", a:"Rómulo", ops:["Rómulo","César","Hércules"]}];
        function cargarTrivia() {
            const d = trivia[0];
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero'; b.innerText = o;
                b.style.marginTop = '5px';
                b.onclick = () => hablar(o === d.a ? "¡Excelente! ¡Respuesta correcta!" : "¡No te rindas, ve más allá!");
                cont.appendChild(b);
            });
        }
        window.onload = cargarTrivia;
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
