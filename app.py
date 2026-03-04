import os
import importlib
from flask import Flask, Blueprint

app = Flask(__name__)
app.secret_key = "mdmdln s asdasnjçasn s asdsnasdfsd"
app.debug = True

def register_blueprints(app):
    routes_dir = os.path.join(os.path.dirname(__file__), "routes")
    routes = [name for name in os.listdir(routes_dir)
              if os.path.isdir(os.path.join(routes_dir, name))
              and "__init__.py" in os.listdir(os.path.join(routes_dir, name))]

    for route in routes:
        try:
            module = importlib.import_module(f"routes.{route}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, Blueprint):
                    app.register_blueprint(attr)
                    break
        except Exception as e:
            pass

register_blueprints(app)
