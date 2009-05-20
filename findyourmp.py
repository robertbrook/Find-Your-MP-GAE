import cgi
import yaml
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
        <head><title>Find Your MP</title></head>
        <body>
          <form action="/search" method="post">
            <input name="postcode" type="text" size="24"/>
            <input type="submit" value="Search by postcode">
          </form>
        </body>
      </html>""")


class SearchResults(webapp.RequestHandler):
  def post(self):
    thepostcode = cgi.escape(self.request.get('postcode'))
    result = urlfetch.fetch("http://findyourmp.parliament.uk/postcodes/" + thepostcode + ".yaml")
    theresult = result.content
    data = theresult
	# if result.status_code == 200:
	# 	  doSomethingWithResult(result.content)
    
	
    self.response.out.write('<html><title>Find Your MP</title></head><body>')
    loaded = yaml.load(data)
    # self.response.out.write(loaded)
        
    self.response.out.write("<p>The postcode is in the Westminster constituency of " + loaded['constituency_name'])
    self.response.out.write("</p><p>The sitting Member is " + loaded['member_name'] + "</p>")
    self.response.out.write('</body></html>')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/search', SearchResults)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()