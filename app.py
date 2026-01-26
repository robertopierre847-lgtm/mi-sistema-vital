from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACIÓN DE LA IA ---
# Reemplaza TU_LLAVE_AQUI con tu clave gsk_...
client = Groq(api_key="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")

# Memoria de larga duración
historial_chat = []

@app.route('/')
def home():
    return render_template_string(HTML_UI)

@app.route('/preguntar')
def preguntar():
    global historial_chat
    user_msg = request.args.get('msg', '')
    if not user_msg:
        return jsonify({"res": "Dime algo, aquí estoy para ti..."})
    
    try:
        # Si el historial está vacío, le damos una instrucción de personalidad
        if len(historial_chat) == 0:
            historial_chat.append({
                "role": "system", 
                "content": "Tu nombre es Ade. Eres una asistente virtual muy amable, cariñosa y atenta. Tu objetivo es ayudar al usuario en todo lo que necesite con mucha dulzura."
            })

        # Guardamos lo que dice el usuario
        historial_chat.append({"role": "user", "content": user_msg})
        
        # Mantener historial (máximo 30 mensajes)
        if len(historial_chat) > 30:
            historial_chat = historial_chat[-30:]

        # Llamada a Groq
        chat_completion = client.chat.completions.create(
            messages=historial_chat,
            model="llama-3.1-8b-instant"
        )
        
        respuesta = chat_completion.choices[0].message.content
        
        # Guardamos la respuesta de Ade en memoria
        historial_chat.append({"role": "assistant", "content": respuesta})
        
        return jsonify({"res": respuesta})
    except Exception as e:
        return jsonify({"res": f"Lo siento, hubo un error técnico: {str(e)}"})

# --- DISEÑO CRISTALIZADO "ADE" ---
HTML_UI = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade - Asistente Virtual</title>
    <style>
        @keyframes floating {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }

        body {
            background: linear-gradient(135deg, #f0f9ff 0%, #bae6fd 100%);
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }

        .glass-panel {
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.7);
            border-radius: 40px;
            padding: 35px;
            width: 90%;
            max-width: 450px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
            animation: floating 6s ease-in-out infinite;
        }

        h1 {
            color: #0369a1;
            font-size: 42px;
            margin-bottom: 5px;
            letter-spacing: -1px;
        }

        .status {
            color: #0ea5e9;
            font-size: 14px;
            margin-bottom: 25px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        input {
            width: 100%;
            padding: 20px;
            font-size: 20px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            background: rgba(255, 255, 255, 0.8);
            color: #0c4a6e;
            margin-bottom: 15px;
            outline: none;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 18px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            background: #0ea5e9;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 5px 15px rgba(14, 165, 233, 0.3);
        }

        button:hover { background: #0284c7; transform: scale(1.02); }

        #output {
            margin-top: 25px;
            padding: 25px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            color: #075985;
            height: 250px;
            overflow-y: auto;
            text-align: left;
            font-size: 22px; /* LETRA GRANDE */
            line-height: 1.6;
            border: 1px solid rgba(255, 255, 255, 0.4);
        }

        #output::-webkit-scrollbar { width: 5px; }
        #output::-webkit-scrollbar-thumb { background: #0ea5e9; border-radius: 10px; }
    </style>
</head>
<body>

    <div class="glass-panel">
        <h1>Ade</h1>
        <div class="status">● Conectada contigo</div>
        
        <input type="text" id="userInput" placeholder="Dime algo, cielo...">
        <button onclick="enviar()">Hablar con Ade</button>
        
        <div id="output">¡Hola! Soy Ade. Estoy aquí para escucharte y ayudarte en lo que necesites con todo mi cariño. ¿De qué quieres hablar?</div>
    </div>

    <script>
        function enviar() {
            const inBox = document.getElementById("userInput");
            const outBox = document.getElementById("output");
            if (!inBox.value) return;

            outBox.innerHTML = "<i style='color: #0ea5e9;'>Ade está escribiendo...</i>";
            
            fetch(`/preguntar?msg=${encodeURIComponent(inBox.value)}`)
                .then(res => res.json())
                .then(data => {
                    outBox.innerText = data.res;
                    inBox.value = "";
                    outBox.scrollTop = 0;
                })
                .catch(err => {
                    outBox.innerText = "Lo siento, perdí la conexión un momento.";
                });
        }

        document.getElementById("userInput").addEventListener("keypress", (e) => {
            if (e.key === "Enter") enviar();
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
