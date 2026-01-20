import os
from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Desafío Cotidiano - Roberto Pierre</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Cinzel:wght@700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --azul: #007bff; 
            --rojo: #dc3545; 
            --verde: #28a745;
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

        /* --- SALA DE RELAJACIÓN --- */
        .relaxation-card {
            background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(15px);
            border-radius: 25px; padding: 20px; width: 90%; max-width: 450px;
            margin: 30px 0; border: 1px solid rgba(255,255,255,0.6); text-align: center;
        }
        .audio-player {
            width: 100%;
            margin-top: 15px;
        }
        .zen-image {
            width: 100%;
            max-height: 200px;
            object-fit: cover;
            border-radius: 15px;
            margin-top: 15px;
        }
    </style>
</head>
<body>

    <div id="intro-capa" onclick="picotear()">
        <div class="crack" id="vidrio"></div>
        <div id="aguila-anim">🧠</div>
        <h2 style="font-family: 'Cinzel'; color: var(--azul);">PICA LA PANTALLA</h2>
        <p id="hits-txt">Quedan: 5</p>
    </div>

    <div class="glass-card-search">
        <h3 style="font-family: 'Cinzel'; color: var(--azul); margin: 0;">Buscador de Vida</h3>
        <input type="text" id="bus" placeholder="Busca un concepto cotidiano...">
        <button class="btn-hero" onclick="buscar()">CONSULTAR</button>
        <img id="res-img" src="">
        <p id="res-txt" style="font-size: 13px; color: #444; margin-top: 10px;"></p>
    </div>

    <div class="glass-card">
        <div id="game-ui">
            <div style="color: var(--azul); font-weight: bold;">Nivel <span id="num">1</span>/10</div>
            <h2 id="pregunta" style="font-size: 18px; color: #333; margin: 15px 0;"></h2>
            <div id="opciones"></div>
            <div id="reto" class="reto-box">❌ ¡ERROR! <br> Retrocedes un nivel...</div>
        </div>
        <div id="win-ui" style="display:none;">
            <h1 style="color: var(--verde);">🏆 ¡MAESTRÍA LOGRADA!</h1>
            <p>Has demostrado gran agilidad mental cotidiana.</p>
            <button class="btn-hero" onclick="location.reload()">REINICIAR</button>
        </div>
    </div>

    <div class="relaxation-card">
        <h3 style="font-family: 'Cinzel'; color: var(--verde); margin: 0;">Sala de Relajación</h3>
        <p style="font-size: 14px; color: #555;">Tómate un descanso y relaja tu mente.</p>
        <img src="https://images.pexels.com/photos/326055/pexels-photo-326055.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" alt="Paisaje relajante" class="zen-image">
        <audio controls loop class="audio-player">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
            Tu navegador no soporta el elemento de audio.
        </audio>
        <p style="font-size: 12px; color: #777;">Música suave para meditar.</p>
    </div>

    <audio id="audio-correct" src="https://www.soundjay.com/buttons/sounds/button-10.mp3" preload="auto"></audio>
    <audio id="audio-wrong" src="https://www.soundjay.com/buttons/sounds/button-9.mp3" preload="auto"></audio>
    <audio id="audio-win" src="https://www.soundjay.com/misc/sounds/success-sound.mp3" preload="auto"></audio>

    <script>
        let clicks = 5;
        function picotear() {
            clicks--;
            document.getElementById('hits-txt').innerText = "Quedan: " + clicks;
            document.getElementById('aguila-anim').style.transform = "scale(1.4)";
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
            img.style.display = "none"; // Ocultar imagen anterior

            try {
                // Intenta buscar en Wikipedia para texto
                const rWiki = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`);
                const dWiki = await rWiki.json();
                
                let foundImage = false;
                if(dWiki.thumbnail && dWiki.thumbnail.source) {
                    img.src = dWiki.thumbnail.source;
                    img.style.display = "block";
                    foundImage = true;
                } else {
                    // Si Wikipedia no tiene imagen, intenta buscar una imagen genérica (ejemplo con Unsplash API)
                    // NOTA: Para producción, necesitarías una API Key real y manejar los límites de solicitudes
                    try {
                        const rImage = await fetch(`https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&client_id=YOUR_UNSPLASH_ACCESS_KEY`); // ¡CAMBIA ESTO!
                        const dImage = await rImage.json();
                        if (dImage.results && dImage.results.length > 0) {
                            img.src = dImage.results[0].urls.small;
                            img.style.display = "block";
                            foundImage = true;
                        }
                    } catch (imageError) {
                        console.error("Error buscando imagen en Unsplash:", imageError);
                        // Fallback o mostrar un mensaje si no se encuentra imagen
                    }
                }
                
                txt.innerText = dWiki.extract || "Sin resultados. Intenta con otra búsqueda.";
                if (!foundImage && !dWiki.thumbnail) { // Si no se encontró ninguna imagen
                    img.style.display = "none";
                }
            } catch(e) { 
                txt.innerText = "Error de conexión o al buscar la información.";
                img.style.display = "none";
            }
        }


        let current = 0;
        const preguntas = [
            {q: "Si duermes 8 horas al día, ¿qué porcentaje del año pasas durmiendo?", a: "33%", o: ["25%", "33%", "50%"]},
            {q: "¿Cuál es el primer paso recomendado para ahorrar?", a: "Hacer un presupuesto", o: ["Hacer un presupuesto", "Gastar en ofertas", "No comer"]},
            {q: "Para mejorar la memoria, ¿qué es más efectivo?", a: "Dormir bien", o: ["Beber café", "Dormir bien", "Mirar el móvil"]},
            {q: "¿Qué fruta tiene más vitamina C que la naranja?", a: "Kiwi", o: ["Kiwi", "Manzana", "Pera"]},
            {q: "Si caminas 10,000 pasos al día, ¿aprox. cuántos km son?", a: "7-8 km", o: ["2-3 km", "15 km", "7-8 km"]},
            {q: "¿Cómo se llama el hábito de posponer tareas?", a: "Procrastinar", o: ["Procrastinar", "Relajarse", "Organizar"]},
            {q: "¿Cuál es la forma más rápida de enfriar una bebida?", a: "Agua, hielo y sal", o: ["Congelador solo", "Nevera", "Agua, hielo y sal"]},
            {q: "¿Qué luz ayuda a dormir mejor por la noche?", a: "Luz cálida/Tenue", o: ["Luz azul", "Luz blanca", "Luz cálida/Tenue"]},
            {q: "¿Cuál es la base de una buena hidratación?", a: "Agua", o: ["Refrescos", "Agua", "Jugos"]},
            {q: "¿Qué técnica divide el trabajo en bloques de 25 min?", a: "Pomodoro", o: ["Pomodoro", "Scrum", "Eisenhower"]}
        ];

        function cargarPregunta() {
            if(current < 0) current = 0; 
            
            if(current >= preguntas.length) {
                document.getElementById('game-ui').style.display = "none";
                document.getElementById('win-ui').style.display = "block";
                document.getElementById('audio-win').play(); // Sonido de victoria
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
                    const todosLosBotones = ops.querySelectorAll('button');
                    todosLosBotones.forEach(b => b.disabled = true);

                    if(opt === p.a) {
                        btn.classList.add('btn-correct');
                        document.getElementById('audio-correct').play(); // Sonido correcto
                        setTimeout(() => {
                            current++;
                            cargarPregunta();
                        }, 800);
                    } else {
                        btn.classList.add('btn-wrong');
                        document.getElementById('audio-wrong').play(); // Sonido incorrecto
                        document.getElementById('reto').style.display = "block";
                        setTimeout(() => {
                            current--; 
                            cargarPregunta();
                        }, 1500);
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
