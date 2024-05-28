from flask import Flask

app = Flask(__name__)

file = open('./public/index.html')
html = file.read()

@app.route("/")
def hello_world():
    return html


file.close()