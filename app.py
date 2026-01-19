import os
from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Imperio Romano - Roberto Pierre</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Cinzel:wght@700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --rojo: #dc3545; --cristal: rgba(255, 255, 255, 0.8); }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #bbdefb 100%);
            background-attachment: fixed;
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }

        /* --- INTRO ÁGUILA --- */
        #intro-capa {
            position: fixed; inset: 0; background: white; z-index: 10000;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            cursor: pointer; text-align: center;
        }
        #aguila-anim { font-size: 100px; transition: 0.1s; }
        .crack {
            position: absolute; inset: 0; background: url('https://www.transparentpng.com/download/glass-shatter/shattered-glass-background-png-6.png');
            background-size: cover; opacity: 0; pointer-events: none;
        }

        /* --- BUSCADOR CRISTAL CON IMÁGENES --- */
        .glass-card-search {
            background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(15px);
            border-radius: 25px; padding: 20px; width: 90%; max-width: 450px;
            margin-top: 50px; border: 1px solid rgba(255,255,255,0.6); text-align: center;
        }
        #res-img { width: 100%; border-radius: 15px; margin-top: 10px; display: none; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }

        /* --- TRIVIA Y JUEGO --- */
        .glass-card {
            background: var(--cristal); backdrop-filter: blur(10px);
            border-radius: 30px; padding: 25px; width: 90%; max-width: 450px;
            margin: 20px 0; border: 1px solid white; text-align: center;
        }
        .btn-hero { 
            background: var(--azul); color: white; border: none; padding: 14px; 
            width: 100%; border-radius: 15px; font-weight: bold; margin-top: 10px; cursor: pointer;
        }
        .reto-box { margin-top: 15px; padding: 15px; border: 3px dashed var(--rojo); color: var(--rojo); display: none; border-radius: 15px; font-weight: bold; animation: shake 0.5s; }
        
        @keyframes shake { 0%, 100% {transform: translateX(0);} 25% {transform: translateX(-5px);} 75% {transform: translateX(5px);} }
        
        input { width: 100%; padding: 12px; border-radius: 15px; border: 1px solid var(--azul); outline: none; margin-bottom: 10px; box-sizing: border-box; }
        #watermark { position: fixed; bottom: 10px; left: 10px; font-size: 10px; color: var(--azul); font-weight: bold; }
    </style>
</head>
<body>

    <div id="intro-capa" onclick="picotear()">
        <div class="crack" id="vidrio"></div>
        <div id="aguila-anim">🦅</div>
        <h2 style="font-family: 'Cinzel'; color: var(--azul);">PICA LA PANTALLA PARA ENTRAR</h2>
        <p id="hits-txt">Quedan: 5</p>
    </div>

    <div id="watermark">SISTEMA VITAL - ROBERTO PIERRE</div>

    <div class="glass-card-search">
        <h3 style="font-family: 'Cinzel'; color: var(--azul); margin: 0 0 10px 0;">Explorador Romano</h3>
        <input type="text" id="bus" placeholder="Busca un personaje o lugar...">
        <button class="btn-hero" onclick="buscar()">BUSCAR EN ARCHIVOS</button>
        <img id="res-img" src="" alt="resultado">
        <p id="res-txt" style="font-size: 13px; color: #444; margin-top: 10px;"></p>
    </div>

    <div class="glass-card">
        <div id="game-ui">
            <div style="color: var(--azul); font-weight: bold;">Pregunta <span id="num">1</span>/30</div>
            <h2 id="pregunta" style="font-size: 20px; color: #333;"></h2>
            <div id="opciones"></div>
            <div id="reto" class="reto-box">❌ ¡PERDISTE! <br> Debes escribir 'Roma es eterna' 5 veces.</div>
        </div>
        <div id="win-ui" style="display:none;">
            <h1 style="color: #28a745;">🏆 ¡VICTORIA TOTAL!</h1>
            <p>Has conquistado el conocimiento del Imperio.</p>
            <button class="btn-hero" onclick="location.reload()">REINTENTAR</button>
        </div>
    </div>

    <script>
        let clicks = 5;
        function picotear() {
            clicks--;
            document.getElementById('hits-txt').innerText = "Quedan: " + clicks;
            document.getElementById('aguila-anim').style.transform = "scale(1.5) translateY(20px)";
            setTimeout(() => document.getElementById('aguila-anim').style.transform = "scale(1)", 100);
            if(clicks <= 3) document.getElementById('vidrio').style.opacity = "0.5";
            if(clicks <= 0) {
                document.getElementById('intro-capa').style.opacity = "0";
                setTimeout(() => {
                    document.getElementById('intro-capa').style.display = "none";
                    cargarPregunta();
                }, 500);
            }
        }

        async function buscar() {
            const query = document.getElementById('bus').value;
            const txt = document.getElementById('res-txt');
            const img = document.getElementById('res-img');
            if(!query) return;
            txt.innerText = "Buscando...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`);
                const d = await r.json();
                txt.innerText = d.extract || "No encontrado.";
                if(d.originalimage) {
                    img.src = d.originalimage.source;
                    img.style.display = "block";
                } else { img.style.display = "none"; }
            } catch(e) { txt.innerText = "Error de red."; }
        }

        let current = 0;
        const preguntas = [
            {q: "¿Quién fue el primer emperador?", a: "Augusto", o: ["César", "Augusto", "Trajano"]},
            {q: "¿Qué río cruza Roma?", a: "Tíber", o: ["Nilo", "Tíber", "Ebro"]},
            {q: "¿En qué año cayó el Imperio de Occidente?", a: "476", o: ["1492", "476", "300"]}
        ];

        function cargarPregunta() {
            if(current >= preguntas.length) {
                document.getElementById('game-ui').style.display = "none";
                document.getElementById('win-ui').style.display = "block";
                return;
            }
            const p = preguntas[current];
            document.getElementById('num').innerText = current + 1;
            document.getElementById('pregunta').innerText = p.q;
            document.getElementById('reto').style.display = "none";
            const ops = document.getElementById('opciones');
            ops.innerHTML = "";
            p.o.forEach(opt => {
                const btn = document.createElement('button');
                btn.className = "btn-hero";
                btn.innerText = opt;
                btn.onclick = () => {
                    if(opt === p.a) {
                        current++;
                        cargarPregunta();
                    } else {
                        document.getElementById('reto').style.display = "block";
                    }
                };
                ops.appendChild(btn);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
