from flask import Blueprint, redirect, render_template, url_for, request
from app.database.nosql import db_connection
from app.models.customer import Customer
from app.models._functions_ import date_string

bpCustomer = Blueprint("customer", __name__, static_folder="static", template_folder="templates")
db = db_connection()
docs = db['customers']

# GET #
@bpCustomer.route('/lista', methods = ['GET'])
def get_list():
    if request.method == "GET":
        list = docs.find({})
        return render_template('customer.list.html', customers = list)

@bpCustomer.route('/objeto/<string:id>', methods = ['GET'])
def get_item(id):
    if request.method == "GET":
        item = docs.find_one({'code': id})
        date = item['birth']
        dt = date_string(date, "%Y-%m-%d", "%d %B %Y")
        return render_template('customer.item.html', customer = item, date = dt)

# POST #
@bpCustomer.route('/insertar', methods = ['GET'])
def insert_form():
    if request.method == "GET":
        sex = [{'value': 'M','name': 'Masculino'},{'value': 'F','name': 'Femenino'}]
        return render_template('customer.form_insert.html', sexs = sex, title='Agregar cliente')

@bpCustomer.route('/insert_customer', methods = ['POST'])
def post_item():
    if request.method == "POST":
        
        nm = request.form['name']
        srnm = request.form['surname']
        brth = request.form['birth']
        sx = request.form['sex']
        ml = request.form['mail']
        phn = request.form['phone']

        if nm and srnm and brth and sx and ml and phn:
            document = Customer(nm, srnm, brth, sx, ml, phn)
            docs.insert_one(document.insert_doc())
            item = docs.find_one(document.select_doc())
            return redirect(url_for('customer.get_item', id = item['code']))

# PUT #
@bpCustomer.route('/objeto/<string:id>/editar', methods = ['GET'])
def update_form(id):
    if request.method == "GET":
        item = docs.find_one({'code': id})
        return render_template('customer.form_update.html', customer = item, title='Modificar cliente')

@bpCustomer.route('/update_customer/<string:id>', methods = ['POST'])
def put_item(id):
    if request.method == "POST":

        nm = request.form['name']
        srnm = request.form['surname']
        brth = request.form['birth']
        sx = request.form['sex']
        ml = request.form['mail']
        phn = request.form['phone']
    
        if nm and srnm and brth and sx and ml and phn:
            document = Customer(nm, srnm, brth, sx, ml, phn)
            docs.find_one_and_update({'code': id},document.update_doc())
            return redirect(url_for('customer.get_item', id = id))
    
# DELETE #
@bpCustomer.route('/delete_customer')
def delete_list():
    docs.delete_many({})
    return redirect(url_for('customer.get_list'))

@bpCustomer.route('/delete_customer/<string:id>')
def delete_item(id):
    docs.delete_one({'code': id})
    return redirect(url_for('customer.get_list'))