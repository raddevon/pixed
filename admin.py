from users import BaseRequestHandler, simpleauth_login_required
from lib.wtforms.ext.dateutil.fields import DateField
from lib.wtforms.fields.simple import TextField, TextAreaField
from lib.wtforms.ext.appengine.db import model_form
from main import PixedPreview

admin_forms = []

# Generate form instances from admin_models
def build_form_class(model, date_fields=None, wysiwyg_fields=None):
    form =  model_form(model)
    for field in form:
        if field.__name__ in date_fields:
            field = DateField(_class="datepicker")
        if field.__name__ in wysiwyg_fields:
            field = TextAreaField(_class="wysiwyg")

    admin_forms.append(form)

build_form_class(PixedPreview, 'date', 'content')

class AdminHandler(BaseRequestHandler):
    '''
    Handler for the admin interface
    '''
    @simpleauth_login_required
    def get(self):
        print self.current_user
        forms = []

        if admin_forms:
            # For each registered model
            for form in admin_forms:
                form_instance = form()
                forms.append(form_instance)
            self.render('admin.html', {'forms': forms})
        else:
            self.render('admin.html', {'error': 'No forms could be generated. This could be because no admin models have been registered.'})