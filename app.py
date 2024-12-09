import os

from app_logic.init_app import create_app
from apis import register_apis


app = create_app(__name__, os.path.abspath("templates"))

register_apis(app, __name__)
