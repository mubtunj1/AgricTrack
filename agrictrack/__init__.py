from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '87e64dc30b90a0365f606482d18df8dc'

from agrictrack import routes