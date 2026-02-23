from flask import Flask
from flask_cors import CORS
from api.person import person_bp
from api.person_detail import person_detail_bp
from api.person_basic import person_basic_bp
from api.relationship_api import relationship_api_bp
from api.parent_child import parent_child_bp
from api.marriage import marriage_bp
from api.avatar_api import avatar_bp
from api.tree_api import tree_bp
from api.announcement_api import announcement_bp
from api.person_delete_api import person_delete_bp
from api.date_utils_api import date_utils_bp
from api.login import login_bp
from api.clean_family_api import clean_family_bp
from api.clean_parent_api import clean_parent_bp

import os

app = Flask(__name__, static_folder="static")
app.config['JSON_AS_ASCII'] = False

from flask import send_from_directory
@app.route('/static/<path:filename>')
def serve_static(filename):
    static_dir = os.path.join(app.root_path, 'static')
    return send_from_directory(static_dir, filename)

ENV = os.environ.get("FLASK_ENV", "development")
print("FLASK_ENV =", ENV)
if ENV == "development":
    CORS(
        app,
        resources={r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }},
        supports_credentials=True
    )
else:
    CORS(
        app,
        resources={r"/api/*": {"origins": "https://familytree.example.com"}},
        supports_credentials=True,
    )

# -----------------------------
# REGISTER BLUEPRINTS — stable
# -----------------------------
app.register_blueprint(person_bp)
app.register_blueprint(person_detail_bp)
app.register_blueprint(person_basic_bp)
app.register_blueprint(relationship_api_bp)
app.register_blueprint(parent_child_bp)
app.register_blueprint(marriage_bp)
app.register_blueprint(avatar_bp)
app.register_blueprint(tree_bp, url_prefix="/api/tree")
app.register_blueprint(announcement_bp)
app.register_blueprint(person_delete_bp)
app.register_blueprint(date_utils_bp)
app.register_blueprint(login_bp, url_prefix="/api")
app.register_blueprint(clean_family_bp)
app.register_blueprint(clean_parent_bp)

@app.route("/")
def index():
    return {"message": "FamilyTree API running OK"}

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )

