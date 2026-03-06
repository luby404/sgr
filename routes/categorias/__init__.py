import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    render_template
)

categorias = Blueprint(
    "categorias",
    __name__,
    url_prefix="/categorias",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)
