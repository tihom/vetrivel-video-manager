'use strict';

Polymer({
  is: 'vvm-team-db',
  properties: {
    _nextId: {
      type: Number,
      value: 0
    }
  },

  getTeam: function() {
    return this.$.xhr.get('/_/team');
  },

  addMember: function(newMember) {
    newMember.id = ++this._nextId;
    return Promise.resolve(newMember);
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
