from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Plus Ultra</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --main-blue: #007bff; --glass: rgba(255, 255, 255, 0.7); }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(45deg, #ffffff, #bbdefb);
            background-attachment: fixed; display: flex; flex-direction: column; align-items: center; padding: 20px;
        }
        /* Efecto Cristal */
        .card {
            background: var(--glass); backdrop-filter: blur(15px);
            border-radius: 25px; padding: 25px; width: 100%; max-width: 420px;
            margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.4);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;
        }
        h2 { color: var(--main-blue); text-transform: uppercase; font-size: 1.2em; }
        .btn {
            background: var(--main-blue); color: white; border: none; padding: 12px;
            border-radius: 12px; width: 100%; cursor: pointer; font-weight: 700; margin-top: 8px;
            transition: 0.3s;
        }
        .btn:hover { transform: scale(1.03); filter: brightness(1.1); }
        /* All Might Miniatura */
        #allmight-mini {
            width: 80px; height: 80px; background: url('https://i.imgur.com/vH9vIqy.png') no-repeat center/contain;
            position: fixed; bottom: 10px; right: 10px; z-index: 100; transition: 0.5s;
        }
        .bubble {
            position: fixed; bottom: 90px; right: 20px; background: white;
            padding: 10px; border-radius: 15px; font-size: 12px; font-weight: bold;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2); max-width: 150px; display: none;
        }
        #karma-bubble { position: fixed; top: 20px; left: 20px; background: gold; color: black; padding: 10px 15px; border-radius: 50px; font-weight: bold; }
        iframe { width: 100%; border-radius: 15px; margin-top: 10px; border: none; }
        img { width: 100%; border-radius: 15px; margin-top: 10px; }
    </style>
</head>
<body>
    <div id="karma-bubble">PODER: <span id="kVal">0</span>%</div>
    <div id="allmight-mini"></div>
    <div class="bubble" id="am-talk">¡Ya estoy aquí!</div>

    <div class="card">
        <h2>Buscador de Historia 🏛️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:10px; border-radius:10px; border:1px solid #ddd;" placeholder="Ej: Comida romana, Pompeya...">
        <button class="btn" onclick="consultarIA()">¡IR MÁS ALLÁ!</button>
        <div id="mediaRes"></div>
    </div>

    <div class="card">
        <h2>Trivia Heroica ⚔️</h2>
        <p id="qText" style="font-weight: 700;"></p>
        <div id="optionsContainer"></div>
        <button class="btn" id="nextBtn" style="display:none; background:#28a745;" onclick="siguiente()">¡OTRO RETO!</button>
    </div>

    <script>
        let karma = 0; let pActual = 0;
        const preguntas = [
            { q: "¿Cómo conservaban la carne los romanos?", a: "Salazón y Humo", ops: ["Neveras", "Salazón y Humo", "Miel"] },
            { q: "¿Quién fue el gran estratega de Cartago?", a: "Aníbal", ops: ["Augusto", "Aníbal", "Nerón"] },
            { q: "¿Qué era el Garum?", a: "Salsa de pescado", ops: ["Un tipo de pan", "Salsa de pescado", "Vino dulce"] }
        ];

        function hablar(msj) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(msj);
            utter.lang = 'es-ES'; utter.pitch = 0.8; utter.rate = 0.9;
            window.speechSynthesis.speak(utter);
            document.getElementById('am-talk').innerText = msj;
            document.getElementById('am-talk').style.display = "block";
            setTimeout(() => document.getElementById('am-talk').style.display = "none", 4000);
        }

        function cargarPregunta() {
            const d = preguntas[pActual];
            document.getElementById('qText').innerText = d.q;
            const container = document.getElementById('optionsContainer');
            container.innerHTML = "";
            document.getElementById('nextBtn').style.display = "none";
            
            // Mezclar opciones para que no siempre sea la 2
            let opciones = [...d.ops].sort(() => Math.random() - 0.5);

            opciones.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn'; b.innerText = o;
                b.onclick = (e) => {
                    if(o === d.a) {
                        e.target.style.background = "#28a745";
                        hablar("¡JA JA JA! ¡Excelente joven! ¡PLUS ULTRA!");
                        karma += 20; document.getElementById('kVal').innerText = karma;
                        document.getElementById('nextBtn').style.display = "block";
                    } else {
                        e.target.style.background = "#dc3545";
                        hablar("¡No te rindas! ¡El fracaso es parte del camino del héroe!");
                    }
                };
                container.appendChild(b);
            });
        }

        async function consultarIA() {
            const t = document.getElementById('iaInput').value;
            const res = document.getElementById('mediaRes');
            res.innerHTML = "¡Analizando archivos imperiales!... 🏛️";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                let html = `<p>${d.extract || 'Información no encontrada'}</p>`;
                if(d.thumbnail) html += `<img src="${d.thumbnail.source}">`;
                
                // Ejemplo de video estático sobre comida si busca "comida"
                if(t.toLowerCase().includes("comida") || t.toLowerCase().includes("alimento")) {
                    html += `<p><b>Video: Preservación en Roma</b></p><iframe height="200" src="https://www.youtube.com/embed/fD3l_oY6kpk" allowfullscreen></iframe>`;
                }
                res.innerHTML = html;
                hablar("¡He encontrado la información! ¡Mírala con atención!");
            } catch(e) { res.innerHTML = "Error joven, pero un héroe no retrocede."; }
        }

        function siguiente() { pActual = (pActual + 1) % preguntas.length; cargarPregunta(); }
        window.onload = () => { cargarPregunta(); hablar("¡YA ESTOY AQUÍ!"); };
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
