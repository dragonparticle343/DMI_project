from models._functions_ import code_document, datetime_document

class Customer:
    def __init__(self, name, surname, birth, sex, mail, phone):
        self.name = str(name)
        self.surname = str(surname)
        self.birth = str(birth)
        self.sex = str(sex)
        self.mail = str(mail)
        self.phone = str(phone)
        
    def insert_document(self):
        code = code_document()
        name = self.name
        surname = self.surname
        birth = self.birth
        sex = self.sex
        mail = self.mail
        phone = self.phone
        post = datetime_document()
        document = {'code': code,'date': {'post': post,'put': post},'name': name,'surname': surname,'birth': birth,'sex': sex,'mail': mail,'phone': phone}
        return document
    
    def select_document(self):
        name = self.name
        surname = self.surname
        birth = self.birth
        sex = self.sex
        mail = self.mail
        phone = self.phone
        document = {'name': name,'surname': surname,'birth': birth,'sex': sex,'mail': mail,'phone': phone}
        return document

    def update_document(self):
        name = self.name
        surname = self.surname
        birth = self.birth
        sex = self.sex
        mail = self.mail
        phone = self.phone
        put = datetime_document()
        document = {'$set': {'date.put': put, 'name': name,'surname': surname,'birth': birth,'sex': sex,'mail': mail,'phone': phone}}
        return document 