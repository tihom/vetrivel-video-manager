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
## User information
### GET /_/me
TODO

### PUT /_/me
TODO
