from flask import Blueprint, redirect, render_template, url_for, request
from app.database.nosql import db_connection
from app.models.product import Product

bpProduct = Blueprint("product", __name__, static_folder="static", template_folder="templates")
db = db_connection()
docs = db['products']

# GET #
@bpProduct.route('/lista', methods = ['GET'])
def get_list():
    if request.method == "GET":
        list = docs.find({})
        return render_template('product.list.html', products = list, title='Productos')

@bpProduct.route('objeto/<string:id>', methods = ['GET'])
def get_item(id):
    if request.method == "GET":
        item = docs.find_one({'code': id})
        return render_template('product.item.html', product = item)

# POST #
@bpProduct.route('/insertar', methods = ['GET'])
def insert_form():
    if request.method == "GET":
        return render_template('product.form_insert.html', title='Agregar producto')
    
@bpProduct.route('/insert_product', methods = ['POST'])
def post_item():
    if request.method == "POST":
    
        nm = request.form['name']
        prc = request.form['price']
        dprtmnt = request.form['department']
        rtcl = request.form['article']
        dscrptn = request.form['description']
        cntnt = request.form['content']

        if nm and prc and dprtmnt and rtcl and dscrptn and cntnt:
            document = Product(nm, prc, dprtmnt, rtcl, dscrptn, cntnt)
            docs.insert_one(document.insert_doc())
            item = docs.find_one(document.select_doc())
            return redirect(url_for('product.get_item', id = item['code']))

# PUT #
@bpProduct.route('objeto/<string:id>/editar', methods = ['GET'])
def update_form(id):
    if request.method == "GET":
        item = docs.find_one({'code': id})
        return render_template('product.form_update.html', product = item, title='Modificar producto')

@bpProduct.route('/update_product/<string:id>', methods=['POST'])
def put_item(id):
    if request.method == "POST":

        nm = request.form['name']
        prc = request.form['price']
        dprtmnt = request.form['department']
        rtcl = request.form['article']
        dscrptn = request.form['description']
        cntnt = request.form['content']
    
        if nm and prc and dprtmnt and rtcl and dscrptn and cntnt:
            document = Product(nm, prc, dprtmnt, rtcl, dscrptn, cntnt)
            docs.find_one_and_update({'code': id},document.update_doc())
            return redirect(url_for('product.get_item', id = id))

# DELETE #
@bpProduct.route('/delete_product')
def delete_list():
    docs.delete_many({})
    return redirect(url_for('product.get_list'))

@bpProduct.route('/delete_product/<string:id>')
def delete_item(id):
    docs.delete_one({'code': id})
    return redirect(url_for('product.get_list'))