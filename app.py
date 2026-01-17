from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Roma Imperial</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            font-family: 'Quicksand', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
            background-attachment: fixed;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            min-height: 100vh;
        }
        /* Efecto Flotante Glassmorphism */
        .card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 25px;
            padding: 25px;
            width: 100%;
            max-width: 400px;
            margin-bottom: 30px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-10px);
        }
        h2 { color: #1c64f2; margin-top: 0; font-weight: 600; }
        .btn {
            background: #1c64f2;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 15px;
            width: 100%;
            cursor: pointer;
            font-weight: 600;
            margin-bottom: 10px;
            box-shadow: 0 4px 15px rgba(28, 100, 242, 0.2);
        }
        .btn:hover { background: #1a56db; }
        .ia-box {
            text-align: left;
            background: rgba(255, 255, 255, 0.5);
            padding: 15px;
            border-radius: 15px;
            margin-top: 15px;
            border-left: 5px solid #1c64f2;
            font-size: 14px;
        }
        .img-ia {
            width: 100%;
            border-radius: 20px;
            margin-top: 15px;
            display: none;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        #karma-bubble {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #1c64f2;
            color: white;
            padding: 12px 18px;
            border-radius: 50px;
            font-weight: bold;
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
            z-index: 1000;
        }
    </style>
</head>
<body>
    <div id="karma-bubble">Karma: <span id="kVal">0</span></div>

    <div class="card">
        <h2>Buscador de Roma 🏛️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:12px; border-radius:12px; border:1px solid #d1d5db; box-sizing: border-box;" placeholder="Ej: Gladiador, Centurión...">
        <button class="btn" style="margin-top:15px;" onclick="consultarIA(document.getElementById('iaInput').value)">Buscar Imagen Real</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <img id="iaImg" class="img-ia" src="">
    </div>

    <div class="card">
        <h2>Trivia de la Antigua Roma ⚔️</h2>
        <p id="qText" style="font-weight: 600; margin-bottom: 20px;"></p>
        <div id="optionsContainer"></div>
        <p id="feedback" style="margin-top: 15px; font-weight: bold;"></p>
        <button class="btn" id="nextBtn" style="display:none; background: #10b981;" onclick="siguientePregunta()">Siguiente Pregunta</button>
    </div>

    <script>
        let karma = 0;
        let pActual = 0;

        const preguntas = [
            { q: "¿Quién fue el primer emperador de Roma?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"] },
            { q: "¿Cómo se llamaba la plaza principal de la ciudad?", a: "Foro Romano", ops: ["Coliseo", "Panteón", "Foro Romano"] },
            { q: "¿Qué río atraviesa la ciudad de Roma?", a: "Tíber", ops: ["Nilo", "Tíber", "Danubio"] },
            { q: "¿Cómo llamaban los romanos a los soldados de infantería?", a: "Legionarios", ops: ["Gladiadores", "Legionarios", "Pretorianos"] },
            { q: "¿Qué animal amamantó a Rómulo y Remo?", a: "Loba", ops: ["Leona", "Loba", "Osa"] }
        ];

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
                b.onclick = () => verificar(op);
                container.appendChild(b);
            });
        }

        function verificar(op) {
            const f = document.getElementById('feedback');
            if(op === preguntas[pActual].a) {
                f.innerText = "¡CORRECTO! 🎉"; f.style.color = "#10b981";
                karma += 25; document.getElementById('kVal').innerText = karma;
            } else {
                f.innerText = "Incorrecto. La respuesta era: " + preguntas[pActual].a;
                f.style.color = "#ef4444";
            }
            document.getElementById('nextBtn').style.display = "block";
            const btns = document.querySelectorAll('#optionsContainer .btn');
            btns.forEach(btn => btn.disabled = true);
        }

        function siguientePregunta() {
            pActual = (pActual + 1) % preguntas.length;
            cargarPregunta();
        }

        async function consultarIA(t) {
            const resDiv = document.getElementById('iaRes');
            const img = document.getElementById('iaImg');
            resDiv.style.display = "block";
            resDiv.innerHTML = "Buscando información real... ✨";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                if(d.extract) {
                    resDiv.innerHTML = `<b>Información encontrada:</b><br>${d.extract}`;
                    if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = "block"; }
                    karma += 10; document.getElementById('kVal').innerText = karma;
                }
            } catch(e) { resDiv.innerHTML = "No se pudo conectar."; }
        }

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
