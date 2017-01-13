'use strict';

Polymer({
  is: 'vvm-team-db',
  properties: {
  },

  getTeam: function() {
    return this.$.xhr.get('/_/team');
  },

  addMember: function(newMember) {
    return this.$.xhr.post('/_/team/add-member', newMember);
  },

  updateMember: function(member) {
    return this.$.xhr.put(this._memberUrl(member), member);
  },

  deleteMember: function(member) {
    return this.$.xhr.del(this._memberUrl(member));
  },

  _memberUrl: function(member) {
    return '/_/team/members/' + member.id;
  }
});
