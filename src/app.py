from flask import Flask, send_from_directory
import os

# Chemin absolu vers le dossier "web"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")

app = Flask(
    __name__,
    static_folder=WEB_DIR,      # tous les fichiers statiques (js, css, json…)
    static_url_path=""          # pour les servir à la racine
)

@app.route("/")
def index():
    # Sert le fichier index.html depuis le dossier web
    return send_from_directory(WEB_DIR, "index.html")


if __name__ == "__main__":
    # debug=True pour le développement
    app.run(host="0.0.0.0", port=5000, debug=True)
