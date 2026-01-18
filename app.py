import os
from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roma Imperial: El Desafío de los 30</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --rojo: #dc3545; --verde: #28a745; --cristal: rgba(255, 255, 255, 0.85); }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffffff, #bbdefb);
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }
        #intro {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--azul); color: white; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: 0.8s; text-align: center;
        }
        .glass {
            background: var(--cristal); backdrop-filter: blur(10px);
            border-radius: 25px; padding: 25px; width: 90%; max-width: 450px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center;
        }
        .btn-hero { background: var(--azul); color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: bold; margin-top: 10px; cursor: pointer; transition: 0.3s; }
        .btn-wrong { background: var(--rojo) !important; transform: scale(0.95); }
        .btn-correct { background: var(--verde) !important; transform: scale(1.05); }
        #am-mini { position: fixed; bottom: 15px; right: 15px; width: 80px; height: 80px; z-index: 1000; filter: drop-shadow(0 5px 10px rgba(0,0,0,0.3)); }
        .reto-box { margin-top: 15px; padding: 15px; border: 2px dashed var(--rojo); color: var(--rojo); background: #fff1f0; display: none; border-radius: 10px; font-weight: bold; }
    </style>
</head>
<body>
    <div id="intro">
        <h1 style="font-size: 3em;">🏛️</h1>
        <h2>¿ESTÁS LISTO PARA LAS 30 PREGUNTAS?</h2>
        <button class="btn-hero" style="width: 250px; background: gold; color: black;" onclick="entrar()">¡SÍ, ALL MIGHT!</button>
    </div>

    <div id="am-mini">
        <img src="https://images.fineartamerica.com/images/artworkimages/mediumlarge/3/all-might-my-hero-academia-andrea-matsumoto.jpg" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 3px solid white;">
    </div>

    <div class="glass">
        <h2 style="color: var(--azul);">Pregunta <span id="num-q">1</span> de 30 ⚔️</h2>
        <p id="pregunta" style="font-weight: bold; font-size: 1.1em; min-height: 50px;"></p>
        <div id="opciones"></div>
        <div id="reto-escolar" class="reto-box"></div>
    </div>

    <script>
        const trivia = [
            {q: "¿Cómo conservaban los romanos la carne por meses?", a: "Salazón y Humo", ops: ["Neveras de piedra", "Salazón y Humo", "Hielo"]},
            {q: "¿Qué usaban para conservar las frutas dulces?", a: "Miel", ops: ["Sal", "Miel", "Vinagre"]},
            {q: "¿Qué idioma era el oficial en Roma?", a: "Latín", ops: ["Griego", "Latín", "Italiano"]},
            {q: "¿Quién fue amamantado por una loba?", a: "Rómulo y Remo", ops: ["César", "Rómulo y Remo", "Augusto"]},
            {q: "¿Cómo se llamaba el gran anfiteatro de Roma?", a: "Coliseo", ops: ["Panteón", "Circo", "Coliseo"]},
            {q: "¿Qué llevaban los ciudadanos romanos?", a: "Toga", ops: ["Toga", "Pantalón", "Capa"]},
            {q: "¿Qué transportaba agua a las ciudades?", a: "Acueductos", ops: ["Tuberías", "Acueductos", "Carros"]},
            {q: "¿Cómo se llamaba la moneda de plata?", a: "Denario", ops: ["Euro", "Denario", "Dracma"]},
            {q: "¿Quién era el dios del rayo y padre de todos?", a: "Júpiter", ops: ["Marte", "Júpiter", "Neptuno"]},
            {q: "¿En qué país actual está la ciudad de Roma?", a: "Italia", ops: ["Francia", "Italia", "España"]},
            {q: "¿Qué volcán enterró la ciudad de Pompeya?", a: "Vesubio", ops: ["Etna", "Vesubio", "Teide"]},
            {q: "¿Cómo se llamaban los soldados de una legión?", a: "Legionarios", ops: ["Caballeros", "Legionarios", "Gladiadores"]},
            {q: "¿Quién fue el primer emperador romano?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"]},
            {q: "¿Qué nombre le daban al Mar Mediterráneo?", a: "Mare Nostrum", ops: ["Mar Grande", "Mare Nostrum", "Mar Azul"]},
            {q: "¿Cuál era el castigo de los 10 soldados?", a: "Diezmo", ops: ["Multa", "Diezmo", "Exilio"]},
            {q: "¿Qué unidad militar tenía unos 5000 hombres?", a: "Legión", ops: ["Legión", "Centuria", "Cohorte"]},
            {q: "¿Qué dios era el protector de la guerra?", a: "Marte", ops: ["Júpiter", "Marte", "Plutón"]},
            {q: "¿Cómo se llamaba la plaza principal de la ciudad?", a: "Foro", ops: ["Foro", "Mercado", "Estadio"]},
            {q: "¿Qué técnica usaban para sus suelos decorados?", a: "Mosaico", ops: ["Pintura", "Mosaico", "Tapiz"]},
            {q: "¿Cuántas colinas tenía la ciudad de Roma?", a: "7", ops: ["5", "7", "12"]},
            {q: "¿Cómo se llamaba el jefe de 100 soldados?", a: "Centurión", ops: ["General", "Centurión", "Cabo"]},
            {q: "¿Qué construyeron para unir todo el imperio?", a: "Calzadas", ops: ["Puentes", "Calzadas", "Túneles"]},
            {q: "¿Quién cruzó los Alpes con elefantes?", a: "Aníbal", ops: ["César", "Aníbal", "Atila"]},
            {q: "¿Dónde se hacían las carreras de carros?", a: "Circo Máximo", ops: ["Coliseo", "Circo Máximo", "Teatro"]},
            {q: "¿Qué material inventaron para construir?", a: "Hormigón", ops: ["Hormigón", "Acero", "Plástico"]},
            {q: "¿Cómo se llamaban los esclavos que luchaban?", a: "Gladiadores", ops: ["Gladiadores", "Legionarios", "Pretorianos"]},
            {q: "¿Quién conquistó las Galias?", a: "Julio César", ops: ["Julio César", "Nerón", "Trajano"]},
            {q: "¿Qué bebían habitualmente mezclado con agua?", a: "Vino", ops: ["Cerveza", "Vino", "Leche"]},
            {q: "¿Qué periodo siguió a la monarquía?", a: "República", ops: ["Imperio", "República", "Dictadura"]},
            {q: "¿Qué emperador construyó una gran muralla en Britania?", a: "Adriano", ops: ["Adriano", "Trajano", "Tito"]}
        ];

        let index = 0;
        function entrar() { document.getElementById('intro').style.transform = 'translateY(-100%)'; hablar("¡Plus Ultra! ¡Resuelve las 30 preguntas!"); }
        
        function hablar(t) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(t);
            u.lang = 'es-ES'; u.pitch = 0.8; window.speechSynthesis.speak(u);
        }

        function cargar() {
            const d = trivia[index];
            document.getElementById('num-q').innerText = index + 1;
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            const reto = document.getElementById('reto-escolar');
            cont.innerHTML = ""; reto.style.display = "none";

            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero'; b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) {
                        b.classList.add('btn-correct');
                        hablar("¡Correcto! ¡Sigue así!");
                        setTimeout(() => { 
                            index++; 
                            if(index < 30) cargar(); 
                            else { 
                                document.getElementById('trivia-box').innerHTML = "<h2>🏆 ¡ERES EL REY DE ROMA! 🏆</h2>";
                                hablar("¡Has superado el entrenamiento! ¡Felicidades!");
                            }
                        }, 1200);
                    } else {
                        b.classList.add('btn-wrong');
                        hablar("¡Fallaste! Cumple tu reto.");
                        reto.innerText = "RETO ESCOLAR: Escribe en una hoja 10 veces: 'Debo aprender más historia de Roma para ser un héroe'.";
                        reto.style.display = "block";
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
    
