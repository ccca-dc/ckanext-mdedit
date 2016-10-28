// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";

ckan.module('ccca_tooltip', function ($, _) {
  return {
    initialize: function () {
      console.log("Tooltip: I've been initialized for element: ", this.el);
    },
    };
  });
