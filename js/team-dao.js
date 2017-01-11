var VVM = VVM || {};
VVM.TeamDao = VVM.TeamDao || class {
  constructor() {
    this._nextId = 0;
  }

  getTeam() {
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
  }

  addMember(newMember) {
    newMember.id = ++this._nextId;
    return Promise.resolve(newMember);
  }

  deleteMember(member) {
    return Promise.resolve({});
  }
};
