from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACION ---
# Reemplaza con tu llave de Groq
client = Groq(api_key="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")

historial_memoria = []

@app.route('/')
def home():
    return render_template_string(HTML_SUPER_APP)

@app.route('/preguntar')
def preguntar():
    global historial_memoria
    msg = request.args.get('msg', '').lower()
    
    try:
        if not historial_memoria:
            # Instrucciones corregidas: Permitimos emojis y eliminamos nombres propios
            historial_memoria.append({
                "role": "system", 
                "content": "Eres Ade, una asistente virtual femenina y amable. Puedes usar emojis en tus respuestas para ser más expresiva. No conoces personalmente al usuario, así que no inventes historias pasadas sobre él."
            })
        
        historial_memoria.append({"role": "user", "content": msg})

        chat = client.chat.completions.create(
            messages=historial_memoria[-10:],
            model="llama-3.1-8b-instant"
        )
        
        respuesta = chat.choices[0].message.content
        historial_memoria.append({"role": "assistant", "content": respuesta})
        
        return jsonify({"res": respuesta})
    except:
        return jsonify({"res": "Hubo un problema con la respuesta. 😕"})

# --- DISEÑO DE CRISTAL MINIMALISTA ---
HTML_SUPER_APP = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade - Interfaz</title>
    <style>
        body { 
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); 
            height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center;
            font-family: sans-serif;
        }
        .glass-box {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            width: 90%; max-width: 400px; padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            color: white;
        }
        #chat { 
            height: 350px; overflow-y: auto; margin-bottom: 15px; padding: 10px;
            background: rgba(0, 0, 0, 0.2); border-radius: 15px; 
        }
        input { 
            width: 100%; padding: 12px; border-radius: 10px; border: none; outline: none;
            background: rgba(255, 255, 255, 0.8); color: #333; margin-bottom: 10px; box-sizing: border-box;
        }
        button { 
            width: 100%; padding: 12px; border-radius: 10px; border: none;
            background: #ffffff; color: #b21f1f; font-weight: bold; cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="glass-box">
        <h2 style="text-align:center; margin-top:0;">Ade ✨</h2>
        <div id="chat">Hola, ¿cómo puedo ayudarte hoy?</div>
        <input type="text" id="userInput" placeholder="Escribe un mensaje...">
        <button onclick="enviar()">Enviar</button>
    </div>

    <script>
        function hablar(texto) {
            window.speechSynthesis.cancel();
            let msg = new SpeechSynthesisUtterance(texto);
            msg.lang = 'es-ES';
            msg.rate = 1.0; // Velocidad normal
            msg.pitch = 1.2; // Tono ligeramente femenino
            window.speechSynthesis.speak(msg);
        }

        function enviar() {
            const input = document.getElementById('userInput');
            const chat = document.getElementById('chat');
            if(!input.value) return;
            
            chat.innerHTML += "<p><b>Tú:</b> " + input.value + "</p>";
            let texto = input.value;
            input.value = "";

            fetch('/preguntar?msg=' + encodeURIComponent(texto))
                .then(r => r.json())
                .then(data => {
                    chat.innerHTML += "<p><b>Ade:</b> " + data.res + "</p>";
                    chat.scrollTop = chat.scrollHeight;
                    hablar(data.res);
                });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
