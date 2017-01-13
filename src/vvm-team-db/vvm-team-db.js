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
    return Promise.resolve({
      name: 'Test Team',
      members: [
        {
          id: ++this._nextId,
          name: 'Suresh',
          email: 'sureshbabu@gmail.com',
          phone: '+91 96345 87822',
          languages: ['English', 'Tamil']
        },
        {
          id: ++this._nextId,
          name: 'Janani',
          email: 'jananikumar@gmail.com',
          phone: '+91 98433 83153',
          languages: ['English', 'Tamil', 'Hindi']
        }
      ]
    });
  },

  addMember: function(newMember) {
    newMember.id = ++this._nextId;
    return Promise.resolve(newMember);
  },

  updateMember: function(member) {
    return Promise.resolve({});
  },

  deleteMember: function(member) {
    return Promise.resolve({});
  }
});
