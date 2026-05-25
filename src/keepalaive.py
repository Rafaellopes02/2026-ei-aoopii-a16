from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "O Antropólogo Digital está vivo e a observar!"

def run():
    # O Render exige que o servidor corra na porta 10000 ou 8080
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()