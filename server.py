# server.py (corregido y funcional)
from flask import Flask, render_template, request, jsonify
import os
import json
import re

app = Flask(__name__)

DATA_DIR = os.path.join(os.getcwd(), "Data")
DATA_JSON_PATH = os.path.join(DATA_DIR, "data.json")
IMAGENES_JSON_PATH = "imagenes_dni.json"

if os.path.exists(IMAGENES_JSON_PATH):
    with open(IMAGENES_JSON_PATH, "r", encoding="utf-8") as f:
        IMAGENES_DNI = json.load(f)
else:
    IMAGENES_DNI = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dni = request.form.get("dni")
        fecha = request.form.get("fecha")
        encontrado = None

        if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", fecha):
            return render_template("index.html", error="❌ Ingrese la fecha con el formato correcto: DD/MM/AAAA")

        if os.path.exists(DATA_JSON_PATH):
            with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                for persona in data:
                    fecha_persona = persona.get("fecha_creacion") or persona.get("fecha")
                    if persona.get("dni") == dni and fecha_persona == fecha:
                        encontrado = persona
                        break

        image_url = IMAGENES_DNI.get(dni)
        return render_template("result.html", persona=encontrado, imagen=image_url)

    return render_template("index.html")

@app.route("/agregar_dato", methods=["POST"])
def agregar_dato():
    persona = request.json.get("persona")
    imagen_url = request.json.get("imagen_url")

    if not persona or not imagen_url:
        return "Datos inválidos", 400

    dni = persona.get("dni")
    if dni:
        IMAGENES_DNI[dni] = imagen_url
        with open(IMAGENES_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(IMAGENES_DNI, f, indent=2, ensure_ascii=False)

    if os.path.exists(DATA_JSON_PATH):
        with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []

    data.append(persona)
    with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return "OK", 200

@app.route("/eliminar_dato", methods=["POST"])
def eliminar_dato():
    dni = request.json.get("dni")

    if not dni:
        return "DNI no proporcionado", 400

    try:
        if os.path.exists(DATA_JSON_PATH):
            with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

            nueva_data = [p for p in data if str(p.get("dni")) != str(dni)]
            with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(nueva_data, f, indent=2, ensure_ascii=False)

        if dni in IMAGENES_DNI:
            del IMAGENES_DNI[dni]
            with open(IMAGENES_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(IMAGENES_DNI, f, indent=2, ensure_ascii=False)

        return "Eliminado correctamente", 200

    except Exception as e:
        return f"Error al eliminar: {str(e)}", 500

@app.route("/api/subir_dato", methods=["POST"])
def subir_dato():
    try:
        tipo = request.form.get("tipo")

        if tipo == "nuevo_miembro":
            dni = request.form.get("dni")
            json_data = json.loads(request.form.get("data"))
            imagen_url = request.form.get("imagen_url")

            IMAGENES_DNI[dni] = imagen_url
            with open(IMAGENES_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(IMAGENES_DNI, f, indent=2, ensure_ascii=False)

            if os.path.exists(DATA_JSON_PATH):
                with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
                    lista = json.load(f)
            else:
                lista = []

            lista.append(json_data)
            with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(lista, f, indent=2, ensure_ascii=False)

            return jsonify({"status": "ok", "msg": "Miembro agregado exitosamente"})

        elif tipo == "eliminar_miembro":
            dni = request.form.get("dni")
            eliminado = False

            if os.path.exists(DATA_JSON_PATH):
                with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
                    lista = json.load(f)
                nueva_lista = [p for p in lista if p.get("dni") != dni]
                eliminado = len(lista) != len(nueva_lista)

                with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(nueva_lista, f, indent=2, ensure_ascii=False)

            if dni in IMAGENES_DNI:
                del IMAGENES_DNI[dni]
                with open(IMAGENES_JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(IMAGENES_DNI, f, indent=2, ensure_ascii=False)

            if eliminado:
                return jsonify({"status": "ok", "msg": f"Miembro con DNI {dni} eliminado"})
            else:
                return jsonify({"status": "error", "msg": "DNI no encontrado"}), 404

        else:
            return jsonify({"status": "error", "msg": "Tipo de operación no válido"}), 400

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
