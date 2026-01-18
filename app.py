import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Diseño Cristal Blanco y Azul - Versión Roberto Pierre
html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Imperio Romano - Roberto Pierre</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --cristal: rgba(255, 255, 255, 0.8); }
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
            border-radius: 25px; padding: 25px; width: 90%; max-width: 450px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center;
            animation: float 5s ease-in-out infinite;
        }
        @keyframes float { 0%, 100% {transform: translateY(0);} 50% {transform: translateY(-10px);} }
        .btn-hero { 
            background: var(--azul); color: white; border: none; padding: 12px; 
            width: 100%; border-radius: 12px; font-weight: bold; margin-top: 10px; 
            cursor: pointer; font-size: 16px;
        }
        #watermark {
            position: fixed; bottom: 15px; left: 15px; background: rgba(0,123,255,0.1);
            color: var(--azul); padding: 8px 12px; border-radius: 10px;
            font-weight: bold; font-size: 12px; border: 1px solid var(--azul);
        }
        .reto-box { 
            margin-top: 15px; padding: 10px; border: 2px dashed #dc3545; 
            color: #dc3545; background: #fff1f0; display: none; border-radius: 10px; font-weight: bold; 
        }
    </style>
</head>
<body>
    <div id="intro">
        <h1 style="font-size: 4em;">🏛️</h1>
        <h2>SISTEMA VITAL ACTUALIZADO</h2>
        <button class="btn-hero" style="width: 200px; background: gold; color: black;" onclick="entrar()">¡ENTRAR!</button>
    </div>

    <div id="watermark">Roberto Pierre - Diseño Clave</div>

    <div class="glass-card" style="margin-top: 50px;">
        <h2 style="color: var(--azul);">Buscador 🔍</h2>
        <input type="text" id="bus" style="width:100%; padding:10px; border-radius:10px; border:1px solid #ddd; box-sizing: border-box;" placeholder="Busca en Wikipedia...">
        <button class="btn-hero" onclick="buscar()">BUSCAR INFO E IMAGEN</button>
        <div id="res-txt" style="margin-top:10px; font-size: 14px; text-align: left;"></div>
        <img id="search-img" style="width: 100%; border-radius: 15px; margin-top: 10px; display: none;">
    </div>

    <div class="glass-card">
        <h2 style="color: var(--azul);">Pregunta <span id="num">1</span>/30</h2>
        <p id="pregunta" style="font-weight: bold; font-size: 18px;"></p>
        <div id="opciones"></div>
        <div id="reto" class="reto-box"></div>
    </div>

    <script>
        function entrar() { document.getElementById('intro').style.transform = 'translateY(-100%)'; }

        async function buscar() {
            const t = document.getElementById('bus').value;
            const txt = document.getElementById('res-txt');
            const img = document.getElementById('search-img');
            txt.innerHTML = "Buscando...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(t)}`);
                const d = await r.json();
                txt.innerHTML = d.extract || "No se encontró nada.";
                if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = 'block'; }
                else { img.style.display = 'none'; }
            } catch(e) { txt.innerHTML = "Error de red."; }
        }

        const trivia = [
            {q: "¿Cómo conservaban los romanos la carne?", a: "Salazón y Humo", ops: ["Hielo", "Salazón y Humo", "Azúcar"]},
            {q: "¿Qué idioma hablaban los romanos?", a: "Latín", ops: ["Latín", "Griego", "Italiano"]},
            {q: "¿Quién fue el primer emperador?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"]},
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

        let idx = 0;
        function cargar() {
            const d = trivia[idx];
            document.getElementById('num').innerText = idx + 1;
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            const rTxt = document.getElementById('reto');
            cont.innerHTML = ""; rTxt.style.display = "none";

            // Lógica para mezclar opciones (Aleatorio real)
            const mezcla = [...d.ops].sort(() => Math.random() - 0.5);

            mezcla.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero'; b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) {
                        b.style.background = "#28a745";
                        setTimeout(() => { idx++; if(idx < 30) cargar(); else alert("¡VICTORIA TOTAL ROBERTO!"); }, 800);
                    } else {
                        b.style.background = "#dc3545";
                        rTxt.innerText = "RETO: ¡Escribe 10 veces 'Perdí' en una hoja!";
                        rTxt.style.display = "block";
                    }
                };
                cont.appendChild(b);
            });
        }
        window.onload = cargar;
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(html_template)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
        
