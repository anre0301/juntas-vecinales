from flask import Flask, render_template, request, jsonify
import os
import json
import re

app = Flask(__name__)

DATA_DIR = os.path.join(os.getcwd(), "Data")
DATA_JSON_PATH = os.path.join(DATA_DIR, "data.json")

# Cargar datos de imagen al iniciar
if os.path.exists("imagenes_dni.json"):
    with open("imagenes_dni.json", "r", encoding="utf-8") as f:
        IMAGENES_DNI = json.load(f)
else:
    IMAGENES_DNI = {
    "00811758": "https://i.ibb.co/Cs5MSDj6/00811758.jpg",
    "16429103": "https://i.ibb.co/2rXqdKn/16429103.jpg",
    "16445545": "https://i.ibb.co/7d2wbCKN/16445545.jpg",
    "16469856": "https://i.ibb.co/9KYd581/16469856.jpg",
    "16478430": "https://i.ibb.co/Fb2gGJwm/16478430.jpg",
    "16553559": "https://i.ibb.co/9mn1k4mt/16553559.jpg",
    "16598349": "https://i.ibb.co/84tHVTmh/16598349.jpg",
    "16628701": "https://i.ibb.co/gMLHsD10/16628701.jpg",
    "16678733": "https://i.ibb.co/Kjx7Bchx/16678733.jpg",
    "16753914": "https://i.ibb.co/GQ2WtMdx/16753914.jpg",
    "16759681": "https://i.ibb.co/S4J6htFh/16759681.jpg",
    "16782540": "https://i.ibb.co/9kt7MnTV/16782540.jpg",
    "16797673": "https://i.ibb.co/PZRVcB9s/16797673.jpg",
    "16801728": "https://i.ibb.co/zTWxHhkS/16801728.jpg",
    "17637201": "https://i.ibb.co/rGBwqNBZ/17637201.jpg",
    "27263560": "https://i.ibb.co/4ZwmYs73/27263560.jpg",
    "27269108": "https://i.ibb.co/1Y2bfcWT/27269108.jpg",
    "27397572": "https://i.ibb.co/WvHMfXQY/27397572.jpg",
    "27413074": "https://i.ibb.co/sTNmh32/27413074.jpg",
    "33663530": "https://i.ibb.co/p6KpRrr0/33663530.jpg",
    "41101613": "https://i.ibb.co/WNPqk7d3/41101613.jpg",
    "41614718": "https://i.ibb.co/WNYf7PgL/41614718.jpg",
    "41657863": "https://i.ibb.co/KzpnM5N4/41657863.jpg",
    "41669360": "https://i.ibb.co/4RtrTR3j/41669360.jpg",
    "41794891": "https://i.ibb.co/0RwjpQgB/41794891.jpg",
    "42047423": "https://i.ibb.co/W4XS721c/42047423.jpg",
    "42189841": "https://i.ibb.co/5Xgt1sdN/42189841.jpg",
    "42290226": "https://i.ibb.co/TqkHxsDq/42290226.jpg",
    "42753439": "https://i.ibb.co/hRpWW4Xs/42753439.jpg",
    "42866711": "https://i.ibb.co/bj92KMsR/42866711.jpg",
    "43229756": "https://i.ibb.co/4Cftj8x/43229756.jpg",
    "43232240": "https://i.ibb.co/20NvTtqC/43232240.jpg",
    "43856165": "https://i.ibb.co/hJdCgWMW/43856165.jpg",
    "44623614": "https://i.ibb.co/5XKJchW5/44623614.jpg",
    "44764529": "https://i.ibb.co/FkD2Q4Gk/44764529.jpg",
    "44912153": "https://i.ibb.co/N66jYksc/44912153.jpg",
    "45067658": "https://i.ibb.co/h19Jty8P/45067658.jpg",
    "45155615": "https://i.ibb.co/jkKCzbNT/45155615.jpg",
    "45281070": "https://i.ibb.co/XkXZS04L/45281070.jpg",
    "45513366": "https://i.ibb.co/qL83gBsx/45513366.jpg",
    "46079713": "https://i.ibb.co/YBBsfPb4/46079713.jpg",
    "46557468": "https://i.ibb.co/bgDfzgdf/46557468.jpg",
    "46708207": "https://i.ibb.co/GvrYZBfZ/46708207.jpg",
    "47247874": "https://i.ibb.co/RkHCqvTm/47247874.jpg",
    "47764489": "https://i.ibb.co/jZs6qr3x/47764489.jpg",
    "47848267": "https://i.ibb.co/rGPtL9r2/47848267.jpg",
    "48440515": "https://i.ibb.co/qYtMNd1f/48440515.jpg",
    "61016423": "https://i.ibb.co/qFpH0f0n/61016423.jpg",
    "70895774": "https://i.ibb.co/39Mx33Jb/70895774.jpg",
    "71965621": "https://i.ibb.co/vWGK7Xf/71965621.jpg",
    "74204169": "https://i.ibb.co/0jSvNwPw/74204169.jpg",
    "74739821": "https://i.ibb.co/SG2P7CJ/74739821.jpg",
    "75666315": "https://i.ibb.co/nqy5yxJF/75666315.jpg",
    "76522510": "https://i.ibb.co/21SPW71b/76522510.jpg",
    "80219071": "https://i.ibb.co/ccDYbDWQ/80219071.jpg",
    "80219749": "https://i.ibb.co/qGMJxmB/80219749.jpg",
    "80256691": "https://i.ibb.co/TxFQrhqN/80256691.jpg",
    "80642437": "https://i.ibb.co/kskNn6rp/80642437.jpg"    
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dni = request.form.get("dni")
        fecha = request.form.get("fecha")
        encontrado = None

        formato_valido = re.fullmatch(r"\d{2}/\d{2}/\d{4}", fecha)
        if not formato_valido:
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

    data_path = os.path.join(DATA_DIR, "data.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []

    data.append(persona)
    with open(data_path, "w", encoding="utf-8") as f:
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

        # También eliminar del diccionario de imágenes
        if dni in IMAGENES_DNI:
            del IMAGENES_DNI[dni]
            with open("imagenes_dni.json", "w", encoding="utf-8") as f:
                json.dump(IMAGENES_DNI, f, indent=2, ensure_ascii=False)

        return "Eliminado correctamente", 200

    except Exception as e:
        return f"Error al eliminar: {str(e)}", 500

# === NUEVA RUTA PARA RECIBIR DATOS ===
@app.route("/api/subir_dato", methods=["POST"])
def subir_dato():
    try:
        tipo = request.form.get("tipo")  # nuevo_miembro o eliminar_miembro

        if tipo == "nuevo_miembro":
            dni = request.form.get("dni")
            json_data = json.loads(request.form.get("data"))
            imagen_url = request.form.get("imagen_url")

            # Agregar imagen al diccionario
            IMAGENES_DNI[dni] = imagen_url
            with open("imagenes_dni.json", "w", encoding="utf-8") as f:
                json.dump(IMAGENES_DNI, f, indent=2, ensure_ascii=False)

            # Agregar JSON al data.json
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
                with open("imagenes_dni.json", "w", encoding="utf-8") as f:
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
