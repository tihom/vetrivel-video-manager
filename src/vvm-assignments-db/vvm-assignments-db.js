'use strict';

Polymer({
  is: 'vvm-assignments-db',
  properties: {
  },

  getCurrentAssignments: function() {
    return this.$.xhr.get('/rest/_/assignments');
  },

  markAsComplete: function(assignmentId) {
    let request = {
      'assignmentId': assignmentId
    };
    return this.$.xhr.post('/rest/_/assignments/mark-as-complete', request);
  },

  markAsAbandoned: function(assignmentId) {
    let request = {
      'assignmentId': assignmentId
    };
    return this.$.xhr.post('/rest/_/assignments/mark-as-abandoned', request);
  },

  getAvailableTasks: function(memberId) {
    let request = {
      'memberId': memberId
    };
    return this.$.xhr.get('/rest/_/assignments/available-tasks', request);
  },

  assignTask: function(memberId, taskId) {
    let request = {
      'memberId': memberId,
      'taskId': taskId
    };
    return this.$.xhr.post('/rest/_/assignments/assign-task', request);
  }
});
