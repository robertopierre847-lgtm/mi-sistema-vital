from flask import Flask, render_template_string

app = Flask(__name__)

diseno_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital: Imperio Romano Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; font-family: 'Quicksand', sans-serif;
            background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
            display: flex; flex-direction: column; align-items: center; padding: 20px;
        }
        .card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.4);
            border-radius: 25px; padding: 25px; width: 100%; max-width: 420px;
            margin-bottom: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.05);
            text-align: center;
        }
        h2 { color: #1976d2; margin-bottom: 15px; }
        .btn {
            background: #1976d2; color: white; border: none; padding: 12px;
            border-radius: 15px; width: 100%; cursor: pointer; font-weight: 600;
            margin-bottom: 10px; transition: 0.3s;
        }
        .btn-romano, .btn-quiz { background: #64b5f6; font-size: 0.9em; }
        .btn-romano:hover, .btn-quiz:hover { background: #1976d2; transform: scale(1.02); }
        .ia-box {
            text-align: left; background: white; padding: 15px; border-radius: 15px;
            margin-top: 15px; border-left: 5px solid #1976d2; font-size: 14px;
        }
        .img-ia { width: 100%; border-radius: 20px; margin-top: 10px; display: none; box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
        #karma-bubble {
            position: fixed; top: 20px; right: 20px; width: 60px; height: 60px;
            background: #1976d2; color: white; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; font-size: 20px; z-index: 1000;
        }
        .quiz-option {
            background: #e3f2fd; color: #1976d2; border: 1px solid #bbdefb;
            padding: 10px; margin-bottom: 8px; border-radius: 10px; cursor: pointer;
            text-align: left; transition: background 0.2s;
        }
        .quiz-option:hover { background: #bbdefb; }
        .quiz-feedback { margin-top: 10px; font-weight: bold; }
    </style>
</head>
<body>

    <div id="karma-bubble">0</div>

    <div class="card">
        <h2>IA Cariñosa Visual ❤️</h2>
        <input type="text" id="iaInput" style="width:100%; padding:12px; border-radius:15px; border:2px solid #bbdefb; margin-bottom:10px;" placeholder="Busca 'Coliseo', 'Gladiador'...">
        <button class="btn" onclick="consultarIA(document.getElementById('iaInput').value)">Ver Imagen Real</button>
        <div id="iaRes" class="ia-box" style="display:none;"></div>
        <img id="iaImg" class="img-ia" src="" alt="Resultado visual">
    </div>

    <div class="card">
        <h2>Museo del Imperio Romano 🏛️</h2>
        <p>Toca para ver cómo preservaban sus alimentos con imágenes reales:</p>
        <button class="btn btn-romano" onclick="consultarIA('Salazón romana')">🥩 Conservación con Sal</button>
        <button class="btn btn-romano" onclick="consultarIA('Garum salsa romana')">🐟 El Garum (Salsa Real)</button>
        <button class="btn btn-romano" onclick="consultarIA('Nivariae o pozo de nieve romano')">❄️ Pozos de Nieve</button>
        <button class="btn btn-romano" onclick="consultarIA('Ánfora romana')">🏺 Almacenamiento en Ánforas</button>
    </div>

    <div class="card">
        <h2>Trivia Romana: ¿Cuánto sabes? ⚔️</h2>
        <p id="quiz-question"></p>
        <div id="quiz-options"></div>
        <p id="quiz-feedback" class="quiz-feedback"></p>
        <button class="btn btn-quiz" onclick="nextQuestion()" id="next-quiz-btn" style="display:none;">Siguiente Pregunta</button>
    </div>

    <script>
        let karma = 0;
        function updateKarma(points) {
            karma += points;
            document.getElementById('karma-bubble').innerText = karma;
        }

        async function consultarIA(tema) {
            if(!tema) return;
            let resDiv = document.getElementById('iaRes');
            let img = document.getElementById('iaImg');
            
            resDiv.style.display = "block";
            resDiv.innerHTML = "Buscando la imagen más clara para ti, tesoro... ✨";
            img.style.display = "none";

            try {
                const res = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${tema}`);
                const data = await res.json();
                
                if(data.extract) {
                    resDiv.innerHTML = `<b>Mi cielo, aquí tienes información sobre ${tema}:</b><br>${data.extract}`;
                    // Intenta cargar la imagen original, si no, busca una alternativa en el 'thumbnail'
                    if(data.originalimage && data.originalimage.source) {
                        img.src = data.originalimage.source;
                        img.style.display = "block";
                    } else if (data.thumbnail && data.thumbnail.source) {
                        img.src = data.thumbnail.source;
                        img.style.display = "block";
                    } else {
                        img.style.display = "none"; // No hay imagen disponible
                    }
                    updateKarma(10);
                } else {
                    resDiv.innerHTML = "No encontré esa imagen o información específica, vida mía. ¿Intentamos con otro nombre?";
                    img.style.display = "none";
                }
            } catch (error) {
                console.error("Error al consultar IA:", error);
                resDiv.innerHTML = "Hubo un pequeño error de conexión, mi vida. Intenta de nuevo más tarde.";
                img.style.display = "none";
            }
        }

        // Lógica del Juego de Trivia Romana
        const quizQuestions = [
            {
                question: "¿Quién fue el primer emperador romano?",
                options: ["Julio César", "Augusto", "Nerón"],
                answer: "Augusto"
            },
            {
                question: "¿Cómo llamaban los romanos a la sopa de pescado fermentado?",
                options: ["Panem", "Vinum", "Garum"],
                answer: "Garum"
            },
            {
                question: "¿Dónde se celebraban las luchas de gladiadores?",
                options: ["En el Panteón", "En el Coliseo", "En el Foro Romano"],
                answer: "En el Coliseo"
            }
        ];
        let currentQuestionIndex = 0;

        function displayQuestion() {
            const q = quizQuestions[currentQuestionIndex];
            document.getElementById('quiz-question').innerText = q.question;
            const optionsDiv = document.getElementById('quiz-options');
            optionsDiv.innerHTML = '';
            q.options.forEach((option, index) => {
                const btn = document.createElement('div');
                btn.className = 'quiz-option';
                btn.innerText = String.fromCharCode(65 + index) + ". " + option; // A. Opcion
                btn.onclick = () => checkAnswer
                
