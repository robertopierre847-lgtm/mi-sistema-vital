from flask import Flask, request, render_template_string, jsonify, redirect, session
import requests, os, random, sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "MENTISCOPE_CORE_PRO_KEY"

DB = "core.db"

# =========================
# DATABASE
# =========================

def db():
    return sqlite3.connect(DB)

def init_db():
    con = db()
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT UNIQUE,
        password TEXT,
        role TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        query TEXT
    )""")
    con.commit()
    con.close()

init_db()

# =========================
# APIs
# =========================

def buscar_anime(q):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={q}&limit=1"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json().get("data", [])
        if not data:
            return None
        a = data[0]
        return {
            "tipo": "Anime",
            "titulo": a.get("title", ""),
            "texto": a.get("synopsis", "Sin descripción disponible."),
            "img": a.get("images", {}).get("jpg", {}).get("large_image_url", "")
        }
    except:
        return None

def buscar_wikipedia(q):
    try:
        url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{q}"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        d = r.json()
        return {
            "tipo": "Información",
            "titulo": d.get("title", ""),
            "texto": d.get("extract", "No se encontró información."),
            "img": d.get("thumbnail", {}).get("source", "")
        }
    except:
        return None

# =========================
# GAME
# =========================

PALABRAS = ["ANIME","SISTEMA","MENTE","CORE","PRO","FLASK","API","DATA","ROMA","DRAGON","NARUTO","BUSCADOR"]

@app.route("/juego")
def juego():
    palabra = random.choice(PALABRAS)
    letras = list(palabra)
    random.shuffle(letras)
    return jsonify({"palabra": palabra, "mezcla": letras})

# =========================
# AUTH
# =========================

@app.route("/")
def root():
    return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        u = request.form["user"]
        p = generate_password_hash(request.form["pass"])
        con = db()
        c = con.cursor()
        try:
            c.execute("INSERT INTO users(user,password,role) VALUES(?,?,?)",(u,p,"user"))
            con.commit()
        except:
            return "Usuario ya existe"
        return redirect("/login")
    return render_template_string(REGISTER_HTML)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u = request.form["user"]
        p = request.form["pass"]
        con = db()
        c = con.cursor()
        c.execute("SELECT password,role FROM users WHERE user=?",(u,))
        row = c.fetchone()
        if row and check_password_hash(row[0],p):
            session["user"]=u
            session["role"]=row[1]
            return redirect("/core")
        return "Login incorrecto"
    return render_template_string(LOGIN_HTML)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =========================
# CORE
# =========================

@app.route("/core")
def core():
    if "user" not in session:
        return redirect("/login")
    return render_template_string(CORE_HTML, user=session["user"], role=session["role"])

@app.route("/buscar")
def buscar():
    if "user" not in session:
        return jsonify({"error":"No autorizado"})
    q = request.args.get("q","").strip()
    if not q:
        return jsonify({"error":"Escribe algo"})
    con = db()
    c = con.cursor()
    c.execute("INSERT INTO history(user,query) VALUES(?,?)",(session["user"],q))
    con.commit()

    anime = buscar_anime(q)
    if anime:
        return jsonify(anime)
    wiki = buscar_wikipedia(q)
    if wiki:
        return jsonify(wiki)
    return jsonify({"error":"No se encontró nada"})

# =========================
# ADMIN
# =========================

@app.route("/admin")
def admin():
    if "user" not in session or session["role"]!="admin":
        return "Acceso denegado"
    con = db()
    c = con.cursor()
    c.execute("SELECT user,role FROM users")
    users = c.fetchall()
    c.execute("SELECT user,query FROM history ORDER BY id DESC LIMIT 50")
    history = c.fetchall()
    return render_template_string(ADMIN_HTML, users=users, history=history)

# =========================
# FRONTEND
# =========================

LOGIN_HTML = """<!DOCTYPE html><html><head><title>Login</title>
<style>body{font-family:Arial;background:#e3f2ff;display:flex;justify-content:center;align-items:center;height:100vh;}
.box{background:white;padding:30px;border-radius:15px;width:300px;}
input,button{width:100%;padding:10px;margin-top:10px;}
button{background:#007bff;color:white;border:none;}
</style></head><body>
<div class="box">
<h2>Login</h2>
<form method="post">
<input name="user" placeholder="Usuario">
<input name="pass" type="password" placeholder="Contraseña">
<button>Entrar</button>
</form>
<a href="/register">Crear cuenta</a>
</div></body></html>"""

REGISTER_HTML = """<!DOCTYPE html><html><head><title>Registro</title>
<style>body{font-family:Arial;background:#e3f2ff;display:flex;justify-content:center;align-items:center;height:100vh;}
.box{background:white;padding:30px;border-radius:15px;width:300px;}
input,button{width:100%;padding:10px;margin-top:10px;}
button{background:#28a745;color:white;border:none;}
</style></head><body>
<div class="box">
<h2>Registro</h2>
<form method="post">
<input name="user">
<input name="pass" type="password">
<button>Crear</button>
</form>
<a href="/login">Volver</a>
</div></body></html>"""

CORE_HTML = """<!DOCTYPE html><html><head><title>Core</title>
<style>
body{font-family:Arial;background:#eef3ff;padding:20px;}
.card{background:white;padding:15px;border-radius:12px;margin:10px;}
.letra{display:inline-block;padding:10px;background:#007bff;color:white;border-radius:8px;margin:5px;cursor:pointer;}
</style></head><body>

<div class="card">Usuario: {{user}} | Rol: {{role}} | <a href="/logout">Salir</a> | <a href="/admin">Admin</a></div>

<div class="card">
<input id="q"><button onclick="buscar()">Buscar</button>
<div id="resultado"></div>
</div>

<div class="card">
<button onclick="cargarJuego()">Juego</button>
<div id="letras"></div>
<div id="respuesta"></div>
</div>

<script>
function buscar(){
fetch("/buscar?q="+encodeURIComponent(q.value))
.then(r=>r.json())
.then(d=>{
resultado.innerHTML=d.error?d.error:"<h3>"+d.titulo+"</h3><p>"+d.texto+"</p>"+(d.img?'<img src="'+d.img+'">':"");
});
}

let palabra="",sel="";
function cargarJuego(){
fetch("/juego").then(r=>r.json()).then(d=>{
palabra=d.palabra;sel="";letras.innerHTML="";
d.mezcla.forEach(l=>{
let s=document.createElement("span");
s.className="letra";
s.innerText=l;
s.onclick=()=>{sel+=l;respuesta.innerText=sel;if(sel.length===palabra.length){alert(sel===palabra?"Correcto":"Incorrecto: "+palabra);sel="";}};
letras.appendChild(s);
});
});
}
</script></body></html>"""

ADMIN_HTML = """<!DOCTYPE html><html><head><title>Admin</title></head><body>
<h2>Usuarios</h2>
<ul>{% for u in users %}<li>{{u[0]}} - {{u[1]}}</li>{% endfor %}</ul>
<h2>Historial</h2>
<ul>{% for h in history %}<li>{{h[0]}}: {{h[1]}}</li>{% endfor %}</ul>
<a href="/core">Volver</a>
</body></html>"""

# =========================
# RUN
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
