from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tmp", methods=["POST"])
def register():
    if not request.form.get("acc"):
        return render_template("failure.html")
    user_name = request.form.get("domain")
    print(user_name)

    return render_template("success.html")


if __name__ == "__main__":
    app.run()
