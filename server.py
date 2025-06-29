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
    IMAGENES_DNI = {
    "00811758": "https://i.ibb.co/NdRxHy2B/00811758.jpg",
    "16429103": "https://i.ibb.co/pFvrLKb/16429103.jpg",
    "16445545": "https://i.ibb.co/VYvrvdk1/16445545.jpg",
    "16469856": "https://i.ibb.co/B23jc6wV/16469856.jpg",
    "16478430": "https://i.ibb.co/LXxLMbQJ/16478430.jpg",
    "16553559": "https://i.ibb.co/mVQY72xj/16553559.jpg",
    "16598349": "https://i.ibb.co/rRh0M1HG/16598349.jpg",
    "16628701": "https://i.ibb.co/d0JcXy4N/16628701.jpg",
    "16678733": "https://i.ibb.co/svtb2VD9/16678733.jpg",
    "16753914": "https://i.ibb.co/QFcRGxzx/16753914.jpg",
    "16759681": "https://i.ibb.co/27j7M793/16759681.jpg",
    "16782540": "https://i.ibb.co/m5Cnc8tM/16782540.jpg",
    "16797673": "https://i.ibb.co/0jZPNC09/16797673.jpg",
    "16801728": "https://i.ibb.co/WWNQq4fn/16801728.jpg",
    "17637201": "https://i.ibb.co/C3LgW3T8/17637201.jpg",
    "27263560": "https://i.ibb.co/Tx58JdwY/27263560.jpg",
    "27269108": "https://i.ibb.co/rG07B0by/27269108.jpg",
    "27397572": "https://i.ibb.co/3DrjkyJ/27397572.jpg",
    "27413074": "https://i.ibb.co/k6yCYr6g/27413074.jpg",
    "33663530": "https://i.ibb.co/JFQ98xb3/33663530.jpg",
    "41101613": "https://i.ibb.co/rK48tLr7/41101613.jpg",
    "41614718": "https://i.ibb.co/NgcW7bdB/41614718.jpg",
    "41657863": "https://i.ibb.co/5g160PQ6/41657863.jpg",
    "41669360": "https://i.ibb.co/tTxHc0RS/41669360.jpg",
    "41794891": "https://i.ibb.co/GvsczSL4/41794891.jpg",
    "42047423": "https://i.ibb.co/67fTT9wv/42047423.jpg",
    "42189841": "https://i.ibb.co/dstSRH18/42189841.jpg",
    "42290226": "https://i.ibb.co/TBXD2vHj/42290226.jpg",
    "42753439": "https://i.ibb.co/Rk1sftQc/42753439.jpg",
    "42866711": "https://i.ibb.co/nMMhzcQp/42866711.jpg",
    "43229756": "https://i.ibb.co/G4LhRz01/43229756.jpg",
    "43232240": "https://i.ibb.co/fYYZCR92/43232240.jpg",
    "43856165": "https://i.ibb.co/yLxKYdW/43856165.jpg",
    "44623614": "https://i.ibb.co/KxGW25cR/44623614.jpg",
    "44764529": "https://i.ibb.co/VpzgHrn3/44764529.jpg",
    "44912153": "https://i.ibb.co/1fg8yhCK/44912153.jpg",
    "45067658": "https://i.ibb.co/ymdRHwHj/45067658.jpg",
    "45155615": "https://i.ibb.co/7NgkRYhm/45155615.jpg",
    "45281070": "https://i.ibb.co/YFXcbLKy/45281070.jpg",
    "45513366": "https://i.ibb.co/VYdGRwN1/45513366.jpg",
    "46079713": "https://i.ibb.co/spDh0W4n/46079713.jpg",
    "46557468": "https://i.ibb.co/C3NzZtPt/46557468.jpg",
    "46708207": "https://i.ibb.co/ccCsBx4W/46708207.jpg",
    "47247874": "https://i.ibb.co/1SmdKM4/47247874.jpg",
    "47764489": "https://i.ibb.co/HTB7nmgb/47764489.jpg",
    "47848267": "https://i.ibb.co/vCx4dVzg/47848267.jpg",
    "48440515": "https://i.ibb.co/r2sW11Gc/48440515.jpg",
    "61016423": "https://i.ibb.co/RGqWX5jy/61016423.jpg",
    "70895774": "https://i.ibb.co/VYstxG4D/70895774.jpg",
    "71965621": "https://i.ibb.co/d4vjv0v8/71965621.jpg",
    "74204169": "https://i.ibb.co/rKWKCTBJ/74204169.jpg",
    "74739821": "https://i.ibb.co/C3XJX8JZ/74739821.jpg",
    "75666315": "https://i.ibb.co/xqhBYxD1/75666315.jpg",
    "76522510": "https://i.ibb.co/Hf8ZGCVs/76522510.jpg",
    "80219071": "https://i.ibb.co/whD8XQYP/80219071.jpg",
    "80219749": "https://i.ibb.co/8nDTCfnN/80219749.jpg",
    "80256691": "https://i.ibb.co/HpTB7RhY/80256691.jpg",
    "80642437": "https://i.ibb.co/20BNVz89/80642437.jpg"
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dni = request.form.get("dni")
        encontrado = None

        if os.path.exists(DATA_JSON_PATH):
            with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                for persona in data:
                    if persona.get("dni") == dni:
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
