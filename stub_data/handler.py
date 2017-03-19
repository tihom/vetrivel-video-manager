#!/usr/bin/env python

import copy
import datetime
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
    default_origin = app_identity.get_default_version_hostname()
    if (source_host_port != default_origin and
        (not source_host_port.endswith('-dot-' + default_origin))):
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


_MEMBERS = [
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
    {
      'id': str(uuid.uuid1()),
      'name': 'Michael',
      'phone': '+91 94430 28947',
      'email': 'thedude@michael.co',
    },
    ]
class GetTeamHandler(webapp2.RequestHandler):
  @XsrfValidated
  def get(self):
    team = {
      'name': 'Test team',
      'members': _MEMBERS,
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


class GetAssignmentsHandler(webapp2.RequestHandler):
  @XsrfValidated
  def get(self):
    tasks = [
        {
          'state': 'available',
        },
        {
          'id': 133,
          'task': 'Subtitle translation',
          'video': {
            'id': 'w0ZQvZLx2KA',
            'title': '''Number Theory: Fermat's Little Theorem''',
          },
          'state': 'assigned',
          'startDate': 'Dec 27, 2016',
        },
        {
          'id': 127,
          'task': 'Subtitle translation',
          'video': {
            'id': 'h_--qw-fv3k',
            'title': 'Decision making | Processing the Environment | MCAT | Khan Academy',
          },
          'state': 'assigned',
          'startDate': 'Dec 5, 2016',
        },
        ]

    assignments = []
    for t, m in zip(tasks, _MEMBERS):
      assn = copy.copy(t)
      assn['owner'] = m
      assignments.append(assn)

    response = {
        'assignments': assignments,
        }
    _WriteJson(self.response, response)


class MarkAssignmentHandler(webapp2.RequestHandler):
  @XsrfValidated
  def post(self):
    _WriteJson(self.response, {})


_TASKS = [
    {
      'id': str(uuid.uuid1()),
      'task': 'Subtitle translation',
      'video': {
        'id': '5-ZFOhHQS68',
        'title': '''Newton's first law of motion | Forces and Newton's laws of motion | Physics | Khan Academy''',
      },
    },
    {
      'id': str(uuid.uuid1()),
      'task': 'Subtitle translation',
      'video': {
        'id': 'D1NubiWCpQg',
        'title': '''Newton's first law of motion concepts | Physics | Khan Academy''',
      },
    },
    {
      'id': str(uuid.uuid1()),
      'task': 'Subtitle translation',
      'video': {
        'id': 'CQYELiTtUs9',
        'title': '''More on Newton's first law of motion | Physics | Khan Academy''',
      },
    },
    {
      'id': str(uuid.uuid1()),
      'task': 'Subtitle translation',
      'video': {
        'id': 'ou9YMWlJgkE',
        'title': '''Newton's second law of motion | Forces and Newton's laws of motion | Physics | Khan Academy''',
      },
    },
    {
      'id': str(uuid.uuid1()),
      'task': 'Subtitle translation',
      'video': {
        'id': 'IBS-vKDw9BM',
        'title': '''More on Newton's Second law''',
      },
    },
    {
      'id': str(uuid.uuid1()),
      'task': 'Subtitle translation',
      'video': {
        'id': 'By-ggTfeuJU',
        'title': '''Newton's third law of motion | Forces and Newton's laws of motion | Physics | Khan Academy''',
      },
    },
    {
      'id': str(uuid.uuid1()),
      'task': 'Subtitle translation',
      'video': {
        'id': '9XCugIQXK-s',
        'title': '''More on Newton's Third Law''',
      },
    },
    ]


class GetAvailableTasksHandler(webapp2.RequestHandler):
    @XsrfValidated
    def get(self):
        response = {
          'tasks': _TASKS,
        }
        _WriteJson(self.response, response)


class AssignTaskHandler(webapp2.RequestHandler):
  @XsrfValidated
  def post(self):
    req = json.loads(self.request.body)
    tasks = [t for t in _TASKS if t['id'] == req['taskId']]
    if len(tasks) != 1:
      raise Exception(
          'Expected exactly one task with ID %s, but got %s' % (
              req['taskId'], tasks))
    members = [m for m in _MEMBERS if m['id'] == req['memberId']]
    if len(members) != 1:
      raise Exception('Expected exactly one member with ID %s, but got %s' % (
          req['memberId'], members))

    new_assignment = {
        'id': str(uuid.uuid1()),
        'owner': {
            'id': members[0]['id'],
            'name': members[0]['name'],
            },
        'task': tasks[0]['task'],
        'video': tasks[0]['video'],
        'state': 'assigned',
        'startDate': datetime.date.today().strftime('%b %d, %Y'),
        }
    response = {
        'assignment': new_assignment,
        }
    _WriteJson(self.response, response)


stub_handler = webapp2.WSGIApplication([
    (r'/rest/_/team', GetTeamHandler),
    (r'/rest/_/team/add-member', AddTeamMemberHandler),
    (r'/rest/_/team/members/(.+)', TeamMemberHandler),
    (r'/rest/_/assignments', GetAssignmentsHandler),
    (r'/rest/_/assignments/mark-as-complete', MarkAssignmentHandler),
    (r'/rest/_/assignments/mark-as-abandoned', MarkAssignmentHandler),
    (r'/rest/_/assignments/available-tasks', GetAvailableTasksHandler),
    (r'/rest/_/assignments/assign-task', AssignTaskHandler),
    ], debug=True)
