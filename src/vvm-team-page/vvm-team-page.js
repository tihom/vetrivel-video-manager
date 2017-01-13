'use strict';

Polymer({
  'is': 'vvm-team-page',
  properties: {
    team: {
      type: Object,
      value: {
        members: []
      }
    },
    _memberEditorAction: {
      type: String
    },
    _editedMember: {
      type: Object
    }
  },
  attached: function() {
    this.$.teamDb.getTeam().then(
      (team) => {
        this.team = team;
      });
  },
  _isAdding: function(action) {
    return action === 'add';
  },
  _newMemberButtonTapped: function() {
    console.log(arguments);
    this._memberEditorAction = 'add';
    this._editedMember = {};
    this.$.editorDialog.open();
  },
  _memberTapped: function(evt) {
    this._memberEditorAction = 'edit';
    this._editedMember = evt.model.member;

    this._editedIndex = this.team.members.findIndex(
        m => m.id === this._editedMember.id, this);
    if (this._editedIndex === -1) {
      throw new Error('Could not find index for edited member.');
    }

    this.$.editorDialog.open();
  },
  _memberSaveButtonTapped: function(evt) {
    if (this._memberEditorAction === 'add') {
      this.$.teamDb.addMember(this._editedMember).then(
          member => {
            this.push('team.members', member);
            this.notifyPath('team.members');
          },
          error => {
            console.log(error);
            evt.preventDefault();
            alert('Adding member failed.');
          });
    } else if (this._memberEditorAction === 'edit') {
      this.$.teamDb.updateMember(this._editedMember)
          .then(
              member => {
                // http://stackoverflow.com/a/32083884/13326
                ['name', 'phone', 'email'].forEach(
                    field => {
                      this.notifyPath(
                          ['team.members', this._editedIndex, field]);
                    },
                    this);
              })
          .catch(
              error => {
                console.log(error);
                evt.preventDefault();
                alert('Editing member failed.');
              });
    } else {
      throw new Error('Unknown action: ' + this._memberEditorAction);
    }
  },
  _memberDeleteButtonTapped: function() {
    let okToDelete = window.confirm(`This will delete ${this._editedMember.name}.`);
    if (!okToDelete) {
      return;
    }

    this.$.teamDb.deleteMember(this._editedMember).then(
        () => {
          this.splice('team.members', this._editedIndex, 1);
          this.notifyPath('team.members');
          this.$.editorDialog.close();
        },
        error => {
          console.log(error);
          alert('Deleting member failed.');
        });
  }
});
