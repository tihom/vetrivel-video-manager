#!/usr/bin/env python

import json
import logging
import uuid
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

class GetTeamHandler(webapp2.RequestHandler):
  def get(self):
    team = {
      'name': 'Test team',
      'members': [
        {
          'id': str(uuid.uuid1()),
          'name': 'Suresh',
          'phone': '+91 96345 87822',
          'email': 'sureshbabu@gmail.com',
        },
        {
          'id': str(uuid.uuid1()),
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


class AddTeamMemberHandler(webapp2.RequestHandler):
  def post(self):
    member = json.loads(self.request.body)
    member['id'] = str(uuid.uuid1())
    _WriteJson(self.response, member)


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
    (r'/_/team', GetTeamHandler),
    (r'/_/team/add-member', AddTeamMemberHandler),
    (r'/_/team/members/(.+)', TeamMemberHandler),
    (r'/_/users/lookup', LookupCurrentUser),
    ], debug=True)
