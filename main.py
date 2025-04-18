from flask import Flask, request, jsonify
import base64, re, io
from PIL import Image
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['th', 'en'])

def extract_amount(text):
    matches = re.findall(r'(\d{1,3}(?:,\d{3})*\.\d{2})', text)
    return matches[-1] if matches else None

@app.route('/read-amount', methods=['POST'])
def read_amount():
    try:
        data = request.get_json()
        image_base64 = data.get("image")
        if not image_base64:
            return jsonify({"error": "Missing image"}), 400
        base64_data = re.sub('^data:image/.+;base64,', '', image_base64)
        image_bytes = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_bytes))
        result = reader.readtext(image)
        text = " ".join([r[1] for r in result])
        amount = extract_amount(text)
        return jsonify({"text": text, "amount": amount})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
