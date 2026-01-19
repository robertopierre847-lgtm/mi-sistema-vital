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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Cinzel:wght@700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --rojo: #dc3545; --cristal: rgba(255, 255, 255, 0.85); --oro: #ffcc00; }
        
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #bbdefb 100%);
            background-attachment: fixed;
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
            overflow-x: hidden;
        }

        /* --- ANIMACIÓN DE INTRODUCCIÓN ÉPICA --- */
        #intro {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle, #1a1a1a 0%, #000 100%);
            color: white; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: 1s cubic-bezier(0.7, 0, 0.3, 1); text-align: center;
            overflow: hidden;
        }

        /* Partículas de ceniza/fuego */
        .particle {
            position: absolute; background: rgba(255, 100, 0, 0.6);
            border-radius: 50%; pointer-events: none;
            animation: rise 4s infinite linear;
        }
        @keyframes rise {
            0% { transform: translateY(100vh) scale(0); opacity: 1; }
            100% { transform: translateY(-10vh) scale(1.5); opacity: 0; }
        }

        .title-epic {
            font-family: 'Cinzel', serif; font-size: 2.5rem;
            color: var(--oro); text-shadow: 0 0 20px rgba(255, 204, 0, 0.6);
            animation: glow 2s infinite alternate; margin-bottom: 5px;
        }
        @keyframes glow { from { opacity: 0.8; transform: scale(1); } to { opacity: 1; transform: scale(1.05); } }

        /* Efecto de Sacudida al hacer click */
        .shake { animation: shake-anim 0.5s cubic-bezier(.36,.07,.19,.97) both; }
        @keyframes shake-anim {
            10%, 90% { transform: translate3d(-1px, 0, 0); }
            20%, 80% { transform: translate3d(2px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
            40%, 60% { transform: translate3d(4px, 0, 0); }
        }

        /* Luces de fondo del juego */
        .bg-circle {
            position: fixed; width: 300px; height: 300px; border-radius: 50%;
            filter: blur(80px); z-index: -1; animation: move 10s infinite alternate;
        }
        .c1 { background: rgba(0, 123, 255, 0.3); top: 10%; left: 10%; }
        .c2 { background: rgba(0, 255, 255, 0.2); bottom: 10%; right: 10%; animation-delay: -5s; }
        @keyframes move { from { transform: translate(0,0); } to { transform: translate(50px, 100px); } }

        .glass-card {
            background: var(--cristal); backdrop-filter: blur(15px);
            border-radius: 30px; padding: 25px; width: 90%; max-width: 450px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.6);
            box-shadow: 0 20px 40px rgba(0, 123, 255, 0.15); text-align: center;
            position: relative; z-index: 10;
        }

        .btn-hero { 
            background: var(--azul); color: white; border: none; padding: 14px; 
            width: 100%; border-radius: 15px; font-weight: bold; margin-top: 10px; cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: 0.3s;
        }
        .btn-hero:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,123,255,0.4); }

        #meme-win {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0);
            z-index: 10000; width: 280px; height: 280px; background: white;
            border-radius: 20px; border: 6px solid gold; overflow: hidden;
            transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #meme-win.show { transform: translate(-50%, -50%) scale(1); }
        #meme-win img { width: 100%; height: 100%; object-fit: cover; }

        #t-bar-cont { width: 100%; height: 8px; background: #eee; border-radius: 10px; margin: 10px 0; overflow: hidden; }
        #t-bar { width: 100%; height: 100%; background: var(--azul); transition: 1s linear; }
        #watermark { position: fixed; bottom: 20px; left: 20px; background: white; color: var(--azul); padding: 10px; border-radius: 10px; font-weight: bold; border: 2px solid var(--azul); font-size: 11px; z-index: 100; }
        .reto-box { margin-top: 15px; padding: 15px; border: 3px dashed var(--rojo); color: var(--rojo); display: none; border-radius: 15px; font-weight: bold; }
    </style>
</head>
<body>
    <div id="intro">
        <h1 style="font-size: 50px; margin: 0;">🦅</h1>
        <h2 class="title-epic">ROMA: SISTEMA VITAL</h2>
        <p style="color: #ccc; letter-spacing: 2px;">EL DESAFÍO DE ROBERTO PIERRE</p>
        <button class="btn-hero" style="width: 220px; background: var(--oro); color: black;" onclick="iniciarConEfecto()">EMPEZAR GLORIA</button>
    </div>

    <div class="bg-circle c1"></div>
    <div class="bg-circle c2"></div>
    <div id="meme-win"><img id="meme-img" src=""></div>
    <div id="watermark">ROBERTO PIERRE</div>

    <div class="glass-card" style="margin-top: 70px;">
        <h3 style="color: var(--azul); margin-top:0;">Buscador 🔍</h3>
        <input type="text" id="bus" onkeypress="if(event.key==='Enter') buscar()" placeholder="Investiga aquí...">
        <button class="btn-hero" onclick="buscar()">CONSULTAR</button>
        <div id="res-txt" style="font-size: 13px; margin-top: 10px; text-align: left;"></div>
        <img id="search-img" src="" style="width: 100%; border-radius: 15px; margin-top: 15px; display: none;">
    </div>

    <div class="glass-card">
        <div id="rango-txt" style="font-size: 12px; color: var(--azul); font-weight: bold;">Rango: Plebeyo</div>
        <div style="font-weight: bold; color: var(--rojo);">⏱️ <span id="segundos">15</span>s | <span id="num-pregunta">1</span>/30</div>
        <div id="t-bar-cont"><div id="t-bar"></div></div>
        <p id="pregunta" style="font-weight: bold; font-size: 18px; margin: 15px 0;"></p>
        <div id="opciones"></div>
        <div id="reto" class="reto-box"></div>
    </div>

    <script>
        // Crear partículas de ceniza
        const intro = document.getElementById('intro');
        for (let i = 0; i < 30; i++) {
            let p = document.createElement('div');
            p.className = 'particle';
            p.style.left = Math.random() * 100 + 'vw';
            p.style.width = p.style.height = Math.random() * 5 + 3 + 'px';
            p.style.animationDelay = Math.random() * 4 + 's';
            intro.appendChild(p);
        }

        let idx = 0; let tiempo = 15; let reloj;
        const memesAcierto = [
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXF4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxx7S9xm0BW/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNndicm9ueXF4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l41lTfuxmS0U87Q9G/giphy.gif"
        ];

        function iniciarConEfecto() {
            document.body.classList.add('shake');
            setTimeout(() => {
                document.getElementById('intro').style.transform = 'scale(2)';
                document.getElementById('intro').style.opacity = '0';
                setTimeout(() => { 
                    document.getElementById('intro').style.display = 'none';
                    document.body.classList.remove('shake');
                    cargar(); 
                }, 800);
            }, 400);
        }

        function actualizarRango() {
            let r = "Plebeyo";
            if(idx > 5) r = "Soldado";
            if(idx > 12) r = "Centurión";
            if(idx > 20) r = "Senador";
            if(idx > 28) r = "Emperador";
            document.getElementById('rango-txt').innerText = "Rango: " + r;
        }

        function iniciarReloj() {
            clearInterval(reloj); tiempo = 15;
            reloj = setInterval(() => {
                tiempo--; document.getElementById('segundos').innerText = tiempo;
                document.getElementById('t-bar').style.width = (tiempo/15*100) + "%";
                if(tiempo <= 0) { clearInterval(reloj); fallar(); }
            }, 1000);
        }

        async function buscar() {
            const t = document.getElementById('bus').value;
            const resTxt = document.getElementById('res-txt');
            const resImg = document.getElementById('search-img');
            if(!t) return;
            resTxt.innerText = "Consultando archivos imperiales...";
            try {
                const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(t)}`);
                const d = await res.json();
                resTxt.innerText = d.extract || "Sin resultados.";
                if(d.thumbnail) { resImg.src = d.thumbnail.source; resImg.style.display = "block"; } 
                else { resImg.style.display = "none"; }
            } catch(e) { resTxt.innerText = "Error de conexión."; }
        }

        function mostrarMeme() {
            const m = document.getElementById('meme-win');
            document.getElementById('meme-img').src = memesAcierto[Math.floor(Math.random()*memesAcierto.length)];
            m.classList.add('show');
            setTimeout(() => { m.classList.remove('show'); }, 1400);
        }

        function fallar() {
            document.getElementById('reto').style.display = "block";
            document.getElementById('reto').innerText = "RETO: Escribe 10 veces 'Perdí' en una hoja.";
        }

        const trivia = [
            {q: "¿Primer emperador romano?", a: "Augusto", ops: ["César", "Augusto", "Nerón"]},
            {q: "¿Idioma de Roma?", a: "Latín", ops: ["Latín", "Griego", "Italiano"]},
            {q: "¿Cómo conservaban carne?", a: "Salazón", ops: ["Hielo", "Salazón", "Miel"]},
            {q: "¿Animal que crió a Rómulo?", a: "Loba", ops: ["Osa", "Loba", "Perra"]},
            {q: "¿Dónde peleaban gladiadores?", a: "Coliseo", ops: ["Teatro", "Coliseo", "Circo"]},
            {q: "¿Volcán de Pompeya?", a: "Vesubio", ops: ["Etna", "Vesubio", "Teide"]},
            {q: "¿Llevaban los ciudadanos?", a: "Toga", ops: ["Capa", "Toga", "Túnica"]},
            {q: "¿Traía agua a la ciudad?", a: "Acueducto", ops: ["Canal", "Acueducto", "Tubo"]},
            {q: "¿Dios del rayo?", a: "Júpiter", ops: ["Marte", "Júpiter", "Apolo"]},
            {q: "¿Jefe de 100 soldados?", a: "Centurión", ops: ["General", "Centurión", "Cabo"]},
            {q: "¿Río que pasa por Roma?", a: "Tíber", ops: ["Nilo", "Tíber", "Sena"]},
            {q: "¿País actual de Roma?", a: "Italia", ops: ["España", "Italia", "Grecia"]},
            {q: "¿Baños públicos romanos?", a: "Termas", ops: ["Termas", "Duchas", "Fuentes"]},
            {q: "¿Soldados de Roma?", a: "Legionarios", ops: ["Caballeros", "Legionarios", "Hoplitas"]},
            {q: "¿Conquistó las Galias?", a: "Julio César", ops: ["Nerón", "Julio César", "Tito"]},
            {q: "¿Cuántas colinas tenía Roma?", a: "Siete", ops: ["Cinco", "Siete", "Nueve"]},
            {q: "¿Carreras de carros?", a: "Circo Máximo", ops: ["Coliseo", "Circo Máximo", "Foro"]},
            {q: "¿Clase social rica?", a: "Patricios", ops: ["Plebeyos", "Patricios", "Esclavos"]},
            {q: "¿Antes del Imperio fue...?", a: "República", ops: ["Reino", "República", "Dictadura"]},
            {q: "¿Emperador filósofo?", a: "Marco Aurelio", ops: ["Trajano", "Marco Aurelio", "Nerón"]},
            {q: "¿Dios de la guerra?", a: "Marte", ops: ["Marte", "Plutón", "Baco"]},
            {q: "¿Moneda de plata?", a: "Denario", ops: ["Euro", "Denario", "Dracma"]},
            {q: "¿Plaza central?", a: "Foro", ops: ["Plaza", "Foro", "Mercado"]},
            {q: "¿Material de construcción?", a: "Hormigón", ops: ["Acero", "Hormigón", "Ladrillo"]},
            {q: "¿Último emperador?", a: "Rómulo Augústulo", ops: ["Augusto", "Rómulo Augústulo", "Tito"]},
            {q: "¿Ciudad rival?", a: "Cartago", ops: ["Atenas", "Cartago", "Esparta"]},
            {q: "¿Qué usaban para endulzar?", a: "Miel", ops: ["Azúcar", "Miel", "Sal"]},
            {q: "¿Enemigo con elefantes?", a: "Aníbal", ops: ["Atila", "Aníbal", "Jerjes"]},
            {q: "¿Diosa del amor?", a: "Venus", ops: ["Venus", "Diana", "Minerva"]},
            {q: "¿Mar de los romanos?", a: "Mare Nostrum", ops: ["Mar Rojo", "Mare Nostrum", "Mar Muerto"]}
        ];

        function cargar() {
            actualizarRango();
            if(idx >= trivia.length) { 
                document.getElementById('pregunta').innerHTML = "<h2 style='color:gold'>🏆 ¡AVE CÉSAR!</h2>Has conquistado Roma."; 
                document.getElementById('opciones').innerHTML = "<button class='btn-hero' onclick='location.reload()'>REINICIAR</button>";
                return; 
            }
            document.getElementById('num-pregunta').innerText = idx + 1;
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
