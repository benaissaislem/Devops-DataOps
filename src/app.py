from flask import Flask, send_from_directory
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")

app = Flask(
    __name__,
    static_folder=WEB_DIR,      
    static_url_path=""          
)

@app.route("/")
def index():
    
    return send_from_directory(WEB_DIR, "index.html")


if __name__ == "__main__":
  
    app.run(host="0.0.0.0", port=5000, debug=True)
