from app.models._functions_ import code_doc, datetime_doc

class Customer:
    def __init__(self, name, surname, birth, sex, mail, phone):
        self.name = str(name)
        self.surname = str(surname)
        self.birth = str(birth)
        self.sex = str(sex)
        self.mail = str(mail)
        self.phone = str(phone)
        
    def insert_doc(self):
        code = code_doc(16)
        name = self.name
        surname = self.surname
        birth = self.birth
        sex = self.sex
        mail = self.mail
        phone = self.phone
        post = datetime_doc()
        document = {'code': code,'date': {'post': post,'put': post},'name': name,'surname': surname,'birth': birth,'sex': sex,'mail': mail,'phone': phone}
        return document
    
    def select_doc(self):
        name = self.name
        surname = self.surname
        birth = self.birth
        sex = self.sex
        mail = self.mail
        phone = self.phone
        document = {'name': name,'surname': surname,'birth': birth,'sex': sex,'mail': mail,'phone': phone}
        return document

    def update_doc(self):
        name = self.name
        surname = self.surname
        birth = self.birth
        sex = self.sex
        mail = self.mail
        phone = self.phone
        put = datetime_doc()
        document = {'$set': {'date.put': put, 'name': name,'surname': surname,'birth': birth,'sex': sex,'mail': mail,'phone': phone}}
        return document 