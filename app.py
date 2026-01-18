from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Imperio Romano: Plus Ultra</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --blue: #007bff; --glass: rgba(255, 255, 255, 0.8); }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #bbdefb 100%);
            background-attachment: fixed; display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }

        /* ANIMACIÓN DE INTRODUCCIÓN */
        #intro-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #fff; z-index: 9999; display: flex; flex-direction: column;
            justify-content: center; align-items: center; transition: 1s;
        }
        .soldier-icon { font-size: 50px; animation: moveSoldier 2s infinite; }
        @keyframes moveSoldier {
            0% { transform: translateX(-50px); }
            50% { transform: translateX(50px); }
            100% { transform: translateX(-50px); }
        }

        /* DISEÑO DE CRISTAL FLOTANTE */
        .card {
            background: var(--glass); backdrop-filter: blur(15px);
            border-radius: 30px; padding: 25px; width: 90%; max-width: 400px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.6);
            box-shadow: 0 20px 50px rgba(0, 123, 255, 0.15);
            text-align: center; animation: float 5s ease-in-out infinite;
        }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }

        /* ALL MIGHT MINIATURA */
        #allmight-container {
            position: fixed; bottom: 20px; right: 20px; z-index: 1000;
            display: flex; flex-direction: column; align-items: center;
        }
        #all_might_img {
            width: 80px; height: 80px;
            background: url('https://i.imgur.com/vH9vIqy.png') no-repeat center/contain;
            filter: drop-shadow(0 5px 15px rgba(0,0,0,0.3));
        }
        .bubble {
            background: white; padding: 8px 12px; border-radius: 15px;
            font-size: 12px; font-weight: bold; margin-bottom: 5px;
            border: 2px solid var(--blue); display: none;
        }
    </style>
</head>
<body>

    <div id="intro-screen">
        <div class="soldier-icon">💂‍♂️🏹</div>
        <h1 style="color: #007bff;">¡PREPÁRATE JOVEN!</h1>
        <p>Cargando el Imperio Romano...</p>
        <button class="btn" style="width:200px; background:#ffcc00; color:black;" onclick="empezar()">¡ENTRAR!</button>
    </div>

    <div id="allmight-container">
        <div class="bubble" id="am-talk">¡YA ESTOY AQUÍ!</div>
        <div id="all_might_img"></div>
    </div>

    <div class="card">
        <h2>Buscador Romano 🏛️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:12px; border-radius:10px; border:1px solid #ddd;" placeholder="Ej: Comida romana...">
        <button class="btn" style="background:#007bff; color:white; padding:10px; width:100%; border:none; border-radius:10px; margin-top:10px;" onclick="consultarIA()">BUSCAR</button>
        <div id="iaRes" style="margin-top:10px; font-size:14px;"></div>
    </div>

    <div class="card">
        <h2>Trivia Plus Ultra ⚔️</h2>
        <p id="qText" style="font-weight:bold;"></p>
        <div id="optionsContainer"></div>
    </div>

    <script>
        function empezar() {
            document.getElementById('intro-screen').style.opacity = '0';
            setTimeout(() => {
                document.getElementById('intro-screen').style.display = 'none';
                hablar("¡Bienvenido al Imperio Romano! ¡Esfuérzate al máximo!");
            }, 1000);
        }

        function hablar(msj) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(msj);
            utter.lang = 'es-ES'; utter.pitch = 0.8; utter.rate = 0.85;
            window.speechSynthesis.speak(utter);
            document.getElementById('am-talk').innerText = msj;
            document.getElementById('am-talk').style.display = "block";
            setTimeout(() => document.getElementById('am-talk').style.display = "none", 4000);
        }

        // --- Lógica de Trivia y Buscador similar a las versiones anteriores ---
        let pActual = 0;
        const preguntas = [{q:"¿Qué era el Garum?", a:"Salsa de pescado", ops:["Vino","Salsa de pescado","Pan"]}];
        
        function cargarPregunta() {
            const d = preguntas[pActual];
            document.getElementById('qText').innerText = d.q;
            const container = document.getElementById('optionsContainer');
            container.innerHTML = "";
            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.innerText = o; b.style.width="100%"; b.style.margin="5px 0";
                b.onclick = () => {
                    if(o === d.a) { hablar("¡Correcto! ¡Eres un verdadero héroe!"); }
                    else { hablar("¡No te rindas! ¡Inténtalo de nuevo!"); }
                };
                container.appendChild(b);
            });
        }

        async function consultarIA() {
            const t = document.getElementById('iaInput').value;
            const res = document.getElementById('iaRes');
            res.innerHTML = "Buscando...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                res.innerHTML = d.extract || "No encontré nada.";
            } catch(e) { res.innerHTML = "Error de conexión."; }
        }

        window.onload = cargarPregunta;
    </script>
</body>
</html>
