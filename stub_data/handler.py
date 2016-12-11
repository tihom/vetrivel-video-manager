#!/usr/bin/env python

import json
import logging
import webapp2


class _StubDataHandler(webapp2.RequestHandler):
  def post(self):
    request = json.loads(self.request.body)
    data = self.GetResponse(request)
    if data is None:
      logging.warning('Response not found for request %s', request)
      self.response.set_status(404)
    else:
      self.response.headers.add_header('Content-Type', 'application/json')
      self.response.write(json.dumps(data))

class LookupCurrentUser(_StubDataHandler):
  _responses = {
      't.manki@gmail.com': {
        'known': True,
        'languages': ['EN', 'TA'],
      },
  }

  def GetResponse(self, request):
    resp = LookupCurrentUser._responses.get(request['email'])
    return {'known': False} if resp is None else resp


stub_handler = webapp2.WSGIApplication([
    ('/_/users/lookup', LookupCurrentUser)
    ], debug=True)
