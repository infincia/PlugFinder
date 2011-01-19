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

class STUNHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(self.request.remote_addr)

class DLHandler(webapp.RequestHandler):
	def get(self,plugid,file):
		plug = Plug.get_by_key_name(plugid)	
		publicip = plug.publicip
		url = "http://" + publicip + "/files/download/" + file
		self.redirect(url)

class MainHandler(webapp.RequestHandler):
	def post(self):
		try:
			sender = self.request.remote_addr
			plugid = self.request.get('plugid')
			localip = self.request.get('localip')
			if Plug.get_by_key_name(plugid):
				plug = Plug.get_by_key_name(plugid)
			else:
				plug = Plug(key_name=plugid)
			plug.publicip = sender
			plug.plugid = plugid
			plug.localip = localip
			plug.put()
		except:
			pass

	def get(self):
		publicip = self.request.remote_addr
		pluglist = Plug.all()
		pluglist.filter("publicip =", publicip)
		if pluglist.count() != 0:
			plugsfound = True
		else:
			plugsfound = False
		template_values = { 'pluglist': pluglist, 'plugsfound': plugsfound }
		path = os.path.join(os.path.dirname(__file__), 'main.html')
		self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/', MainHandler),('/stun', STUNHandler),(r'/dl/(\w+)/(\w+)', DLHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
