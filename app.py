import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Vital - Arena de Cazadores</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Poppins:wght@300;600&display=swap" rel="stylesheet">
    <style>
        :root { 
            --azul: #00f3ff; --rojo: #ff0055; --verde: #00ff88; --oro: #ffd700; 
            --fondo: #050510; --btn-size: 14px; 
        }
        body { 
            margin: 0; background: var(--fondo); color: white; 
            font-family: 'Poppins', sans-serif; overflow-x: hidden; transition: 0.3s; 
        }
        h1, h2, h3, .orbitron { font-family: 'Orbitron', sans-serif; }

        /* --- HUD SUPERIOR --- */
        .hud { 
            position: fixed; top: 0; width: 100%; background: rgba(0,0,0,0.9); 
            padding: 10px; display: flex; justify-content: space-around; 
            border-bottom: 2px solid var(--azul); z-index: 1000; font-size: 11px;
        }

        /* --- BUSCADOR (1) --- */
        .buscador-container {
            margin-top: 70px; padding: 20px; width: 90%; max-width: 500px;
            background: rgba(255,255,255,0.05); border-radius: 15px;
            border: 1px solid var(--azul); margin-left: auto; margin-right: auto;
            position: relative; z-index: 10;
        }
        input { 
            width: 70%; padding: 10px; border-radius: 5px; border: 1px solid var(--azul);
            background: rgba(0,0,0,0.5); color: white;
        }

        /* --- MAPA E ISLAS (2) --- */
        .mapa { height: 80vh; position: relative; display: flex; justify-content: center; align-items: center; z-index: 10; }
        .isla { 
            position: absolute; width: 130px; height: 85px; background: rgba(0,0,0,0.8);
            border: 2px solid var(--azul); border-radius: 15px; display: flex;
            flex-direction: column; align-items: center; justify-content: center;
            cursor: pointer; transition: 0.3s; text-align: center; font-size: 12px;
        }
        .isla:hover { transform: scale(1.1); box-shadow: 0 0 20px var(--azul); }
        
        #base { top: 10%; border-color: var(--oro); }
        #entrenar { left: 10%; top: 40%; border-color: var(--verde); }
        #calabozo { right: 10%; top: 40%; border-color: var(--rojo); }
        #mochila-icon { bottom: 10%; left: 20%; width: 60px; height: 60px; border-radius: 50%; }
        #ajustes-icon { bottom: 10%; right: 20%; width: 60px; height: 60px; border-radius: 50%; }

        /* --- PANTALLAS --- */
        .pantalla { 
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.98); z-index: 2000; flex-direction: column;
            align-items: center; justify-content: center; text-align: center;
        }
        .btn-game { 
            padding: var(--btn-size); margin: 10px; border: none; border-radius: 8px;
            font-family: 'Orbitron'; cursor: pointer; font-weight: bold;
        }

        /* --- JEFE --- */
        #jefe-hp-bar { width: 250px; height: 15px; background: #333; border: 1px solid red; margin: 15px; }
        #jefe-hp-fill { height: 100%; background: red; width: 100%; transition: 0.3s; }

        /* --- INVENTARIO --- */
        .grid-items { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .item-slot { width: 70px; height: 70px; border: 1px dashed var(--azul); display: flex; align-items: center; justify-content: center; font-size: 25px; }

        /* --- 新增动画样式 --- */
        .soldado{
            position:absolute;
            width:40px;
            height:40px;
            border-radius:50%;
            z-index: 5;
        }
        #soldadoBueno{
            background:#22c55e;
            left:50px;
            bottom:100px;
        }
        #soldadoMalo{
            background:#ef4444;
            right:200px;
            bottom:120px;
            transition:0.5s;
        }

        /* BOLA DE ENERGÍA */
        #energia{
            position:absolute;
            width:20px;
            height:20px;
            border-radius:50%;
            background:#38bdf8;
            box-shadow:0 0 20px #38bdf8;
            left:90px;
            bottom:120px;
            z-index: 5;
        }

        /* COLISEO SIMBÓLICO */
        #coliseo{
            position:absolute;
            right:60px;
            bottom:50px;
            display:grid;
            grid-template-columns:repeat(4,30px);
            gap:5px;
            z-index: 5;
        }
        .bloque{
            width:30px;
            height:30px;
            background:#facc15;
            transition:0.6s;
        }
    </style>
</head>
<body>

    <!-- 新增动画元素 -->
    <div id="soldadoBueno" class="soldado"></div>
    <div id="soldadoMalo" class="soldado"></div>
    <div id="energia"></div>
    <div id="coliseo">
        <div class="bloque"></div><div class="bloque"></div>
        <div class="bloque"></div><div class="bloque"></div>
        <div class="bloque"></div><div class="bloque"></div>
        <div class="bloque"></div><div class="bloque"></div>
    </div>

    <div class="hud">
        <div>💰 <span id="m-val">500</span></div>
        <div class="orbitron" style="color:var(--rojo)">🏹 <span id="clase-val">CLASE E</span></div>
        <div class="orbitron" style="color:var(--oro)">LVL <span id="lvl-val">1</span></div>
    </div>

    <div class="buscador-container">
        <h3 class="orbitron" style="color:var(--azul); margin:0 0 10px 0;">1. BUSCADOR VITAL</h3>
        <input type="text" id="bus-input" placeholder="Ej: Meditación...">
        <button class="btn-game" style="background:var(--azul); margin:0;" onclick="buscar()">Wiki</button>
        <p id="wiki-res" style="font-size:11px; margin-top:10px; color:#ccc;"></p>
    </div>

    <div class="mapa">
        <div class="isla" id="base" onclick="abrir('p-base')">🏰 <b>LA BASE</b><small>Tienda</small></div>
        <div class="isla" id="entrenar" onclick="abrir('p-entrenar')">🏋️ <b>ENTRENO</b><small>+ Monedas</small></div>
        <div class="isla" id="calabozo" onclick="abrir('p-jefe')">👹 <b>CALABOZO</b><small>Jefe Final</small></div>
        
        <div class="isla" id="mochila-icon" onclick="abrir('p-mochila')">🎒</div>
        <div class="isla" id="ajustes-icon" onclick="abrir('p-ajustes')">⚙️</div>
    </div>

    <div id="p-base" class="pantalla">
        <h1 class="orbitron" style="color:var(--oro)">LA BASE CENTRAL</h1>
        <button class="btn-game" style="background:var(--rojo); color:white;" onclick="subirClase()">SUBIR A CLASE S (1000 Mo)</button>
        <button class="btn-game" style="background:var(--azul)" onclick="comprarItem('⚡', 'Súper Láser', 300)">SÚPER LÁSER (300 Mo)</button>
        <button class="btn-game" onclick="cerrar()">SALIR</button>
    </div>

    <div id="p-jefe" class="pantalla">
        <h2 class="orbitron" style="color:var(--rojo)">BOSS: EL DESTRUCTOR</h2>
        <div id="jefe-img" style="font-size:100px;">👹</div>
        <div id="jefe-hp-bar"><div id="jefe-hp-fill"></div></div>
        <button class="btn-game" style="background:var(--rojo); color:white;" onclick="atacarJefe()">ATAQUE SÓNICO</button>
        <button class="btn-game" id="btn-especial" style="display:none; background:var(--azul)" onclick="atacarJefe(100)">USAR LÁSER</button>
        <button onclick="cerrar()" style="background:none; color:white; border:none;">HUIR</button>
    </div>

    <div id="p-mochila" class="pantalla">
        <h1 class="orbitron">INVENTARIO</h1>
        <div class="grid-items">
            <div class="item-slot">🗡️</div>
            <div class="item-slot" id="slot-especial">空</div>
            <div class="item-slot">空</div>
        </div>
        <button class="btn-game" onclick="cerrar()">CERRAR</button>
    </div>

    <div id="p-ajustes" class="pantalla">
        <h1 class="orbitron">AJUSTES</h1>
        <p>Tamaño de Controles:</p>
        <button class="btn-game" onclick="setBtnSize('12px')">PEQUEÑO</button>
        <button class="btn-game" onclick="setBtnSize('22px')">GRANDE</button>
        <button class="btn-game" onclick="cerrar()" style="background:var(--verde)">GUARDAR</button>
    </div>

    <div id="p-entrenar" class="pantalla">
        <h1 class="orbitron">SALA DE ENTRENAMIENTO</h1>
        <p>¿Qué te da Súper Fuerza?</p>
        <button class="btn-game" style="background:var(--verde)" onclick="ganar(100)">Comer Sano</button>
        <button class="btn-game" style="background:var(--rojo)" onclick="ganar(0)">Golosinas</button>
        <button onclick="cerrar()">VOLVER</button>
    </div>

    <script>
        let monedas = 500;
        let claseIdx = 0;
        let clases = ["CLASE E", "CLASE D", "CLASE C", "CLASE B", "CLASE S", "NACIONAL"];
        let hpJefe = 1000;
        let armaLvl = 1;

        function abrir(id) { document.getElementById(id).style.display = 'flex'; }
        function cerrar() { document.querySelectorAll('.pantalla').forEach(p => p.style.display = 'none'); }

        async function buscar() {
            const q = document.getElementById('bus-input').value;
            const res = document.getElementById('wiki-res');
            if(!q) return;
            res.innerText = "Buscando datos...";
            try {
                const r = await fetch(`https://es.wikipedia.org/api/rest_v1/page/summary/${q}`);
                const d = await r.json();
                res.innerText = d.extract || "No hallado.";
            } catch(e) { res.innerText = "Error de red."; }
        }

        function ganar(cant) {
            if(cant > 0) {
                monedas += cant;
                actualizarHud();
                alert("¡Entrenamiento completado! +100 Mo.");
            } else { alert("Mal hábito. No ganas monedas."); }
        }

        function comprarItem(icon, nombre, precio) {
            if(monedas >= precio) {
                monedas -= precio;
                document.getElementById('slot-especial').innerText = icon;
                document.getElementById('btn-especial').style.display = 'inline-block';
                actualizarHud();
                alert(nombre + " añadido a la mochila.");
            } else { alert("Monedas insuficientes."); }
        }

        function subirClase() {
            if(monedas >= 1000 && claseIdx < clases.length - 1) {
                monedas -= 1000;
                claseIdx++;
                actualizarHud();
                alert("¡Rango de Cazador actualizado!");
            } else { alert("Faltan monedas o eres Rango Máximo."); }
        }

        function atacarJefe(bonus = 0) {
            let danio = (25 * armaLvl) + bonus;
            hpJefe -= danio;
            if(hpJefe < 0) hpJefe = 0;
            document.getElementById('jefe-hp-fill').style.width = (hpJefe/10) + "%";
            
            // Subir nivel de arma por usarla
            armaLvl += 0.1;
            document.getElementById('lvl-val').innerText = Math.floor(armaLvl);

            if(hpJefe <= 0) {
                alert("¡CALABOZO CONQUISTADO! Eres una Leyenda.");
                cerrar();
            }
        }

        function setBtnSize(s) { document.documentElement.style.setProperty('--btn-size', s); }

        function actualizarHud() {
            document.getElementById('m-val').innerText = monedas;
            document.getElementById('clase-val').innerText = clases[claseIdx];
        }

        // --- 新增动画脚本 ---
        let energia = document.getElementById("energia");
        let enemigo = document.getElementById("soldadoMalo");
        let bloques = document.querySelectorAll(".bloque");

        let x = 90;
        let y = 120;
        let fase = 1;

        let animacion = setInterval(()=>{
            if(fase === 1){
                x += 6;
                y += 2;
                energia.style.left = x+"px";
                energia.style.bottom = y+"px";

                if(x > window.innerWidth - 300){
                    fase = 2;
                    enemigo.style.opacity = "0.3";
                }
            }

            if(fase === 2){
                x += 4;
                y -= 2;
                energia.style.left = x+"px";
                energia.style.bottom = y+"px";

                if(x > window.innerWidth - 120){
                    fase = 3;
                    bloques.forEach(b=>{
                        b.style.transform="scale(0)";
                        b.style.opacity="0";
                    });
                    energia.style.transform="scale(3)";

               
