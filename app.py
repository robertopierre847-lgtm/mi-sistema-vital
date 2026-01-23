from flask import Flask, request, render_template_string, redirect, session, jsonify
import sqlite3, os, random, time

app = Flask(__name__)
app.secret_key = "MENTISCOPE_474_CORE_KEY"

# =========================
# SISTEMA CENTRAL
# =========================

SYSTEM_STATE = {
    "core": "ACTIVO",
    "nivel": "DIOS",
    "sistema": "VIVO",
    "evolucion": "INICIADA"
}

# =========================
# BASE DE DATOS
# =========================

DB = "mentiscope.db"

def db():
    return sqlite3.connect(DB)

def init_db():
    c = db()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        level INTEGER DEFAULT 1,
        exp INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        action TEXT,
        timestamp TEXT
    )
    """)

    c.commit()
    c.close()

init_db()

# =========================
# NUCLEO COGNITIVO
# =========================

def core_perception(text):
    score = 0
    if len(text) > 20:
        score += 10
    if "porque" in text.lower():
        score += 15
    if "siempre" in text.lower() or "nunca" in text.lower():
        score -= 10
    return score

def core_logic(score):
    if score >= 20:
        return "ALTA COHERENCIA"
    elif score >= 10:
        return "COHERENCIA MEDIA"
    else:
        return "BAJA COHERENCIA"

def core_decision(state):
    if state == "ALTA COHERENCIA":
        return "RESPUESTA CONFIABLE"
    elif state == "COHERENCIA MEDIA":
        return "RESPUESTA DUDOSA"
    else:
        return "RESPUESTA INESTABLE"

def core_learning(exp, gain):
    exp += gain
    if exp >= 100:
        return 1, exp - 100
    return 0, exp

# =========================
# AUTENTICACION
# =========================

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["user"]
        p = request.form["pass"]
        c = db()
        cur = c.cursor()
        try:
            cur.execute("INSERT INTO users(username,password) VALUES(?,?)",(u,p))
            c.commit()
        except:
            pass
        c.close()
        return redirect("/login")
    return render_template_string(REGISTER_HTML)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["user"]
        p = request.form["pass"]
        c = db()
        cur = c.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
        r = cur.fetchone()
        c.close()
        if r:
            session["user"] = u
            return redirect("/core")
    return render_template_string(LOGIN_HTML)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =========================
# NUCLEO
# =========================

@app.route("/core", methods=["GET","POST"])
def core():
    if "user" not in session:
        return redirect("/login")

    result = None
    state = None
    decision = None
    gain = 0

    if request.method == "POST":
        text = request.form.get("input","")
        score = core_perception(text)
        state = core_logic(score)
        decision = core_decision(state)

        gain = random.randint(5,15)

        c = db()
        cur = c.cursor()
        cur.execute("SELECT level,exp FROM users WHERE username=?",(session["user"],))
        lvl, exp = cur.fetchone()

        up, new_exp = core_learning(exp, gain)
        lvl += up

        cur.execute("UPDATE users SET level=?, exp=? WHERE username=?",(lvl,new_exp,session["user"]))
        cur.execute("INSERT INTO logs(user,action,timestamp) VALUES(?,?,?)",
                    (session["user"], f"ANALISIS:{decision}", str(time.time())))
        c.commit()
        c.close()

        result = score

    c = db()
    cur = c.cursor()
    cur.execute("SELECT level,exp FROM users WHERE username=?",(session["user"],))
    lvl, exp = cur.fetchone()
    c.close()

    return render_template_string(CORE_HTML,
        result=result,
        state=state,
        decision=decision,
        level=lvl,
        exp=exp,
        sys=SYSTEM_STATE
    )

# =========================
# JUEGO PRO
# =========================

WORDS = ["MENTE","LOGICA","COHERENCIA","SISTEMA","NEURONA","RAZON","ETICA","CIENCIA","ORDEN","INTELIGENCIA"]

@app.route("/game")
def game():
    w = random.choice(WORDS)
    letters = list(w)
    random.shuffle(letters)
    return jsonify({"word":w,"letters":letters})

# =========================
# FRONTEND
# =========================

REGISTER_HTML = """
<h2>Registro</h2>
<form method="post">
<input name="user" placeholder="Usuario"><br>
<input name="pass" placeholder="Clave"><br>
<button>Registrar</button>
</form>
"""

LOGIN_HTML = """
<h2>Login</h2>
<form method="post">
<input name="user" placeholder="Usuario"><br>
<input name="pass" placeholder="Clave"><br>
<button>Entrar</button>
</form>
"""

CORE_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MENTISCOPE 474 PRO</title>
<style>
body{background:#f2f7ff;font-family:Arial;margin:0;padding:20px}
.card{background:white;border-radius:15px;padding:15px;margin-bottom:15px;box-shadow:0 10px 25px rgba(0,0,0,0.1)}
button{padding:10px 15px;border:none;border-radius:10px;background:#0066ff;color:white}
input{width:100%;padding:10px;border-radius:10px;border:1px solid #aac}
.letra{display:inline-block;padding:10px;margin:5px;background:#0066ff;color:white;border-radius:8px;cursor:pointer}
</style>
</head>
<body>

<div class="card">
<h3>Estado del sistema</h3>
<p>Core: {{sys.core}}</p>
<p>Nivel: {{sys.nivel}}</p>
<p>Sistema: {{sys.sistema}}</p>
<p>Evolucion: {{sys.evolucion}}</p>
</div>

<div class="card">
<h3>Usuario: {{session.user}}</h3>
<p>Nivel: {{level}}</p>
<p>Experiencia: {{exp}} / 100</p>
</div>

<div class="card">
<h3>Nucleo Cognitivo</h3>
<form method="post">
<input name="input" placeholder="Escribe una afirmacion">
<button>Analizar</button>
</form>

{% if result %}
<p>Puntaje: {{result}}</p>
<p>Estado: {{state}}</p>
<p>Decision: {{decision}}</p>
{% endif %}
</div>

<div class="card">
<h3>Juego Cognitivo</h3>
<button onclick="loadGame()">Iniciar</button>
<p id="pista"></p>
<div id="letters"></div>
<p id="resp"></p>
</div>

<script>
let real="";
let sel="";

function loadGame(){
fetch("/game").then(r=>r.json()).then(d=>{
real=d.word;
sel="";
document.getElementById("resp").innerText="";
let l=document.getElementById("letters");
l.innerHTML="";
d.letters.forEach(x=>{
let s=document.createElement("span");
s.className="letra";
s.innerText=x;
s.onclick=()=>pick(x);
l.appendChild(s);
});
});
}

function pick(l){
sel+=l;
document.getElementById("resp").innerText=sel;
if(sel.length==real.length){
if(sel==real){
alert("Correcto");
}else{
alert("Incorrecto. Era: "+real);
}
sel="";
}
}
</script>

</body>
</html>
"""

# =========================
# RUN
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
