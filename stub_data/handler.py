#!/usr/bin/env python

import json
import logging
import webapp2


def _WriteJson(response, data):
  response.headers.add_header('Content-Type', 'application/json')
  response.write(json.dumps(data))


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

class GetTeam(webapp2.RequestHandler):
  def get(self):
    team = {
      'name': 'Test team',
      'members': [
        {
          'id': 1,
          'name': 'Suresh',
          'phone': '+91 96345 87822',
          'email': 'sureshbabu@gmail.com',
        },
        {
          'id': 2,
          'name': 'Janani',
          'phone': '+91 98433 83153',
          'email': 'jananikumar@gmail.com',
        },
      ],
    }
    _WriteJson(self.response, team)


class TeamMemberHandler(webapp2.RequestHandler):
  def put(self, member_id):
    logging.info('Storing member %s', member_id)
    _WriteJson(self.response, {})

  def delete(self, member_id):
    logging.info('Deleting member %s', member_id)
    _WriteJson(self.response, {})

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
    ('/_/team', GetTeam),
    (r'/_/team/members/(.+)', TeamMemberHandler),
    ('/_/users/lookup', LookupCurrentUser),
    ], debug=True)
