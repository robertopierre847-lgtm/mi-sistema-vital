import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Base de datos temporal (en memoria)
chat_mensajes = []
jugadores_conectados = {}

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arena Vital 3vs3</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Roboto:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon-blue: #00f3ff; --neon-red: #ff0055; --dark: #0a0a12; }
        body { background: var(--dark); color: white; font-family: 'Roboto', sans-serif; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        h1 { font-family: 'Orbitron', sans-serif; color: var(--neon-blue); text-shadow: 0 0 10px var(--neon-blue); }
        
        .arena-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; width: 100%; max-width: 1000px; }
        
        .card { background: rgba(255,255,255,0.05); border: 1px solid var(--neon-blue); border-radius: 15px; padding: 20px; box-shadow: 0 0 15px rgba(0,243,255,0.2); }
        
        /* Chat Estilo Gaming */
        #chat-box { height: 200px; overflow-y: auto; background: rgba(0,0,0,0.5); border-radius: 10px; padding: 10px; margin-bottom: 10px; border-left: 3px solid var(--neon-blue); }
        .msg { margin-bottom: 8px; font-size: 14px; }
        .msg b { color: var(--neon-blue); }

        .btn { background: none; border: 2px solid var(--neon-blue); color: var(--neon-blue); padding: 10px 20px; cursor: pointer; font-family: 'Orbitron', sans-serif; font-weight: bold; transition: 0.3s; border-radius: 5px; }
        .btn:hover { background: var(--neon-blue); color: black; box-shadow: 0 0 20px var(--neon-blue); }
        
        input { background: rgba(255,255,255,0.1); border: 1px solid var(--neon-blue); color: white; padding: 10px; border-radius: 5px; width: 70%; }
        
        .team-select { display: flex; justify-content: space-around; margin-top: 20px; }
        .team-red { color: var(--neon-red); border-color: var(--neon-red); }
    </style>
</head>
<body>

    <h1>3vs3 ARENA VITAL</h1>

    <div class="arena-container">
        
        <div class="card">
            <h3>🛡️ Tu Perfil de Guerrero</h3>
            <div id="status">
                <p>Estado: <span id="user-status">Buscando Equipo...</span></p>
                <div class="team-select">
                    <button class="btn" onclick="unirse('Azul')">EQUIPO AZUL</button>
                    <button class="btn team-red" onclick="unirse('Rojo')">EQUIPO ROJO</button>
                </div>
            </div>
            <hr style="border: 0.5px solid #333; margin: 20px 0;">
            <h3>⚔️ Acciones de Batalla</h3>
            <div id="battle-btns">
                <button class="btn" onclick="atacar()">ATACAR</button>
                <button class="btn" style="border-color: #28a745; color: #28a745;">CURAR</button>
            </div>
        </div>

        <div class="card">
            <h3>💬 Chat de Escuadrón</h3>
            <div id="chat-box">
                <div class="msg"><b>Sistema:</b> Bienvenido a la arena. Esperando jugadores...</div>
                {% for m in mensajes %}
                <div class="msg"><b>{{ m.user }}:</b> {{ m.texto }}</div>
                {% endfor %}
            </div>
            <form action="/enviar" method="POST" style="display:flex; gap:5px;">
                <input type="text" name="mensaje" placeholder="Escribe a tu equipo..." required>
                <button type="submit" class="btn">ENVIAR</button>
            </form>
        </div>

    </div>

    <script>
        function unirse(equipo) {
            document.getElementById('user-status').innerText = "Conectado al Equipo " + equipo;
            alert("Te has unido al equipo " + equipo + ". ¡Prepara tus habilidades!");
        }

        function atacar() {
            const daño = Math.floor(Math.random() * 50) + 10;
            alert("¡Ataque realizado! Has causado " + daño + " de daño al equipo enemigo.");
        }
        
        // Auto-scroll del chat al final
        const chat = document.getElementById('chat-box');
        chat.scrollTop = chat.scrollHeight;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template, mensajes=chat_mensajes)

@app.route('/enviar', methods=['POST'])
def enviar():
    msg = request.form.get('mensaje')
    if msg:
        # Guardamos el mensaje (en un sistema real usaríamos el nombre del usuario logueado)
        chat_mensajes.append({"user": "Jugador", "texto": msg})
        # Limitamos a los últimos 15 mensajes para no saturar
        if len(chat_mensajes) > 15: chat_mensajes.pop(0)
    return home()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
