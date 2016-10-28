// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('ccca_popover', function ($, _) {
  return {
    initialize: function () {
      console.log("Popover: I've been initialized for element: ", this.el);

      $.proxyAll(this, /_on/);

      this.sandbox.subscribe('standard_popover_clicked',
                             this._onPopoverClicked);
    },
      teardown: function() {
      this.sandbox.unsubscribe('standard_popover_clicked',
                               this._onPopoverClicked);
                           },

    };
  });
