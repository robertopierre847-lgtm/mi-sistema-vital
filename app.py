import os
from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Desafío Vital - Roberto Pierre</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Cinzel:wght@700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --azul: #007bff; 
            --rojo: #dc3545; 
            --verde: #28a745;
            --oro: #ffd700;
            --cristal: rgba(255, 255, 255, 0.8); 
        }
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
            cursor: pointer; text-align: center; transition: 0.5s;
        }
        #aguila-anim { font-size: 100px; transition: 0.1s; }
        .crack {
            position: absolute; inset: 0; background: url('https://www.transparentpng.com/download/glass-shatter/shattered-glass-background-png-6.png');
            background-size: cover; opacity: 0; pointer-events: none;
        }

        /* --- BUSCADOR CRISTAL --- */
        .glass-card-search {
            background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(15px);
            border-radius: 25px; padding: 20px; width: 90%; max-width: 450px;
            margin-top: 50px; border: 1px solid rgba(255,255,255,0.6); text-align: center;
        }
        #res-img { width: 100%; border-radius: 15px; margin-top: 10px; display: none; }

        /* --- TRIVIA --- */
        .glass-card {
            background: var(--cristal); backdrop-filter: blur(10px);
            border-radius: 30px; padding: 25px; width: 90%; max-width: 450px;
            margin: 20px 0; border: 1px solid white; text-align: center;
        }
        .btn-hero { 
            background: var(--azul); color: white; border: none; padding: 14px; 
            width: 100%; border-radius: 15px; font-weight: bold; margin-top: 10px; cursor: pointer;
            transition: background 0.2s;
        }
        .btn-correct { background: var(--verde) !important; }
        .btn-wrong { background: var(--rojo) !important; }

        .reto-box { margin-top: 15px; padding: 15px; border: 3px dashed var(--rojo); color: var(--rojo); display: none; border-radius: 15px; font-weight: bold; }
        
        input { width: 100%; padding: 12px; border-radius: 15px; border: 1px solid var(--azul); outline: none; margin-bottom: 10px; box-sizing: border-box; }

        /* SALA RELAJACIÓN */
        .relax-zone {
            background: rgba(255, 255, 255, 0.5); backdrop-filter: blur(10px);
            border-radius: 25px; padding: 20px; width: 90%; max-width: 450px;
            margin-bottom: 50px; text-align: center; border: 1px solid white;
        }
        .rango-badge {
            background: var(--oro); color: #333; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 10px;
        }
    </style>
</head>
<body>

    <div id="intro-capa" onclick="picotear()">
        <div class="crack" id="vidrio"></div>
        <div id="aguila-anim">🧘‍♂️</div>
        <h2 style="font-family: 'Cinzel'; color: var(--azul);">PICA PARA EMPEZAR</h2>
        <p id="hits-txt">Quedan: 5</p>
    </div>

    <div class="glass-card-search">
        <h3 style="font-family: 'Cinzel'; color: var(--azul); margin: 0;">Buscador Vital</h3>
        <input type="text" id="bus" placeholder="Busca algo de la vida...">
        <button class="btn-hero" onclick="buscar()">CONSULTAR</button>
        <img id="res-img" src="">
        <p id="res-txt" style="font-size: 13px; color: #444; margin-top: 10px;"></p>
    </div>

    <div class="glass-card">
        <div id="game-ui">
            <div id="rango" class="rango-badge">Rango: Novato</div>
            <div style="color: var(--azul); font-weight: bold;">Nivel <span id="num">1</span>/10</div>
            <h2 id="pregunta" style="font-size: 18px; color: #333; margin: 15px 0;"></h2>
            <div id="opciones"></div>
            <div id="reto" class="reto-box"></div>
        </div>
        <div id="win-ui" style="display:none;">
            <h1 style="color: var(--verde);">🏆 ¡MAESTRO DE LA VIDA!</h1>
            <p id="premio-final" style="font-weight: bold; color: var(--oro);"></p>
            <button class="btn-hero" onclick="location.reload()">VOLVER A JUGAR</button>
        </div>
    </div>

    <div class="relax-zone">
        <h4 style="margin: 0; color: var(--verde);">Sala de Relajación</h4>
        <p style="font-size: 12px;">Escucha música suave mientras descansas</p>
        <audio id="player" controls style="width: 100%; margin-top: 10px;">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
        </audio>
        <div style="margin-top: 10px;">
            <button onclick="cambiarMusica(1)" style="font-size: 10px; padding: 5px;">Zen 1</button>
            <button onclick="cambiarMusica(2)" style="font-size: 10px; padding: 5px;">Zen 2</button>
            <button onclick="cambiarMusica(3)" style="font-size: 10px; padding: 5px;">Zen 3</button>
        </div>
    </div>

    <script>
        let clicks = 5;
        function picotear() {
            clicks--;
            document.getElementById('hits-txt').innerText = "Quedan: " + clicks;
            if(clicks <= 0) {
                document.getElementById('intro-capa').style.display = "none";
                cargarPregunta();
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
                txt.innerText = d.extract || "Sin resultados.";
                if(d.thumbnail) {
                    img.src = d.thumbnail.source;
                    img.style.display = "block";
                } else { img.style.display = "none"; }
            } catch(e) { txt.innerText = "Error."; }
        }

        function cambiarMusica(track) {
            const p = document.getElementById('player');
            const tracks = {
                1: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                2: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                3: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
            };
            p.src = tracks[track];
            p.play();
        }

        let current = 0;
        const preguntas = [
            {q: "Nivel 1: ¿Cuántas horas mínimo debe dormir un adulto?", a: "7-8 horas", o: ["4-5 horas", "7-8 horas", "10-12 horas"], ex: "Haz 5 sentadillas"},
            {q: "Nivel 2: ¿Cuál es el gasto hormiga más común?", a: "Café diario", o: ["Alquiler", "Seguro", "Café diario"], ex: "Haz 5 flexiones"},
            {q: "Nivel 3: ¿Qué nutriente es la principal fuente de energía?", a: "Carbohidratos", o: ["Carbohidratos", "Vitaminas", "Sal"], ex: "Toca la punta de tus pies 5 veces"},
            {q: "Nivel 4: ¿Qué técnica ayuda a concentrarse 25 min?", a: "Pomodoro", o: ["Siesta", "Pomodoro", "Multitarea"], ex: "Salta 10 veces"},
            {q: "Nivel 5: ¿Cuánta agua debe beberse al día aprox.?", a: "2 litros", o: ["1 litro", "2 litros", "5 litros"], ex: "Mantén el equilibrio en un pie 15 seg"},
            {q: "Nivel 6: ¿Qué reduce el estrés de forma inmediata?", a: "Respirar profundo", o: ["Gritar", "Respirar profundo", "Comer dulce"], ex: "Haz 10 abdominales"},
            {q: "Nivel 7: ¿Qué es mejor para la salud financiera?", a: "Ahorrar el 10%", o: ["Ahorrar el 10%", "Gastar todo", "Pedir créditos"], ex: "Estira tus brazos hacia arriba 20 seg"},
            {q: "Nivel 8: ¿Cómo se llama posponer lo importante?", a: "Procrastinar", o: ["Dormir", "Procrastinar", "Delegar"], ex: "Haz 5 burpees"},
            {q: "Nivel 9: ¿Qué vitamina aporta el sol?", a: "Vitamina D", o: ["Vitamina C", "Vitamina D", "Vitamina B12"], ex: "Mueve el cuello en círculos 10 veces"},
            {q: "Nivel 10: ¿Cuál es la clave de la felicidad según estudios?", a: "Relaciones sanas", o: ["Dinero", "Fama", "Relaciones sanas"], ex: "Haz 20 saltos de tijera (Jumping Jacks)"}
        ];

        const rangos = ["Novato", "Aprendiz", "Intermedio", "Avanzado", "Experto", "Sabio", "Gurú", "Maestro", "Leyenda", "Avatar Vital"];
        const premios = ["Medalla de Bronce", "Medalla de Plata", "Trofeo de Oro", "Capa de Sabiduría", "Llave del Éxito"];

        function cargarPregunta() {
            if(current >= preguntas.length) {
                document.getElementById('game-ui').style.display = "none";
                document.getElementById('win-ui').style.display = "block";
                document.getElementById('premio-final').innerText = "PREMIO: " + premios[Math.floor(Math.random()*premios.length)];
                return;
            }
            const p = preguntas[current];
            document.getElementById('num').innerText = current + 1;
            document.getElementById('rango').innerText = "Rango: " + rangos[current];
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
                        btn.classList.add('btn-correct');
                        setTimeout(() => { current++; cargarPregunta(); }, 1000);
                    } else {
                        btn.classList.add('btn-wrong');
                        const r = document.getElementById('reto');
                        r.innerHTML = "⏮️ ¡ERROR! Retrocediendo... <br> PENITENCIA: " + p.ex;
                        r.style.display = "block";
                        setTimeout(() => {
                            if(current > 0) current--;
                            cargarPregunta();
                        }, 3000);
                    }
                };
                ops.appendChild(btn);
            });
        }
    </script>
</body>
</html>
