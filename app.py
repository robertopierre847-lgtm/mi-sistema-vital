from flask import Flask, render_template_string

app = Flask(__name__)

# Diseño Limpio Blanco y Azul
diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Imperio Romano</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; font-family: 'Quicksand', sans-serif; background: #f0f7ff; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .card { background: white; border-radius: 20px; padding: 20px; width: 100%; max-width: 400px; margin-bottom: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; border: 1px solid #e1effe; }
        h2 { color: #1c64f2; margin-top: 0; }
        .btn { background: #1c64f2; color: white; border: none; padding: 12px; border-radius: 12px; width: 100%; cursor: pointer; font-weight: 600; margin-bottom: 10px; }
        .ia-box { text-align: left; background: #f9fafb; padding: 15px; border-radius: 12px; margin-top: 10px; border-left: 4px solid #1c64f2; font-size: 14px; }
        .img-ia { width: 100%; border-radius: 15px; margin-top: 10px; display: none; }
        #karma-bubble { position: fixed; top: 10px; right: 10px; background: #1c64f2; color: white; padding: 10px 15px; border-radius: 30px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    </style>
</head>
<body>
    <div id="karma-bubble">Karma: <span id="kVal">0</span></div>

    <div class="card">
        <h2>IA Cariñosa Visual ❤️</h2>
        <input type="text" id="iaInput" style="width:90%; padding:10px; border-radius:10px; border:1px solid #ccc;" placeholder="Ej: Catapulta, Coliseo...">
        <button class="btn" style="margin-top:10px;" onclick="consultarIA(document.getElementById('iaInput').value)">Ver Imagen Real</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <img id="iaImg" class="img-ia" src="">
    </div>

    <div class="card">
        <h2>Trivia Romana ⚔️</h2>
        <p id="qText">¿Quién fue el primer emperador?</p>
        <button class="btn" onclick="check('Julio César')">A. Julio César</button>
        <button class="btn" onclick="check('Augusto')">B. Augusto</button>
        <button class="btn" onclick="check('Nerón')">C. Nerón</button>
        <p id="feedback" style="font-weight:bold;"></p>
    </div>

    <script>
        let karma = 0;
        async function consultarIA(t) {
            const resDiv = document.getElementById('iaRes');
            const img = document.getElementById('iaImg');
            resDiv.style.display = "block";
            resDiv.innerHTML = "Buscando para ti, mi cielo... ✨";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${t}`);
                const d = await r.json();
                if(d.extract) {
                    resDiv.innerHTML = `<b>Cielo, aquí tienes:</b><br>${d.extract}`;
                    if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = "block"; }
                    karma += 10; document.getElementById('kVal').innerText = karma;
                }
            } catch(e) { resDiv.innerHTML = "Error, vida mía."; }
        }
        function check(ans) {
            const f = document.getElementById('feedback');
            if(ans === 'Augusto') {
                f.innerText = "¡FELICIDADES! 🎉 Es correcto."; f.style.color = "green";
                karma += 25; document.getElementById('kVal').innerText = karma;
            } else {
                f.innerText = "Casi, tesoro. Fue Augusto."; f.style.color = "red";
            }
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
