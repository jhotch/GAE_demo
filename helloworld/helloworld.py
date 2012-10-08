import cgi
import datetime
import urllib
import webapp2
import jinja2
import os
import json

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Greeting(db.Model):
  author = db.StringProperty()
  content = db.StringProperty(multiline = True)
  date = db.DateTimeProperty(auto_now_add = True)
  
class Visitor(db.Model):
	name = db.StringProperty()
	escortName = db.StringProperty()
	expectedArrival = db.DateTimeProperty()
	actualArrival = db.DateTimeProperty()
	actualDeparture = db.DateTimeProperty()

def guestbook_key(guestbook_name = None):
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')
  
def to_json(gql_object):
	result = []
	for item in gql_object:
		result.append(dict([(p, getattr(item, p)) for p in item.properties()]))
	return json.dumps(result, cls=JSONEncoder)
  
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'): #handles both date and datetime objects
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)  
  
class RPCHandler(webapp2.RequestHandler):
		
	def get(self):
		guestbook_name = self.request.get('guestbook_name')
		greetings_query = Greeting.all().order('-date')
		greetings = greetings_query.fetch(10)
		jsonGreetings = to_json(greetings)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(jsonGreetings)

class MainPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name')
        greetings_query = Greeting.all().ancestor(guestbook_key(guestbook_name)).order('-date')
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
  def post(self):
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
      greeting.author = users.get_current_user().nickname()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))


app = webapp2.WSGIApplication([('/', MainPage),('/sign', Guestbook),('/rpc', RPCHandler)],debug = True)