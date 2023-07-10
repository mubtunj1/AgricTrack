from agrictrack import app, db
from agrictrack.models import User


with app.app_context():
    # Create the database
    db.create_all()
    #db.drop_all()
    # users = User.query.all()
    # print(users)
