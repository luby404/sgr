import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    render_template
)

cardapio = Blueprint(
    "cardapio",
    __name__,
    url_prefix="/cardapio",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)


@cardapio.get("/")
def index():
    
    return render_template("cardapio.index.html")