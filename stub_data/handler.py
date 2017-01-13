#!/usr/bin/env python

import json
import logging
import urlparse
import uuid
import webapp2

from google.appengine.api.app_identity import app_identity


def _WriteJson(response, data):
  response.headers.add_header('Content-Type', 'application/json')
  response.write(json.dumps(data))


def _ExtractHostPort(url):
  parsed_url = urlparse.urlparse(url)
  result = ''
  if parsed_url.hostname is not None:
    result += parsed_url.hostname
  if parsed_url.port is not None:
    result += ':' + str(parsed_url.port)
  return result


def _SourceHostPort(request):
  if 'Origin' in request.headers:
    return _ExtractHostPort(request.headers['Origin'])
  elif 'Referer' in request.headers:
    return _ExtractHostPort(request.headers['Referer'])
  else:
    return '(unknown)'


def XsrfValidated(fn):
  # XSRF prevention done based on advice from
  # https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet
  # We apply all of section 2.1 (identifying source origin) and
  # section 2.2.4 (use of custom request headers).
  def wrapper(handler, *args, **kwargs):
    source_host_port = _SourceHostPort(handler.request)
    if source_host_port != app_identity.get_default_version_hostname():
      handler.response.headers.add_header('Content-Type', 'text/plain')
      handler.response.set_status(403)
      handler.response.write(
          'Declining request from origin %s.' % source_host_port)
      return

    app_name = handler.request.headers.get('X-App-Name')
    if app_name != 'VVManager':
      handler.response.headers.add_header('Content-Type', 'text/plain')
      handler.response.set_status(403)
      handler.response.write('Declining request without magic header.')
      return

    return fn(handler, *args, **kwargs)
  return wrapper


class _StubDataHandler(webapp2.RequestHandler):
  @XsrfValidated
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
  @XsrfValidated
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
  @XsrfValidated
  def put(self, member_id):
    _WriteJson(self.response, {})

  @XsrfValidated
  def delete(self, member_id):
    _WriteJson(self.response, {})


class AddTeamMemberHandler(webapp2.RequestHandler):
  @XsrfValidated
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
