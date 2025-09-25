from flask import Blueprint, render_template, request
from database.database import db_connection

stor = Blueprint("store", __name__, static_folder="static", template_folder="templates")
db = db_connection()

# GET #

@stor.route('/lista', methods = ['GET'])
def get_list():
    if request.method == "GET":
        docs = db['stores']
        list = docs.find({})
        return render_template('store/index.html', stores = list)

@stor.route('objeto/<string:id>', methods = ['GET'])
def get_item(id):
    if request.method == "GET":
        docs = db['stores']
        item = docs.find_one({'code': id})
        return render_template('store/item.html', store = item)