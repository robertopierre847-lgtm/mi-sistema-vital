from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Configura tu llave de Groq aquí
client = Groq(api_key="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")

@app.route('/')
def home():
    return render_template_string(HTML_TEST)

@app.route('/preguntar')
def preguntar(        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_msg}],
            model="llama-3.3-70b-versatile",", # Prueba con este si el otro falla
)
             ):
    user_msg = request.args.get('msg', '')
    try:
        # Aquí conectamos con el modelo Llama 3 de Groq
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_msg}],
            model="llama3-8b-8192",
        )
        respuesta = chat_completion.choices[0].message.content
        return jsonify({"res": respuesta})
    except Exception as e:
        return jsonify({"res": f"Error: {str(e)}"})

HTML_TEST = """
<!DOCTYPE html>
<html>
<head>
    <title>Prueba Groq</title>
    <style>
        body { background: #121212; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 50px; }
        .box { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; width: 300px; border: 1px solid rgba(255,255,255,0.2); }
        input { width: 100%; padding: 10px; margin-top: 10px; border-radius: 5px; border: none; box-sizing: border-box; }
        button { width: 100%; padding: 10px; margin-top: 10px; background: #00ffa3; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
        #output { margin-top: 20px; font-size: 0.9em; color: #00ffa3; }
    </style>
</head>
<body>
    <div class="box">
        <h3>Prueba de IA</h3>
        <input id="in" placeholder="Escribe un saludo...">
        <button onclick="enviar()">Probar conexión</button>
        <div id="output"></div>
    </div>
    <script>
        function enviar() {
            let m = document.getElementById("in").value;
            let out = document.getElementById("output");
            out.innerText = "Pensando...";
            fetch("/preguntar?msg="+m).then(r=>r.json()).then(d=>{
                out.innerText = d.res;
            });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
