from flask import Flask, render_template
from routes.customer import cust
from routes.product import prod
from routes.order import ord
from routes.store import stor
import os

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)
app.register_blueprint(cust, url_prefix="/clientes")
app.register_blueprint(prod, url_prefix="/productos")
app.register_blueprint(ord, url_prefix="/ordenes")
app.register_blueprint(stor, url_prefix="/tiendas")

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)