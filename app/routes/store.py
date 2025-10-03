from flask import Blueprint, render_template, request
from app.database.nosql import db_connection

bpStore = Blueprint("store", __name__)
db = db_connection()
docs = db['stores']

# GET #
@bpStore.route('/lista', methods = ['GET'])
def get_list():
    if request.method == "GET": 
        list = docs.find({})
        return render_template('store.list.html', stores = list, title = 'Sucursales')

@bpStore.route('objeto/<string:id>', methods = ['GET'])
def get_item(id):
    if request.method == "GET":
        item = docs.find_one({'code': id})
        return render_template('store.item.html', store = item)
