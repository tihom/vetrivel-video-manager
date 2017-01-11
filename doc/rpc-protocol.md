# Vetrivel Video Manager RPC APIs
This document specifies the interface between JavaScript that runs in the
browser and the Python code that runs on App Engine server. Requests are made
as `XmlHTTPRequest`s (*XHRs* from here on); request and response objects are
encoded as [JSON](http://json.org/).

## Making requests
### Authentication
All of the API methods are accessible only when the user is signed into the
application. Currently, signing in with a
[Google account](https://en.wikipedia.org/wiki/Google_Account) is the only
option. Any request that is not authenticated, i.e. not signed in, will be
served a [403 response](https://httpstatuses.com/403). Any method that does not
require the user to be signed in will be explicitly marked as such.

### XSRF prevention
TODO: provide XSRF prevention information.

### APIs
## Team information
### GET /_/team
This method does not accept any input. It returns the currently logged-in
user's team as a JSON object.

### POST /_/team/members/add
This method accepts an incomplete member object (as a JSON object) as the POST
body input and persists the new team member. Specifically, the input member
must not have a member ID. Returns a JSON representation of the newly-added
member with fields like member ID filled in.

### PUT /_/team/members/:memberId
This method updates the member with the specified member ID (:memberId in the
URL). Returns a JSON representation of the updated member.

### DELETE /_/team/members/:memberId
This method deletes the member with the specified member ID (:memberId in the
URL). When successful, responds with a "204 No Content" response.
