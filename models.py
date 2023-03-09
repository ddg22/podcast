# Importo da flask_login la classe user predefinita
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, name, surname, creator, password):
        # Aggiungo i dati che mi interessano alla classe User
        self.id = id
        self.email = email
        self.name = name
        self.surname = surname
        self.creator = creator
        self.password = password

        return