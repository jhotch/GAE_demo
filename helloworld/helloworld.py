import cgi
import datetime
import time
import urllib
import webapp2
import jinja2
import os
import json
import logging

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
	expectedArrivalDate = db.DateTimeProperty()
	expectedArrivalTime = db.DateTimeProperty()
	actualArrivalTime = db.DateTimeProperty()
	actualDepartureTime = db.DateTimeProperty()

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
        
	def post(self):
		self.methods = RPCMethods()
		
		args = json.loads(self.request.body)
		func, args = args[0], args[1:]

		if func[0] == '_':
			self.error(403) # access denied
			return

		func = getattr(self.methods, func, None)
		if not func:
			self.error(404) # file not found
			return

		jsonResult = func(*args)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(jsonResult)
		
class RPCMethods:
	""" Defines the methods that can be RPCed. NOTE: Do not allow remote callers access to private/protected "_*" methods. """
	def GetAllGreetings(self):
		greetings_query = Greeting.all().order('-date')
		greetings = greetings_query.fetch(10)
		jsonResult = to_json(greetings)
		return jsonResult
		
	def AddVisitor(self, argsArray):
		visitor = Visitor()
		visitor.name = argsArray[0].get("value")
		visitor.escortName = argsArray[1].get("value")
		visitor.expectedArrivalDate = datetime.datetime.strptime(argsArray[2].get("value"), "%Y-%m-%d")
		visitor.expectedArrivalTime = datetime.datetime.strptime(argsArray[3].get("value"), "%H:%M")
		visitor.put()
		logging.info(visitor.key())
		#jsonVisitorKey = json.dumps(visitor.key(), cls=JSONEncoder)
		return "jsonVisitorKey"

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