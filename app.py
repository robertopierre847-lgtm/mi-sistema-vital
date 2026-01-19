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
        :root { 
            --azul: #007bff; 
            --rojo: #dc3545; 
            --cristal: rgba(255, 255, 255, 0.7); 
        }
        
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #bbdefb 100%);
            background-attachment: fixed;
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
            overflow-x: hidden;
        }

        /* --- INTRO INTERACTIVA: EL ÁGUILA --- */
        #intro-capa {
            position: fixed; inset: 0; background: white; z-index: 10000;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            cursor: pointer; transition: 0.8s cubic-bezier(0.7, 0, 0.3, 1);
        }
        #aguila-anim {
            font-size: 100px; transition: transform 0.1s;
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1));
        }
        .crack {
            position: absolute; width: 100%; height: 100%;
            background-image: url('https://www.transparentpng.com/download/glass-shatter/shattered-glass-background-png-6.png');
            background-size: cover; opacity: 0; pointer-events: none;
        }

        /* --- BUSCADOR EFECTO CRISTAL --- */
        .glass-card-search {
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 25px; padding: 20px; width: 90%; max-width: 450px;
            margin-top: 70px; text-align: center; z-index: 10;
            box-shadow: 0 15px 35px rgba(0, 123, 255, 0.1);
        }

        /* --- CARTAS Y BOTONES ORIGINALES --- */
        .glass-card {
            background: var(--cristal); backdrop-filter: blur(10px);
            border-radius: 30px; padding: 25px; width: 90%; max-width: 450px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.8);
            box-shadow: 0 20px 40px rgba(0, 123, 255, 0.1); text-align: center;
            position: relative; z-index: 10;
        }

        .btn-hero { 
            background: var(--azul); color: white; border: none; padding: 14px; 
            width: 100%; border-radius: 15px; font-weight: bold; margin-top: 10px; cursor: pointer;
            transition: 0.3s;
        }
        .btn-hero:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,123,255,0.3); }

        input[type="text"] {
            width: 100%; padding: 12px; border-radius: 15px; box-sizing: border-box;
            background: rgba(255, 255, 255, 0.6); border: 1px solid var(--azul);
            outline: none; color: #333; font-weight: bold; margin-bottom: 10px;
        }

        /* Luces de fondo */
        .bg-circle {
            position: fixed; width: 300px; height: 300px; border-radius: 50%;
            filter: blur(80px); z-index: -1; animation: move 10s infinite alternate;
        }
        .c1 { background: rgba(0, 123, 255, 0.2); top: 10%; left: 10%; }
        .c2 { background: rgba(0, 255, 255, 0.15); bottom: 10%; right: 10%; }

        @keyframes move { from { transform: translate(0,0); } to { transform: translate(50px, 80px); } }

        #watermark { position: fixed; bottom: 20px; left: 20px; background: white; color: var(--azul); padding: 8px 12px; border-radius: 10px; font-weight: bold; border: 2px solid var(--azul); font-size: 11px; z-index: 100; }
        .reto-box { margin-top: 15px; padding: 15px; border: 3px dashed var(--rojo); color: var(--rojo); display: none; border-radius: 15px; font-weight: bold; }
    </style>
</head>
<body>

    <div id="intro-capa" onclick="picotear()">
        <div class="crack" id="vidrio"></div>
        <div id="aguila-anim">🦅</div>
        <h2 style="font-family: 'Cinzel'; color: var(--azul); margin-top: 20px;">TOCA PARA QUE EL ÁGUILA ABRA LA PANTALLA</h2>
        <p id="hits-txt" style="color: #666;">Picotazos restantes: 5</p>
    </div>

    <div class="bg-circle c1"></div>
    <div class="bg-circle c2"></div>
    <div id="watermark">ROBERTO PIERRE</div>

    <div class="glass-card-search">
        <h3 style="color: var(--azul); margin-top:0; font-family: 'Cinzel';">Buscador de la Legión 🔍</h3>
        <input type="text" id="bus" placeholder="Escribe para investigar...">
        <button class="btn-hero" onclick="buscar()">CONSULTAR</button>
        <div id="res-txt" style="font-size: 13px; margin-top: 10px; text-align: left; color: #444;"></div>
    </div>

    <div class="glass-card">
        <div style="font-size: 12px; color: var(--azul); font-weight: bold; margin-bottom: 5px;">Rango: <span id="rango-txt">Plebeyo</span></div>
        <div style="font-weight: bold; color: var(--rojo); margin-bottom: 10px;">⏱️ <span id="segundos">15</span>s | Pregunta <span id="num-pregunta">1</span>/30</div>
        <p id="pregunta" style="font-weight: bold; font-size: 18px; margin-bottom: 20px; color: #333;"></p>
        <div id="opciones"></div>
        <div id="reto" class="reto-box"></div>
    </div>

    <script>
        let clicks = 5;
        function picotear() {
            const aguila = document.getElementById('aguila-anim');
            const vidrio = document.getElementById('vidrio');
            const capa = document.getElementById('intro-capa');
            
            clicks--;
            document.getElementById('hits-txt').innerText = "Picotazos restantes: " + clicks;
            
            // Animación de picotazo
            aguila.style.transform = "scale(1.4) translateY(30px)";
            setTimeout(() => { aguila.style.transform = "scale(1)"; }, 100);

            // Aparecen grietas poco a poco
            if(clicks <= 3) vidrio.style.opacity = "0.4";
            if(clicks <= 1) vidrio.style.opacity = "0.8";

            if(clicks <= 0) {
                capa.style.transform = "scale(1.5)";
                capa.style.opacity = "0";
                setTimeout(() => { 
                    capa.style.display = "none"; 
                    cargar(); 
                }, 600);
            }
        }

        let idx = 0;
        const trivia = [
            {q: "¿Primer emperador romano?", a: "Augusto", ops: ["César", "Augusto", "Nerón"]},
            {q: "¿Idioma de Roma?", a: "Latín", ops: ["Latín", "Griego", "Italiano"]},
            {q: "¿Dónde peleaban los gladiadores?", a: "Coliseo", ops: ["Teatro", "Coliseo", "Circo"]}
            // Aquí puedes seguir añadiendo tus 30 preguntas
        ];

        async function buscar() {
            const t = document.getElementById('bus').value;
            const resTxt = document.getElementById('res-txt');
            if(!t) return;
            resTxt.innerText = "Buscando en los pergaminos...";
            try {
                const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(t)}`);
                const d = await res.json();
                resTxt.innerText = d.extract || "No hay resultados.";
            } catch(e) { resTxt.innerText = "Error de conexión."; }
        }

        function cargar() {
            if(idx >= trivia.length) {
                document.getElementById('pregunta').innerText = "¡VICTORIA IMPERIAL!";
                document.getElementById('opciones').innerHTML = "";
                return;
            }
            document.getElementById('num-pregunta').innerText = idx + 1;
            const d = trivia[idx];
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            cont.innerHTML = "";
            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero';
                b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) { idx++; cargar(); }
                    else { 
                        document.getElementById('reto').style.display = "block";
                        document.getElementById('reto').innerText = "RETO: Escribe 'Roma es eterna' 5 veces.";
                    }
                };
                cont.appendChild(b);
            });
        }
    </script>
</body>
</html>
