from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACIÓN ---
client = Groq(api_key="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")

# Memoria de larga duración
historial_chat = []

@app.route('/')
def home():
    return render_template_string(HTML_ADE_TOTAL)

@app.route('/preguntar')
def preguntar():
    global historial_chat
    user_msg = request.args.get('msg', '').lower()
    
    if not user_msg:
        return jsonify({"res": "Dime algo, cielo...", "color": "#ffffff"})

    # Lógica de "Humores" (Cambio de color según palabras)
    color_fondo = "#ffffff" # Blanco por defecto
    if any(p in user_msg for p in ["amo", "quiero", "linda", "bella", "hermosa", "cariño"]):
        color_fondo = "#fff0f6" # Rosa suave (Amor)
    elif any(p in user_msg for p in ["triste", "mal", "ayuda", "solo", "problema"]):
        color_fondo = "#e0f2fe" # Azul calma (Apoyo)
    elif any(p in user_msg for p in ["feliz", "bien", "genial", "jaja", "si"]):
        color_fondo = "#fefce8" # Amarillito (Alegría)

    try:
        if not historial_chat:
            historial_chat.append({
                "role": "system", 
                "content": "Eres Ade, una novia virtual cariñosa. Eres amable, dulce y atenta. Puedes traducir idiomas, guardar recordatorios y jugar. Habla siempre con amor."
            })
        
        historial_chat.append({"role": "user", "content": user_msg})

        completion = client.chat.completions.create(
            messages=historial_chat[-20:],
            model="llama-3.1-8b-instant"
        )
        
        respuesta = completion.choices[0].message.content
        historial_chat.append({"role": "assistant", "content": respuesta})
        
        return jsonify({"res": respuesta, "color": color_fondo})
    except Exception as e:
        return jsonify({"res": "Hubo un pequeño error, pero aquí sigo para ti.", "color": "#ffffff"})

# --- DISEÑO BLANCO DINÁMICO ---
HTML_ADE_TOTAL = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade - Tu Compañera Virtual</title>
    <style>
        body { 
            transition: background 0.8s ease; 
            background: #f8fafc; 
            font-family: 'Segoe UI', sans-serif; 
            display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; 
        }
        .container { 
            background: rgba(255, 255, 255, 0.9); 
            backdrop-filter: blur(10px);
            padding: 30px; border-radius: 40px; 
            box-shadow: 0 20px 50px rgba(0,0,0,0.05); 
            width: 92%; max-width: 450px; text-align: center; border: 1px solid #eee;
        }
        h1 { color: #0ea5e9; font-size: 40px; margin: 0; letter-spacing: -1px; }
        #chat-box { 
            background: white; border-radius: 25px; padding: 20px; height: 300px; 
            overflow-y: auto; margin: 20px 0; text-align: left; font-size: 19px; 
            color: #334155; border: 1px solid #f1f5f9; line-height: 1.5;
        }
        .options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }
        .opt { font-size: 12px; background: #f1f5f9; padding: 5px; border-radius: 10px; color: #64748b; }
        input { width: 100%; padding: 18px; border-radius: 20px; border: 1px solid #e2e8f0; box-sizing: border-box; font-size: 17px; outline: none; }
        button { width: 100%; padding: 18px; background: #0ea5e9; color: white; border: none; border-radius: 20px; margin-top: 10px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #0284c7; }
    </style>
</head>
<body id="bg">
    <div class="container">
        <h1>Ade</h1>
        <p style="color: #ef4444; font-weight: bold; margin: 5px 0;">❤️ Tu IA Completa</p>
        
        <div class="options-grid">
            <div class="opt">📝 Recordatorios</div>
            <div class="opt">🌍 Traductora</div>
            <div class="opt">🎨 Modos de Ánimo</div>
            <div class="opt">🎮 Juegos</div>
        </div>

        <div id="chat-box">¡Hola amor! Estoy lista con todas mis funciones activadas. Puedo ser tu agenda, tu traductora o simplemente escucharte. ¿Qué hacemos hoy? ✨</div>
        
        <input type="text" id="userInput" placeholder="Escribe aquí...">
        <button onclick="enviar()">Hablar con Ade</button>
    </div>

    <script>
        function enviar() {
            const inBox = document.getElementById("userInput");
            const outBox = document.getElementById("chat-box");
            const body = document.getElementById("bg");
            
            if(!inBox.value) return;
            outBox.innerHTML = "<i style='color:#0ea5e9'>Ade está pensando...</i>";
            
            fetch(`/preguntar?msg=${encodeURIComponent(inBox.value)}`)
                .then(r => r.json())
                .then(data => {
                    outBox.innerText = data.res;
                    body.style.background = data.color; // Cambia el color según el ánimo
                    
                    // Voz de Ade
                    let v = new SpeechSynthesisUtterance(data.res);
                    v.lang = 'es-ES';
                    window.speechSynthesis.speak(v);
                    
                    inBox.value = "";
                    outBox.scrollTop = outBox.scrollHeight;
                });
        }
    </script>
</body>
</html>
