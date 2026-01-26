from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACIÓN DE LA IA ---
# Pon tu clave aquí dentro de las comillas
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
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_msg}],
            model="llama-3.1-8b-instant"
        )
        respuesta = chat_completion.choices[0].message.content
        return jsonify({"res": respuesta})
    except Exception as e:
        return jsonify({"res": f"Error técnico: {str(e)}"})

# --- DISEÑO CRISTALIZADO, FLOTANTE Y FIJO ---
HTML_UI = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IA Crystal Floating</title>
    <style>
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
            100% { transform: translateY(0px); }
        }

        body {
            background: linear-gradient(135deg, #f0f9ff 0%, #bae6fd 100%);
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', sans-serif;
            overflow: hidden; /* Evita que la pantalla entera se mueva */
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
            animation: float 4s ease-in-out infinite; /* EFECTO FLOTANTE */
        }

        h2 { color: #0369a1; margin-bottom: 15px; font-weight: 300; }

        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid rgba(255, 255, 255, 0.5);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.6);
            box-sizing: border-box;
            outline: none;
            color: #0c4a6e;
        }

        button {
            width: 100%;
            background-color: #0ea5e9;
            color: white;
            padding: 14px;
            margin: 5px 0;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
        }

        /* CUADRO DE RESPUESTA CON SCROLL FIJO */
        #output {
            margin-top: 15px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            color: #075985;
            height: 150px; /* Altura fija para que no crezca más */
            overflow-y: auto; /* Permite scroll si el texto es largo */
            text-align: left;
            font-size: 0.9em;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        /* Estilo para el scroll interno */
        #output::-webkit-scrollbar { width: 4px; }
        #output::-webkit-scrollbar-thumb { background: #0ea5e9; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="glass-box">
        <h2>IA Flotante</h2>
        <input type="text" id="userInput" placeholder="Escribe tu duda aquí...">
        <button onclick="enviar()">Enviar Mensaje</button>
        <div id="output">¡Hola! Mi respuesta se quedará aquí dentro aunque sea muy larga, así siempre verás el botón de arriba.</div>
    </div>

    <script>
        function enviar() {
            const inBox = document.getElementById("userInput");
            const outBox = document.getElementById("output");
            if (!inBox.value) return;

            outBox.innerHTML = "<i>Pensando...</i>";
            
            fetch(`/preguntar?msg=${encodeURIComponent(inBox.value)}`)
                .then(res => res.json())
                .then(data => {
                    outBox.innerText = data.res;
                    inBox.value = "";
                })
                .catch(err => {
                    outBox.innerText = "Error: Verifica tu clave.";
                });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
