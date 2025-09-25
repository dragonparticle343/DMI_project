from flask import Blueprint, render_template, request, redirect, url_for
from database.database import db_connection
from models.order import Article, Order, Pay
from models._functions_ import total_array

ord = Blueprint("order", __name__, static_folder="static", template_folder="templates")
db = db_connection()

# GET #

@ord.route('/lista', methods = ['GET'])
def get_list():
    if request.method == "GET":
        docs = db['orders']
        list = docs.find({})
        return render_template('order/index.html', orders = list)

@ord.route('/objeto/<string:id>', methods = ['GET'])
def get_item(id):
    if request.method == "GET":
        docs = db['orders']
        item = docs.find_one({'code': id})
        return render_template('order/item.html', order = item)

# POST #

@ord.route('/insertar', methods = ['GET'])
def insert_form():
    if request.method == "GET":
        cust = db['customers']
        custs = cust.find({})
        stor = db['stores']
        stors = stor.find({})
        pay = {'Dinero en efectivo','Tarjetas de crédito'}
        return render_template('order/form_insert.html', customers = custs, stores = stors, pays = pay)

@ord.route('/insert_order', methods = ['POST'])
def post_item():
    if request.method == "POST":
        store = request.form['store']
        customer = request.form['customer']
        payment = request.form['payment']

        if store and customer and payment:
        
            cust = db['customers']
            cust_data = cust.find_one({'code': customer})
            cstid = cust_data['code']
            cstnm = cust_data['name']
            cstsrnm = cust_data['surname']

            stor = db['stores']
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

            doc = db['orders']
            document = Order(strid, strnm, strddrss, strpstl, strct, strstt, strcntr, cstid, cstnm, cstsrnm, payment)
            doc.insert_one(document.insert_document())
            item = doc.find_one(document.select_document())
            return redirect(url_for('order.update_product_form', id = item['code']))

# PUT #

@ord.route('/objeto/<string:id>/insertar-productos', methods = ['GET'])
def update_product_form(id):
    if request.method == "GET":
        prod = db['products']
        select = prod.find({})
        docs = db['orders']
        item = docs.find_one({'code': id})
        return render_template('order/form_update-product.html', order = item, products = select)
    
@ord.route('/<string:id>/update_insert_product', methods = ['POST'])
def put_product(id):
    if request.method == "POST":

        product = request.form['product']
        units = request.form['units']

        if product and units:

            prod = db['products']
            prod_data = prod.find_one({'code': product})
            cd = prod_data['code']
            nm = prod_data['name']
            prc = prod_data['price']

            doc = db['orders']
            document = Article(cd, nm, prc, units)
            doc.find_one_and_update({'code': id},document.insert_document())

            item = doc.find_one({'code': id})
            products = item['products']
            prod_units = total_array(products,'units')
            prod_total = total_array(products,'subtotal') 
            doc.find_one_and_update({'code': id},{'$set': {'quantity': prod_units,'total': prod_total}})

            return redirect(url_for('order.update_product_form', id = id))

@ord.route('/<string:id>/update_delete_one_product/<string:ed>')
def delete_one_product(id, ed):
    doc = db['orders']
    doc.find_one_and_update({'code': id},{'$pull': {'products': {'code': ed}}})
    item = doc.find_one({'code': id})
    products = item['products']
    prod_units = total_array(products,'units')
    prod_total = total_array(products,'subtotal') 
    doc.find_one_and_update({'code': id},{'$set': {'quantity': prod_units,'total': prod_total}})
    return redirect(url_for('order.update_product_form', id = id))

@ord.route('/<string:id>/update_delete_all_product')
def delete_all_product(id):  
    doc = db['orders']
    doc.find_one_and_update({'code': id},{'$pull': {'products': []}})
    item = doc.find_one({'code': id})
    products = item['products']
    prod_units = total_array(products,'units')
    prod_total = total_array(products,'subtotal') 
    doc.find_one_and_update({'code': id},{'$set': {'quantity': prod_units,'total': prod_total}})
    return redirect(url_for('order.update_product_form', id = id))
        
@ord.route('/objeto/<string:id>/insertar-pago', methods = ['GET'])
def update_pay_form(id):
    if request.method == "GET":
        docs = db['orders']
        item = docs.find_one({'code': id})
        return render_template('order/form_update-pay.html', order = item)
    
@ord.route('/<string:id>/update_insert_pay', methods = ['POST'])
def put_pay(id):
    if request.method == "POST":

        pay = request.form['pay']

        if pay:

            doc = db['orders']
            item = doc.find_one({'code': id})
            ttl = item['total']
            py = float(pay)
        
            if py >= ttl:
                document = Pay(ttl,py)
                doc.find_one_and_update({'code': id},document.insert_document())
                return redirect(url_for('order.get_item', id = id))
            else:
                return redirect(url_for('order.update_pay_form', id = id))

# DELETE #

@ord.route('/delete_order')
def delete_list():
    doc = db['orders']
    doc.delete_many({})
    return redirect(url_for('order.get_list'))

@ord.route('/delete_order/<string:id>')
def delete_item(id):
    doc = db['orders']
    doc.delete_one({'code': id})
    return redirect(url_for('order.get_list'))