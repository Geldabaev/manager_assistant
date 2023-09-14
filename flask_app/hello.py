from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/reg/<name_photo>")
def reg(name_photo):
    return render_template("index.html", name_image=name_photo)


if __name__ == "__main__":
    app.run()
