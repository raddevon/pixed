import webapp2, jinja2, os
from lib import chimpy, AmazonSignatureUtil

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'static/templates')))

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
        self.render('hero.html', {'slices-sub': False, 'pixed-sub': False})

class PaymentHandler(Handler):
    """Processes return data from Amazon after payment"""
    def get(self):
        sig = AmazonSignatureUtil.AmazonSignatureUtil('AKIAI5DZUI3IEJ4MCKRQ','00PlWeg9jzk4PHGwtUz4ddPQhL9zX5LYKBWTFNOQ')
        if sig.verify('http://www.pixed.us/success', self.request.GET):
            paymentEmail = self.request.get('customerEmail')
            name = self.request.get('customerName')
            chimp = chimpy.Connection('b08025f9fdc60b1144be7d11c009285e-us6')
            fname, lname = name.split(' ')
            if lname or fname:
                chimp.list_subscribe('a46baaaf4e', email, {'FNAME':fname, 'LNAME':lname})
            else:
                chimp.list_subscribe('a46baaaf4e', email, {})
            self.render('success.html', {'pixed-sub': True})
        else:
            errors = ['Something went wrong with your payment.']
            self.render('error.html', {'errors': errors})

class EmailHandler(Handler):
    """Submits user's preferred e-mail to Mailchimp"""
    def post(self, email, fname=None, lname=None):
        if lname or fname:
            chimp.list_subscribe('a46baaaf4e', email, {'FNAME':fname, 'LNAME':lname})
        else:
            chimp.list_subscribe('a46baaaf4e', email, {})


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/success', PaymentHandler),
    ('/complete', EmailHandler)

], debug=True)