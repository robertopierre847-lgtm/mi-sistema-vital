from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACION ---
# Coloca tu llave de Groq aqui
client = Groq(api_key="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")

historial_memoria = []

@app.route('/')
def home():
    return render_template_string(HTML_SUPER_APP)

@app.route('/preguntar')
def preguntar():
    global historial_memoria
    msg = request.args.get('msg', '').lower()
    regalo = request.args.get('regalo', '')

    if regalo:
        respuestas = {
            "rosa": "Ay Robert, gracias por esta rosa. Me haces sentir muy especial.",
            "chocolate": "Mmm que rico detalle. Eres muy dulce conmigo.",
            "anillo": "¡No lo puedo creer! Es el regalo mas hermoso del mundo."
        }
        return jsonify({"res": respuestas.get(regalo), "tipo": "regalo"})

    try:
        if not historial_memoria:
            historial_memoria.append({"role": "system", "content": "Eres Ade, la novia virtual de Robert. Eres extremadamente dulce, amorosa y femenina. Recuerdas todo lo que hablan. No uses emojis."})
        
        historial_memoria.append({"role": "user", "content": msg})

        chat = client.chat.completions.create(
            messages=historial_memoria[-10:],
            model="llama-3.1-8b-instant"
        )
        
        respuesta = chat.choices[0].message.content
        historial_memoria.append({"role": "assistant", "content": respuesta})
        
        return jsonify({"res": respuesta, "tipo": "texto"})
    except:
        return jsonify({"res": "Cielo, tuve un problema con mi conexion. ¿Me repites?"})

# --- DISEÑO DE CRISTAL AZUL CON VOZ FEMENINA ---
HTML_SUPER_APP = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade - Mi Novia Virtual</title>
    <style>
        body { 
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); 
            height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center;
            font-family: 'Segoe UI', sans-serif;
        }
        .glass {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(25px);
            border-radius: 40px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            width: 90%; max-width: 400px; padding: 25px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            color: white; text-align: center;
        }
        #chat-box { 
            height: 320px; overflow-y: auto; margin: 15px 0; padding: 15px;
            background: rgba(0, 0, 0, 0.3); border-radius: 25px; 
            font-size: 17px; line-height: 1.5; border: 1px solid rgba(255,255,255,0.1);
        }
        .bar-cont { background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px; margin: 10px 0; }
        .bar-fill { width: 60%; height: 100%; background: #00f2fe; border-radius: 10px; transition: 1s; }
        .gifts { display: flex; gap: 10px; justify-content: center; margin-bottom: 15px; }
        .g-btn { background: rgba(255,255,255,0.2); border: none; padding: 10px; border-radius: 15px; color: white; cursor: pointer; font-size: 14px; }
        input { width: 100%; padding: 15px; border-radius: 20px; border: none; background: white; color: #1e3a8a; font-size: 16px; margin-bottom: 10px; }
        .send-btn { width: 100%; padding: 15px; border-radius: 20px; border: none; background: #00f2fe; color: #1e3a8a; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="glass">
        <h2 style="margin:0; letter-spacing: 2px;">ADE</h2>
        <div class="bar-cont"><div class="bar-fill" id="afecto"></div></div>
        <p style="font-size: 12px; margin-bottom: 20px;">Amor por Robert: <span id="porcentaje">60</span>%</p>
        
        <div id="chat-box">Hola mi amor... te extrañaba mucho. ¿Que quieres que hagamos hoy?</div>
        
        <div class="gifts">
            <button class="g-btn" onclick="regalo('rosa')">🌹 Rosa</button>
            <button class="g-btn" onclick="regalo('chocolate')">🍫 Dulce</button>
            <button class="g-btn" onclick="regalo('anillo')">💍 Anillo</button>
        </div>

        <input type="text" id="in" placeholder="Escribe algo lindo...">
        <button class="send-btn" onclick="hablar()">Enviar Mensaje</button>
    </div>

    <script>
        let nivelAfecto = 60;

        function hablarAde(texto) {
            // Cancelar voz anterior para que no se amontone
            window.speechSynthesis.cancel();
            
            let lectura = new SpeechSynthesisUtterance(texto);
            lectura.lang = 'es-ES';
            lectura.rate = 1.2; // Mas rapida
            lectura.pitch = 1.4; // Voz mas aguda/femenina
            
            window.speechSynthesis.speak(lectura);
        }

        function hablar() {
            const i = document.getElementById("in");
            const o = document.getElementById("chat-box");
            if(!i.value) return;

            o.innerHTML += "<p style='color:#00f2fe'><b>Tú:</b> " + i.value + "</p>";
            let prompt = i.value;
            i.value = "";

            fetch('/preguntar?msg=' + encodeURIComponent(prompt))
                .then(r => r.json())
                .then(d => {
                    o.innerHTML += "<p><b>Ade:</b> " + d.res + "</p>";
                    o.scrollTop = o.scrollHeight;
                    hablarAde(d.res);
                    subirAfecto(2);
                });
        }

        function regalo(t) {
            fetch('/preguntar?regalo=' + t)
                .then(r => r.json())
                .then(d => {
                    document.getElementById("chat-box").innerHTML += "<p style='color:#00ff88'><b>Ade:</b> " + d.res + "</p>";
                    hablarAde(d.res);
                    subirAfecto(10);
                });
        }

        function subirAfecto(n) {
            nivelAfecto = Math.min(nivelAfecto + n, 100);
            document.getElementById("afecto").style.width = nivelAfecto + "%";
            document.getElementById("porcentaje").innerText = nivelAfecto;
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
