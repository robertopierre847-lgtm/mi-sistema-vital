import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Codigo corregido y numerado: 1 Buscador, 2 Juego
html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital - Roberto Pierre</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --rojo: #dc3545; --verde: #28a745; }
        body { margin: 0; font-family: 'Poppins', sans-serif; background: #f0f8ff; display: flex; flex-direction: column; align-items: center; padding: 10px; }
        .card { background: white; border-radius: 20px; padding: 20px; width: 95%; max-width: 450px; margin: 10px 0; border: 1px solid #ddd; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .btn { background: var(--azul); color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: bold; margin-top: 10px; cursor: pointer; }
        .rango { font-weight: 900; padding: 8px 15px; border-radius: 5px; color: white; text-transform: uppercase; margin-bottom: 10px; display: inline-block; text-shadow: 1px 1px 2px black; }
        .bronce { background: #cd7f32; } .plata { background: #c0c0c0; } .oro { background: #ffd700; color: #333; }
        .platino { background: #00ced1; } .diamante { background: #b9f2ff; color: #333; }
        .heroico { background: #ff4500; } .maestro { background: #8a2be2; box-shadow: 0 0 10px #8a2be2; }
        #res-img { width: 100%; border-radius: 10px; margin-top: 10px; display: none; border: 2px solid var(--azul); }
        input { width: 100%; padding: 12px; border-radius: 10px; border: 1px solid var(--azul); box-sizing: border-box; outline: none; }
        .reto { margin-top: 15px; padding: 10px; border: 2px solid var(--rojo); color: var(--rojo); display: none; border-radius: 10px; font-weight: bold; background: #fff5f5; }
    </style>
</head>
<body>

    <div class="card">
        <h2 style="color: var(--azul); margin-top:0;">1. Buscador Vital</h2>
        <input type="text" id="bus" placeholder="Busca salud, nutrición o ejercicio...">
        <button class="btn" onclick="buscar()">CONSULTAR WIKIPEDIA</button>
        <img id="res-img" src="">
        <p id="res-txt" style="font-size: 13px; color: #444; margin-top: 10px;"></p>
    </div>

    <div class="card">
        <h2 style="color: var(--azul); margin-top:0;">2. Desafío de Rangos</h2>
        <div id="game-ui">
            <div id="badge" class="rango bronce">BRONCE I</div>
            <div style="font-weight: bold; color: #555;">Nivel <span id="num">1</span>/10</div>
            <h3 id="pregunta" style="font-size: 18px; color: #333;"></h3>
            <div id="opciones"></div>
            <div id="reto" class="reto"></div>
        </div>
        <div id="win-ui" style="display:none;">
            <h1 style="color: var(--verde);">🏆 ¡GRAN MAESTRO!</h1>
            <p>Has conquistado la cima de la salud vital.</p>
            <button class="btn" onclick="location.reload()">REINICIAR TEMPORADA</button>
        </div>
    </div>

    <script>
        async function buscar() {
            const q = document.getElementById('bus').value;
            const t = document.getElementById('res-txt');
            const img = document.getElementById('res-img');
            if(!q) return;
            t.innerText = "Buscando...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(q)}`);
                const d = await r.json();
                t.innerText = d.extract || "Sin resultados.";
                if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = "block"; }
                else { img.style.display = "none"; }
            } catch(e) { t.innerText = "Error de conexión."; }
        }

        let current = 0;
        const preguntas = [
            {q: "¿Qué mejora la salud mental?", a: "Dormir bien", o: ["Mucho café", "Dormir bien"], ex: "5 Sentadillas", r: "BRONCE", c: "bronce"},
            {q: "¿Es vital tomar agua?", a: "Sí", o: ["No", "Sí"], ex: "5 Flexiones", r: "PLATA", c: "plata"},
            {q: "¿Mejor fuente de energía?", a: "Frutas", o: ["Dulces", "Frutas"], ex: "10 Saltos", r: "ORO", c: "oro"},
            {q: "¿Qué es procrastinar?", a: "Posponer", o: ["Avanzar", "Posponer"], ex: "Estira 15s", r: "PLATINO", c: "platino"},
            {q: "¿Hacer ejercicio ayuda?", a: "Mucho", o: ["Nada", "Mucho"], ex: "Toca tus pies", r: "DIAMANTE", c: "diamante"},
            {q: "¿Clave para aprender?", a: "Atención", o: ["Distracción", "Atención"], ex: "5 Abdominales", r: "DIAMANTE IV", c: "diamante"},
            {q: "¿El sol da vitamina...?", a: "D", o: ["C", "D"], ex: "5 Burpees", r: "HEROICO", c: "heroico"},
            {q: "¿Leer es bueno?", a: "Sí", o: ["No", "Sí"], ex: "Gira el cuello", r: "HEROICO II", c: "heroico"},
            {q: "¿Comer sano da vida?", a: "Sí", o: ["No", "Sí"], ex: "Plancha 10s", r: "ELITE", c: "heroico"},
            {q: "¿Cuál es tu meta?", a: "Ser mejor", o: ["Rendirse", "Ser mejor"], ex: "Baile de victoria", r: "GRAN MAESTRO", c: "maestro"}
        ];

        function cargar() {
            if(current >= 10) { document.getElementById('game-ui').style.display="none"; document.getElementById('win-ui').style.display="block"; return; }
            const p = preguntas[current];
            document.getElementById('num').innerText = current + 1;
            document.getElementById('badge').innerText = p.r;
            document.getElementById('badge').className = "rango " + p.c;
            document.getElementById('pregunta').innerText = p.q;
            document.getElementById('reto').style.display = "none";
            const ops = document.getElementById('opciones'); ops.innerHTML = "";
            p.o.forEach(o => {
                const b = document.createElement('button'); b.className = "btn"; b.innerText = o;
                b.onclick = () => {
                    if(o === p.a) { current++; cargar(); }
                    else { 
                        document.getElementById('reto').innerHTML = "📉 ERROR - PENITENCIA: <br>" + p.ex; 
                        document.getElementById('reto').style.display = "block";
                        if(current > 0) current--; 
                        setTimeout(cargar, 3000); 
                    }
                };
                ops.appendChild(b);
            });
        }
        cargar();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
