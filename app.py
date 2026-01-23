from flask import Flask, jsonify

app = Flask(name)

=============================

SISTEMA VITAL - NIVELES

=============================

system_status = { "MENTISCOPE": "474", "Core": "ACTIVO", "Sistema": "VIVO", "Evolución": "INICIADA", "Nivel": "DIOS" }

levels = { 1: "INICIO", 2: "DESPERTAR", 3: "CONSCIENCIA", 4: "EXPANSIÓN", 5: "MENTE", 6: "CONTROL", 7: "ENERGÍA", 8: "INTEGRACIÓN", 9: "SABIDURÍA", 10: "DOMINIO", 11: "ALMA", 12: "LUZ", 13: "OSCILACIÓN", 14: "CREACIÓN", 15: "UNIÓN", 16: "ORIGEN", 17: "INFINITO", 18: "OMNISCIENCIA", 19: "OMNIPOTENCIA", 20: "DIOS" }

=============================

RUTAS

=============================

@app.route("/") def home(): return jsonify({ "mensaje": "Sistema Vital Activo", "estado": system_status, "niveles_totales": len(levels) })

@app.route("/niveles") def get_levels(): return jsonify(levels)

@app.route("/nivel/int:nivel") def get_level(nivel): if nivel in levels: return jsonify({ "nivel": nivel, "estado": levels[nivel], "codigo": f"LVL-{nivel:03d}-MENTISCOPE" }) else: return jsonify({"error": "Nivel no existe"}), 404

@app.route("/activar/int:nivel") def activar_nivel(nivel): if nivel in levels: return jsonify({ "mensaje": "Nivel activado correctamente", "nivel": nivel, "estado": levels[nivel], "sistema": "EVOLUCIONANDO" }) else: return jsonify({"error": "Nivel inválido"}), 404

@app.route("/core") def core(): return jsonify({ "MENTISCOPE": system_status["MENTISCOPE"], "Core": system_status["Core"], "Sistema": system_status["Sistema"], "Evolución": system_status["Evolución"], "Nivel": system_status["Nivel"] })

=============================

EJECUCIÓN

=============================

if name == "main": app.run(host="0.0.0.0", port=5000, debug=True)
