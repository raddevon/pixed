from users import BaseRequestHandler
from lib.wtforms.ext.appengine.db import model_form
from main import PixedPreview

# List of models registered with admin
admin_models = [
    PixedPreview,
]

class AdminHandler(BaseRequestHandler):
    # todo-devon Write handler for an administration interface
    # Check for login
    # If not logged in and if not me, redirect to some other page
    # If logged in, show a page that allows adding of new issue descriptions
    forms = []
    for model in admin_models:
        forms.append(model_form(model, ))