from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Imperio Romano Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --azul-primario: #007bff;
            --azul-oscuro: #0056b3;
            --fondo-gradiente: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
        }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: var(--fondo-gradiente);
            background-attachment: fixed;
            display: flex; flex-direction: column; align-items: center;
            padding: 20px; min-height: 100vh; color: #333;
        }
        .card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 30px;
            padding: 30px; width: 100%; max-width: 450px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 123, 255, 0.1);
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .card:hover { transform: translateY(-10px); }
        h2 { color: var(--azul-primario); margin-top: 0; font-weight: 600; }
        .btn {
            background: var(--azul-primario); color: white; border: none;
            padding: 15px; border-radius: 20px; width: 100%;
            cursor: pointer; font-weight: 600; margin-bottom: 12px;
            transition: all 0.3s;
        }
        .btn:hover { background: var(--azul-oscuro); transform: scale(1.02); }
        .btn-audio { background: #6c757d; margin-top: 10px; font-size: 0.9em; }
        .ia-box {
            text-align: left; background: white; padding: 20px;
            border-radius: 20px; margin-top: 20px;
            border-left: 6px solid var(--azul-primario); font-size: 14px;
        }
        .img-ia { width: 100%; border-radius: 20px; margin-top: 20px; display: none; }
        #karma-bubble {
            position: fixed; top: 20px; right: 20px;
            background: white; color: var(--azul-primario);
            padding: 12px 20px; border-radius: 50px; font-weight: bold;
            box-shadow: 0 10px 30px rgba(0,123,255,0.2);
            z-index: 1000; border: 2px solid var(--azul-primario);
        }
        input {
            width: 100%; padding: 15px; border-radius: 15px;
            border: 2px solid #e3f2fd; outline: none; box-sizing: border-box;
        }
    </style>
</head>
<body>
    <div id="karma-bubble">Karma: <span id="kVal">0</span></div>

    <div class="card">
        <h2>Buscador con Voz 🏛️</h2>
        <input type="text" id="iaInput" placeholder="Ej: Gladiador, Acueducto...">
        <button class="btn" style="margin-top:15px;" onclick="consultarIA(document.getElementById('iaInput').value)">Buscar Datos</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <button id="btnLeer" class="btn btn-audio" style="display:none;" onclick="leerTexto()">🔊 Leer Información</button>
        <img id="iaImg" class="img-ia" src="">
    </div>

    <div class="card">
        <h2>Trivia Romana ⚔️</h2>
        <p id="qText" style="font-weight: 600; margin-bottom: 20px;"></p>
        <div id="optionsContainer"></div>
        <button class="btn" id="nextBtn" style="display:none; background: #28a745;" onclick="siguientePregunta()">Siguiente Desafío</button>
    </div>

    <script>
        let karma = 0;
        let pActual = 0;
        let textoParaLeer = "";

        const preguntas = [
            { q: "¿Qué emperador nombró a su caballo cónsul?", a: "Calígula", ops: ["Nerón", "Calígula", "Trajano"] },
            { q: "¿Cómo se llama la formación que imitaba a una tortuga?", a: "Testudo", ops: ["Testudo", "Falange", "Triarii"] },
            { q: "¿Quién cruzó los Alpes con elefantes?", a: "Aníbal", ops: ["Aníbal", "Atila", "Espartaco"] }
        ];

        function hablar(mensaje) {
            const synth = window.speechSynthesis;
            const utterThis = new SpeechSynthesisUtterance(mensaje);
            utterThis.lang = 'es-ES';
            synth.speak(utterThis);
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
                b.onclick = () => verificar(op);
                container.appendChild(b);
            });
        }

        function verificar(op) {
            if(op === preguntas[pActual].a) {
                hablar("¡Excelente! Respuesta correcta.");
                karma += 50;
            } else {
                hablar("Incorrecto. Inténtalo de nuevo.");
                karma = Math.max(0, karma - 10);
            }
            document.getElementById('kVal').innerText = karma;
            document.getElementById('nextBtn').style.display = "block";
        }

        function siguientePregunta() {
            pActual = (pActual + 1) % preguntas.length;
            cargarPregunta();
        }

        async function consultarIA(t) {
            const resDiv = document.getElementById('iaRes');
            const img = document.getElementById('iaImg');
            const btnLeer = document.getElementById('btnLeer');
            resDiv.style.display = "block";
            resDiv.innerHTML = "Consultando archivos...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                if(d.extract) {
                    resDiv.innerHTML = d.extract;
                    textoParaLeer = d.extract;
                    btnLeer.style.display = "block";
                    if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = "block"; }
                }
            } catch(e) { resDiv.innerHTML = "Error de conexión."; }
        }

        function leerTexto() {
            hablar(textoParaLeer);
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
    
