from flask import Flask, render_template, jsonify, request

app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(threaded=True)
