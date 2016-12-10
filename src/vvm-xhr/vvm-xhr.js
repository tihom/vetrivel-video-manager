Polymer({
  is: 'vvm-xhr',
  properties: {
  },
  post: function(url, body) {
    this.$.ajax.method = 'POST';
    this.$.ajax.url = url;
    this.$.ajax.body = body;
    return this.$.ajax.generateRequest().completes.then((request) => {
      // request is the iron-request.
      return Promise.resolve(request.response);
    }).catch((error) => {
      return Promise.reject(error);
    });
  }
});
