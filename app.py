from flask import Flask, request, jsonify, render_template_string
import requests
import random

app = Flask(__name__)

# Base de datos de preguntas para el juego (se pueden expandir)
banco_preguntas = [
    {"q": "¿Quién es la madre de tu madre?", "a": "abuela", "cat": "Familia"},
    {"q": "¿Cómo se llama el hijo de tu hermano?", "a": "sobrino", "cat": "Familia"},
    {"q": "¿Qué parentesco tiene contigo el hermano de tu padre?", "a": "tio", "cat": "Familia"},
    {"q": "¿Cuál es el planeta más grande?", "a": "jupiter", "cat": "Ciencia"},
    {"q": "¿En qué país están las pirámides de Giza?", "a": "egipto", "cat": "Cultura"},
    {"q": "¿Qué animal dice miau?", "a": "gato", "cat": "Animales"},
    {"q": "¿Cuál es el color de las esmeraldas?", "a": "verde", "cat": "General"}
]

# Estado del juego global (Nota: En producción usar una DB o sesión)
estado_usuario = {"nivel": 1}

def obtener_respuesta_wikipedia(query):
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        headers = {'User-Agent': 'AdeOS/1.0 (contact@example.com)'}
        res = requests.get(url, headers=headers).json()
        
        if "extract" in res:
            texto = res["extract"]
            img = res.get("thumbnail", {}).get("source", "")
            return texto, img
        return "No encontré información sobre eso. Intenta con otra palabra.", ""
    except:
        return "Error de conexión con el servidor de conocimiento.", ""

@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ade OS 💎</title>
    <style>
        :root {
            --glass: rgba(255, 255, 255, 0.15);
            --border: rgba(255, 255, 255, 0.2);
        }

        body {
            margin: 0;
            height: 100vh;
            background: url('https://images.unsplash.com/photo-1464802686167-b939a6910659?auto=format&fit=crop&q=80') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        /* Efecto Flotante */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
            100% { transform: translateY(0px); }
        }

        .window {
            width: 450px;
            height: 650px;
            background: var(--glass);
            backdrop-filter: blur(25px) saturate(180%);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid var(--border);
            border-radius: 25px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            animation: float 5s ease-in-out infinite;
            overflow: hidden;
        }

        .header {
            padding: 20px;
            text-align: center;
            color: white;
            border-bottom: 1px solid var(--border);
            font-weight: bold;
            letter-spacing: 2px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }

        #chat-area {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            scrollbar-width: none;
        }

        .bubble {
            margin-bottom: 15px;
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 85%;
            font-size: 14px;
            line-height: 1.5;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }

        .ai { background: rgba(0, 122, 255, 0.3); color: white; align-self: flex-start; border-bottom-left-radius: 2px; }
        .user { background: rgba(255, 255, 255, 0.8); color: #333; margin-left: auto; border-bottom-right-radius: 2px; }

        .wiki-img { width: 100%; border-radius: 10px; margin-top: 10px; border: 1px solid var(--border); }

        .input-bar {
            padding: 20px;
            display: flex;
            gap: 10px;
            background: rgba(0,0,0,0.1);
        }

        input {
            flex: 1;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: rgba(255,255,255,0.1);
            color: white;
            outline: none;
        }

        input::placeholder { color: rgba(255,255,255,0.6); }

        button {
            padding: 10px 20px;
            border-radius: 12px;
            border: none;
            background: #00d2ff;
            color: white;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
        }

        button:hover { background: #3a7bd5; transform: scale(1.05); }

        .status-tag {
            font-size: 10px;
            background: rgba(0,0,0,0.2);
            padding: 2px 8px;
            border-radius: 10px;
            margin-bottom: 5px;
            display: inline-block;
        }
    </style>
</head>
<body>

<div class="window">
    <div class="header">ADE OS v2.0 💎</div>
    <div id="chat-area">
        <div class="bubble ai">Bienvenido al Sistema Operativo Ade. <br><br>• Escribe "buscar [tema]" para Wikipedia.<br>• Escribe "jugar" para iniciar el desafío de 666 niveles.</div>
    </div>
    <div class="input-bar">
        <input type="text" id="userInput" placeholder="Escribe un comando..." onkeypress="handleKey(event)">
        <button onclick="process()">Enviar</button>
    </div>
</div>

<script>
    async function process() {
        const input = document.getElementById("userInput");
        const chat = document.getElementById("chat-area");
        const val = input.value.trim();
        if(!val) return;

        chat.innerHTML += `<div class="bubble user">${val}</div>`;
        input.value = "";

        const response = await fetch("/api/logic", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({msg: val})
        });

        const data = await response.json();
        
        let aiHtml = `<div class="bubble ai">`;
        if(data.type === "juego") aiHtml += `<span class="status-tag">NIVEL ${data.nivel}/666</span><br>`;
        aiHtml += data.response;
        if(data.img) aiHtml += `<img src="${data.img}" class="wiki-img">`;
        aiHtml += `</div>`;
        
        chat.innerHTML += aiHtml;
        chat.scrollTop = chat.scrollHeight;
    }

    function handleKey(e) { if(e.key === "Enter") process(); }
</script>

</body>
</html>
    """)

@app.route("/api/logic", methods=["POST"])
def logic():
    data = request.json
    msg = data.get("msg", "").lower().strip()
    
    # LÓGICA DE BÚSQUEDA WIKIPEDIA
    if msg.startswith("buscar"):
        tema = msg.replace("buscar", "").strip()
        texto, imagen = obtener_respuesta_wikipedia(tema)
        return jsonify({"response": texto, "img": imagen, "type": "wiki"})

    # LÓGICA DEL JUEGO
    if "jugar" in msg or "nivel" in msg:
        pregunta = random.choice(banco_preguntas)
        return jsonify({
            "response": f"Pregunta de {pregunta['cat']}: {pregunta['q']}",
            "nivel": estado_usuario["nivel"],
            "type": "juego",
            "ans": pregunta['a'] # Guardamos respuesta para comparar
        })

    # LÓGICA DE RESPUESTA A PREGUNTAS
    # (Simulación de niveles: si responde bien, sube nivel)
    for p in banco_preguntas:
        if msg == p['a']:
            estado_usuario["nivel"] += 1
            nueva = random.choice(banco_preguntas)
            return jsonify({
                "response": f"✨ ¡Correcto! Avanzas al siguiente nivel.\n\nSiguiente: {nueva['q']}",
                "nivel": estado_usuario["nivel"],
                "type": "juego"
            })

    return jsonify({"response": "No reconozco ese comando. Intenta 'buscar' algo o 'jugar'.", "type": "chat"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
                                  
