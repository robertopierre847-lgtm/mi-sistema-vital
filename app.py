import os
from flask import Flask, render_template_string

app = Flask(__name__)

# CÓDIGO TODO EN UNO PARA EVITAR ERRORES DE CARGA
html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roma Plus Ultra: 30 Retos</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --rojo: #dc3545; --verde: #28a745; }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff, #d1e9ff);
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }
        /* Pantalla de Inicio */
        #intro {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--azul); color: white; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: 0.8s;
        }
        /* Efecto Cristal */
        .glass {
            background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(10px);
            border-radius: 25px; padding: 25px; width: 90%; max-width: 450px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center;
        }
        .btn-hero { background: var(--azul); color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: bold; margin-top: 10px; cursor: pointer; }
        .btn-wrong { background: var(--rojo) !important; }
        .btn-correct { background: var(--verde) !important; }
        .reto-caja { margin-top: 15px; padding: 15px; border: 2px dashed var(--rojo); color: var(--rojo); font-weight: bold; display: none; background: #fff1f0; }
        #am-mini { position: fixed; bottom: 10px; right: 10px; width: 70px; z-index: 100; }
    </style>
</head>
<body>
    <div id="intro">
        <h1 style="font-size: 3em;">🏛️</h1>
        <h2>30 NIVELES DE HISTORIA</h2>
        <button class="btn-hero" style="width: 200px; background: gold; color: black;" onclick="entrar()">¡ENTRAR!</button>
    </div>

    <div id="am-mini"><img src="https://i.imgur.com/vH9vIqy.png" style="width: 100%;"></div>

    <div class="glass">
        <h2 style="color: var(--azul);">Pregunta <span id="num-q">1</span>/30</h2>
        <p id="pregunta" style="font-size: 1.1em; font-weight: bold;"></p>
        <div id="opciones"></div>
        <div id="reto-escolar" class="reto-caja"></div>
    </div>

    <script>
        const trivia = [
            {q: "¿Cómo conservaban los romanos la carne?", a: "Salazón y Humo", ops: ["Salazón y Humo", "Neveras", "Hielo"]},
            {q: "¿Qué usaban para conservar fruta?", a: "Miel", ops: ["Azúcar", "Miel", "Sal"]},
            {q: "¿Qué idioma hablaban?", a: "Latín", ops: ["Latín", "Griego", "Italiano"]},
            // ... (Se añaden las demás preguntas internamente)
        ];
        // Rellenar hasta 30 preguntas de forma rápida para el ejemplo
        for(let i=4; i<=30; i++) { trivia.push({q: "Pregunta de reto " + i + ": ¿Roma fue un imperio?", a: "Sí", ops: ["Sí", "No", "Quizás"]}); }

        let index = 0;
        function entrar() { document.getElementById('intro').style.transform = 'translateY(-100%)'; hablar("¡Plus Ultra! A jugar."); }
        
        function hablar(t) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(t);
            u.lang = 'es-ES'; u.pitch = 0.7; window.speechSynthesis.speak(u);
        }

        function cargar() {
            const d = trivia[index];
            document.getElementById('num-q').innerText = index + 1;
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            const reto = document.getElementById('reto-escolar');
            cont.innerHTML = ""; reto.style.display = "none";

            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero'; b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) {
                        b.classList.add('btn-correct');
                        hablar("¡Correcto!");
                        setTimeout(() => { index++; if(index < 30) cargar(); else alert("¡Ganaste!"); }, 1000);
                    } else {
                        b.classList.add('btn-wrong');
                        hablar("¡Fallaste! ¡Castigo escolar!");
                        reto.innerText = "RETO: Escribe en una hoja 10 veces: 'Debo estudiar la historia de Roma'.";
                        reto.style.display = "block";
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
    # Esto es vital para que Render no falle
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
