#!/usr/bin/env python
#
"""
Copyright (c) 2009, Steve Oliver (steve@xercestech.com)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the 
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY STEVE OLIVER ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL STEVE OLIVER BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;                    
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND 
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""

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
