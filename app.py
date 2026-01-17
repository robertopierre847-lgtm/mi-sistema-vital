from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital Maestro</title>
    <style>
        :root {
            --azul: #00a8ff;
            --blanco: #ffffff;
            --fondo: #f5f7fa;
            --sombra: rgba(0, 168, 255, 0.1);
        }
        * { box-sizing: border-box; }
        body {
            background: var(--fondo);
            font-family: 'Quicksand', sans-serif;
            display: flex; flex-direction: column; align-items: center;
            padding: 20px; margin: 0;
        }
        .panel {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            padding: 25px; border-radius: 35px;
            width: 100%; max-width: 480px;
            margin-bottom: 20px; text-align: center;
            border: 1px solid white;
            box-shadow: 0 10px 30px var(--sombra);
            animation: entrar 0.5s ease-out;
        }
        @keyframes entrar { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        h2 { color: var(--azul); font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px; }
        .btn { 
            background: var(--azul); color: white; border: none; 
            padding: 12px 20px; border-radius: 20px; cursor: pointer; 
            font-weight: bold; transition: 0.3s; margin: 5px;
        }
        .btn:hover { transform: scale(1.05); filter: brightness(1.1); }
        input { 
            width: 85%; padding: 12px; border-radius: 15px; 
            border: 1px solid #eee; outline: none; margin-bottom: 10px;
        }
        
        /* Modulos específicos */
        #timerDisplay { font-size: 2rem; font-weight: bold; color: #333; }
        #waterDisplay { font-size: 1.8rem; margin: 10px 0; }
        .nota-item { 
            background: white; padding: 10px; border-radius: 15px; 
            margin-top: 8px; text-align: left; border-left: 4px solid var(--azul);
            font-size: 0.9rem; box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>

    <div class="panel">
        <h2>Núcleo Azul</h2>
        <input type="text" id="wikiIn" placeholder="Investigar tema...">
        <button class="btn" onclick="buscar()">SCAN</button>
        <div id="resWiki" style="font-size: 0.85rem; text-align: left; margin-top: 15px; color: #555;"></div>
    </div>

    <div class="panel">
        <h2>Hidratación Vital</h2>
        <div id="waterDisplay">💧 0 Vasos</div>
        <button class="btn" onclick="cambiarAgua(1)">+ Vaso</button>
        <button class="btn" onclick="cambiarAgua(-1)" style="background:#eee; color:#666;">-</button>
    </div>

    <div class="panel">
        <h2>Escáner de Enfoque</h2>
        <div id="timerDisplay">25:00</div>
        <button class="btn" onclick="toggleTimer()" id="btnTimer">Iniciar Ciclo</button>
    </div>

    <div class="panel">
        <h2>Memo-Blue</h2>
        <input type="text" id="notaIn" placeholder="Escribe algo importante...">
        <button class="btn" onclick="addNota()">Guardar Nota</button>
        <div id="listaNotas"></div>
    </div>

    <div class="panel">
        <h2>Misión del Día</h2>
        <p id="misionTxt" style="font-weight: 500; font-size: 0.95rem;">Pulsa para recibir una misión...</p>
        <button class="btn" onclick="nuevaMision()">Generar</button>
    </div>

    <script>
        // LÓGICA BUSCADOR
        async function buscar() {
            const q = document.getElementById('wikiIn').value;
            const res = document.getElementById('resWiki');
            if(!q) return;
            res.innerHTML = "Sincronizando con la red...";
            try {
                const url = `https://es.wikipedia.org/api/rest_v1/page/summary/${q.trim().replace(/ /g, '_')}`;
                const r = await fetch(url);
                const d = await r.json();
                res.innerHTML = d.extract ? `<b>${d.title}:</b> ${d.extract}` : "No se hallaron datos.";
            } catch(e) { res.innerHTML = "Error de conexión."; }
        }

        // LÓGICA AGUA
        let vasos = 0;
        function cambiarAgua(n) {
            vasos = Math.max(0, vasos + n);
            document.getElementById('waterDisplay').innerText = `💧 ${vasos} Vasos`;
        }

        // LÓGICA TIMER (POMODORO)
        let timer;
        let running = false;
        let timeLeft = 25 * 60;
        function toggleTimer() {
            const btn = document.getElementById('btnTimer');
            if(running) {
                clearInterval(timer);
                btn.innerText = "Reanudar";
            } else {
                timer = setInterval(() => {
                    timeLeft--;
                    let min = Math.floor(timeLeft / 60);
                    let sec = timeLeft % 60;
                    document.getElementById('timerDisplay').innerText = `${min}:${sec < 10 ? '0' : ''}${sec}`;
                    if(timeLeft <= 0) { clearInterval(timer); alert("Ciclo completo. ¡Descansa!"); }
                }, 1000);
                btn.innerText = "Pausar";
            }
            running = !running;
        }

        // LÓGICA NOTAS
        function addNota() {
            const val = document.getElementById('notaIn').value;
            if(!val) return;
            const item = document.createElement('div');
            item.className = 'nota-item';
            item.innerText = val;
            document.getElementById('listaNotas').prepend(item);
            document.getElementById('notaIn').value = "";
        }

        // LÓGICA MISIONES
        function nuevaMision() {
            const m = [
                "Escribe un mensaje positivo a alguien.",
                "Dedica 5 minutos a estirar tu cuerpo.",
                "Bebe un vaso de agua ahora mismo.",
                "Organiza un rincón de tu espacio.",
                "Lee 3 páginas de un libro pendiente."
            ];
            document.getElementById('misionTxt').innerText = m[Math.floor(Math.random()*m.length)];
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
