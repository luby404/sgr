import os
from flask import *

from .views import pages

dashboard = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

@dashboard.get("/")
@dashboard.get("/<name>")
def index(name=None):
    if not name:
        name = "home"
    
    
    class Dados:
        ...
    
    if name in pages:
        print(name)
        Dados.view =  render_template(pages[name], dados=Dados)
    else:
        return render_template("404.html")

    return render_template("dh.index.html", dados=Dados)





