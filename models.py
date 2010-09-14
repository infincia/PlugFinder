#!/usr/bin/env python
from google.appengine.ext import db

class Plug(db.Model):
	publicip = db.StringProperty("Public IP address we received the ping from", multiline=False)
	plugip = db.StringProperty("Private IP address the plug reported to us",multiline=False)
	found = db.DateTimeProperty("Date and time plug contacted us", auto_now_add=True)