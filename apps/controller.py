from .models import *

class controller:

    def addUser(username, email, password):
        new_user = Users(username = username ,email=email, password= password) 
        db.session.add(new_user)
        db.session.commit()
        return new_user


