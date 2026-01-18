import os
import random
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
        :root { --azul: #007bff; --cristal: rgba(255, 255, 255, 0.75); }
        
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
            transition: 1s ease-in-out; text-align: center;
        }

        .glass-card {
            background: var(--cristal);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 30px;
            padding: 25px;
            width: 90%; max-width: 450px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 20px 50px rgba(0, 123, 255, 0.1);
            animation: float 5s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        .btn-hero {
            background: var(--azul); color: white; border: none;
            padding: 12px; width: 100%; border-radius: 12px;
            font-weight: bold; cursor: pointer; transition: 0.3s;
            margin-top: 10px; font-size: 16px;
        }

        #watermark {
            position: fixed; bottom: 20px; right: 20px;
            background: rgba(0, 123, 255, 0.2);
            color: #007bff; padding: 10px 15px;
            border-radius: 15px; font-weight: bold;
            border: 1px solid #007bff; backdrop-filter: blur(5px);
            font-size: 14px; z-index: 1000;
        }

        .reto-text { color: #dc3545; font-weight: bold; margin-top: 15px; display: none; padding: 10px; border: 2px dashed #dc3545; border-radius: 10px; }
    </style>
</head>
<body>

    <div id="intro">
        <h1 style="font-size: 60px; margin: 0;">🏛️</h1>
        <h2>¡SISTEMA VITAL ROMANO!</h2>
        <button class="btn-hero" style="width: 200px; background: #ffcc00; color: #000;" onclick="entrar()">¡ENTRAR!</button>
    </div>

    <div id="watermark">Roberto Pierre</div>

    <div class="glass-card" style="margin-top: 40px;">
        <h2 style="color: var(--azul); margin-top: 0;">Buscador 🔍</h2>
        <input type="text" id="bus" style="width:100%; padding:12px; border-radius:10px; border:1px solid #ddd; box-sizing: border-box;" placeholder="Busca en Wikipedia...">
        <button class="btn-hero" onclick="buscar()">BUSCAR</button>
        <div id="res-txt" style="margin-top:15px; font-size: 14px; text-align: left;"></div>
        <img id="search-img" style="width: 100%; border-radius: 15px; margin-top: 15px; display: none;">
    </div>

    <div class="glass-card">
        <h2 style="color: var(--azul); margin-top: 0;">Pregunta <span id="num">1</span>/30</h2>
        <p id="pregunta" style="font-weight: bold; font-size: 17px;"></p>
        <div id="opciones"></div>
        <div id="reto" class="reto-text"></div>
    </div>

    <script>
        function entrar() {
            document.getElementById('intro').style.transform = 'translateY(-100%)';
            hablar("Sistema actualizado. Lógica de juego activada.");
        }

        function hablar(t) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(t);
            u.lang = 'es-ES'; u.rate = 0.9;
            window.speechSynthesis.speak(u);
        }

        async function buscar() {
            const t = document.getElementById('bus').value;
            const txt = document.getElementById('res-txt');
            const img = document.getElementById('search-img');
            txt.innerHTML = "Buscando...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(t)}`);
                const d = await r.json();
                txt.innerHTML = d.extract || "No encontré nada.";
                if(d.thumbnail) { img.src = d.thumbnail.source; img.style.display = 'block'; }
                else { img.style.display = 'none'; }
            } catch(e) { txt.innerHTML = "Error."; }
        }

        const preguntas = [
            {q: "¿Cómo conservaban los romanos la carne?", a: "Salazón y Humo", ops: ["Hielo", "Salazón y Humo", "Azúcar"]},
            {q: "¿Qué idioma hablaban los romanos?", a: "Latín", ops: ["Latín", "Griego", "Italiano"]},
            {q: "¿Quién fue el primer emperador romano?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"]},
            {q: "¿Qué animal amamantó a Rómulo y Remo?", a: "Loba", ops: ["Osa", "Loba", "Leona"]},
            {q: "¿Dónde luchaban los gladiadores?", a: "Coliseo", ops: ["Teatro", "Coliseo", "Circo"]},
            {q: "¿Cómo llamaban al Mar Mediterráneo?", a: "Mare Nostrum", ops: ["Mar Azul", "Mare Nostrum", "Mar Grande"]},
            {q: "¿Qué llevaban los ciudadanos romanos?", a: "Toga", ops: ["Toga", "Capa", "Túnica"]},
            {q: "¿Qué volcán destruyó Pompeya?", a: "Vesubio", ops: ["Etna", "Vesubio", "Teide"]},
            {q: "¿Qué transportaba agua a las ciudades?", a: "Acueductos", ops: ["Canales", "Acueductos", "Tuberías"]},
            {q: "¿Quién cruzó los Alpes con elefantes?", a: "Aníbal", ops: ["César", "Aníbal", "Atila"]},
            {q: "¿Cuál era la moneda de plata?", a: "Denario", ops: ["Euro", "Denario", "Dracma"]},
            {q: "¿Cómo se llamaba la plaza principal?", a: "Foro", ops: ["Plaza", "Foro", "Ágora"]},
            {q: "¿Quién fue el dios del rayo?", a: "Júpiter", ops: ["Marte", "Júpiter", "Neptuno"]},
            {q: "¿Qué material inventaron para construir?", a: "Hormigón", ops: ["Acero", "Hormigón", "Ladrillo"]},
            {q: "¿Cómo se llamaba el jefe de 100 soldados?", a: "Centurión", ops: ["General", "Centurión", "Cabo"]},
            {q: "¿Qué país actual es la cuna de Roma?", a: "Italia", ops: ["España", "Italia", "Francia"]},
            {q: "¿Qué hacían para divertirse con agua?", a: "Termas", ops: ["Piscinas", "Termas", "Duchas"]},
            {q: "¿Qué animal usaba Aníbal en guerra?", a: "Elefante", ops: ["Caballo", "Elefante", "Camello"]},
            {q: "¿Cómo llamaban a los soldados?", a: "Legionarios", ops: ["Caballeros", "Legionarios", "Gladiadores"]},
            {q: "¿Quién conquistó las Galias?", a: "Julio César", ops: ["Nerón", "Julio César", "Trajano"]},
            {q: "¿Qué prenda NO usaban los hombres?", a: "Pantalones", ops: ["Togas", "Túnicas", "Pantalones"]},
            {q: "¿Qué dios era el de la guerra?", a: "Marte", ops: ["Júpiter", "Marte", "Plutón"]},
            {q: "¿Cuántas colinas tenía Roma?", a: "Siete", ops: ["Cinco", "Siete", "Diez"]},
            {q: "¿Qué hacían en el Circo Máximo?", a: "Carreras de carros", ops: ["Teatro", "Carreras de carros", "Luchas"]},
            {q: "¿Cómo se llamaba la familia rica?", a: "Patricios", ops: ["Plebeyos", "Patricios", "Esclavos"]},
            {q: "¿Qué sistema hubo antes del Imperio?", a: "República", ops: ["Reino", "República", "Dictadura"]},
            {q: "¿Cómo se llama el río de Roma?", a: "Tíber", ops: ["Nilo", "Tíber", "Ebro"]},
            {q: "¿Qué emperador fue filósofo?", a: "Marco Aurelio", ops: ["Nerón", "Marco Aurelio", "Tito"]},
            {q: "¿Cómo conservaban frutas?", a: "Miel", ops: ["Sal", "Miel", "Hielo"]},
            {q: "¿Quién fue el último emperador?", a: "Rómulo Augústulo", ops: ["Augusto", "Rómulo Augústulo", "Constantino"]}
        ];

        let index = 0;
        const retos = [
            "RETO: ¡Escribe 10 veces 'Perdí' en una hoja!",
            "RETO: ¡Haz 10 sentadillas!",
            "RETO: ¡Dibuja un casco romano rápido!",
            "RETO: ¡Escribe 10 veces 'Debo estudiar más'!"
        ];

        function shuffle(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        }

        function cargar() {
            const d = preguntas[index];
            document.getElementById('num').innerText = index + 1;
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            const rTxt = document.getElementById('reto');
            cont.innerHTML = ""; rTxt.style.display = "none";

            // Mezclar opciones para que la respuesta no esté siempre en el medio
            const opcionesMezcladas = shuffle([...d.ops]);

            opcionesMezcladas.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero';
                b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) {
                        b.style.background = "#28a745";
                        hablar("¡Excelente!");
                        setTimeout(() => { 
                            index++; 
                            if(index < preguntas.length) cargar(); 
                            else { 
                                document.getElementById('pregunta').innerText = "¡VICTORIA TOTAL ROBERTO!"; 
                                cont.innerHTML = "🏆";
                            }
                        }, 800);
                    } else {
                        b.style.background = "#dc3545";
                        hablar("Mal. Haz el reto.");
                        rTxt.innerText = retos[Math.floor(Math.random()*retos.length)];
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
