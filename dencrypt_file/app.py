from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    if 'file' not in request.files or 'key' not in request.form:
        return jsonify({"error": "No file or key part"}), 400
    file = request.files['file']
    key = request.form['key']

    try:
        cipher = Fernet(base64.urlsafe_b64decode(key))
    except Exception as e:
        return jsonify({"error": "Invalid key"}), 400

    file_content = file.read()

    try:
        decrypted_content = cipher.decrypt(file_content)
    except Exception as e:
        return jsonify({"error": "Decryption failed"}), 400

    decrypted_filename = file.filename.replace('.enc', '')
    
    with open(decrypted_filename, 'wb') as dec_file:
        dec_file.write(decrypted_content)

    return jsonify({"message": "File decrypted successfully", "decrypted_file": decrypted_filename}), 200

if __name__ == '__main__':
    app.run(port=5002, debug=True)
