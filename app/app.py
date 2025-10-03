from flask import Flask
from app.routes.main import bpMain
from app.routes.customer import bpCustomer
from app.routes.product import bpProduct
from app.routes.store import bpStore
from app.routes.order import bpOrder

def create_app(testing=False):
    app = Flask(__name__)
    app.register_blueprint(bpMain)
    app.register_blueprint(bpCustomer, url_prefix="/clientes")
    app.register_blueprint(bpProduct, url_prefix="/productos")
    app.register_blueprint(bpStore, url_prefix="/sucursales") 
    app.register_blueprint(bpOrder, url_prefix="/ordenes")
    return app