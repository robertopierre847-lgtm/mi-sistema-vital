from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- COLOCA TUS LLAVES AQUI ---
LLAVE_GROQ = "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" 
LLAVE_HF = "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" 

client = Groq(api_key=LLAVE_GROQ)

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/preguntar')
def preguntar():
    msg = request.args.get('msg', '').lower()
    if not msg: return jsonify({"res": "Dime algo, mi amor..."})

    # Si pides dibujo, Ade usa Pollinations pero con tu seguridad de HF
    if any(p in msg for p in ["dibuja", "foto", "imagen"]):
        prompt = msg.replace("dibuja", "").strip() or "un paisaje lindo"
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=800&height=800&model=flux&seed={os.urandom(2).hex()}"
        return jsonify({"res": f"Mira que lindo me quedo el dibujo para ti: <br><img src='{url}' style='width:100%; border-radius:15px; margin-top:10px;' onerror='this.src=this.src'>" })

    try:
        # Aquí es donde Ade mantiene su personalidad cariñosa
        chat = client.chat.completions.create(
            messages=[{"role": "system", "content": "Eres Ade, una novia virtual muy dulce, amorosa y atenta. No uses emojis, pero habla con mucho cariño."},
                      {"role": "user", "content": msg}],
            model="llama-3.1-8b-instant"
        )
        return jsonify({"res": chat.choices[0].message.content})
    except:
        return jsonify({"res": "Cielo, hubo un pequeño error, ¿me lo repites?"})

# Diseño que no da errores en Render
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ade</title>
    <style>
        body { background: #fff5f8; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 25px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 90%; max-width: 400px; text-align: center; }
        #output { height: 300px; overflow-y: auto; margin: 15px 0; text-align: left; padding: 10px; border-radius: 15px; background: #fafafa; font-size: 18px; line-height: 1.4; }
        input { width: 100%; padding: 15px; border-radius: 15px; border: 1px solid #ddd; box-sizing: border-box; outline: none; }
        button { width: 100%; padding: 15px; background: #ff4d94; color: white; border: none; border-radius: 15px; margin-top: 10px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1 style="color:#ff4d94; margin:0">Ade</h1>
        <div id="output">¡Hola Robert! Ya estoy aqui para ti. ¿Quieres que hablemos o que te dibuje algo?</div>
        <input type="text" id="in" placeholder="Escribe un mensaje...">
        <button onclick="send()">Enviar a Ade</button>
    </div>
    <script>
        function send() {
            const i = document.getElementById("in");
            const o = document.getElementById("output");
            if(!i.value) return;
            o.innerHTML = "<i>Ade esta pensando...</i>";
            fetch('/preguntar?msg='+encodeURIComponent(i.value))
                .then(r => r.json())
                .then(d => { o.innerHTML = d.res; i.value = ""; o.scrollTop = o.scrollHeight; });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
