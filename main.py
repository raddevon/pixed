import webapp2, jinja2, re
import os
from google.appengine.api import mail

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'static/templates')))

RE_EMAIL = re.compile(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$', re.IGNORECASE)

def valid_email(email):
    return RE_EMAIL.match(email)

def valid_message(message):
    return len(message) > 5

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, *a, **kw):
        t = jinja_env.get_template(template)
        return t.render(*a, **kw)
    def render(self, template, *a, **kw):
        self.write(self.render_str(template, *a, **kw))

class MainHandler(Handler):
    def get(self):
        self.render('hero.html')

class PixedHandler(Handler):
    def get(self):
        self.render('pixed.html')

class SlicesHandler(Handler):
    def get(self):
        self.render('slices.html')

class HelpHandler(Handler):
    def get(self):
        self.render('help.html')


class ContactHandler(Handler):
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



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    webapp2.Route('/pixed', webapp2.RedirectHandler,defaults={'_uri': '/pixed/'}),
    ('/pixed/', PixedHandler),
    webapp2.Route('/slices', webapp2.RedirectHandler,defaults={'_uri': '/slices/'}),
    ('/slices/', SlicesHandler),
    webapp2.Route('/help', webapp2.RedirectHandler,defaults={'_uri': '/help/'}),
    ('/help/', HelpHandler),
    webapp2.Route('/contact', webapp2.RedirectHandler,defaults={'_uri': '/contact/'}),
    ('/contact/', ContactHandler)

], debug=True)