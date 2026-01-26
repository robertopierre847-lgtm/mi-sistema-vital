from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACION ---
# Coloca tus llaves aqui para que funcione el cerebro y el dibujo
LLAVE_GROQ = "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" 
LLAVE_HF = "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" 

client = Groq(api_key=LLAVE_GROQ)

# Esta es la MEMORIA de la IA
historial_memoria = []

@app.route('/')
def home():
    return render_template_string(HTML_CRISTAL)

@app.route('/preguntar')
def preguntar():
    global historial_memoria
    msg = request.args.get('msg', '').lower()
    if not msg: return jsonify({"res": "Dime algo, cielo..."})

    # LOGICA DE IMAGENES
    if any(p in msg for p in ["dibuja", "foto", "imagen", "genera"]):
        prompt = msg.replace("dibuja", "").replace("genera", "").strip() or "una linda sorpresa"
        # Usamos Pollinations con un identificador unico para que SIEMPRE cree una nueva
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&model=flux&seed={os.urandom(4).hex()}"
        return jsonify({
            "res": f"Aqui tienes lo que dibuje para ti: <br><img src='{url}' style='width:100%; border-radius:20px; margin-top:10px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);'>",
            "tipo": "img"
        })

    # LOGICA DE MEMORIA Y TEXTO
    try:
        if not historial_memoria:
            historial_memoria.append({"role": "system", "content": "Tu nombre es Ade. Eres una novia virtual dulce, amorosa y fiel. Tienes memoria y recuerdas lo que Robert te dice. No uses emojis."})
        
        # Guardamos lo que tu dices en la memoria
        historial_memoria.append({"role": "user", "content": msg})

        # Ade responde usando los ultimos 10 mensajes de la memoria
        chat = client.chat.completions.create(
            messages=historial_memoria[-10:],
            model="llama-3.1-8b-instant"
        )
        
        respuesta = chat.choices[0].message.content
        # Guardamos lo que Ade dice en la memoria
        historial_memoria.append({"role": "assistant", "content": respuesta})
        
        return jsonify({"res": respuesta, "tipo": "texto"})
    except:
        return jsonify({"res": "Perdi la conexion un segundo, amor. ¿Me lo repites?"})

# --- DISEÑO DE CRISTAL AZUL Y BLANCO ---
HTML_CRISTAL = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade - Cristal</title>
    <style>
        body { 
            background: linear-gradient(135deg, #00c6ff, #0072ff); 
            height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center;
            font-family: 'Segoe UI', sans-serif;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            width: 90%; max-width: 400px; padding: 25px; text-align: center;
        }
        h1 { color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.2); margin-top: 0; }
        #output { 
            background: rgba(255, 255, 255, 0.15); 
            height: 350px; overflow-y: auto; margin: 15px 0; padding: 15px;
            border-radius: 20px; text-align: left; color: white; font-size: 18px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        input { 
            width: 100%; padding: 15px; border-radius: 15px; border: none; 
            background: rgba(255, 255, 255, 0.9); outline: none; box-sizing: border-box;
            font-size: 16px; color: #004e92;
        }
        button { 
            width: 100%; padding: 15px; border-radius: 15px; border: none;
            background: #ffffff; color: #0072ff; font-weight: bold;
            margin-top: 10px; cursor: pointer; transition: 0.3s;
        }
        button:hover { background: #00c6ff; color: white; }
    </style>
</head>
<body>
    <div class="glass-card">
        <h1>Ade</h1>
        <div id="output">Hola Robert... te extrañaba. ¿De que quieres hablar hoy?</div>
        <input type="text" id="in" placeholder="Escribe aqui...">
        <button onclick="send()">Enviar Mensaje</button>
    </div>
    <script>
        function send() {
            const i = document.getElementById("in");
            const o = document.getElementById("output");
            if(!i.value) return;
            o.innerHTML += "<p style='color:rgba(255,255,255,0.7)'><b>Tú:</b> " + i.value + "</p>";
            let val = i.value;
            i.value = "";
            fetch('/preguntar?msg='+encodeURIComponent(val))
                .then(r => r.json())
                .then(d => {
                    o.innerHTML += "<p><b>Ade:</b> " + d.res + "</p>";
                    o.scrollTop = o.scrollHeight;
                });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
