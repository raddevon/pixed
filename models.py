from google.appengine.ext import db

class Subscriber(db.Model):
    """Newsletter subscribers"""
    email = db.EmailProperty(required=True)
    paymentEmail = db.EmailProperty()
    paidThrough = db.DateProperty()


