import os
from flask import (
    Blueprint,
    request,
    url_for,
    redirect,
    session,
    render_template
)

lp = Blueprint(
    "lp",
    __name__,
    url_prefix="/lp",
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)
