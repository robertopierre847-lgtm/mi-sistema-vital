import os
from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Imperio Romano - Roberto Pierre</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --rojo: #dc3545; --cristal: rgba(255, 255, 255, 0.85); }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #bbdefb 100%);
            background-attachment: fixed;
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }
        #intro {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--azul); color: white; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: 0.8s; text-align: center;
        }
        .glass-card {
            background: var(--cristal); backdrop-filter: blur(15px);
            border-radius: 30px; padding: 25px; width: 90%; max-width: 450px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.6);
            box-shadow: 0 20px 40px rgba(0, 123, 255, 0.15); text-align: center;
        }

        /* BARRA DE BUSCAR CRISTAL CON SOMBRA AZUL AL CLICAR */
        input[type="text"] {
            width: 100%; padding: 12px; border-radius: 15px;
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.7);
            box-sizing: border-box; outline: none;
            color: #333; font-weight: bold;
            transition: 0.3s ease;
        }
        input[type="text"]:focus {
            box-shadow: 0 0 15px rgba(0, 123, 255, 0.5);
            border: 1px solid var(--azul);
        }

        #meme-win {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0);
            z-index: 10000; width: 300px; height: 300px; background: white;
            border-radius: 20px; border: 8px solid #ffcc00; overflow: hidden;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: flex; justify-content: center; align-items: center;
        }
        #meme-win.show { transform: translate(-50%, -50%) scale(1); }
        #meme-win img { width: 100%; height: 100%; object-fit: contain; }

        .btn-hero { 
            background: var(--azul); color: white; border: none; padding: 14px; 
            width: 100%; border-radius: 15px; font-weight: bold; margin-top: 10px; cursor: pointer;
        }
        #t-bar-cont { width: 100%; height: 8px; background: #eee; border-radius: 10px; margin: 10px 0; overflow: hidden; }
        #t-bar { width: 100%; height: 100%; background: var(--azul); transition: 1s linear; }
        #watermark { position: fixed; bottom: 20px; left: 20px; background: white; color: var(--azul); padding: 10px; border-radius: 10px; font-weight: bold; border: 2px solid var(--azul); font-size: 12px; }
        .reto-box { margin-top: 15px; padding: 15px; border: 3px dashed var(--rojo); color: var(--rojo); display: none; border-radius: 15px; font-weight: bold; }
    </style>
</head>
<body>
    <div id="intro">
        <h1>🏛️</h1>
        <h2>SISTEMA VITAL ACTUALIZADO</h2>
        <button class="btn-hero" style="width: 200px; background: gold; color: black;" onclick="entrar()">¡EMPEZAR!</button>
    </div>

    <div id="meme-win"><img id="meme-img" src=""></div>
    <div id="watermark">ROBERTO PIERRE</div>

    <div class="glass-card" style="margin-top: 70px;">
        <h3 style="color: var(--azul); margin-top:0;">Buscador 🔍</h3>
        <input type="text" id="bus" onkeypress="if(event.key==='Enter') buscar()" placeholder="Busca en los archivos...">
        <button class="btn-hero" onclick="buscar()">CONSULTAR</button>
        <div id="res-txt" style="font-size: 12px; margin-top: 10px; text-align: left;"></div>
    </div>

    <div class="glass-card">
        <div style="font-weight: bold; color: var(--rojo);">⏱️ <span id="segundos">15</span>s</div>
        <div id="t-bar-cont"><div id="t-bar"></div></div>
        <p id="pregunta" style="font-weight: bold; font-size: 18px;"></p>
        <div id="opciones"></div>
        <div id="reto" class="reto-box"></div>
    </div>

    <script>
        let idx = 0; let tiempo = 15; let reloj;
        const memes = [
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXF4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxx7S9xm0BW/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXF4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/S8BllEizYv8s/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXF4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/10YqOasfL05hO8/giphy.gif"
        ];

        function entrar() { document.getElementById('intro').style.transform = 'translateY(-100%)'; cargar(); }
        function iniciarReloj() {
            clearInterval(reloj); tiempo = 15;
            reloj = setInterval(() => {
                tiempo--; document.getElementById('segundos').innerText = tiempo;
                document.getElementById('t-bar').style.width = (tiempo/15*100) + "%";
                if(tiempo <= 0) { clearInterval(reloj); fallar(); }
            }, 1000);
        }
        function mostrarMeme() {
            const m = document.getElementById('meme-win');
            document.getElementById('meme-img').src = memes[Math.floor(Math.random()*memes.length)];
            m.classList.add('show');
            setTimeout(() => { m.classList.remove('show'); }, 1500);
        }
        function fallar() {
            document.getElementById('reto').innerText = "RETO: ¡Escribe 10 veces 'Perdí'!";
            document.getElementById('reto').style.display = "block";
        }
        async function buscar() {
            const t = document.getElementById('bus').value;
            const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(t)}`);
            const d = await res.json();
            document.getElementById('res-txt').innerText = d.extract || "No hay info.";
        }

        const trivia = [
            {q: "¿Cómo conservaban los romanos la carne?", a: "Salazón y Humo", ops: ["Hielo", "Salazón y Humo", "Azúcar"]},
            {q: "¿Qué idioma hablaban los romanos?", a: "Latín", ops: ["Latín", "Griego", "Italiano"]},
            {q: "¿Quién fue el primer emperador romano?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"]},
            {q: "¿Qué animal amamantó a Rómulo y Remo?", a: "Loba", ops: ["Osa", "Loba", "Leona"]},
            {q: "¿Dónde luchaban los gladiadores?", a: "Coliseo", ops: ["Teatro", "Coliseo", "Circo"]},
            {q: "¿Cómo llamaban al Mar Mediterráneo?", a: "Mare Nostrum", ops: ["Mar Azul", "Mare Nostrum", "Mar Grande"]},
            {q: "¿Qué llevaban los ciudadanos romanos?", a: "Toga", ops: ["Toga", "Capa", "Túnica"]},
            {q: "¿Qué volcán destruyó Pompeya?", a: "Vesubio", ops: ["Etna", "Vesubio", "Teide"]},
            {q: "¿Qué transportaba agua?", a: "Acueductos", ops: ["Canales", "Acueductos", "Tuberías"]},
            {q: "¿Quién usó elefantes en la guerra?", a: "Aníbal", ops: ["César", "Aníbal", "Atila"]},
            {q: "¿Cuál era la moneda de plata?", a: "Denario", ops: ["Euro", "Denario", "Dracma"]},
            {q: "¿Cómo se llamaba la plaza principal?", a: "Foro", ops: ["Plaza", "Foro", "Ágora"]},
            {q: "¿Quién era el dios del rayo?", a: "Júpiter", ops: ["Marte", "Júpiter", "Neptuno"]},
            {q: "¿Qué material usaban para construir?", a: "Hormigón", ops: ["Acero", "Hormigón", "Ladrillo"]},
            {q: "¿Cómo se llamaba el jefe de 100 soldados?", a: "Centurión", ops: ["General", "Centurión", "Cabo"]},
            {q: "¿En qué país está la ciudad de Roma?", a: "Italia", ops: ["España", "Italia", "Francia"]},
            {q: "¿Qué eran las termas?", a: "Baños públicos", ops: ["Cárceles", "Baños públicos", "Escuelas"]},
            {q: "¿Cómo se llamaban los soldados?", a: "Legionarios", ops: ["Caballeros", "Legionarios", "Gladiadores"]},
            {q: "¿Quién conquistó las Galias?", a: "Julio César", ops: ["Nerón", "Julio César", "Trajano"]},
            {q: "¿Cuántas colinas tenía Roma?", a: "Siete", ops: ["Cinco", "Siete", "Diez"]},
            {q: "¿Qué hacían en el Circo Máximo?", a: "Carreras de carros", ops: ["Teatro", "Carreras de carros", "Luchas"]},
            {q: "¿Cómo se llamaba la familia rica?", a: "Patricios", ops: ["Plebeyos", "Patricios", "Esclavos"]},
            {q: "¿Qué sistema hubo antes del Imperio?", a: "República", ops: ["Reino", "República", "Dictadura"]},
            {q: "¿Cómo se llama el río de Roma?", a: "Tíber", ops: ["Nilo", "Tíber", "Ebro"]},
            {q: "¿Qué emperador fue filósofo?", a: "Marco Aurelio", ops: ["Nerón", "Marco Aurelio", "Tito"]},
            {q: "¿Cómo conservaban frutas?", a: "Miel", ops: ["Sal", "Miel", "Hielo"]},
            {q: "¿Qué usaban para escribir?", a: "Estilo y cera", ops: ["Bolígrafo", "Estilo y cera", "Lápiz"]},
            {q: "¿Qué dios era el de la guerra?", a: "Marte", ops: ["Júpiter", "Marte", "Plutón"]},
            {q: "¿Quién fue el último emperador?", a: "Rómulo Augústulo", ops: ["Augusto", "Rómulo Augústulo", "Constantino"]},
            {q: "¿Qué ciudad era la rival de Roma?", a: "Cartago", ops: ["Atenas", "Cartago", "Esparta"]}
        ];

        function cargar() {
            if(idx >= trivia.length) { document.getElementById('pregunta').innerText = "¡VICTORIA TOTAL ROBERTO PIERRE!"; return; }
            const d = trivia[idx];
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            cont.innerHTML = ""; document.getElementById('reto').style.display = "none";
            iniciarReloj();
            [...d.ops].sort(()=>Math.random()-0.5).forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero'; b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) { clearInterval(reloj); b.style.background = "#28a745"; mostrarMeme(); setTimeout(() => { idx++; cargar(); }, 1600); }
                    else { clearInterval(reloj); b.style.background = "var(--rojo)"; fallar(); }
                };
                cont.appendChild(b);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(html_template)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
