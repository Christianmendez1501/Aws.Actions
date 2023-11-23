from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola, Mundo! Este es un servidor web simple con Flask.'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
