Polymer({

  is: 'vvm-app',

  properties: {
  },
  observers: [
    '_pageChanged(routeData.page)'
  ],

  attached: function() {
    // TODO: Choose the default page smartly.
    this.set('routeData.page', 'assignments');
  },

  _pageChanged: function(page) {
    if (!page) {
      return;
    }
    let eltName = `vvm-${page}-page`;
    this.importHref(this.resolveUrl(`../${eltName}/${eltName}.html`), null, null, true);
  },

  _loginComplete: function() {
    // TODO: check if the user is new. For now, assuming they *are* new.
    if (!this.$.meta.byKey('/user/id')) {
      throw new Error('User has not logged in.');
    }

    this.$.xhr.post('/rest/_/users/lookup', {
      'email': this.$.meta.byKey('/user/email')
    }).then((response) => {
      console.log(response);
      this.page = 'edit-user';
    }).catch((error) => {
      console.log('User lookup XHR error: ', error);
    });
  },

  _loginStateChanged: function(e) {
    if (!e.target.isAuthorized) {
      this.page = 'login';
    }
  },

});
