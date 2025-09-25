from flask import Blueprint, render_template, request, redirect, url_for
from database.database import db_connection
from models.customer import Customer

cust = Blueprint("customer", __name__, static_folder="static", template_folder="templates")
db = db_connection()

# GET #

@cust.route('/lista', methods = ['GET'])
def get_list():
    if request.method == "GET":
        docs = db['customers']
        list = docs.find({})
        return render_template('customer/index.html', customers = list)

@cust.route('/objeto/<string:id>', methods = ['GET'])
def get_item(id):
    if request.method == "GET":
        docs = db['customers']
        item = docs.find_one({'code': id})
        return render_template('customer/item.html', customer = item)

# POST #

@cust.route('/insertar', methods = ['GET'])
def insert_form():
    if request.method == "GET":
        sex = [{'value': 'M','name': 'Masculino'},{'value': 'F','name': 'Femenino'}]
        return render_template('customer/form_insert.html', sexs = sex)

@cust.route('/insert_customer', methods = ['POST'])
def post_item():
    if request.method == "POST":
        
        nm = request.form['name']
        srnm = request.form['surname']
        brth = request.form['birth']
        sx = request.form['sex']
        ml = request.form['mail']
        phn = request.form['phone']

        if nm and srnm and brth and sx and ml and phn:
            doc = db['customers']
            document = Customer(nm, srnm, brth, sx, ml, phn)
            doc.insert_one(document.insert_document())
            item = doc.find_one(document.select_document())
            return redirect(url_for('customer.get_item', id = item['code'])) 

# PUT #
 
@cust.route('/objeto/<string:id>/editar', methods = ['GET'])
def update_form(id):
    if request.method == "GET":
        docs = db['customers']
        item = docs.find_one({'code': id})
        return render_template('customer/form_update.html', customer = item)

@cust.route('/update_customer/<string:id>', methods = ['POST'])
def put_item(id):
    if request.method == "POST":
        nm = request.form['name']
        srnm = request.form['surname']
        brth = request.form['birth']
        sx = request.form['sex']
        ml = request.form['mail']
        phn = request.form['phone']
    
        if nm and srnm and brth and sx and ml and phn:
            doc = db['customers']
            document = Customer(nm, srnm, brth, sx, ml, phn)
            doc.find_one_and_update({'code': id},document.update_document())
            return redirect(url_for('customer.get_item', id = id))
    
# DELETE #

@cust.route('/delete_customer')
def delete_list():
    doc = db['customers']
    doc.delete_many({})
    return redirect(url_for('customer.get_list'))

@cust.route('/delete_customer/<string:id>')
def delete_item(id):
    doc = db['customers']
    doc.delete_one({'code': id})
    return redirect(url_for('customer.get_list'))