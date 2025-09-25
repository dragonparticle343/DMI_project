from models._functions_ import code_document, datetime_document

class Product:
    def __init__(self, name, price, department, article, description, content):
        self.name = str(name)
        self.price = float(price)
        self.department = str(department)
        self.article = str(article)
        self.description = str(description)
        self.content = str(content)
        
    def content_array(self):
        chain = self.content
        token = chain.split(", ")
        return token
    
    def category_object(self):
        department = self.department 
        article = self.article
        category = {'department': department,'article': article}
        return category

    def insert_document(self):
        code = code_document()
        name = self.name
        price = round(self.price,2)
        category = self.category_object()
        description = self.description
        content = self.content_array()
        post = datetime_document()
        document = {'code': code,'date': {'post': post,'put': post},'name': name,'price': price,'category': category,'description': description,'content': content}
        return document
    
    def select_document(self):
        name = self.name
        price = round(self.price,2)
        department = self.department
        article = self.article
        description = self.description
        content = self.content_array()
        document = {'name': name,'price': price,'category.department': department,'category.article': article,'description': description,'content': content}
        return document
    
    def update_document(self):
        name = self.name
        price = round(self.price,2)
        description = self.description
        content = self.content_array()
        put = datetime_document()
        document = {'$set': {'date.put': put,'name': name,'price': price,'description': description,'content': content}}
        return document