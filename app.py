<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Mi Sistema Vital</title>

<style>

/* =====================================================
   MI SISTEMA VITAL — MÁRMOL ÉLITE
   ===================================================== */

*{
    box-sizing:border-box;
    margin:0;
    padding:0;
}

:root{
    --gold:#d6ad55;
    --gold-light:#f4d98a;
    --black:#11110f;
    --white:#f8f7f3;
    --gray:#77746c;
    --glass:rgba(255,255,255,.55);
}

body{
    font-family:Georgia, "Times New Roman", serif;
    color:#24221d;
    min-height:100vh;

    background:
        linear-gradient(
            120deg,
            rgba(255,255,255,.95),
            rgba(220,218,211,.75),
            rgba(250,249,245,.95)
        );

    overflow-x:hidden;
}

/* Mármol */

body::before{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;

    background:
        repeating-linear-gradient(
            115deg,
            transparent 0px,
            transparent 90px,
            rgba(90,88,82,.07) 92px,
            transparent 95px,
            transparent 180px
        );

    opacity:.8;
}

/* =====================================================
   SPLASH
   ===================================================== */

#splash{
    position:fixed;
    inset:0;
    z-index:9999;

    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;

    background:
        radial-gradient(
            circle at center,
            #3b382f,
            #11110f 70%
        );

    color:white;

    animation:
        splashHide 1s ease 2.3s forwards;
}

.logo{
    width:100px;
    height:100px;

    border-radius:50%;

    border:2px solid var(--gold);

    display:flex;
    align-items:center;
    justify-content:center;

    font-size:42px;

    color:var(--gold-light);

    box-shadow:
        0 0 40px rgba(214,173,85,.3);

    animation:
        logoPulse 1.5s infinite;
}

#splash h1{
    margin-top:25px;
    letter-spacing:4px;
    font-size:24px;
}

#splash p{
    margin-top:10px;
    color:#aaa;
    font-family:Arial,sans-serif;
    font-size:12px;
}

/* =====================================================
   APP
   ===================================================== */

.app{
    position:relative;
    z-index:2;

    width:min(680px,100%);
    margin:auto;

    padding-bottom:110px;
}

/* =====================================================
   HEADER
   ===================================================== */

header{
    padding:30px 22px 15px;

    display:flex;
    justify-content:space-between;
    align-items:center;
}

.brand{
    font-family:Arial,sans-serif;
    font-size:10px;
    letter-spacing:4px;
    color:#8b6b29;
    font-weight:bold;
}

header h1{
    margin-top:8px;
    font-size:29px;
}

header p{
    font-family:Arial,sans-serif;
    color:var(--gray);
    font-size:13px;
    margin-top:5px;
}

.profile{
    width:48px;
    height:48px;

    border-radius:50%;

    border:1px solid rgba(170,130,50,.5);

    background:
        linear-gradient(
            145deg,
            #fff,
            #d8d5cc
        );

    font-size:20px;

    box-shadow:
        0 8px 20px rgba(0,0,0,.1);
}

/* =====================================================
   PÁGINAS
   ===================================================== */

.page{
    display:none;
    padding:10px 20px;
    animation:pageIn .5s ease;
}

.page.active{
    display:block;
}

/* =====================================================
   NIVEL
   ===================================================== */

.level-card{
    position:relative;

    padding:22px;

    border-radius:28px;

    color:white;

    background:
        linear-gradient(
            135deg,
            #292720,
            #11110f
        );

    box-shadow:
        0 18px 45px rgba(0,0,0,.25);

    overflow:hidden;
}

.level-card::after{
    content:"";
    position:absolute;

    width:180px;
    height:180px;

    right:-80px;
    top:-80px;

    border-radius:50%;

    border:1px solid rgba(214,173,85,.4);
}

.level-top{
    display:flex;
    justify-content:space-between;
}

.level-label{
    color:#b9b5a8;
    font-family:Arial,sans-serif;
    font-size:10px;
    letter-spacing:2px;
}

.level-number{
    display:block;
    color:var(--gold-light);
    font-size:38px;
    margin-top:3px;
}

.xp{
    text-align:right;
    font-family:Arial,sans-serif;
}

.xp strong{
    color:var(--gold-light);
    font-size:20px;
}

.xp span{
    display:block;
    color:#aaa;
    font-size:10px;
}

.xp-bar{
    height:7px;
    margin-top:18px;

    background:#35332e;

    border-radius:20px;
    overflow:hidden;
}

.xp-bar div{
    height:100%;
    width:0;

    background:
        linear-gradient(
            90deg,
            #a87b25,
            #f4d98a
        );

    transition:width .8s ease;
}

.xp-info{
    display:flex;
    justify-content:space-between;

    margin-top:7px;

    font-family:Arial,sans-serif;
    font-size:10px;
    color:#aaa;
}

/* =====================================================
   ESTADO VITAL
   ===================================================== */

.vital-status{
    margin-top:15px;

    background:
        rgba(255,255,255,.72);

    backdrop-filter:blur(20px);

    border:1px solid rgba(150,130,90,.22);

    border-radius:28px;

    padding:24px;

    box-shadow:
        0 12px 35px rgba(0,0,0,.08);
}

.section-title{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.section-title small{
    font-family:Arial,sans-serif;
    letter-spacing:2px;
    font-size:9px;
    color:#8b6b29;
}

.section-title h2{
    font-size:22px;
    margin-top:4px;
}

.percent{
    color:#96732d;
    font-family:Arial,sans-serif;
    font-weight:bold;
}

/* círculo */

.circle-container{
    display:flex;
    justify-content:center;
    padding:25px 0;
}

.circle{
    width:175px;
    height:175px;

    border-radius:50%;

    display:flex;
    justify-content:center;
    align-items:center;

    background:
        conic-gradient(
            var(--gold) 0deg,
            #e8e5dd 0deg
        );

    box-shadow:
        0 12px 35px rgba(120,90,20,.15);

    transition:background 1s ease;
}

.circle-inner{
    width:139px;
    height:139px;

    border-radius:50%;

    background:
        linear-gradient(
            145deg,
            #fff,
            #e5e2da
        );

    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;

    box-shadow:
        inset 0 2px 8px rgba(0,0,0,.08);
}

.circle-inner strong{
    font-size:32px;
}

.circle-inner span{
    font-family:Arial,sans-serif;
    color:#858177;
    font-size:10px;
}

/* =====================================================
   SISTEMA
   ===================================================== */

.system-title{
    margin:22px 0 12px;
}

.system-title small{
    font-family:Arial,sans-serif;
    font-size:9px;
    color:#8b6b29;
    letter-spacing:2px;
}

.system-title h2{
    margin-top:4px;
}

/* tarjetas */

.cards{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:12px;
}

.card{
    position:relative;

    min-height:170px;

    padding:18px;

    border-radius:24px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.9),
            rgba(225,222,213,.72)
        );

    border:1px solid rgba(130,110,70,.2);

    box-shadow:
        0 12px 28px rgba(0,0,0,.08);

    transition:
        transform .25s ease,
        box-shadow .25s ease;
}

.card:active{
    transform:scale(.96);
}

.card:hover{
    transform:translateY(-4px);

    box-shadow:
        0 18px 35px rgba(0,0,0,.13);
}

.card-icon{
    font-size:30px;
}

.card-label{
    display:block;

    margin-top:20px;

    font-family:Arial,sans-serif;
    font-size:9px;
    letter-spacing:1px;

    color:#777269;
}

.card h3{
    margin-top:5px;
    font-size:24px;
}

.card small{
    color:#858177;
    font-family:Arial,sans-serif;
    font-size:10px;
}

.mini-bar{
    position:absolute;
    bottom:17px;
    left:18px;
    right:18px;

    height:4px;

    background:#d3d0c8;

    border-radius:10px;
}

.mini-bar div{
    height:100%;
    width:0;

    border-radius:10px;

    background:
        linear-gradient(
            90deg,
            #9c7425,
            #e6c56f
        );

    transition:width .5s ease;
}

/* =====================================================
   MISIÓN
   ===================================================== */

.mission{
    margin-top:15px;

    padding:20px;

    border-radius:25px;

    background:
        linear-gradient(
            135deg,
            #201e19,
            #0f0f0d
        );

    color:white;

    display:flex;
    gap:14px;
    align-items:center;

    box-shadow:
        0 15px 35px rgba(0,0,0,.22);
}

.mission-icon{
    width:52px;
    height:52px;

    border-radius:17px;

    display:grid;
    place-items:center;

    background:
        linear-gradient(
            145deg,
            #b58b36,
            #624817
        );

    font-size:24px;
}

.mission-content{
    flex:1;
}

.mission-content small{
    color:#c8a957;
    font-family:Arial,sans-serif;
    font-size:9px;
    letter-spacing:1px;
}

.mission-content h3{
    margin-top:4px;
    font-size:15px;
}

.mission-content p{
    margin-top:4px;

    color:#aaa;

    font-family:Arial,sans-serif;
    font-size:10px;
}

.mission-xp{
    color:#e8c96e;
    font-family:Arial,sans-serif;
    font-weight:bold;
    font-size:11px;
}

/* =====================================================
   ESTADÍSTICAS
   ===================================================== */

.page-heading{
    padding:15px 0 20px;
}

.page-heading small{
    color:#8b6b29;
    font-family:Arial,sans-serif;
    font-size:9px;
    letter-spacing:2px;
}

.page-heading h2{
    font-size:30px;
    margin-top:6px;
}

.page-heading p{
    color:#777269;
    font-family:Arial,sans-serif;
    font-size:12px;
    margin-top:6px;
}

.stats{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:12px;
}

.stat{
    padding:20px;

    border-radius:23px;

    background:rgba(255,255,255,.75);

    border:1px solid rgba(130,110,70,.18);

    box-shadow:
        0 10px 25px rgba(0,0,0,.07);
}

.stat-icon{
    font-size:25px;
}

.stat strong{
    display:block;
    font-size:28px;
    margin-top:12px;
}

.stat small{
    color:#817d73;
    font-family:Arial,sans-serif;
    font-size:10px;
}

/* gráfico */

.chart-card{
    margin-top:15px;

    padding:20px;

    border-radius:25px;

    background:rgba(255,255,255,.72);

    border:1px solid rgba(130,110,70,.18);
}

.chart{
    height:190px;

    display:flex;
    align-items:end;

    gap:8px;

    margin-top:25px;
}

.chart div{
    flex:1;

    border-radius:8px 8px 2px 2px;

    background:
        linear-gradient(
            180deg,
            #e1bd61,
            #8f6825
        );

    animation:barUp .8s ease;
}

/* =====================================================
   MISIONES
   ===================================================== */

.mission-list{
    display:flex;
    flex-direction:column;
    gap:12px;
}

.mission-row{
    padding:18px;

    display:flex;
    align-items:center;
    gap:13px;

    border-radius:23px;

    background:rgba(255,255,255,.76);

    border:1px solid rgba(130,110,70,.18);
}

.mission-row-icon{
    width:50px;
    height:50px;

    border-radius:16px;

    display:grid;
    place-items:center;

    background:#e7e2d6;

    font-size:24px;
}

.mission-row-content{
    flex:1;
}

.mission-row-content small{
    color:#92702c;
    font-family:Arial,sans-serif;
    font-size:8px;
}

.mission-row-content h3{
    font-size:14px;
    margin-top:4px;
}

.mission-row-content p{
    font-family:Arial,sans-serif;
    color:#858177;
    font-size:10px;
    margin-top:4px;
}

.mission-row > strong{
    color:#9b762d;
    font-family:Arial,sans-serif;
    font-size:11px;
}

/* =====================================================
   NIVEL
   ===================================================== */

.level-showcase{
    text-align:center;

    padding:30px 20px;

    border-radius:30px;

    color:white;

    background:
        radial-gradient(
            circle,
            #403a2c,
            #12120f 70%
        );

    box-shadow:
        0 20px 45px rgba(0,0,0,.25);
}

.level-orb{
    width:165px;
    height:165px;

    margin:auto;

    border-radius:50%;

    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;

    border:2px solid var(--gold);

    box-shadow:
        0 0 45px rgba(214,173,85,.2);
}

.level-orb span{
    font-family:Arial,sans-serif;
    font-size:9px;
    color:#aaa;
    letter-spacing:2px;
}

.level-orb strong{
    color:#f2d27b;
    font-size:65px;
}

.level-showcase h2{
    margin-top:20px;
}

.level-showcase p{
    margin-top:8px;
    color:#aaa;
    font-family:Arial,sans-serif;
    font-size:11px;
    line-height:1.5;
}

.achievement{
    margin-top:25px;
    margin-bottom:12px;
}

.badges{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:12px;
}

.badge{
    padding:20px;

    text-align:center;

    border-radius:22px;

    background:rgba(255,255,255,.75);

    border:1px solid rgba(130,110,70,.18);

    font-size:30px;
}

.badge span{
    display:block;

    margin-top:8px;

    font-family:Arial,sans-serif;
    color:#777269;
    font-size:10px;
}

/* =====================================================
   NAVEGACIÓN
   ===================================================== */

.bottom-nav{
    position:fixed;

    z-index:100;

    bottom:15px;
    left:50%;

    transform:translateX(-50%);

    width:min(620px,calc(100% - 25px));

    padding:8px;

    border-radius:25px;

    background:
        rgba(25,24,21,.94);

    backdrop-filter:blur(20px);

    border:1px solid rgba(214,173,85,.3);

    display:flex;
    justify-content:space-around;

    box-shadow:
        0 15px 35px rgba(0,0,0,.25);
}

.nav-btn{
    border:0;
    background:none;

    color:#888;

    padding:8px 12px;

    border-radius:17px;

    font-family:Arial,sans-serif;

    transition:.2s;
}

.nav-btn span{
    display:block;
    font-size:19px;
}

.nav-btn small{
    display:block;
    margin-top:3px;
    font-size:8px;
}

.nav-btn.active{
    color:#f0d37d;

    background:
        rgba(214,173,85,.12);
}

/* =====================================================
   TOAST
   ===================================================== */

.toast{
    position:fixed;

    left:50%;
    bottom:95px;

    transform:
        translateX(-50%)
        translateY(20px);

    background:#171613;

    color:white;

    border:1px solid rgba(214,173,85,.4);

    padding:13px 20px;

    border-radius:15px;

    font-family:Arial,sans-serif;
    font-size:12px;

    opacity:0;

    pointer-events:none;

    transition:.3s;

    z-index:5000;
}

.toast.show{
    opacity:1;
    transform:
        translateX(-50%)
        translateY(0);
}

/* =====================================================
   ANIMACIONES
   ===================================================== */

@keyframes splashHide{
    to{
        opacity:0;
        visibility:hidden;
    }
}

@keyframes logoPulse{
    50%{
        transform:scale(1.06);
        box-shadow:
            0 0 65px rgba(214,173,85,.5);
    }
}

@keyframes pageIn{
    from{
        opacity:0;
        transform:translateY(15px);
    }

    to{
        opacity:1;
        transform:translateY(0);
    }
}

@keyframes barUp{
    from{
        height:0;
    }
}

/* =====================================================
   MÓVIL
   ===================================================== */

@media(max-width:420px){

    header h1{
        font-size:25px;
    }

    .cards{
        gap:9px;
    }

    .card{
        min-height:160px;
        padding:15px;
    }

    .circle{
        width:155px;
        height:155px;
    }

    .circle-inner{
        width:123px;
        height:123px;
    }

}

</style>
</head>

<body>

<!-- SPLASH -->

<div id="splash">

    <div class="logo">✦</div>

    <h1>MI SISTEMA VITAL</h1>

    <p>Tu progreso. Tu sistema.</p>

</div>


<div class="app">

<!-- =====================================================
     HEADER
     ===================================================== -->

<header>

    <div>

        <div class="brand">
            MI SISTEMA VITAL
        </div>

        <h1>Buenos días 👋</h1>

        <p>
            Hoy tienes una nueva oportunidad.
        </p>

    </div>

    <button class="profile">
        👤
    </button>

</header>


<!-- =====================================================
     INICIO
     ===================================================== -->

<section id="home" class="page active">

    <!-- NIVEL -->

    <div class="level-card">

        <div class="level-top">

            <div>

                <div class="level-label">
                    NIVEL ACTUAL
                </div>

                <strong
                    class="level-number"
                    id="level">
                    1
                </strong>

            </div>

            <div class="xp">

                <strong id="xp">
                    0
                </strong>

                <span>
                    XP
                </span>

            </div>

        </div>

        <div class="xp-bar">
            <div id="xpProgress"></div>
        </div>

        <div class="xp-info">

            <span id="xpCurrent">
                0 XP
            </span>

            <span id="xpNeeded">
                100 XP
            </span>

        </div>

    </div>


    <!-- ESTADO VITAL -->

    <div class="vital-status">

        <div class="section-title">

            <div>

                <small>
                    RESUMEN
                </small>

                <h2>
                    Estado vital
                </h2>

            </div>

            <span
                class="percent"
                id="dayPercent">
                0%
            </span>

        </div>


        <div class="circle-container">

            <div
                class="circle"
                id="circle">

                <div class="circle-inner">

                    <strong
                        id="dailyPercent">
                        0%
                    </strong>

                    <span>
                        completado
                    </span>

                </div>

            </div>

        </div>

    </div>


    <!-- SISTEMA -->

    <div class="system-title">

        <small>
            TU SISTEMA
        </small>

        <h2>
            Control diario
        </h2>

    </div>


    <div class="cards">

        <!-- AGUA -->

        <div
            class="card"
            onclick="addWater()">

            <div class="card-icon">
                💧
            </div>

            <span class="card-label">
                HIDRATACIÓN
            </span>

            <h3>
                <span id="water">
                    0
                </span>/8
            </h3>

            <small>
                vasos
            </small>

            <div class="mini-bar">
                <div id="waterBar"></div>
            </div>

        </div>


        <!-- SUEÑO -->

        <div class="card">

            <div class="card-icon">
                🌙
            </div>

            <span class="card-label">
                DESCANSO
            </span>

            <h3>
                7h 30m
            </h3>

            <small>
                objetivo diario
            </small>

            <div class="mini-bar">
                <div style="width:78%"></div>
            </div>

        </div>


        <!-- ACTIVIDAD -->

        <div class="card">

            <div class=
