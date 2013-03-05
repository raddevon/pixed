from users import BaseRequestHandler, simpleauth_login_required
from lib.wtforms.ext.appengine.db import model_form
from wtforms import widgets as w
from main import PixedPreview

admin_form_classes = []
admin_forms = []

class WidgetPrebind(object):
    def __init__(self, widget, **kwargs):
        self.widget = widget
        self.kw = kwargs

    def __call__(self, field, **kwargs):
        return self.widget(field, **dict(self.kw, **kwargs))

def build_form_class(model, date_fields=(), editor_fields=()):
    field_args = {}
    for field_name in date_fields:
        kw = {'class': 'datepicker'}
        field_args[field_name] = {
            'widget': WidgetPrebind(w.TextInput(), **kw)
        }

    for field_name in editor_fields:
        kw = {'class': 'editor'}
        field_args[field_name] = {
            'widget': WidgetPrebind(w.TextArea(), **kw)
        }

    return model_form(model, field_args=field_args)

# Register models for the admin interface here
admin_form_classes.append(
    build_form_class(PixedPreview, ['date'], ['content'])
)

for form in admin_form_classes:
    admin_forms.append(form())

class AdminHandler(BaseRequestHandler):
    '''
    Handler for the admin interface
    '''
    @simpleauth_login_required
    def get(self):
        # todo-devon Figure out how to test for the authorized user
        print self.current_user

        if admin_forms:
            self.render('admin.html', {'forms': admin_forms})
        else:
            self.render('admin.html', {'error': 'No forms could be generated. This could be because no admin models \
            have been registered.'})