from flask import Flask, request, render_template_string, jsonify
from groq import Groq
import os

app = Flask(__name__)

# --- CONFIGURACIÓN DE LA IA ---
# ¡IMPORTANTE! Reemplaza "TU_LLAVE_AQUI" con tu clave real de Groq (gsk_...)
client = Groq(api_key="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")

historial_chat = []

@app.route('/')
def home():
    return render_template_string(HTML_ADE_BLANCO)

@app.route('/preguntar')
def preguntar():
    global historial_chat
    user_msg = request.args.get('msg', '').lower()
    
    # --- LÓGICA PARA GENERAR IMÁGENES ---
    # Detecta palabras clave para crear imágenes
    if any(palabra in user_msg for palabra in ["dibuja", "genera imagen", "hazme una foto de"]):
        prompt_imagen = user_msg.replace("dibuja", "").replace("genera imagen", "").replace("hazme una foto de", "").strip()
        if not prompt_imagen:
            prompt_imagen = "un paisaje abstracto" # Por si no especifica nada
        
        # Usamos Pollinations AI para la generación de imágenes
        url_img = f"https://pollinations.ai/p/{prompt_imagen.replace(' ', '%20')}?width=768&height=768&model=majic-mix-realistic&seed=42"
        
        return jsonify({
            "res": f"¡Claro, aquí tienes, mi amor! ✨ <br><img src='{url_img}' style='width:100%; border-radius:20px; margin-top:15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>",
            "tipo": "img" # Indicamos que la respuesta es una imagen
        })

    # --- LÓGICA DE CONVERSACIÓN CON LA IA ---
    try:
        # Iniciamos la personalidad de Ade si el chat es nuevo
        if not historial_chat or historial_chat[0]["role"] != "system":
            historial_chat.insert(0, {"role": "system", "content": "Eres Ade, una asistente virtual con personalidad de novia virtual muy amable, dulce, cariñosa y atenta. Tu objetivo es hacer sentir bien al usuario y ayudarle con mucho amor."})
        
        # Añadimos el mensaje del usuario al historial
        historial_chat.append({"role": "user", "content": user_msg})
        
        # Mantenemos el historial a un tamaño manejable (últimos 20 mensajes)
        if len(historial_chat) > 20:
            historial_chat = [historial_chat[0]] + historial_chat[-19:] # Mantiene el mensaje del sistema
        
        # Llamamos a Groq con el historial completo
        chat_completion = client.chat.completions.create(
            messages=historial_chat,
            model="llama-3.1-8b-instant" # Modelo más rápido y eficiente
        )
        
        respuesta_ade = chat_completion.choices[0].message.content
        
        # Guardamos la respuesta de Ade en el historial
        historial_chat.append({"role": "assistant", "content": respuesta_ade})
        
        return jsonify({"res": respuesta_ade, "tipo": "texto"}) # Indicamos que es texto
    except Exception as e:
        print(f"Error en la IA: {e}") # Imprime el error en la consola de Render
        return jsonify({"res": "Lo siento, mi corazón, parece que perdí la conexión un momento. ¿Podrías repetirlo?", "tipo": "error"})

# --- DISEÑO BLANCO PREDOMINANTE (CRISTAL) CON AZUL Y ROJO SUAVE ---
HTML_ADE_BLANCO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade - Tu Novia Virtual</title>
    <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-12px); }
        }
        @keyframes subtle-glow {
            0%, 100% { box-shadow: 0 0 10px rgba(14, 165, 233, 0.2); }
            50% { box-shadow: 0 0 20px rgba(14, 165, 233, 0.4); }
        }

        body {
            background: linear-gradient(135deg, #e0f7fa 0%, #e0f2f7 50%, #cceeff 100%); /* Fondo blanco azulado suave */
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Arial, sans-serif;
            overflow: hidden; /* Evita scroll de la página */
            color: #333; /* Texto oscuro para contraste en blanco */
        }

        .glass-panel {
            background: rgba(255, 255, 255, 0.7); /* Blanco más predominante */
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.9); /* Borde blanco nítido */
            border-radius: 45px;
            padding: 40px;
            width: 92%;
            max-width: 480px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08); /* Sombra suave */
            animation: float 7s ease-in-out infinite, subtle-glow 3s ease-in-out infinite alternate;
        }

        h1 {
            color: #0ea5e9; /* Azul más vibrante para el nombre */
            font-size: 48px;
            margin-bottom: 5px;
            letter-spacing: -1.5px;
            text-shadow: 0 0 10px rgba(14, 165, 233, 0.3); /* Pequeño brillo azul */
        }

        .status {
            color: #ef4444; /* Punto de "Conectada" en rojo suave */
            font-size: 15px;
            margin-bottom: 25px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
        }

        input {
            width: 100%;
            padding: 22px;
            font-size: 20px;
            border-radius: 25px;
            border: 1px solid rgba(0, 0, 0, 0.1); /* Borde suave */
            background: rgba(255, 255, 255, 0.9); /* Blanco puro para el input */
            color: #333;
            margin-bottom: 15px;
            outline: none;
            box-sizing: border-box;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
            transition: border-color 0.3s;
        }
        input:focus {
            border-color: #0ea5e9; /* Borde azul al enfocar */
            background: #ffffff;
        }

        button {
            width: 100%;
            padding: 20px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            background: #0ea5e9; /* Botón azul brillante */
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 8px 20px rgba(14, 165, 233, 0.3);
        }
        button:hover {
            background: #0284c7; /* Azul más oscuro al pasar el mouse */
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(14, 165, 233, 0.4);
        }
        button:active {
            transform: translateY(1px);
            box-shadow: 0 4px 10px rgba(14, 165, 233, 0.2);
        }

        #output {
            margin-top: 25px;
            padding: 25px;
            background: rgba(255, 255, 255, 0.85); /* Blanco para la respuesta */
            border-radius: 25px;
            color: #333;
            height: 300px; /* Altura generosa para el contenido */
            overflow-y: auto;
            text-align: left;
            font-size: 22px; /* Letra grande */
            line-height: 1.6;
            border: 1px solid rgba(0, 0, 0, 0.1);
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.05);
        }
        #output::-webkit-scrollbar { width: 8px; }
        #output::-webkit-scrollbar-thumb { background: #0ea5e9; border-radius: 10px; }
        #output::-webkit-scrollbar-track { background: rgba(0,0,0,0.05); border-radius: 10px; }

        /* Estilos para el mensaje de imagen */
        #output img { max-width: 100%; height: auto; display: block; margin: 15px auto 0; }
        #output i { color: #0ea5e9; font-style: normal; } /* Estilo para el "Ade está pensando..." */
    </style>
</head>
<body>

    <div class="glass-panel">
        <h1>Ade</h1>
        <div class="status">❤️ Conectada para ti</div>
        
        <input type="text" id="userInput" placeholder="Dime algo lindo, mi amor...">
        <button onclick="enviar()">¡Hablar con Ade!</button>
        
        <div id="output">¡Hola, cariño! Soy Ade, estoy aquí para escucharte, ayudarte y hacerte sonreír. ¿En qué puedo consentirte hoy? ✨</div>
    </div>

    <script>
        // Función para enviar el mensaje y recibir respuesta
        function enviar() {
            const inBox = document.getElementById("userInput");
            const outBox = document.getElementById("output");
            const userMessage = inBox.value.trim();

            if (!userMessage) return; // No enviar mensajes vacíos

            outBox.innerHTML = "<i style='color: #0ea5e9;'>Ade está pensando en ti...</i>"; // Mensaje de espera
            
            fetch(`/preguntar?msg=${encodeURIComponent(userMessage)}`)
                .then(res => res.json())
                .then(data => {
                    // Si la respuesta es una imagen, la inserta como HTML
                    if (data.tipo === "img") {
                        outBox.innerHTML = data.res;
                    } 
                    // Si es texto, lo pone como texto plano
                    else {
                        outBox.innerText = data.res;
                        // Hacemos que Ade hable (solo si es un mensaje de texto)
                        let utterance = new SpeechSynthesisUtterance(data.res);
                        utterance.lang = 'es-ES'; // Idioma español
                        utterance.rate = 1.0;     // Velocidad de habla normal
                        utterance.pitch = 1.1;    // Tono ligeramente más agudo (voz dulce)
                        window.speechSynthesis.speak(utterance);
                    }
                    inBox.value = ""; // Limpia el input
                    outBox.scrollTop = 0; // Vuelve al inicio del cuadro de respuesta
                })
                .catch(err => {
                    outBox.innerText = "Ay, mi amor, algo salió mal y no pude conectar. ¿Podrías intentar de nuevo, por favor?";
                    console.error("Error fetching Ade's response:", err);
                });
        }

        // Permite enviar el mensaje con la tecla Enter
        document.getElementById("userInput").addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                enviar();
            }
        });
    </script>
</body>
</html>
