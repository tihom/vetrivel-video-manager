'use strict';

Polymer({
  'is': 'vvm-team-page',
  properties: {
    team: {
      type: Object
    }
  },
  attached: function() {
    let teamDao = new VVM.TeamDao();
    teamDao.getTeam().then(
      (team) => {
        this.team = team;
      });
  },
  _newMemberButtonTapped: function() {
    console.log(arguments);
  },
  _memberTapped: function() {
    console.log(arguments);
  }
});
