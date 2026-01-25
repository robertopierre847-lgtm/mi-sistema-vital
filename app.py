from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACIÓN DE LA IA ---
# REEMPLAZA ÚNICAMENTE EL TEXTO gsk_... POR TU CLAVE REAL
# Mantén las comillas al principio y al final.
client = Groq(api_key="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")

@app.route('/')
def home():
    return render_template_string(HTML_UI)

@app.route('/preguntar')
def preguntar():
    user_msg = request.args.get('msg', '')
    if not user_msg:
        return jsonify({"res": "Escribe algo para comenzar..."})
    
    try:
        # Usamos un modelo que siempre está activo y es gratuito
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_msg}],
            model="llama-3.1-8b-instant"
        )
        respuesta = chat_completion.choices[0].message.content
        return jsonify({"res": respuesta})
    except Exception as e:
        return jsonify({"res": f"Error técnico: {str(e)}"})

# --- DISEÑO CRISTALIZADO AZUL Y BLANCO ---
HTML_UI = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat IA Crystal</title>
    <style>
        body {
            background: linear-gradient(135deg, #f0f9ff 0%, #bae6fd 100%);
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .glass-box {
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.7);
            border-radius: 25px;
            padding: 2rem;
            width: 90%;
            max-width: 420px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            text-align: center;
        }
        h2 { color: #0369a1; margin-bottom: 20px; font-weight: 300; }
        input {
            width: 100%;
            padding: 12px 20px;
            margin: 8px 0;
            display: inline-block;
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.6);
            box-sizing: border-box;
            outline: none;
            color: #0c4a6e;
        }
        button {
            width: 100%;
            background-color: #0ea5e9;
            color: white;
            padding: 14px 20px;
            margin: 10px 0;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
        }
        button:hover { background-color: #0284c7; transform: scale(1.02); }
        #output {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            color: #075985;
            min-height: 80px;
            text-align: left;
            font-size: 0.95em;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
    </style>
</head>
<body>
    <div class="glass-box">
        <h2>Asistente Crystal</h2>
        <input type="text" id="userInput" placeholder="Escribe tu duda aquí...">
        <button onclick="enviar()">Enviar a la Nube</button>
        <div id="output">Hola, ¿en qué puedo ayudarte hoy?</div>
    </div>

    <script>
        function enviar() {
            const inBox = document.getElementById("userInput");
            const outBox = document.getElementById("output");
            if (!inBox.value) return;

            outBox.innerHTML = "<i>Procesando en la nube...</i>";
            
            fetch(`/preguntar?msg=${encodeURIComponent(inBox.value)}`)
                .then(res => res.json())
                .then(data => {
                    outBox.innerText = data.res;
                    inBox.value = "";
                })
                .catch(err => {
                    outBox.innerText = "Error: Verifica tu conexión u API Key.";
                });
        }
        // Enviar con la tecla Enter
        document.getElementById("userInput").addEventListener("keypress", (e) => {
            if (e.key === "Enter") enviar();
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
