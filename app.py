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
            --azul: #007bff; --rojo: #dc3545; --verde: #28a745; --oro: #ffd700; --cristal: rgba(255, 255, 255, 0.9); 
        }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }
        .glass-card {
            background: var(--cristal); backdrop-filter: blur(10px);
            border-radius: 25px; padding: 20px; width: 90%; max-width: 450px;
            margin: 15px 0; border: 1px solid white; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .btn-hero { 
            background: var(--azul); color: white; border: none; padding: 12px; 
            width: 100%; border-radius: 12px; font-weight: bold; margin-top: 8px; cursor: pointer;
        }
        .btn-correct { background: var(--verde) !important; }
        .btn-wrong { background: var(--rojo) !important; }
        .reto-box { 
            margin-top: 15px; padding: 15px; border: 3px dashed var(--rojo); 
            color: var(--rojo); display: none; border-radius: 15px; font-weight: bold; 
            background: rgba(220, 53, 69, 0.1);
        }
        input { 
            width: 100%; padding: 12px; border-radius: 12px; border: 1px solid #ddd; 
            outline: none; margin-bottom: 10px; box-sizing: border-box; 
        }
        .rango-badge { 
            background: var(--oro); color: #333; padding: 5px 15px; 
            border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 10px; 
        }
    </style>
</head>
<body>

    <div class="glass-card">
        <h3 style="color: var(--azul); margin: 0 0 10px 0;">🔍 Buscador Vital</h3>
        <input type="text" id="bus" placeholder="Ej: Meditación, Agua, Sueño...">
        <button class="btn-hero" onclick="buscar()">CONSULTAR</button>
        <p id="res-txt" style="font-size: 13px; color: #444; margin-top: 10px;"></p>
    </div>

    <div class="glass-card">
        <div id="game-ui">
            <div id="rango" class="rango-badge">Rango: Novato</div>
            <div style="color: var(--azul); font-weight: bold;">Nivel <span id="num">1</span>/10</div>
            <h2 id="pregunta" style="font-size: 18px; margin: 15px 0;"></h2>
            <div id="opciones"></div>
            <div id="reto" class="reto-box"></div>
        </div>
        <div id="win-ui" style="display:none;">
            <h1 style="color: var(--verde);">🏆 ¡MAESTRO TOTAL!</h1>
            <p id="premio" style="font-weight: bold; color: #b8860b; font-size: 20px;"></p>
            <button class="btn-hero" onclick="location.reload()">VOLVER A EMPEZAR</button>
        </div>
    </div>

    <div class="glass-card">
        <h4 style="margin: 0; color: var(--verde);">🎵 Música Suave</h4>
        <audio id="player" controls style="width: 100%; margin-top: 10px;">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
        </audio>
    </div>

    <script>
        // BUSCADOR
        async function buscar() {
            const q = document.getElementById('bus').value;
            const t = document.getElementById('res-txt');
            if(!q) return;
            t.innerText = "Buscando...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(q)}`);
                const d = await r.json();
                t.innerText = d.extract || "No encontré información.";
            } catch(e) { t.innerText = "Error de conexión."; }
        }

        // LÓGICA DEL JUEGO
        let current = 0;
        const preguntas = [
            {q: "¿Horas mínimas de sueño?", a: "7-8", o: ["4-5", "7-8", "10-12"], ex: "5 Sentadillas", r: "Novato"},
            {q: "¿Principal fuente de hidratación?", a: "Agua", o: ["Refresco", "Agua", "Café"], ex: "5 Flexiones", r: "Principiante"},
            {q: "¿Qué es procrastinar?", a: "Posponer", o: ["Ahorrar", "Posponer", "Ejercitar"], ex: "10 Saltos", r: "Aprendiz"},
            {q: "¿Vitamina que da el sol?", a: "D", o: ["C", "D", "B12"], ex: "Estira tus brazos 15s", r: "Intermedio"},
            {q: "¿Clave para el ahorro?", a: "Presupuesto", o: ["Gastar", "Presupuesto", "Deudas"], ex: "Toca tus pies 10 veces", r: "Avanzado"},
            {q: "¿Ayuda a reducir el estrés?", a: "Respirar", o: ["Gritar", "Respirar", "Cafeína"], ex: "5 Abdominales", r: "Experto"},
            {q: "¿Fruta con mucha Vitamina C?", a: "Kiwi", o: ["Plátano", "Kiwi", "Manzana"], ex: "Mueve el cuello 10s", r: "Sabio"},
            {q: "¿Técnica Pomodoro?", a: "25 min", o: ["5 min", "25 min", "2 horas"], ex: "Haz 5 Burpees", r: "Maestro"},
            {q: "¿Mejor para el corazón?", a: "Caminar", o: ["Fumar", "Caminar", "Estar sentado"], ex: "Salta la cuerda imaginaria 20s", r: "Leyenda"},
            {q: "¿Base de una vida feliz?", a: "Salud y Amor", o: ["Dinero solo", "Fama", "Salud y Amor"], ex: "20 Jumping Jacks", r: "Avatar Vital"}
        ];

        const premios = ["🏆 Medalla de Diamante", "🌟 Título de Sabio", "👑 Corona del Éxito", "💎 Gema de la Vitalidad"];

        function cargarPregunta() {
            if(current >= preguntas.length) {
                document.getElementById('game-ui').style.display = "none";
                document.getElementById('win-ui').style.display = "block";
                document.getElementById('premio').innerText = premios[Math.floor(Math.random()*premios.length)];
                return;
            }
            const p = preguntas[current];
            document.getElementById('num').innerText = current + 1;
            document.getElementById('rango').innerText = "Rango: " + p.r;
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
                        r.innerHTML = "❌ ¡ERROR! PENITENCIA: <br>" + p.ex;
                        r.style.display = "block";
                        if(current > 0) current--;
                        setTimeout(cargarPregunta, 4000);
                    }
                };
                ops.appendChild(btn);
            });
        }
        cargarPregunta();
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
