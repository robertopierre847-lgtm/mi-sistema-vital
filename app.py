from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Imperio Romano Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; font-family: 'Quicksand', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
            display: flex; flex-direction: column; align-items: center; padding: 20px;
        }
        .card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.4);
            border-radius: 25px; padding: 25px; width: 100%; max-width: 420px;
            margin-bottom: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.05);
            text-align: center;
        }
        h2 { color: #1976d2; margin-bottom: 15px; }
        .btn {
            background: #1976d2; color: white; border: none; padding: 12px;
            border-radius: 15px; width: 100%; cursor: pointer; font-weight: 600;
            margin-bottom: 10px; transition: 0.3s;
        }
        .btn-romano { background: #64b5f6; font-size: 0.9em; }
        .btn-romano:hover { background: #1976d2; transform: scale(1.02); }
        .ia-box {
            text-align: left; background: white; padding: 15px; border-radius: 15px;
            margin-top: 15px; border-left: 5px solid #1976d2; font-size: 14px;
        }
        .img-ia { width: 100%; border-radius: 20px; margin-top: 10px; display: none; box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
        #karma-bubble {
            position: fixed; top: 20px; right: 20px; width: 60px; height: 60px;
            background: #1976d2; color: white; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; font-size: 20px; z-index: 1000;
        }
    </style>
</head>
<body>

    <div id="karma-bubble">0</div>

    <div class="card">
        <h2>IA Cariñosa Visual ❤️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:12px; border-radius:15px; border:2px solid #bbdefb; margin-bottom:10px;" placeholder="Busca 'Catapulta', 'Coliseo'...">
        <button class="btn" onclick="consultarIA(document.getElementById('iaInput').value)">Ver Imagen Real</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <img id="iaImg" class="img-ia" src="" alt="Resultado visual">
    </div>

    <div class="card">
        <h2>Museo del Imperio Romano 🏛️</h2>
        <p>Toca para ver cómo preservaban sus alimentos con imágenes reales:</p>
        <button class="btn btn-romano" onclick="consultarIA('Salazón de pescado romano')">🥩 Conservación con Sal</button>
        <button class="btn btn-romano" onclick="consultarIA('Garum romano')">🐟 El Garum (Salsa Real)</button>
        <button class="btn btn-romano" onclick="consultarIA('Nivariae romano')">❄️ Pozos de Nieve</button>
        <button class="btn btn-romano" onclick="consultarIA('Anfora romana')">🏺 Almacenamiento en Ánforas</button>
    </div>

    <script>
        let karma = 0;
        async function consultarIA(tema) {
            if(!tema) return;
            let resDiv = document.getElementById('iaRes');
            let img = document.getElementById('iaImg');
            
            resDiv.style.display = "block";
            resDiv.innerHTML = "Buscando la imagen más clara para ti, tesoro... ✨";
            img.style.display = "none";

            try {
                const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${tema}`);
                const data = await res.json();
                
                if(data.extract) {
                    resDiv.innerHTML = `<b>Mi cielo, aquí tienes información sobre ${tema}:</b><br>${data.extract}`;
                    if(data.originalimage) {
                        img.src = data.originalimage.source;
                        img.style.display = "block";
                        karma += 10;
                        document.getElementById('karma-bubble').innerText = karma;
                    }
                } else {
                    resDiv.innerHTML = "No encontré esa imagen específica, vida mía. ¿Intentamos con otro nombre?";
                }
            } catch {
                resDiv.innerHTML = "Error de conexión, amor. Intenta de nuevo.";
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
