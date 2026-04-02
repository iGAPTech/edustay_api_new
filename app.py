from flask import Flask, send_from_directory
from config import Config

from routes.auth import auth_bp
from routes.student import student_bp
from routes.provider import provider_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(provider_bp, url_prefix="/api/provider")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

@app.route('/uploads/properties/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads/properties', filename)

@app.route('/uploads/proofs/<filename>')
def uploaded_id(filename):
    return send_from_directory('uploads/proofs', filename)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='192.168.1.78', port=5000, debug=True)

