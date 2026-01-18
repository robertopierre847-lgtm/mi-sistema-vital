from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roma Plus Ultra: 30 Retos de All Might</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root { --azul: #007bff; --rojo: #dc3545; --verde: #28a745; }
        body {
            margin: 0; font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding-bottom: 50px;
        }
        .intro-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--azul); color: white; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: 0.8s;
        }
        .glass {
            background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px);
            border-radius: 25px; padding: 25px; width: 90%; max-width: 450px;
            margin: 20px 0; border: 1px solid rgba(255,255,255,0.5);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center;
        }
        .btn-hero { background: var(--azul); color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: bold; margin-top: 10px; cursor: pointer; transition: 0.3s; }
        .btn-wrong { background: var(--rojo) !important; animation: shake 0.3s; }
        .btn-correct { background: var(--verde) !important; }
        @keyframes shake { 0%, 100% {transform: translateX(0);} 25% {transform: translateX(-5px);} 75% {transform: translateX(5px);} }
        .reto-caja { margin-top: 15px; padding: 15px; border: 2px dashed var(--rojo); color: var(--rojo); font-size: 14px; display: none; background: rgba(255,0,0,0.05); }
    </style>
</head>
<body>

    <div id="intro" class="intro-screen">
        <h1 style="font-size: 3em;">🏛️</h1>
        <h2>30 RETOS DEL IMPERIO</h2>
        <button class="btn-hero" style="width: 250px; background: white; color: var(--azul);" onclick="entrar()">¡ACEPTAR EL DESAFÍO!</button>
    </div>

    <div class="glass" id="trivia-box">
        <h2 style="color: var(--azul);">Pregunta <span id="num-q">1</span>/30 ⚔️</h2>
        <p id="pregunta" style="font-weight: bold; font-size: 1.1em;"></p>
        <div id="opciones"></div>
        <div id="reto-escolar" class="reto-caja"></div>
    </div>

    <script>
        function entrar() {
            document.getElementById('intro').style.transform = 'translateY(-100%)';
            hablar("¡Ya estoy aquí! 30 preguntas te separan de la gloria. ¡Plus Ultra!");
        }

        function hablar(msj) {
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(msj);
            u.lang = 'es-ES'; u.pitch = 0.7; u.rate = 0.9;
            window.speechSynthesis.speak(u);
        }

        const trivia = [
            {q: "¿Cómo conservaban los romanos la carne y el pescado?", a: "Salazón y Humo", ops: ["Neveras de piedra", "Salazón y Humo", "Solo con agua"]},
            {q: "¿Qué usaban para conservar frutas por mucho tiempo?", a: "Miel", ops: ["Azúcar", "Miel", "Sal"]},
            {q: "¿Qué idioma hablaban los romanos?", a: "Latín", ops: ["Latín", "Griego", "Italiano"]},
            {q: "¿Cuál era el nombre del mercado principal de Roma?", a: "Foro", ops: ["Foro", "Ágora", "Plaza"]},
            {q: "¿Quién fue el primer emperador de Roma?", a: "Augusto", ops: ["Julio César", "Augusto", "Nerón"]},
            {q: "¿Cómo llamaban a los soldados de élite?", a: "Pretorianos", ops: ["Pretorianos", "Gladiadores", "Centuriones"]},
            {q: "¿Qué construcción llevaba agua a las ciudades?", a: "Acueductos", ops: ["Puentes", "Acueductos", "Tuberías"]},
            {q: "¿En qué península está Roma?", a: "Itálica", ops: ["Ibérica", "Itálica", "Balcánica"]},
            {q: "¿Qué animal amamantó a Rómulo y Remo?", a: "Una loba", ops: ["Una osa", "Una loba", "Una cabra"]},
            {q: "¿Cuál era el espectáculo más famoso del Coliseo?", a: "Lucha de Gladiadores", ops: ["Teatro", "Carreras de barcos", "Lucha de Gladiadores"]},
            {q: "¿Cómo se llamaba la prenda de vestir de los ciudadanos?", a: "Toga", ops: ["Túnica corta", "Toga", "Pantalón"]},
            {q: "¿Cuál era la unidad principal del ejército?", a: "Legión", ops: ["Legión", "Batallón", "Horda"]},
            {q: "¿Qué ciudad destruyó Roma en las Guerras Púnicas?", a: "Cartago", ops: ["Atenas", "Cartago", "Alejandría"]},
            {q: "¿Qué volcán destruyó Pompeya?", a: "Vesubio", ops: ["Etna", "Vesubio", "Teide"]},
            {q: "¿Cómo se llamaba el padre de los dioses romanos?", a: "Júpiter", ops: ["Zeus", "Júpiter", "Marte"]},
            {q: "¿Qué camino famoso llegaba a Roma?", a: "Vía Appia", ops: ["Vía Appia", "Ruta de la seda", "Calle Mayor"]},
            {q: "¿Quién cruzó los Alpes con elefantes?", a: "Aníbal", ops: ["Aníbal", "Escipión", "César"]},
            {q: "¿Cómo llamaban los romanos al Mar Mediterráneo?", a: "Mare Nostrum", ops: ["Mar Azul", "Mare Nostrum", "Mar Magno"]},
            {q: "¿Qué material inventaron para sus grandes edificios?", a: "Hormigón romano", ops: ["Ladrillo hueco", "Hormigón romano", "Acero"]},
            {q: "¿En qué año se fundó Roma según la leyenda?", a: "753 a.C.", ops: ["100 d.C.", "753 a.C.", "500 a.C."]},
            {q: "¿Cuántas colinas tenía Roma?", a: "7", ops: ["5", "7", "12"]},
            {q: "¿Cómo se llamaba la plaza donde luchaban los carros?", a: "Circo Máximo", ops: ["Circo Máximo", "Anfiteatro", "Estadio"]},
            {q: "¿Qué dios era el de la guerra?", a: "Marte", ops: ["Marte", "Apolo", "Neptuno"]},
            {q: "¿Qué hacían los romanos para divertirse en el agua?", a: "Termas", ops: ["Surf", "Termas", "Pesca"]},
            {q: "¿Cuál era el castigo máximo en el ejército?", a: "Diezmo", ops: ["Multa", "Diezmo", "Cárcel"]},
            {q: "¿Qué emperador fue famoso por incendiar Roma?", a: "Nerón", ops: ["Nerón", "Trajano", "Tito"]},
            {q: "¿Cómo se llamaba la parte de la casa al aire libre?", a: "Atrio", ops: ["Cocina", "Atrio", "Balcón"]},
            {q: "¿Qué usaban para escribir en tablas de madera?", a: "Estilo", ops: ["Pluma", "Estilo", "Lápiz"]},
            {q: "¿Quién fue el general que conquistó las Galias?", a: "Julio César", ops: ["Ciro", "Julio César", "Pompeyo"]},
            {q: "¿Qué sistema de gobierno tuvo Roma antes del Imperio?", a: "República", ops: ["República", "Dictadura", "Tribus"]}
        ];
        
        let index = 0;

        function cargarTrivia() {
            const d = trivia[index];
            document.getElementById('num-q').innerText = index + 1;
            document.getElementById('pregunta').innerText = d.q;
            const cont = document.getElementById('opciones');
            const reto = document.getElementById('reto-escolar');
            cont.innerHTML = "";
            reto.style.display = "none";

            d.ops.forEach(o => {
                const b = document.createElement('button');
                b.className = 'btn-hero'; b.innerText = o;
                b.onclick = () => {
                    if(o === d.a) {
                        b.classList.add('btn-correct');
                        hablar("¡Sublime! ¡Avanza, joven héroe!");
                        setTimeout(() => { 
                            index++; 
                            if(index < trivia.length) cargarTrivia();
                            else { 
                                document.getElementById('trivia-box').innerHTML = "<h2>¡HAS CONQUISTADO ROMA! 🏆</h2><p>Eres un verdadero Símbolo de la Paz e Historia.</p>";
                                hablar("¡Felicidades! ¡Has ido más allá de tus límites!");
                            }
                        }, 1500);
                    } else {
                        b.classList.add('btn-wrong');
                        hablar("¡Fallaste! El castigo escolar te espera.");
                        const retos = [
                            "RETO: Escribe 10 veces en una hoja: 'Debo estudiar más para ser un héroe'.",
                            "RETO: Explica a alguien en tu casa cómo conservaban los romanos la carne.",
                            "RETO: Haz 5 sentadillas por cada respuesta incorrecta.",
                            "RETO: Escribe en una hoja los nombres de 3 dioses romanos."
                        ];
                        reto.innerText = retos[Math.floor(Math.random()*retos.length)];
                        reto.style.display = "block";
                    }
                };
                cont.appendChild(b);
            });
        }
        window.onload = cargarTrivia;
    </script>
</body>
</html>
