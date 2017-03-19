Polymer({
  'is': 'vvm-assignments-page',
  properties: {
    assignments: {
      type: Array,
      value: []
    },
    availableTasks: {
      type: Array,
      value: []
    }
  },

  _STATE_AVAILABLE: 'available',

  attached: function() {
    this.$.assignmentsDb.getCurrentAssignments().then(
        response => {
          this.assignments = response.assignments;
        });
  },

  _isAvailable: function(assignment) {
    return assignment.state === this._STATE_AVAILABLE;
  },

  _availableMemberTapped: function(evt) {
    this.$.assignmentsDb.getAvailableTasks(evt.model.assn.owner.id).then(
        response => {
          this._currentAssignment = evt.model.assn;
          this._currentIndex = this.assignments.findIndex(
              a => a.owner.id === this._currentAssignment.owner.id, this);
          if (this._currentIndex === -1) {
            throw new Error('Could not find index in assignments array');
          }

          this.availableTasks = response.tasks;
          this.$.addAssignmentDialog.open();
        },
        error => {
          console.log(error);
          alert('Could not get available tasks.');
        });
  },

  _assignButtonTapped: function(evt) {
    if (!this._currentAssignment.owner.id) {
      throw new Error('Don\'t know whom to assign task to');
    }

    let memberId = this._currentAssignment.owner.id;
    let taskId = this.$.taskList.selected;

    this.$.assignmentsDb.assignTask(memberId, taskId).then(
        response => {
          this.set(['assignments', this._currentIndex], response.assignment);

          delete this._currentAssignment;
          delete this._currentIndex;
          this.$.taskList.selected = undefined;

          this.$.addAssignmentDialog.close();
        },
        error => {
          console.log(error);
          alert('Could not save task assignment.');
        });
  },

  _assignmentTapped: function(evt) {
    if (!evt.model.assn.id) {
      throw new Error('Could not find edited assignment');
    }

    this._currentAssignment = evt.model.assn;
    this._currentIndex = this.assignments.findIndex(
        a => a.id === this._currentAssignment.id, this);
    if (this._currentIndex === -1) {
      throw new Error('Could not find index of edited assignment');
    }

    this.$.editAssignmentDialog.open();
  },

  _assertCurrentlyEditing: function() {
    if (!this._currentAssignment.id) {
      throw new Error('Current assignment id is not set.');
    }

    if (this._currentIndex === -1) {
      throw new Error('Current assignment index is not set');
    }
  },

  _unassign: function(assignment) {
    assignment.state = this._STATE_AVAILABLE;
    delete assignment.id;
    delete assignment.task;
    delete assignment.video;
    delete assignment.startDate;

    let copy = Object.assign({}, assignment)
    this.set(['assignments', this._currentIndex], copy);
  },

  _markAsCompleteTapped: function(evt) {
    this._assertCurrentlyEditing();

    this.$.assignmentsDb.markAsComplete(this._currentAssignment.id).then(
        response => {
          this._unassign(this._currentAssignment);
          this.$.editAssignmentDialog.close();
        },
        error => {
          console.log(error);
          alert('Saving assignment failed.');
        });
  },

  _markAsAbandonedTapped: function(evt) {
    this._assertCurrentlyEditing();

    if (!this._currentAssignment.id) {
      throw new Error('No current assignment.');
    }

    this.$.assignmentsDb.markAsAbandoned(this._currentAssignment.id).then(
        response => {
          this._unassign(this._currentAssignment);
          this.$.editAssignmentDialog.close();
        },
        error => {
          console.log(error);
          alert('Saving assignment failed.');
        });
  }
});
