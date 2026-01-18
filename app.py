import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Este código es ultraligero para que Render no falle
html_final = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roma Plus Ultra</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; font-family: 'Poppins', sans-serif; background: #e3f2fd; text-align: center; }
        #intro { 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: #007bff; color: white; display: flex; flex-direction: column; 
            justify-content: center; align-items: center; z-index: 1000; transition: 0.8s;
        }
        .container { padding: 20px; display: none; }
        .glass { background: white; border-radius: 20px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 20px auto; max-width: 400px; }
        .btn { background: #ffcc00; border: none; padding: 15px 30px; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 18px; }
        #am-mini { position: fixed; bottom: 20px; right: 20px; width: 80px; height: 80px; background: white; border-radius: 50%; border: 3px solid #007bff; overflow: hidden; }
    </style>
</head>
<body>
    <div id="intro">
        <h1 style="font-size: 50px;">🏛️</h1>
        <h2>¡CONVIÉRTETE EN UN HÉROE DE LA HISTORIA!</h2>
        <button class="btn" onclick="entrar()">¡EMPEZAR EL DESAFÍO!</button>
    </div>

    <div id="am-mini">
        <img src="https://images.fineartamerica.com/images/artworkimages/mediumlarge/3/all-might-my-hero-academia-andrea-matsumoto.jpg" style="width:100%; height:100%; object-fit:cover;">
    </div>

    <div class="container" id="main-content">
        <div class="glass">
            <h2 style="color:#007bff;">Buscador Imperial 🔍</h2>
            <input type="text" id="bus" style="width:80%; padding:10px; border-radius:10px; border:1px solid #ddd;" placeholder="Busca algo...">
            <button onclick="buscar()" style="margin-top:10px; padding:10px; width:80%; cursor:pointer;">BUSCAR IMAGEN</button>
            <div id="res" style="margin-top:10px;"></div>
            <img id="img-wiki" style="width:100%; border-radius:10px; margin-top:10px; display:none;">
        </div>
        
        <div class="glass">
            <h2 style="color:#007bff;">Trivia 30 Niveles ⚔️</h2>
            <p id="q" style="font-weight:bold;"></p>
            <div id="ops"></div>
        </div>
    </div>

    <script>
        function entrar() {
            document.getElementById('intro').style.transform = 'translateY(-100%)';
            document.getElementById('main-content').style.display = 'block';
            hablar("¡YA ESTOY AQUÍ! ¡Comencemos el entrenamiento!");
        }

        function hablar(t) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(t);
            u.lang = 'es-ES'; u.pitch = 0.8;
            window.speechSynthesis.speak(u);
        }

        async function buscar() {
            const t = document.getElementById('bus').value;
            const res = document.getElementById('res');
            const img = document.getElementById('img-wiki');
            res.innerHTML = "Buscando...";
            const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
            const d = await r.json();
            res.innerHTML = d.extract || "No encontré nada.";
            if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = 'block'; }
        }

        const trivia = [
            {q: "¿Cómo conservaban la carne?", a: "Salazón y Humo", ops: ["Neveras", "Salazón y Humo", "Miel"]},
            {q: "¿Qué idioma hablaban?", a: "Latín", ops: ["Latín", "Griego", "Inglés"]}
            // Aquí puedes añadir las 30 preguntas siguiendo este formato
        ];
        
        function cargarTrivia() {
            const d = trivia[0];
            document.getElementById('q').innerText = d.q;
            const ops = document.getElementById('ops');
            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.innerText = o; b.style.width="100%"; b.style.margin="5px 0"; b.style.padding="10px";
                b.onclick = () => {
                    if(o === d.a) { b.style.background="#28a745"; hablar("¡Correcto!"); }
                    else { b.style.background="#dc3545"; hablar("¡Fallaste! ¡Reto escolar: Escribe 10 veces perdí!"); }
                };
                ops.appendChild(b);
            });
        }
        window.onload = cargarTrivia;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_final)

if __name__ == '__main__':
    # Esto soluciona el error de Render Status 1
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
