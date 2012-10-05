import webapp2, jinja2
import os

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
        self.response.out.write('Hello world!')


app = webapp2.WSGIApplication([
    ('/', MainHandler),

], debug=True)

