from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)

# Генерация ключа шифрования
key = Fernet.generate_key()
cipher = Fernet(key)

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    file_content = file.read()

    encrypted_content = cipher.encrypt(file_content)
    encrypted_filename = file.filename + '.enc'
    
    with open(encrypted_filename, 'wb') as enc_file:
        enc_file.write(encrypted_content)

    return jsonify({"message": "File encrypted successfully", "encrypted_file": encrypted_filename, "key": base64.urlsafe_b64encode(key).decode()}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
