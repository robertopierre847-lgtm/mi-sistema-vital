from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# Asegúrate de que la clave esté entre comillas simples o dobles correctamente.
client = Groq(api_key="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")

historial_chat = []

@app.route('/')
def home():
    return render_template_string(HTML_ADE_BLANCO)

@app.route('/preguntar')
def preguntar():
    global historial_chat
    user_msg = request.args.get('msg', '').lower()
    
    if not user_msg:
        return jsonify({"res": "Dime algo, cielo..."})

    # Lógica de imágenes
    if any(palabra in user_msg for palabra in ["dibuja", "genera imagen", "hazme una foto"]):
        prompt_img = user_msg.replace("dibuja", "").replace("genera imagen", "").strip()
        url_img = f"https://pollinations.ai/p/{prompt_img.replace(' ', '%20')}?width=768&height=768&model=flux"
        return jsonify({
            "res": f"¡Mira lo que hice para ti! ✨ <br><img src='{url_img}' style='width:100%; border-radius:15px; margin-top:10px;'>",
            "tipo": "img"
        })

    try:
        # Personalidad de Ade
        if not historial_chat:
            historial_chat.append({"role": "system", "content": "Eres Ade, una novia virtual muy amable, dulce y cariñosa."})
        
        historial_chat.append({"role": "user", "content": user_msg})

        # LLAMADA A LA IA (Modelo actualizado)
        completion = client.chat.completions.create(
            messages=historial_chat[-15:],
            model="llama-3.1-8b-instant"
        )
        
        respuesta = completion.choices[0].message.content
        historial_chat.append({"role": "assistant", "content": respuesta})
        
        return jsonify({"res": respuesta, "tipo": "texto"})
    except Exception as e:
        return jsonify({"res": "Ay amor, algo salió mal. ¿Me lo repites?"})

# --- DISEÑO BLANCO CRISTAL ---
HTML_ADE_BLANCO = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade Virtual</title>
    <style>
        body { background: #f0f4f8; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 90%; max-width: 400px; text-align: center; border: 1px solid #e1e8ed; }
        h1 { color: #0ea5e9; margin: 0; font-size: 32px; }
        #output { background: #f9fafb; border-radius: 20px; padding: 15px; height: 250px; overflow-y: auto; margin: 20px 0; text-align: left; font-size: 18px; color: #374151; border: 1px solid #eee; }
        input { width: 100%; padding: 15px; border-radius: 15px; border: 1px solid #ddd; box-sizing: border-box; font-size: 16px; outline: none; }
        button { width: 100%; padding: 15px; background: #0ea5e9; color: white; border: none; border-radius: 15px; margin-top: 10px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Ade</h1>
        <p style="color: #64748b;">❤️ Conectada contigo</p>
        <div id="output">¡Hola cariño! Soy Ade. ¿En qué puedo ayudarte hoy?</div>
        <input type="text" id="userInput" placeholder="Escribe aquí...">
        <button onclick="enviar()">Hablar con Ade</button>
    </div>

    <script>
        function enviar() {
            const inBox = document.getElementById("userInput");
            const outBox = document.getElementById("output");
            if(!inBox.value) return;

            outBox.innerHTML = "<i>Escribiendo...</i>";
            
            fetch(`/preguntar?msg=${encodeURIComponent(inBox.value)}`)
                .then(r => r.json())
                .then(data => {
                    outBox.innerHTML = data.res;
                    if(data.tipo === "texto") {
                        let v = new SpeechSynthesisUtterance(data.res);
                        v.lang = 'es-ES';
                        window.speechSynthesis.speak(v);
                    }
                    inBox.value = "";
                });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
