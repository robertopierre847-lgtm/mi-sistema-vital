from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roma Imperial: Plus Ultra Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --blue: #007bff; --glass: rgba(255, 255, 255, 0.75); }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff, #d1e9ff);
            background-attachment: fixed; display: flex; flex-direction: column; align-items: center; padding: 20px;
        }
        /* EFECTO FLOTANTE PARA TODO */
        .card {
            background: var(--glass); backdrop-filter: blur(15px);
            border-radius: 30px; padding: 30px; width: 100%; max-width: 420px;
            margin-bottom: 30px; border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 20px 40px rgba(0, 123, 255, 0.15);
            text-align: center;
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: float 4s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        h2 { color: var(--blue); font-weight: 700; margin-top: 0; }
        .btn {
            background: var(--blue); color: white; border: none; padding: 15px;
            border-radius: 15px; width: 100%; cursor: pointer; font-weight: 700; margin-top: 10px;
            transition: 0.3s; box-shadow: 0 10px 20px rgba(0, 123, 255, 0.2);
        }
        .btn:hover { transform: scale(1.05); filter: brightness(1.2); }
        
        /* MINI ALL MIGHT MEJORADO */
        #allmight-mini {
            width: 100px; height: 100px; 
            background: url('https://img.izismile.com/img/img11/20180808/640/cool_all_might_fan_art_for_my_hero_academia_fans_640_04.jpg') no-repeat center/cover;
            position: fixed; bottom: 20px; right: 20px; z-index: 100;
            border-radius: 50%; border: 4px solid var(--blue); box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .bubble {
            position: fixed; bottom: 130px; right: 30px; background: white;
            padding: 15px; border-radius: 20px; font-size: 14px; font-weight: bold;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2); max-width: 180px; display: none; z-index: 101;
        }
        #karma-bubble { position: fixed; top: 20px; left: 20px; background: #ffcc00; color: #000; padding: 12px 20px; border-radius: 50px; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        iframe { width: 100%; border-radius: 20px; margin-top: 15px; height: 230px; display: none; }
        img { width: 100%; border-radius: 20px; margin-top: 15px; display: none; }
    </style>
</head>
<body>
    <div id="karma-bubble">PODER: <span id="kVal">0</span>%</div>
    <div id="allmight-mini"></div>
    <div class="bubble" id="am-talk">¡YA ESTOY AQUÍ!</div>

    <div class="card">
        <h2>Buscador de Historia 🏛️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:15px; border-radius:15px; border:2px solid #e1effe; box-sizing: border-box;" placeholder="Busca 'Comida romana'...">
        <button class="btn" onclick="consultarIA()">¡INVESTIGACIÓN PLUS ULTRA!</button>
        <div id="iaRes" style="margin-top: 15px; text-align: left; font-size: 14px;"></div>
        <img id="iaImg" src="">
        <iframe id="iaVid" src="" allowfullscreen></iframe>
    </div>

    <div class="card">
        <h2>Trivia del Héroe ⚔️</h2>
        <p id="qText" style="font-weight: 700; margin-bottom: 20px;"></p>
        <div id="optionsContainer"></div>
        <button class="btn" id="nextBtn" style="display:none; background:#28a745;" onclick="siguiente()">¡OTRO DESAFÍO!</button>
    </div>

    <script>
        let karma = 0; let pActual = 0;
        const preguntas = [
            { q: "¿Cómo conservaban los romanos la carne?", a: "Salazón y Humo", ops: ["Hielo", "Salazón y Humo", "Miel"] },
            { q: "¿Qué nombre recibía la salsa de pescado romana?", a: "Garum", ops: ["Garum", "Ketchup", "Pesto"] },
            { q: "¿Qué emperador amaba las batallas de gladiadores?", a: "Cómodo", ops: ["Cómodo", "Trajano", "Adriano"] }
        ];

        function hablar(msj) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(msj);
            utter.lang = 'es-ES'; utter.pitch = 0.8; utter.rate = 0.9;
            window.speechSynthesis.speak(utter);
            const b = document.getElementById('am-talk');
            b.innerText = msj; b.style.display = "block";
            setTimeout(() => b.style.display = "none", 5000);
        }

        function cargarPregunta() {
            const d = preguntas[pActual];
            document.getElementById('qText').innerText = d.q;
            const container = document.getElementById('optionsContainer');
            container.innerHTML = "";
            document.getElementById('nextBtn').style.display = "none";
            
            // Mezcla real para que no siempre sea la misma opción
            let opciones = [...d.ops].sort(() => Math.random() - 0.5);

            opciones.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn'; b.innerText = o;
                b.onclick = (e) => {
                    const btns = document.querySelectorAll('#optionsContainer .btn');
                    if(o === d.a) {
                        e.target.style.background = "#28a745";
                        hablar("¡Increíble joven! ¡Has respondido con valor!");
                        karma += 25; document.getElementById('kVal').innerText = karma;
                        document.getElementById('nextBtn').style.display = "block";
                        btns.forEach(btn => { if(btn !== e.target) btn.style.display = "none"; });
                    } else {
                        e.target.style.background = "#dc3545";
                        hablar("¡Levántate! ¡El fracaso es solo un peldaño hacia la victoria!");
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
            
            res.innerHTML = "Buscando en los archivos de la justicia...";
            img.style.display = "none"; vid.style.display = "none";

            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                res.innerHTML = d.extract || "No encontré datos, ¡pero no te rindas!";
                
                if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = "block"; }
                
                // Mostrar vídeo si busca comida o preservación
                if(t.includes("comida") || t.includes("alimento") || t.includes("preservar")) {
                    vid.src = "https://www.youtube.com/embed/fD3l_oY6kpk"; // Video educativo sobre cocina romana
                    vid.style.display = "block";
                    hablar("¡Mira este documento en vídeo sobre la cocina de Roma!");
                }
            } catch(e) { res.innerHTML = "Error de conexión con el Senado."; }
        }

        function siguiente() { pActual = (pActual + 1) % preguntas.length; cargarPregunta(); }
        window.onload = () => { cargarPregunta(); setTimeout(() => hablar("¡Ya estoy aquí para guiarte!"), 1000); };
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(diseno_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
