from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roma Plus Ultra: Edición Escolar</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --rojo: #dc3545; --verde: #28a745; }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }
        .intro-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--azul); color: white; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: 0.8s;
        }
        .glass {
            background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px);
            border-radius: 25px; padding: 25px; width: 90%; max-width: 400px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center;
        }
        .btn-hero { background: var(--azul); color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: bold; margin-top: 10px; cursor: pointer; transition: 0.3s; }
        .btn-wrong { background: var(--rojo) !important; animation: shake 0.3s; }
        .btn-correct { background: var(--verde) !important; }
        @keyframes shake { 0%, 100% {transform: translateX(0);} 25% {transform: translateX(-5px);} 75% {transform: translateX(5px);} }
        #img-res { width: 100%; border-radius: 15px; margin-top: 15px; display: none; }
        .reto-caja { margin-top: 15px; padding: 10px; border: 2px dashed var(--rojo); color: var(--rojo); font-size: 13px; display: none; }
    </style>
</head>
<body>

    <div id="intro" class="intro-screen">
        <h1 style="font-size: 3em;">🏛️</h1>
        <h2>SISTEMA VITAL ROMANO</h2>
        <button class="btn-hero" style="width: 200px; background: white; color: var(--azul);" onclick="entrar()">EMPEZAR</button>
    </div>

    <div class="glass">
        <h2 style="color: var(--azul);">Buscador de Historia 🔍</h2>
        <input type="text" id="busqueda" style="width:100%; padding:10px; border-radius:8px; border:1px solid #ddd;" placeholder="Ej: Gladiador...">
        <button class="btn-hero" onclick="buscar()">CONSULTAR</button>
        <div id="texto-res" style="margin-top: 15px; font-size: 14px; text-align: left;"></div>
        <img id="img-res" src="">
    </div>

    <div class="glass" id="trivia-box">
        <h2 style="color: var(--azul);">Trivia Imperial ⚔️</h2>
        <p id="pregunta" style="font-weight: bold;"></p>
        <div id="opciones"></div>
        <div id="reto-escolar" class="reto-caja"></div>
    </div>

    <script>
        function entrar() {
            document.getElementById('intro').style.transform = 'translateY(-100%)';
            hablar("¡Ya estoy aquí! Prepárate para aprender o enfrentar los retos escolares.");
        }

        function hablar(msj) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(msj);
            u.lang = 'es-ES'; u.pitch = 0.75; u.rate = 0.9;
            window.speechSynthesis.speak(u);
        }

        async function buscar() {
            const t = document.getElementById('busqueda').value;
            const res = document.getElementById('texto-res');
            const img = document.getElementById('img-res');
            res.innerHTML = "Buscando...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                res.innerHTML = d.extract || "No hay resultados.";
                if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = 'block'; }
            } catch(e) { res.innerHTML = "Error de conexión."; }
        }

        const trivia = [
            {q: "¿Qué idioma hablaban los romanos?", a: "Latín", ops: ["Griego", "Latín", "Español"]},
            {q: "¿Cuál era la moneda de Roma?", a: "Denario", ops: ["Euro", "Denario", "Dólar"]}
        ];
        let index = 0;

        function cargarTrivia() {
            const d = trivia[index];
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            const reto = document.getElementById('reto-escolar');
            cont.innerHTML = "";
            reto.style.display = "none";

            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero'; b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) {
                        b.classList.add('btn-correct');
                        hablar("¡Correcto! ¡Has demostrado gran inteligencia!");
                        setTimeout(() => { index = (index + 1) % trivia.length; cargarTrivia(); }, 2000);
                    } else {
                        b.classList.add('btn-wrong');
                        hablar("¡Has fallado! Deberás cumplir un castigo escolar.");
                        reto.innerText = "RETO: Escribe en una hoja 10 veces: 'Debo prestar más atención a las clases de historia'.";
                        reto.style.display = "block";
                    }
                };
                cont.appendChild(b);
            });
        }
        window.onload = cargarTrivia;
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
