import os
from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roma Plus Ultra: Edición Cristal</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --cristal: rgba(255, 255, 255, 0.7); }
        
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #bbdefb 100%);
            background-attachment: fixed;
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }

        /* Pantalla de Intro Azul */
        #intro {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--azul); color: white; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: 1s ease-in-out; text-align: center;
        }

        /* Efecto Cristal y Flotante */
        .glass-card {
            background: var(--cristal);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 30px;
            padding: 25px;
            width: 90%; max-width: 450px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 20px 50px rgba(0, 123, 255, 0.1);
            animation: float 5s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        /* Botones Estilo Héroe */
        .btn-hero {
            background: var(--azul); color: white; border: none;
            padding: 12px; width: 100%; border-radius: 12px;
            font-weight: bold; cursor: pointer; transition: 0.3s;
            margin-top: 10px; font-size: 16px;
        }
        .btn-hero:hover { transform: scale(1.02); background: #0056b3; }

        /* All Might Mini */
        #am-mini {
            position: fixed; bottom: 20px; right: 20px;
            width: 80px; height: 80px; z-index: 1000;
        }
        #am-mini img {
            width: 100%; height: 100%; border-radius: 50%;
            border: 4px solid white; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        /* Resultados del Buscador */
        #search-img { width: 100%; border-radius: 15px; margin-top: 15px; display: none; }
        .reto-text { color: #dc3545; font-weight: bold; margin-top: 10px; display: none; }
    </style>
</head>
<body>

    <div id="intro">
        <h1 style="font-size: 60px; margin: 0;">🏛️</h1>
        <h2 style="padding: 0 20px;">¡SISTEMA VITAL ROMANO!</h2>
        <button class="btn-hero" style="width: 200px; background: #ffcc00; color: #000;" onclick="entrar()">¡PLUS ULTRA!</button>
    </div>

    <div id="am-mini">
        <img src="https://images.fineartamerica.com/images/artworkimages/mediumlarge/3/all-might-my-hero-academia-andrea-matsumoto.jpg">
    </div>

    <div class="glass-card" style="margin-top: 40px;">
        <h2 style="color: var(--azul); margin-top: 0;">Buscador Imperial 🔍</h2>
        <input type="text" id="bus" style="width:100%; padding:12px; border-radius:10px; border:1px solid #ddd; box-sizing: border-box;" placeholder="Busca Gladiadores, César...">
        <button class="btn-hero" onclick="buscar()">CONSULTAR WIKIPEDIA</button>
        <div id="res-txt" style="margin-top:15px; font-size: 14px; text-align: left;"></div>
        <img id="search-img">
    </div>

    <div class="glass-card">
        <h2 style="color: var(--azul); margin-top: 0;">Trivia: Pregunta <span id="num">1</span>/30</h2>
        <p id="pregunta" style="font-weight: bold; font-size: 17px;"></p>
        <div id="opciones"></div>
        <div id="reto" class="reto-text">RETO: ¡Escribe 10 veces 'Perdí' en una hoja!</div>
    </div>

    <script>
        function entrar() {
            document.getElementById('intro').style.transform = 'translateY(-100%)';
            hablar("¡Ya estoy aquí para enseñarte historia, joven!");
        }

        function hablar(t) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(t);
            u.lang = 'es-ES'; u.pitch = 0.8;
            window.speechSynthesis.speak(u);
        }

        async function buscar() {
            const t = document.getElementById('bus').value;
            const txt = document.getElementById('res-txt');
            const img = document.getElementById('search-img');
            txt.innerHTML = "Buscando en los archivos...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(t)}`);
                const d = await r.json();
                txt.innerHTML = d.extract || "No encontré nada, joven.";
                if(d.thumbnail) {
                    img.src = d.thumbnail.source;
                    img.style.display = 'block';
                } else { img.style.display = 'none'; }
                hablar("He encontrado esto sobre " + t);
            } catch(e) { txt.innerHTML = "Error de conexión."; }
        }

        const preguntas = [
            {q: "¿Cómo conservaban los romanos la carne por meses?", a: "Salazón y Humo", ops: ["Hielo", "Salazón y Humo", "Azúcar"]},
            {q: "¿Qué idioma hablaban los antiguos romanos?", a: "Latín", ops: ["Latín", "Griego", "Italiano"]},
            {q: "¿Quién fue el primer emperador romano?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"]}
            // Agrega aquí las otras 27 preguntas...
        ];

        let index = 0;
        function cargar() {
            const d = preguntas[index];
            document.getElementById('num').innerText = index + 1;
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            const rTxt = document.getElementById('reto');
            cont.innerHTML = ""; rTxt.style.display = "none";

            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero';
                b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) {
                        b.style.background = "#28a745";
                        hablar("¡Soberbio! ¡Siguiente nivel!");
                        setTimeout(() => { index++; if(index < preguntas.length) cargar(); }, 1000);
                    } else {
                        b.style.background = "#dc3545";
                        hablar("¡Fallaste! ¡Cumple tu reto escolar!");
                        rTxt.style.display = "block";
                    }
                };
                cont.appendChild(b);
            });
        }
        window.onload = cargar;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

if __name__ == '__main__':
    # Esto es lo que evita el error Status 1 en Render
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
