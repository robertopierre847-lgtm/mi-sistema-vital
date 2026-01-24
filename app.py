from flask import Flask, render_template_string, jsonify
from flask_socketio import SocketIO, emit
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pixel_race_secret_123'

# Configuración de SocketIO optimizada para servidores públicos
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- CONFIGURACIÓN DEL JUEGO ---
CANVAS_SIZE = 100  # Matriz de 100x100
# Inicializamos el lienzo blanco
lienzo = [["#ffffff" for _ in range(CANVAS_SIZE)] for _ in range(CANVAS_SIZE)]
last_pixel_time = {} # Diccionario para controlar el tiempo por usuario

@app.route('/')
def index():
    return render_template_string(HTML_UI)

@socketio.on('paint')
def handle_paint(data):
    user_id = data.get('user_id')
    x = int(data.get('x'))
    y = int(data.get('y'))
    color = data.get('color')
    power = data.get('power', 'normal')
    
    now = time.time()
    
    # Validación de Cooldown: 3 segundos
    if user_id in last_pixel_time and now - last_pixel_time[user_id] < 3:
        return 

    if 0 <= x < CANVAS_SIZE and 0 <= y < CANVAS_SIZE:
        # Lógica de Poderes
        if power == 'normal':
            lienzo[y][x] = color
            emit('update_pixel', {'x': x, 'y': y, 'color': color}, broadcast=True)
        
        elif power == 'bomba': # Explota área de 5x5
            for i in range(y-2, y+3):
                for j in range(x-2, x+3):
                    if 0 <= i < CANVAS_SIZE and 0 <= j < CANVAS_SIZE:
                        lienzo[i][j] = color
                        emit('update_pixel', {'x': j, 'y': i, 'color': color}, broadcast=True)
        
        elif power == 'agujero': # Borra área de 7x7
            for i in range(y-3, y+4):
                for j in range(x-3, x+4):
                    if 0 <= i < CANVAS_SIZE and 0 <= j < CANVAS_SIZE:
                        lienzo[i][j] = "#ffffff"
                        emit('update_pixel', {'x': j, 'y': i, 'color': "#ffffff"}, broadcast=True)

        last_pixel_time[user_id] = now

@socketio.on('connect')
def on_connect():
    # Al conectar, enviamos el estado actual del mural al nuevo jugador
    emit('full_canvas', {'lienzo': lienzo})

# --- INTERFAZ DE USUARIO (HTML/JS) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Pixel Race: Mural del Caos</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { 
            margin: 0; background: #0b0e14; color: white; 
            font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center;
            overflow-x: hidden;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 15px; margin: 10px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            text-align: center;
        }
        canvas { 
            background: white; border-radius: 5px; cursor: crosshair;
            image-rendering: pixelated; touch-action: none;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
            max-width: 95vw; height: auto;
        }
        .controls { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; margin-top: 15px; }
        .btn {
            padding: 12px 18px; border: none; border-radius: 12px; 
            color: white; font-weight: bold; cursor: pointer; transition: 0.2s;
        }
        .btn-az { background: #007bff; }
        .btn-rs { background: #ff4da6; }
        .btn-ng { background: #333; border: 1px solid #555; }
        .active { outline: 3px solid white; transform: scale(1.1); }
        input[type="color"] { width: 50px; height: 45px; border: none; border-radius: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="glass-card">
        <h2 style="margin:0; color:#00d2ff;">Pixel Race: Mural del Caos</h2>
        <p style="font-size: 0.8em; opacity: 0.7;">1 píxel cada 3 segundos. ¡Gana la zona!</p>
        <canvas id="canvas" width="1000" height="1000"></canvas>
        
        <div class="controls">
            <input type="color" id="colorPicker" value="#ff0000">
            <button class="btn btn-az active" onclick="setPower('normal', this)">Píxel</button>
            <button class="btn btn-rs" onclick="setPower('bomba', this)">Bomba</button>
            <button class="btn btn-ng" onclick="setPower('agujero', this)">Agujero</button>
        </div>
    </div>

    <script>
        const socket = io();
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const userId = "user_" + Math.random().toString(36).substr(2, 9);
        let selectedPower = 'normal';

        function setPower(p, el) {
            selectedPower = p;
            document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            el.classList.add('active');
        }

        socket.on('full_canvas', (data) => {
            data.lienzo.forEach((row, y) => {
                row.forEach((color, x) => {
                    ctx.fillStyle = color;
                    ctx.fillRect(x * 10, y * 10, 10, 10);
                });
            });
        });

        socket.on('update_pixel', (data) => {
            ctx.fillStyle = data.color;
            ctx.fillRect(data.x * 10, data.y * 10, 10, 10);
        });

        canvas.addEventListener('mousedown', handleInput);
        canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            handleInput(e.touches[0]);
        });

        function handleInput(e) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const x = Math.floor(((e.clientX - rect.left) * scaleX) / 10);
            const y = Math.floor(((e.clientY - rect.top) * scaleY) / 10);
            const color = document.getElementById('colorPicker').value;

            socket.emit('paint', { user_id: userId, x, y, color, power: selectedPower });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    # Detecta puerto automáticamente para servidores como Render o GitHub Codespaces
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
