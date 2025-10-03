from app.models._functions_ import code_doc, datetime_doc

class Order:
    
    def __init__(self, stor, store, address, postal, city, state, country, cust, name, surname, pay):
        self.stor = str(stor)
        self.store = str(store)
        self.address = str(address)
        self.postal = str(postal)
        self.city = str(city)
        self.state = str(state)
        self.country = str(country)
        self.cust = str(cust)
        self.name = str(name)
        self.surname = str(surname)
        self.pay = str(pay)

    def insert_doc(self):
        code = code_doc(24)
        date = datetime_doc()
        fullname = '{} {}'.format(self.name,self.surname)
        store = self.store
        street = '{}, {}'.format(self.address,self.postal)
        region = '{}, {}, {}'.format(self.city,self.state,self.country)
        pay = self.pay
        document = {
            'code': code,
            'date': date,
            'customer': fullname,
            'store': store,'street': street,'region': region,
            'method_pay': pay,
            'products': [],
            'quantity': 0,'total': 0,'pay': 0,'change': 0
        }   
        return document

class Article:
    def __init__(self, code, name, price, units):
        self.code = str(code)
        self.name = str(name)
        self.price = float(price)
        self.units = int(units)

    def total_price(self):
        price = self.price
        units = self.units
        subtotal = float(price * units)
        total = round(subtotal, 2)
        return total
    
    def insert_doc(self):
        code = self.code
        name = self.name
        price = self.price
        units = self.units
        subtotal = self.total_price()
        item = {'$addToSet': {'products': {'code': code,'name': name,'price': price,'units': units,'subtotal': subtotal}}}
        return item
    
class Pay:
    def __init__(self, total, pay):
        self.total = float(total)
        self.pay = float(pay)

    def order_change(self):
        total = self.total
        pay = self.pay
        change = pay - total
        return change
    
    def insert_doc(self):
        pay = self.pay
        change = self.order_change()
        document = {'$set': {'pay': pay,'change': change}} 
        return document