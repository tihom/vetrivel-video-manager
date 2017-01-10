Polymer({

  is: 'vvm-app',

  properties: {
    page: {
      type: String,
      observer: '_pageChanged',
      value: 'team'
    }
  },

  _pageChanged: function(page) {
    console.log(page);
    let eltName = `vvm-${page}-page`;
    console.log(`Importing ../${eltName}/${eltName}.html`);
    this.importHref(this.resolveUrl(`../${eltName}/${eltName}.html`), null, null, true);
  },

  _loginComplete: function() {
    // TODO: check if the user is new. For now, assuming they *are* new.
    if (!this.$.meta.byKey('/user/id')) {
      throw new Error('User has not logged in.');
    }

    this.$.xhr.post('/_/users/lookup', {
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
