from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACION ---
# Reemplaza esto con tu llave de Groq
client = Groq(api_key="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")

historial_chat = []

@app.route('/')
def home():
    return render_template_string(HTML_ADE_FINAL)

@app.route('/preguntar')
def preguntar():
    global historial_chat
    user_msg = request.args.get('msg', '').lower()
    
    if not user_msg:
        return jsonify({"res": "Aqui estoy, dime algo...", "color": "#ffffff"})

    # --- LOGICA DE POLLINATIONS AI (IMAGENES) ---
    if any(p in user_msg for p in ["dibuja", "genera imagen", "hazme una foto"]):
        # Extraemos lo que el usuario quiere ver
        prompt_limpio = user_msg.replace("dibuja", "").replace("genera imagen", "").replace("hazme una foto", "").strip()
        if not prompt_limpio: prompt_limpio = "un paisaje hermoso"
        
        # Creamos la URL para Pollinations AI
        url_img = f"https://pollinations.ai/p/{prompt_limpio.replace(' ', '%20')}?width=1024&height=1024&model=flux&seed={os.urandom(4).hex()}"
        
        return jsonify({
            "res": f"He terminado tu dibujo: <br><img src='{url_img}' style='width:100%; border-radius:15px; margin-top:10px;'>",
            "tipo": "img",
            "color": "#ffffff"
        })

    # --- LOGICA DE HUMORES (COLORES) ---
    color_fondo = "#ffffff"
    if any(p in user_msg for p in ["amo", "quiero", "linda", "carino"]): color_fondo = "#fff0f6"
    elif any(p in user_msg for p in ["triste", "mal", "ayuda"]): color_fondo = "#e0f2fe"
    elif any(p in user_msg for p in ["feliz", "bien", "jaja"]): color_fondo = "#fefce8"

    try:
        if not historial_chat:
            historial_chat.append({"role": "system", "content": "Tu nombre es Ade. Eres una novia virtual dulce y atenta. No uses emojis. Habla siempre con amor."})
        
        historial_chat.append({"role": "user", "content": user_msg})

        completion = client.chat.completions.create(
            messages=historial_chat[-12:],
            model="llama-3.1-8b-instant"
        )
        
        respuesta = completion.choices[0].message.content
        historial_chat.append({"role": "assistant", "content": respuesta})
        
        return jsonify({"res": respuesta, "tipo": "texto", "color": color_fondo})
    except Exception as e:
        return jsonify({"res": "Perdi la conexion un segundo, puedes repetirlo?", "color": "#ffffff"})

# --- DISENO BLANCO LIMPIO ---
HTML_ADE_FINAL = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade Virtual</title>
    <style>
        body { transition: background 0.8s; background: #fdfdfd; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 40px; box-shadow: 0 15px 50px rgba(0,0,0,0.05); width: 92%; max-width: 420px; text-align: center; border: 1px solid #f0f0f0; }
        h1 { color: #0ea5e9; margin: 0; font-size: 45px; letter-spacing: -2px; }
        #output { background: #ffffff; border-radius: 25px; padding: 20px; height: 280px; overflow-y: auto; margin: 20px 0; text-align: left; font-size: 20px; color: #334155; border: 1px solid #f1f5f9; line-height: 1.5; }
        input { width: 100%; padding: 18px; border-radius: 20px; border: 1px solid #e2e8f0; box-sizing: border-box; font-size: 18px; outline: none; background: #f8fafc; }
        button { width: 100%; padding: 18px; background: #0ea5e9; color: white; border: none; border-radius: 20px; margin-top: 10px; font-weight: bold; font-size: 18px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #0284c7; }
    </style>
</head>
<body id="bg">
    <div class="card">
        <h1>Ade</h1>
        <p style="color: #ef4444; font-weight: bold; margin-bottom: 15px;">Conectada</p>
        <div id="output">Hola. Ya estoy lista para hablar y dibujar para ti. Que quieres hacer hoy?</div>
        <input type="text" id="userInput" placeholder="Escribe un mensaje...">
        <button onclick="enviar()">Enviar mensaje</button>
    </div>
    <script>
        function enviar() {
            const inBox = document.getElementById("userInput");
            const outBox = document.getElementById("output");
            const body = document.getElementById("bg");
            if(!inBox.value) return;
            outBox.innerHTML = "<i>Ade esta escribiendo...</i>";
            fetch(`/preguntar?msg=${encodeURIComponent(inBox.value)}`)
                .then(r => r.json())
                .then(data => {
                    outBox.innerHTML = data.res;
                    body.style.background = data.color;
                    if(data.tipo === "texto") {
                        let v = new SpeechSynthesisUtterance(data.res);
                        v.lang = 'es-ES';
                        window.speechSynthesis.speak(v);
                    }
                    inBox.value = "";
                    outBox.scrollTop = 0;
                });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
