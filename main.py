# -*- coding: utf8 -*-

import sys

# inject './lib' dir in the path so that we can simply do "import ndb"
# or whatever there's in the app lib dir.
if 'lib' not in sys.path:
    sys.path[0:0] = ['lib']

import webapp2, re, os, users
from google.appengine.api import mail
from google.appengine.ext import db
from users import BaseRequestHandler
from secrets import SESSION_KEY

current_path = os.path.abspath(os.path.dirname(__file__))

# webapp2 config
app_config = {
    'webapp2_extras.sessions': {
        'cookie_name': '_simpleauth_sess',
        'secret_key': SESSION_KEY
    },
    'webapp2_extras.auth': {
        'user_attributes': []
    },
    'webapp2_extras.jinja2': {
        'template_path': os.path.join(current_path, 'static/templates')
    }
}

RE_EMAIL = re.compile(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$', re.IGNORECASE)

next_issue = u"In the previous issue, I showed you how to record your podcast. Next issue, I'll show you how to get it online in podcast form. Subscribe before <b>7am Eastern on Friday, February 15th, 2013</b>, to start your subscription with this issue! (Psst. Subscribe this week and send me a message using the <a href=\"/contact/\">contact form</a>, and I'll catch you up by sending you a free copy of the podcast recording issue!)"

class PixedPreview(db.Model):
    date = db.DateProperty(required=True)
    content = db.TextProperty(required=True)

def valid_email(email):
    return RE_EMAIL.match(email)

def valid_message(message):
    return len(message) > 5

def fetch_pixed_preview():
    # todo-devon Write this fetching function with caching
    pass

class MainHandler(BaseRequestHandler):
    def get(self):
        self.render('hero.html', {'next_issue': next_issue})

class PixedHandler(BaseRequestHandler):
    def get(self):
        self.render('pixed.html', {'next_issue': next_issue})

class SlicesHandler(BaseRequestHandler):
    def get(self):
        self.render('slices.html')

class HelpHandler(BaseRequestHandler):
    def get(self):
        self.render('help.html')

class ContactHandler(BaseRequestHandler):
    def get(self):
        self.render('contact.html')
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        message = self.request.get('message')

        email_error = not valid_email(email)
        message_error = not valid_message(message)

        if email_error or message_error:
            error_dict = {'errors': True, 'email_error': email_error, 'email': email, 'message_error': message_error, 'message': message, 'name': name}
            self.render('contact.html', error_dict)
        else:
            if not name:
                name = "Name not provided"
            mail.send_mail('raddevon@gmail.com', 'devon@pixed.us', '%s contact form' % email, "%s\n%s\n%s" % (name, email, message))
            self.render('contactsuccess.html')

class FreebiesHandler(BaseRequestHandler):
    def get(self):
        self.render('freebies.html')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    webapp2.Route('/pixed', webapp2.RedirectHandler,defaults={'_uri': '/pixed/'}),
    ('/pixed/', PixedHandler),
    webapp2.Route('/slices', webapp2.RedirectHandler,defaults={'_uri': '/slices/'}),
    ('/slices/', SlicesHandler),
    webapp2.Route('/help', webapp2.RedirectHandler,defaults={'_uri': '/help/'}),
    ('/help/', HelpHandler),
    webapp2.Route('/contact', webapp2.RedirectHandler,defaults={'_uri': '/contact/'}),
    ('/contact/', ContactHandler),
    webapp2.Route('/freebies', webapp2.RedirectHandler,defaults={'_uri': '/freebies/'}),
    ('/freebies/', FreebiesHandler),
    webapp2.Route('/login/', webapp2.RedirectHandler,defaults={'_uri': '/auth/google/'}),
    webapp2.Route('/logout/', handler='users.AuthHandler:logout', name='logout'),
    webapp2.Route('/auth/<provider>/', handler='users.AuthHandler:_simple_auth', name='auth_login'),
    webapp2.Route('/auth/<provider>/callback/', handler='users.AuthHandler:_auth_callback', name='auth_callback'),
    webapp2.Route('/admin/', handler='admin.AdminHandler')

],config=app_config, debug=True)