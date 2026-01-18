from flask import Flask, render_template_string

app = Flask(__name__)

# Diseño de Cristal Blanco y Azul
html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roma Plus Ultra</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff, #e3f2fd);
            display: flex; flex-direction: column; align-items: center; padding: 20px; min-height: 100vh;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px);
            border-radius: 20px; padding: 20px; width: 100%; max-width: 380px;
            margin: 15px 0; border: 1px solid rgba(255,255,255,0.4);
            box-shadow: 0 8px 32px rgba(0, 123, 255, 0.1); text-align: center;
        }
        .btn {
            background: #007bff; color: white; border: none; padding: 12px;
            border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold; margin-top: 10px;
        }
        /* All Might Miniatura */
        #am-mini {
            position: fixed; bottom: 20px; right: 20px; width: 70px; height: 70px;
            background: url('https://i.imgur.com/vH9vIqy.png') no-repeat center/contain;
            filter: drop-shadow(0 5px 10px rgba(0,0,0,0.2)); z-index: 100;
        }
        .bubble {
            position: fixed; bottom: 95px; right: 25px; background: white;
            padding: 8px 12px; border-radius: 15px; font-size: 11px; font-weight: bold;
            border: 2px solid #007bff; display: none; z-index: 101;
        }
    </style>
</head>
<body>
    <div id="am-mini"></div>
    <div class="bubble" id="talk">¡YA ESTOY AQUÍ!</div>

    <div class="glass-card">
        <h2 style="color:#007bff;">Buscador Romano 🏛️</h2>
        <input type="text" id="in" style="width:90%; padding:10px; border-radius:8px; border:1px solid #ddd;" placeholder="Ej: Comida romana">
        <button class="btn" onclick="buscar()">¡PLUS ULTRA!</button>
        <div id="res" style="margin-top:10px; font-size:14px; text-align:left;"></div>
    </div>

    <div class="glass-card">
        <h2 style="color:#007bff;">Trivia ⚔️</h2>
        <p id="q" style="font-weight:bold;"></p>
        <div id="ops"></div>
    </div>

    <script>
        const trivia = [{q:"¿Cómo conservaban la carne?", a:"Salazón", ops:["Hielo","Salazón","Azúcar"]}];
        
        function hablar(t) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(t);
            u.lang = 'es-ES'; u.pitch = 0.7; u.rate = 0.85; // Voz imponente
            window.speechSynthesis.speak(u);
            const b = document.getElementById('talk');
            b.innerText = t; b.style.display = "block";
            setTimeout(()=> b.style.display="none", 4000);
        }

        async function buscar() {
            const t = document.getElementById('in').value;
            const r = document.getElementById('res');
            r.innerHTML = "Buscando...";
            const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
            const d = await res.json();
            r.innerHTML = d.extract || "No encontré nada, joven.";
            hablar("¡He encontrado la información para tu formación!");
        }

        function cargar() {
            const d = trivia[0];
            document.getElementById('q').innerText = d.q;
            const c = document.getElementById('ops');
            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn'; b.innerText = o;
                b.onclick = () => hablar(o===d.a ? "¡JA JA JA! ¡Correcto!" : "¡No te rindas!");
                c.appendChild(b);
            });
        }
        window.onclick = () => { hablar("¡Bienvenido al Imperio!"); window.onclick = null; };
        window.onload = cargar;
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
