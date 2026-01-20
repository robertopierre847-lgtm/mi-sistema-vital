import os
from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Desafío Vital - Roberto Pierre</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --azul: #007bff; --rojo: #dc3545; --verde: #28a745; --cristal: rgba(255, 255, 255, 0.95); 
        }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #f0f8ff 0%, #bbdefb 100%);
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }
        .glass-card {
            background: var(--cristal); border-radius: 20px; padding: 20px; width: 90%; max-width: 450px;
            margin: 10px 0; border: 1px solid #e0e0e0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }
        .btn-hero { 
            background: var(--azul); color: white; border: none; padding: 12px; 
            width: 100%; border-radius: 10px; font-weight: bold; margin-top: 8px; cursor: pointer;
        }
        /* RANGOS */
        .rango-badge {
            font-weight: 900; padding: 8px 20px; border-radius: 5px; color: white;
            text-transform: uppercase; display: inline-block; margin-bottom: 10px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5); font-size: 14px;
        }
        .bronce { background: #cd7f32; }
        .plata { background: #c0c0c0; }
        .oro { background: #ffd700; color: #333; }
        .platino { background: #00ced1; }
        .diamante { background: #b9f2ff; color: #333; }
        .heroico { background: #ff4500; }
        .gran-maestro { background: #8a2be2; box-shadow: 0 0 15px #8a2be2; }

        #res-img { width: 100%; border-radius: 10px; margin-top: 10px; display: none; border: 2px solid var(--azul); }
        .reto-box { margin-top: 15px; padding: 15px; border: 2px solid var(--rojo); color: var(--rojo); display: none; border-radius: 10px; font-weight: bold; background: #fff5f5; }
        input { width: 100%; padding: 12px; border-radius: 10px; border: 1px solid var(--azul); outline: none; box-sizing: border-box; }
    </style>
</head>
<body>

    <div class="glass-card">
        <h3 style="color: var(--azul); margin: 0 0 10px 0;">🔍 Buscador con Imágenes</h3>
        <input type="text" id="bus" placeholder="Busca salud, deporte, comida...">
        <button class="btn-hero" onclick="buscar()">CONSULTAR</button>
        <img id="res-img" src="" alt="Resultado">
        <p id="res-txt" style="font-size: 13px; color: #444; margin-top: 10px;"></p>
    </div>

    <div class="glass-card">
        <div id="game-ui">
            <div id="badge" class="rango-badge bronce">BRONCE I</div>
            <div style="color: var(--azul); font-weight: bold; margin-bottom: 10px;">NIVEL: <span id="num">1</span>/10</div>
            <h2 id="pregunta" style="font-size: 17px; margin: 10px 0;"></h2>
            <div id="opciones"></div>
            <div id="reto" class="reto-box"></div>
        </div>
        <div id="win-ui" style="display:none;">
            <h1 style="color: var(--azul);">🏆 ¡GRAN MAESTRO!</h1>
            <button class="btn-hero" onclick="location.reload()">REINICIAR</button>
        </div>
    </div>

    <script>
        async function buscar() {
            const q = document.getElementById('bus').value;
            const t = document.getElementById('res-txt');
            const img = document.getElementById('res-img');
            if(!q) return;
            t.innerText = "Buscando...";
            img.style.display = "none";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(q)}`);
                const d = await r.json();
                t.innerText = d.extract || "No hay resultados.";
                if(d.thumbnail) {
                    img.src = d.thumbnail.source;
                    img.style.display = "block";
                }
            } catch(e) { t.innerText = "Error de conexión."; }
        }

        let current = 0;
        const preguntas = [
            {q: "¿Qué mejora la memoria?", a: "Leer", o: ["Dormir poco", "Leer", "Ver redes"], ex: "5 Sentadillas", r: "BRONCE I", c: "bronce"},
            {q: "¿Es vital desayunar?", a: "Sí", o: ["No", "Sí", "Dá igual"], ex: "5 Flexiones", r: "PLATA II", c: "plata"},
            {q: "¿Litros de agua al día?", a: "2 Litros", o: ["Medio", "2 Litros", "10 Litros"], ex: "10 Saltos", r: "ORO III", c: "oro"},
            {q: "¿Qué es procrastinar?", a: "Posponer", o: ["Avanzar", "Posponer", "Dormir"], ex: "10 Abdominales", r: "PLATINO IV", c: "platino"},
            {q: "¿Mejor para estudiar?", a: "Hacer pausas", o: ["No parar", "Hacer pausas", "Música alta"], ex: "Estiramiento 15s", r: "DIAMANTE I", c: "diamante"},
            {q: "¿Fruta con Vitamina C?", a: "Naranja", o: ["Pan", "Naranja", "Carne"], ex: "Equilibrio 10s", r: "DIAMANTE IV", c: "diamante"},
            {q: "¿Ayuda a los nervios?", a: "Respirar", o: ["Correr", "Respirar", "Gritar"], ex: "5 Burpees", r: "HEROICO", c: "heroico"},
            {q: "¿El sol nos da Vitamina...?", a: "D", o: ["A", "D", "B12"], ex: "20 Saltos", r: "HEROICO II", c: "heroico"},
            {q: "¿Caminar es bueno?", a: "Sí, mucho", o: ["No", "Sí, mucho", "Es malo"], ex: "Plancha 15s", r: "ELITE", c: "heroico"},
            {q: "¿Clave del éxito?", a: "Disciplina", o: ["Suerte", "Disciplina", "Esperar"], ex: "Baile de victoria", r: "GRAN MAESTRO", c: "gran-maestro"}
        ];

        function cargarPregunta() {
            if(current >= preguntas.length) {
                document.getElementById('game-ui').style.display = "none";
                document.getElementById('win-ui').style.display = "block";
                return;
            }
            const p = preguntas[current];
            const badge = document.getElementById('badge');
            document.getElementById('num').innerText = current + 1;
            document.getElementById('pregunta').innerText = p.q;
            badge.innerText = p.r;
            badge.className = "rango-badge " + p.c;
            document.getElementById('reto').style.display = "none";
            const ops = document.getElementById('opciones');
            ops.innerHTML = "";
            p.o.forEach(opt => {
                const b = document.createElement('button');
                b.className = "btn-hero"; b.innerText = opt;
                b.onclick = () => {
                    if(opt === p.a) { current++; cargarPregunta(); }
                    else {
                        document.getElementById('reto').innerHTML = "📉 BAJASTE DE RANGO <br>PENITENCIA: " + p.ex;
                        document.getElementById('reto').style.display = "block";
                        if(current > 0) current--;
                        setTimeout(cargarPregunta, 3000);
                    }
                };
                ops.appendChild(b);
            });
        }
        cargarPregunta();
    </script>
</body>
</html>
