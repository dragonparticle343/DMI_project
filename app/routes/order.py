from flask import Blueprint, redirect, render_template, url_for, request
from app.database.nosql import db_connection
from app.models.order import Article, Order, Pay
from app.models._functions_ import date_string, total_array

bpOrder = Blueprint("order", __name__, static_folder="static", template_folder="templates")
db = db_connection()
docs = db['orders'] 
cust = db['customers']
stor = db['stores']
prod = db['products']

# GET #
@bpOrder.route('/lista', methods = ['GET'])
def get_list():
    if request.method == "GET":
        list = docs.find({})
        return render_template('order.list.html', orders = list, title='Ordenes')

@bpOrder.route('/objeto/<string:id>', methods = ['GET'])
def get_item(id):
    if request.method == "GET":
        item = docs.find_one({'code': id})
        date = item['date']
        dt = date_string(date, "%m/%d/%Y-%H:%M:%S", "%d %B %Y %H:%M:%S")
        return render_template('order.item.html', order = item, title='Orden seleccionado', date = dt)

# POST #
@bpOrder.route('/insertar', methods = ['GET'])
def insert_form():
    if request.method == "GET":
        custs = cust.find({})
        stors = stor.find({})
        pay = {'Dinero en efectivo','Tarjetas de crédito'}
        return render_template('order.form_insert.html', customers = custs, stores = stors, pays = pay, title='Crear orden')

@bpOrder.route('/insert_order', methods = ['POST'])
def post_item():
    if request.method == "POST":
        store = request.form['store']
        customer = request.form['customer']
        payment = request.form['payment']

        if store and customer and payment:
        
            cust_data = cust.find_one({'code': customer})
            cstid = cust_data['code']
            cstnm = cust_data['name']
            cstsrnm = cust_data['surname']

            stor_data = stor.find_one({'code': store})
            strid = stor_data['code']
            strnm = stor_data['name']
            strt = stor_data['street']
            strddrss = strt['address']
            strpstl = strt['postal']
            rgn = stor_data['region']
            strct = rgn['city']
            strstt = rgn['state']
            strcntr = rgn['country']

            document = Order(strid, strnm, strddrss, strpstl, strct, strstt, strcntr, cstid, cstnm, cstsrnm, payment)
            docs.insert_one(document.insert_doc())
            item = docs.find_one(sort=[('date', -1)])
            code = item['code']
            return redirect(url_for('order.update_product_form', id = code))

@bpOrder.route('/objeto/<string:id>/insertar-productos', methods = ['GET'])
def update_product_form(id):
    if request.method == "GET":
        select = prod.find({})
        item = docs.find_one({'code': id})
        return render_template('order.form_update-product.html', order = item, products = select, title='Carro de compras')
    
@bpOrder.route('/<string:id>/update_insert_product', methods = ['POST'])
def put_product(id):
    if request.method == "POST":

        product = request.form['product']
        units = request.form['units']

        if product and units:

            prod_data = prod.find_one({'code': product})
            cd = prod_data['code']
            nm = prod_data['name']
            prc = prod_data['price']

            document = Article(cd, nm, prc, units)
            docs.find_one_and_update({'code': id},document.insert_doc())

            item = docs.find_one({'code': id})
            products = item['products']
            prod_units = total_array(products,'units')
            prod_total = total_array(products,'subtotal') 
            docs.find_one_and_update({'code': id},{'$set': {'quantity': prod_units,'total': prod_total}})

            return redirect(url_for('order.update_product_form', id = id))

@bpOrder.route('/<string:id>/update_delete_one_product/<string:ed>')
def delete_one_product(id, ed):
    docs.find_one_and_update({'code': id},{'$pull': {'products': {'code': ed}}})
    item = docs.find_one({'code': id})
    products = item['products']
    prod_units = total_array(products,'units')
    prod_total = total_array(products,'subtotal') 
    docs.find_one_and_update({'code': id},{'$set': {'quantity': prod_units,'total': prod_total}})
    return redirect(url_for('order.update_product_form', id = id))

@bpOrder.route('/<string:id>/update_delete_all_product')
def delete_all_product(id):  
    docs.find_one_and_update({'code': id},{'$pull': {'products': []}})
    item = docs.find_one({'code': id})
    products = item['products']
    prod_units = total_array(products,'units')
    prod_total = total_array(products,'subtotal') 
    docs.find_one_and_update({'code': id},{'$set': {'quantity': prod_units,'total': prod_total}})
    return redirect(url_for('order.update_product_form', id = id))
        
@bpOrder.route('/objeto/<string:id>/insertar-pago', methods = ['GET'])
def update_pay_form(id):
    if request.method == "GET":
        item = docs.find_one({'code': id})
        return render_template('order.form_update-pay.html', order = item, title='Pagos')
    
@bpOrder.route('/<string:id>/update_insert_pay', methods = ['POST'])
def put_pay(id):
    if request.method == "POST":

        pay = request.form['pay']

        if pay:

            item = docs.find_one({'code': id})
            ttl = item['total']
            py = float(pay)
        
            if py >= ttl:
                document = Pay(ttl,py)
                docs.find_one_and_update({'code': id},document.insert_doc())
                return redirect(url_for('order.get_item', id = id))
            else:
                return redirect(url_for('order.update_pay_form', id = id))

# DELETE #
@bpOrder.route('/delete_order')
def delete_list():
    docs.delete_many({})
    return redirect(url_for('order.get_list'))

@bpOrder.route('/delete_order/<string:id>')
def delete_item(id):
    docs.delete_one({'code': id})
    return redirect(url_for('order.get_list'))