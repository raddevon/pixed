from users import BaseRequestHandler, simpleauth_login_required
from lib.wtforms.ext.appengine.db import model_form
from main import PixedPreview

# List of models registered with admin
admin_models = [
    PixedPreview,
]

admin_forms = []

# Generate form instances from admin_models
if admin_models:
    for model in admin_models:
        admin_forms.append(model_form(model))

class AdminHandler(BaseRequestHandler):
    # todo-devon Write handler for an administration interface
    # Check for login
    # If not logged in and if not me, redirect to some other page
    # If logged in, show a page that allows adding of new issue descriptions
    @simpleauth_login_required
    def get(self):
        print self.current_user
        forms = []

        if admin_models:
            # For each registered model
            for form in admin_forms:
                form_instance = form()
                forms.append(form_instance)

            self.render('admin.html', {'forms': forms})
        else:
            self.render('admin.html', {'error': 'No forms could be generated. This could be because no admin models have been registered.'})
