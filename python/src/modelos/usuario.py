from flask_login import UserMixin

class Usuario(UserMixin):

    def __init__(self, id:int, username:str)->None:
        
        self.id=id
        self.username=username