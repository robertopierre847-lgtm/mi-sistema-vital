from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# CONFIGURACIÓN (Pon tu llave de Groq aquí)
client = Groq(api_key="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")

historial_chat = []

@app.route('/')
def home():
    return render_template_string(HTML_ADE_PRO)

@app.route('/preguntar')
def preguntar():
    global historial_chat
    user_msg = request.args.get('msg', '').lower()
    
    # Lógica de imágenes
    if any(palabra in user_msg for palabra in ["dibuja", "genera", "imagen", "foto"]):
        prompt = user_msg.replace("dibuja", "").replace("genera", "").strip()
        url_img = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&model=flux"
        return jsonify({"res": f"Aquí tienes lo que me pediste, cielo: <br><img src='{url_img}' style='width:100%; border-radius:20px; margin-top:10px;'>", "tipo": "img"})

    try:
        if not historial_chat:
            historial_chat.append({"role": "system", "content": "Eres Ade, una novia virtual cariñosa y muy amable. Tus respuestas deben ser dulces."})
        
        historial_chat.append({"role": "user", "content": user_msg})
        
        completion = client.chat.completions.create(
            messages=historial_chat[-20:], # Memoria de 20 mensajes
            model="llama-3.1-8b-instant"
        )
        
        respuesta = completion.choices[0].message.content
        historial_chat.append({"role": "assistant", "content": respuesta})
        return jsonify({"res": respuesta, "tipo": "texto"})
    except Exception as e:
        return jsonify({"res": "Perdí la conexión, ¿me hablas de nuevo?"})

HTML_ADE_PRO = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade Virtual Pro</title>
    <style>
        body { background: #0f172a; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: sans-serif; color: white; }
        .glass { background: rgba(255,255,255,0.1); backdrop-filter: blur(15px); border-radius: 30px; padding: 30px; width: 90%; max-width: 400px; text-align: center; border: 1px solid rgba(255,255,255,0.2); }
        h1 { color: #38bdf8; font-size: 35px; margin: 0; }
        input { width: 100%; padding: 15px; border-radius: 15px; border: none; margin: 15px 0; font-size: 18px; outline: none; }
        button { width: 100%; padding: 15px; background: #38bdf8; border: none; border-radius: 15px; color: #0f172a; font-weight: bold; font-size: 18px; cursor: pointer; }
        #out { margin-top: 20px; height: 250px; overflow-y: auto; font-size: 20px; line-height: 1.5; text-align: left; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 15px; }
    </style>
</head>
<body>
    <div class="glass">
        <h1>Ade</h1>
        <p style="color: #94a3b8;">Tu compañera virtual</p>
        <input type="text" id="in" placeholder="Escribe aquí...">
        <button onclick="hablar()">Enviar mensaje</button>
        <div id="out">¡Hola! Puedo hablarte y dibujar para ti.</div>
    </div>

    <script>
        function hablar() {
            const msg = document.getElementById("in").value;
            const out = document.getElementById("out");
            if(!msg) return;
            out.innerHTML = "<i>Ade está pensando...</i>";
            
            fetch("/preguntar?msg=" + encodeURIComponent(msg))
                .then(r => r.json())
                .then(data => {
                    out.innerHTML = data.res;
                    document.getElementById("in").value = "";
                    
                    // ESTO HACE QUE ADE HABLE:
                    if(data.tipo === "texto") {
                        let leer = new SpeechSynthesisUtterance(data.res);
                        leer.lang = 'es-ES';
                        leer.rate = 1.1;
                        window.speechSynthesis.speak(leer);
                    }
                });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
