from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# CONFIGURACIÓN: Pon tu API Key de Groq aquí
client = Groq(api_key="Groq(api_key="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"

@app.route('/')
def home():
    return render_template_string(HTML_UI)

@app.route('/preguntar')
def preguntar():
    user_msg = request.args.get('msg', '')
    if not user_msg:
        return jsonify({"res": "Escribe algo primero..."})
        
    try:
        # Usamos el modelo más estable y rápido disponible
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_msg}],
            model="llama-3.1-8b-instant"
        )
        respuesta = chat_completion.choices[0].message.content
        return jsonify({"res": respuesta})
    except Exception as e:
        return jsonify({"res": f"Error: {str(e)}"})

# DISEÑO EN CRISTAL AZUL Y BLANCO
HTML_UI = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA Crystal Chat</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Roboto, sans-serif;
            color: white;
            overflow: hidden;
        }

        /* Efecto de cristal */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 30px;
            width: 90%;
            max-width: 450px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            text-align: center;
        }

        h2 { color: #38bdf8; margin-bottom: 20px; font-weight: 300; letter-spacing: 1px; }

        input {
            width: 100%;
            padding: 15px;
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            color: white;
            font-size: 16px;
            margin-bottom: 15px;
            outline: none;
            transition: 0.3s;
        }

        input:focus { border-color: #38bdf8; background: rgba(255, 255, 255, 0.12); }

        button {
            width: 100%;
            padding: 15px;
            background: #38bdf8;
            border: none;
            border-radius: 12px;
            color: #0f172a;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
            text-transform: uppercase;
        }

        button:hover { background: #7dd3fc; transform: translateY(-2px); }

        #output {
            margin-top: 25px;
            min-height: 100px;
            max-height: 250px;
            overflow-y: auto;
            text-align: left;
            padding: 15px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.6;
            color: #e2e8f0;
            border-left: 3px solid #38bdf8;
        }

        /* Scrollbar bonito */
        #output::-webkit-scrollbar { width: 5px; }
        #output::-webkit-scrollbar-thumb { background: rgba(56, 189, 248, 0.5); border-radius: 10px; }
    </style>
</head>
<body>

    <div class="glass-card">
        <h2>Crystal Chat IA</h2>
        <input type="text" id="userInput" placeholder="Escribe tu mensaje aquí...">
        <button onclick="enviar()">Enviar Mensaje</button>
        <div id="output">¡Hola! Soy tu IA en la nube. ¿En qué puedo ayudarte hoy?</div>
    </div>

    <script>
        function enviar() {
            const input = document.getElementById("userInput");
            const output = document.getElementById("output");
            const mensaje = input.value;

            if (!mensaje) return;

            output.innerHTML = "<i>Pensando...</i>";
            input.value = "";

            fetch(`/preguntar?msg=${encodeURIComponent(mensaje)}`)
                .then(response => response.json())
                .then(data => {
                    output.innerText = data.res;
                })
                .catch(error => {
                    output.innerText = "Error: No se pudo conectar con la IA.";
                    console.error(error);
                });
        }

        // Permitir enviar con la tecla Enter
        document.getElementById("userInput").addEventListener("keypress", function(e) {
            if (e.key === "Enter") enviar();
        });
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
            
