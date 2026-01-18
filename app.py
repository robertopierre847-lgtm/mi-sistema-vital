from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Edición Símbolo de la Paz</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --blue: #007bff; --glass: rgba(255, 255, 255, 0.8); }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #bbdefb 100%);
            background-attachment: fixed; display: flex; flex-direction: column; align-items: center; padding: 20px;
        }
        /* EFECTO CRISTAL FLOTANTE */
        .card {
            background: var(--glass); backdrop-filter: blur(15px);
            border-radius: 30px; padding: 30px; width: 100%; max-width: 400px;
            margin-bottom: 30px; border: 1px solid rgba(255,255,255,0.6);
            box-shadow: 0 20px 50px rgba(0, 123, 255, 0.15);
            text-align: center; animation: float 5s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }
        h2 { color: var(--blue); font-weight: 700; margin-bottom: 20px; }
        .btn {
            background: var(--blue); color: white; border: none; padding: 15px;
            border-radius: 15px; width: 100%; cursor: pointer; font-weight: 700;
            transition: 0.3s; box-shadow: 0 8px 15px rgba(0, 123, 255, 0.2);
        }
        .btn:hover { transform: scale(1.05); filter: brightness(1.1); }
        
        /* MINI ALL MIGHT - AHORA SÍ APARECE */
        #allmight-container {
            position: fixed; bottom: 20px; right: 20px; z-index: 1000;
            display: flex; flex-direction: column; align-items: center;
        }
        #allmight-mini {
            width: 90px; height: 90px;
            background: url('https://i.pinimg.com/originals/ce/03/65/ce0365775877be92658826d9111306c5.png') no-repeat center/contain;
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.3));
        }
        .bubble {
            background: white; padding: 10px 15px; border-radius: 20px;
            font-size: 13px; font-weight: bold; margin-bottom: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2); display: none;
            border: 2px solid var(--blue); max-width: 150px;
        }
    </style>
</head>
<body>
    <div id="allmight-container">
        <div class="bubble" id="am-talk">¡YA ESTOY AQUÍ!</div>
        <div id="allmight-mini"></div>
    </div>

    <div class="card">
        <h2>Buscador de Justicia 🏛️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:15px; border-radius:15px; border:2px solid #ddd; box-sizing:border-box;" placeholder="Busca 'Comida romana'...">
        <button class="btn" style="margin-top:15px;" onclick="consultarIA()">¡INVESTIGACIÓN PLUS ULTRA!</button>
        <div id="iaRes" style="margin-top: 15px; text-align: left; font-size: 14px; color: #444;"></div>
        <img id="iaImg" style="width:100%; border-radius:20px; margin-top:15px; display:none;">
        <iframe id="iaVid" style="width:100%; height:220px; border-radius:20px; margin-top:15px; display:none; border:none;" allowfullscreen></iframe>
    </div>

    <div class="card" style="animation-delay: 1s;">
        <h2>Trivia del Héroe ⚔️</h2>
        <p id="qText" style="font-weight: 700; color: #333;"></p>
        <div id="optionsContainer"></div>
        <button class="btn" id="nextBtn" style="display:none; background:#28a745;" onclick="siguiente()">¡OTRO RETO!</button>
    </div>

    <script>
        let karma = 0; let pActual = 0;
        const preguntas = [
            { q: "¿Cómo conservaban la carne los romanos?", a: "Salazón y Humo", ops: ["Hielo", "Salazón y Humo", "Miel"] },
            { q: "¿Qué era el Garum?", a: "Salsa de pescado", ops: ["Garum", "Vino tinto", "Aceite"] }
        ];

        function hablar(msj) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(msj);
            utter.lang = 'es-ES';
            utter.pitch = 0.8; // Más grave
            utter.rate = 0.85; // Un poco más lento para que no sea robótico
            window.speechSynthesis.speak(utter);
            
            const b = document.getElementById('am-talk');
            b.innerText = msj; b.style.display = "block";
            setTimeout(() => b.style.display = "none", 4000);
        }

        function cargarPregunta() {
            const d = preguntas[pActual];
            document.getElementById('qText').innerText = d.q;
            const container = document.getElementById('optionsContainer');
            container.innerHTML = "";
            document.getElementById('nextBtn').style.display = "none";
            
            let opciones = [...d.ops].sort(() => Math.random() - 0.5);
            opciones.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn'; b.style.marginTop = "10px"; b.innerText = o;
                b.onclick = (e) => {
                    if(o === d.a) {
                        e.target.style.background = "#28a745";
                        hablar("¡Increíble joven! ¡Has respondido con justicia! ¡Sigue así!");
                        document.getElementById('nextBtn').style.display = "block";
                    } else {
                        e.target.style.background = "#dc3545";
                        hablar("¡No te rindas! ¡Incluso yo tuve que aprender! ¡Prueba otra vez!");
                    }
                };
                container.appendChild(b);
            });
        }

        async function consultarIA() {
            const t = document.getElementById('iaInput').value.toLowerCase();
            const res = document.getElementById('iaRes');
            const img = document.getElementById('iaImg');
            const vid = document.getElementById('iaVid');
            
            res.innerHTML = "Consultando los archivos históricos...";
            img.style.display = "none"; vid.style.display = "none";

            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                res.innerHTML = d.extract || "No encontré nada, ¡pero un héroe nunca se rinde!";
                if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = "block"; }
                
                if(t.includes("comida") || t.includes("preservar")) {
                    vid.src = "https://www.youtube.com/embed/fD3l_oY6kpk";
                    vid.style.display = "block";
                    hablar("¡Mira este vídeo sobre la cocina romana, joven! ¡Es fascinante!");
                }
            } catch(e) { res.innerHTML = "Hubo un error de conexión."; }
        }

        function siguiente() { pActual = (pActual + 1) % preguntas.length; cargarPregunta(); }
        
        // El truco para que hable: tiene que haber un clic primero
        window.onclick = () => { if(window.speechSynthesis.speaking === false) hablar("¡YA ESTOY AQUÍ!"); window.onclick = null; };
        window.onload = cargarPregunta;
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
