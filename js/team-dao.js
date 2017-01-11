var VVM = VVM || {};
VVM.TeamDao = VVM.TeamDao || class {
  constructor() {
  }

  getTeam() {
    return Promise.resolve({
      name: 'Test Team',
      members: [
        {
          name: 'Suresh',
          email: 'sureshbabu@gmail.com',
          phone: '+91 96345 87822',
          languages: ['English', 'Tamil']
        },
        {
          name: 'Janani',
          email: 'jananikumar@gmail.com',
          phone: '+91 98433 83153',
          languages: ['English', 'Tamil', 'Hindi']
        }
      ]
    });
  }
};
