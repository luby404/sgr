import os
from flask import Flask



from ext.routes import init_routes
from ext.admin import init_admin
from models import init_db

app = Flask(__name__)
app.secret_key = "mdmdln s asdasnjçasn s asdsnasdfsd"

init_db()
init_admin(app)
init_routes(app)



