Polymer({
  is: 'vvm-xhr',
  properties: {
  },
  get: function(url) {
    return this._sendRequest('GET', url);
  },
  post: function(url, body) {
    return this._sendRequest('POST', url, body);
  },
  put: function(url, body) {
    return this._sendRequest('PUT', url, body);
  },
  del: function(url) {
    return this._sendRequest('DELETE', url);
  },
  _sendRequest: function(method, url, body) {
    this.$.ajax.method = method;
    this.$.ajax.url = url;
    this.$.ajax.body = body;
    return this.$.ajax.generateRequest().completes.then(
        request => {
          // request is the iron-request.
          return Promise.resolve(request.response);
        },
        error => {
          return Promise.reject(error);
        });
  }
});
