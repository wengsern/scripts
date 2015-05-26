#!/usr/bin/python27

####################################################################
#  Script to list Google Users' aliases from Google Apps for Work  #
####################################################################

from httplib2 import Http
from apiclient import errors
from apiclient.discovery import build
from datetime import datetime, timedelta
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import SignedJwtAssertionCredentials
import json
import re

# Get client email and generate key.pem from Google Developers Console
client_email = 'insert client_email'
with open("key.pem") as f:
  private_key = f.read()

# Note: add "authorized API clients to Google Apps" via Admin Console
# Security -> Advanced Settings -> Authentication -> Manage API Client Access
credentials = SignedJwtAssertionCredentials(client_email, private_key,
     "https://www.googleapis.com/auth/admin.directory.user",
     sub='insert email, example: admin@domain.name')

# Create an httplib2.Http object and authorize it with our credentials
http = Http()
http = credentials.authorize(http)

# Set build version: https://developers.google.com/apis-explorer/#p/
reports_service = build('admin', 'directory_v1', http=http)
users_resource = reports_service.users()

# Set domain name
users_request = users_resource.list(domain="insert domain")
aliases_resource = reports_service.users().aliases()

# print to stdout
print 'User, Aliases'
while users_request is not None:
   users = users_request.execute()
   for user in users['users']:
      # Process data
      user_str = str(user['primaryEmail'])
      user_local_part = re.sub('@domain.name$', '', user_str)
      print user_local_part,",",
      aliases = aliases_resource.list(userKey=user['primaryEmail']).execute()
      if 'aliases' in aliases:
         for alias in aliases['aliases']:
            alias_str = str(alias['alias'])
            alias_local_part = re.sub('@domain.name$', '', alias_str)
            print alias_local_part,
      print ""     
   users_request = users_resource.list_next(users_request, users)
import sys
sys.exit(0)
