<script>
/* ====== ESTADO DEL JUEGO ====== */
let monedas = 500;
let nivel = 1;
let xp = 0;
let xpMax = 100;

let claseIdx = 0;
let clases = ["CLASE E", "CLASE D", "CLASE C", "CLASE B", "CLASE S"];

let hpJefeMax = 1000;
let hpJefe = hpJefeMax;

let armaNivel = 1;
let entrenando = false;

/* ====== UI ====== */
function actualizarHud() {
    document.getElementById("m-val").innerText = monedas;
    document.getElementById("lvl-val").innerText = nivel;
    document.getElementById("clase-val").innerText = clases[claseIdx];
}

/* ====== PANTALLAS ====== */
function abrir(id) {
    document.getElementById(id).style.display = "flex";
}
function cerrar() {
    let p = document.getElementsByClassName("pantalla");
    for (let i = 0; i < p.length; i++) {
        p[i].style.display = "none";
    }
}

/* ====== ENTRENAMIENTO ====== */
function ganar(cantidad) {
    if (entrenando) {
        alert("⏳ Espera un momento...");
        return;
    }
    entrenando = true;

    setTimeout(function () {
        entrenando = false;
    }, 8000);

    if (cantidad > 0) {
        monedas += 100;
        ganarXP(40);
        alert("💪 Buen hábito. +100 monedas");
    } else {
        monedas -= 50;
        if (monedas < 0) monedas = 0;
        alert("❌ Mal hábito. Pierdes monedas");
    }
    actualizarHud();
}

/* ====== EXPERIENCIA ====== */
function ganarXP(cant) {
    xp += cant;
    if (xp >= xpMax) {
        xp = 0;
        nivel++;
        xpMax += 50;
        alert("⬆️ SUBISTE A NIVEL " + nivel);
    }
}

/* ====== TIENDA ====== */
function comprarItem(icono, nombre, precio) {
    if (monedas < precio) {
        alert("💰 No tienes suficientes monedas");
        return;
    }
    monedas -= precio;
    armaNivel++;
    document.getElementById("slot-especial").innerText = icono;
    document.getElementById("btn-especial").style.display = "inline-block";
    alert(nombre + " adquirido");
    actualizarHud();
}

/* ====== SUBIR CLASE ====== */
function subirClase() {
    if (monedas >= 1000 && claseIdx < clases.length - 1) {
        monedas -= 1000;
        claseIdx++;
        alert("🏅 Ascendiste a " + clases[claseIdx]);
    } else {
        alert("❌ No cumples requisitos");
    }
    actualizarHud();
}

/* ====== COMBATE CONTRA JEFE ====== */
function atacarJefe(extra) {
    if (!extra) extra = 0;

    let danioJugador = Math.floor((20 * armaNivel) + extra);
    let danioJefe = Math.floor(Math.random() * 40);

    hpJefe -= danioJugador;
    monedas -= danioJefe;

    if (monedas < 0) monedas = 0;
    if (hpJefe < 0) hpJefe = 0;

    document.getElementById("jefe-hp-fill").style.width =
        (hpJefe / hpJefeMax * 100) + "%";

    actualizarHud();

    if (hpJefe === 0) {
        alert("🏆 JEFE DERROTADO\nEres un verdadero Cazador");
        ganarXP(200);
        cerrar();
        hpJefe = hpJefeMax;
    }

    if (monedas === 0) {
        alert("💀 Has sido derrotado\nRegresas a la base");
        cerrar();
        hpJefe = hpJefeMax;
    }
}

/* ====== BUSCADOR SEGURO ====== */
function buscar() {
    let q = document.getElementById("bus-input").value;
    let res = document.getElementById("wiki-res");
    if (q.length < 2) return;
    res.innerText = "Buscando...";

    fetch("https://es.wikipedia.org/api/rest_v1/page/summary/" + q)
        .then(r => r.json())
        .then(d => {
            res.innerText = d.extract || "No encontrado";
        })
        .catch(() => {
            res.innerText = "Error de conexión";
        });
}

/* ====== ANIMACIÓN SIMPLE ====== */
let energia = document.getElementById("energia");
let x = 90;
let y = 120;

setInterval(function () {
    x += 3;
    if (x > window.innerWidth - 100) x = 90;
    energia.style.left = x + "px";
}, 50);

/* ====== INIT ====== */
actualizarHud();
</script>
