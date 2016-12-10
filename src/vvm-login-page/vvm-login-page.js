Polymer({
  is: 'vvm-login-page',
  properties: {
    // All _user properties are bound to this.$.meta.
    _userId: String,
    _userEmail : String,
    _userFullName: String,
    _userPhotoUrl: String
  },
  _logInSucceeded: function() {
    let profile =
        window.gapi.auth2.getAuthInstance()['currentUser'].get().getBasicProfile();
    this._userId = profile.getId();
    this._userEmail = profile.getEmail();
    this._userFullName = profile.getName();
    this._userPhotoUrl = profile.getImageUrl();

    this.fire('login-complete');
  }
});
