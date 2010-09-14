#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from models import *
import logging

class MainHandler(webapp.RequestHandler):
	
	def post(self):
		sender = self.request.remote_addr
		if self.request.get('plugip'):
			if Plug.get_by_key_name(sender):
				plug = Plug.get_by_key_name(sender)
			else:
				plug = Plug(key_name=sender)
			plug.publicip = sender
			plug.plugip = self.request.get('plugip')
			plug.put()
		else:
			pass
	
	def get(self):
		plugip = ''
		string = ''
		pluglist = db.GqlQuery("SELECT * FROM Plug")
		if pluglist.count() != 0:
			for plug in pluglist:
				if plug.publicip == self.request.remote_addr:
					string = '<span><br/><br/><br/><img src="/images/up.png"/><br/><br/><br/>Plug found! Its current IP address is ' 
					string += plug.plugip
					string += '</span>'
					#logging.info('string is %s' % string)
				else:
					pass
		if string == '':
			#logging.info('no plug found')
			#logging.info('string is %s' % string)
			string = '''<span><br/><br/><br/><img src="/images/down.png"/><br/><br/><br/>Could not find a plug at your location, please make sure your plug can reach the internet</span>'''
		#template_values = { 'user': user, 'serverlist': serverlist, }	
		template_values = { 'string': string }
		path = os.path.join(os.path.dirname(__file__), 'main.html')
		self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
