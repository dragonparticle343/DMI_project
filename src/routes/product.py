from flask import Blueprint, render_template, request, redirect, url_for
from database.database import db_connection
from models.product import Product

prod = Blueprint("product", __name__, static_folder="static", template_folder="templates")
db = db_connection()

# GET #

@prod.route('/lista', methods = ['GET'])
def get_list():
    if request.method == "GET":
        docs = db['products']
        list = docs.find({})
        return render_template('product/index.html', products = list)

@prod.route('objeto/<string:id>', methods = ['GET'])
def get_item(id):
    if request.method == "GET":
        docs = db['products']
        item = docs.find_one({'code': id})
        return render_template('product/item.html', product = item)

# POST #

@prod.route('/insertar', methods = ['GET'])
def insert_form():
    if request.method == "GET":
        return render_template('product/form_insert.html')
    
@prod.route('/insert_product', methods = ['POST'])
def post_item():
    if request.method == "POST":
    
        nm = request.form['name']
        prc = request.form['price']
        dprtmnt = request.form['department']
        rtcl = request.form['article']
        dscrptn = request.form['description']
        cntnt = request.form['content']

        if nm and prc and dprtmnt and rtcl and dscrptn and cntnt:
            doc = db['products']
            document = Product(nm, prc, dprtmnt, rtcl, dscrptn, cntnt)
            doc.insert_one(document.insert_document())
            item = doc.find_one(document.select_document())
            return redirect(url_for('product.get_item', id = item['code']))

# PUT #

@prod.route('objeto/<string:id>/editar', methods = ['GET'])
def update_form(id):
    if request.method == "GET":
        docs = db['products']
        item = docs.find_one({'code': id})
        return render_template('product/form_update.html', product = item)

@prod.route('/update_product/<string:id>', methods=['POST'])
def put_item(id):
    if request.method == "POST":

        nm = request.form['name']
        prc = request.form['price']
        dprtmnt = request.form['department']
        sbdprtmnt = request.form['subdepartment']
        sctn = request.form['section']
        rtcl = request.form['article']
        dscrptn = request.form['description']
        cntnt = request.form['content']
    
        if nm and prc and dprtmnt and sbdprtmnt and sctn and rtcl and dscrptn and cntnt:
            doc = db['products']
            document = Product(nm, prc, dprtmnt, sbdprtmnt, sctn, rtcl, dscrptn, cntnt)
            doc.find_one_and_update({'code': id},document.update_document())
            return redirect(url_for('product.get_item', id = id))

# DELETE #

@prod.route('/delete_product')
def delete_list():
    doc = db['products']
    doc.delete_many({})
    return redirect(url_for('product.get_list'))

@prod.route('/delete_product/<string:id>')
def delete_item(id):
    doc = db['products']
    doc.delete_one({'code': id})
    return redirect(url_for('product.get_list'))
