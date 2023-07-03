from agrictrack import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) # nullable=False means that the field can't be empty
    email = db.Column(db.String(120), unique=True, nullable=False) # unique=True means that the field can't be repeated
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # default='default.jpg' means that if the user doesn't have an image, a default image will be assigned to him/her
    password = db.Column(db.String(60), nullable=False) # 60 is the maximum number of characters allowed for the password

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    
