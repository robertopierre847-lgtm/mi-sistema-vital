from flask import Flask, request, jsonify, render_template_string
from groq import Groq
import os

app = Flask(__name__)

# --- IMPORTANTE: PON TU LLAVE AQUI DENTRO DE LAS COMILLAS ---
LLAVE_REAL = "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" 

client = Groq(api_key=LLAVE_REAL)

@app.route("/")
def home():
    return render_template_string(HTML_DISENO)

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        msg = data.get("msg","")
        # El cerebro de Ade con emojis y modo cariñoso
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Eres Ade, una IA dulce y femenina. Usa emojis y colores en tus palabras. Eres amiga del usuario."},
                {"role": "user", "content": msg}
            ]
        )
        return jsonify({"response": chat_completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"Lo siento, hay un error: {str(e)}"})

# DISEÑO SATISFACTORIO (AZUL Y BLANCO)
HTML_DISENO = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: linear-gradient(135deg, #e0f2fe, #f0f9ff); font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .glass { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); padding: 30px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); width: 400px; border: 1px solid white; }
        #box { height: 300px; overflow-y: auto; margin-bottom: 20px; padding: 10px; font-size: 18px; color: #334155; }
        input { width: 100%; padding: 15px; border-radius: 15px; border: 1px solid #e2e8f0; outline: none; }
        button { width: 100%; padding: 15px; background: #38bdf8; color: white; border: none; border-radius: 15px; margin-top: 10px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="glass">
        <h2 style="color:#0ea5e9; text-align:center;">Ade ✨</h2>
        <div id="box">Hola, ¿jugamos o charlamos? 😊</div>
        <input type="text" id="in" placeholder="Escribe aquí...">
        <button onclick="enviar()">Enviar</button>
    </div>
    <script>
        function enviar() {
            const i = document.getElementById("in");
            const b = document.getElementById("box");
            if(!i.value) return;
            b.innerHTML += "<p><b>Tú:</b> "+i.value+"</p>";
            
            fetch("/api/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({msg: i.value})
            })
            .then(r => r.json())
            .then(d => {
                b.innerHTML += "<p><b>Ade:</b> "+d.response+"</p>";
                i.value = "";
                b.scrollTop = b.scrollHeight;
                // Voz femenina
                window.speechSynthesis.cancel();
                let m = new SpeechSynthesisUtterance(d.response);
                m.lang = 'es-ES'; m.pitch = 1.3;
                window.speechSynthesis.speak(m);
            });
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

