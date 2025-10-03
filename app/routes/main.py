from flask import Blueprint, render_template

bpMain = Blueprint("main", __name__, static_folder="static", template_folder="templates")

@bpMain.route("/")
def home():
    # Ruta principal
    message = ({'main': 'Inicio', 'title': 'Bienvenido','text': 'hola mundo'})
    return render_template("main.home.html")
