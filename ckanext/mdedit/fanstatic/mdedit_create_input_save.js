"use strict";

ckan.module('mdedit_create_input', function ($, _) {
    var next = 0;
    var origin;
    var ci_field1;
    var ci_field2;
    var ci_field3;
    var ci_field4;
    var ci_field5;

  return {
    initialize: function () {
         console.log("Data initialized for element: ", this.el);
        $.proxyAll(this, /_on/);
        this.el.on('click', this._onClick);
        origin = this.options.field;

        ci_field1 = this.options.field1;
        ci_field2 = this.options.field2;
        ci_field3 = this.options.field3;
        ci_field4 = this.options.field4;
        ci_field5 = this.options.field5;

        if(origin !== "button"){
          // Wird schon durch click initiiert
            this.createInput();
        }
    },

    _onClick: function(event) {
        ci_field1 = "";
        ci_field2 = "";
        ci_field3 = "";
        ci_field4 = "";

        this.createInput();
    },

    createInput: function () {
        next = next + 1;

        // when field or imagename was not filled out last time, it gets filled out with 'true' and therefore it is here set to '' again
        if(ci_field1 == true){
            ci_field1 = "";
        }
        if(ci_field2 == true){
            ci_field2 = "";
        }
        if(ci_field3 == true){
            ci_field3 = "";
        }
        if(ci_field4 == true){
            ci_field4 = "";
        }

        console.log("createInput");

        //this adds two input fields with the given text (when pictures previously saved) and one remove button

        var select_options =$('<option value="custodian">Custodian</option><option value="distributor">Distributor</option><option value="originator">Originator</option><option value="owner">Owner</option><option value="pointOfContact">Point of Contact</option><option value="principalInvestigator">Principal Investigator</option><option value="processor">Processor</option><option value="publisher">Publisher</option><option value="resourceProvider">Resource Provider</option><option value="user">User</option><option value="metadataPointofContact">Metadata Point of Contact</option><option value="author">Author</option>');

        var newInputField1 = $('<br id="brn' + next + '" ><label id="label-field1'+ next + '" class="control-label" for="field1' + next + '">Name</label><input  class="input form-control" id="field1' + next + '" name="contact_info" type="text" placeholder="e.g. Joe Example"  value="' + ci_field1 + '" style ="margin-left:2%;margin-bottom:5%"/></input>');
        var newInputField2 =  $('<br id="brd' + next + '" ><label id="label-field3'+ next + '" class="control-label" for="field3' + next + '">Department</label><input  class="input form-control" id="field3' + next + '" name="contact_info" type="text" placeholder="e.g. Department for Geophysics"  value="' + ci_field3 + '" style ="margin-left:2%;margin-bottom:5%"/></input>');
        var newInputField3 =  $('<br id="brm' + next + '" ><label id="label-field2'+ next + '" class="control-label" for="field2' + next + '">Mail</label><input  class="input form-control" id="field2' + next + '" name="contact_info" type="text" placeholder="e.g. joe@example.com"  value="' + ci_field2 + '" style ="margin-left:2%;margin-bottom:5%"/></input>');
        var newSelectRole1= $('<br id="brs' + next + '" ><label id="label-field4'+ next + '" class="control-label" for="field4' + next + '">Role</label><select id="field4' + next + '" name="contact_info" type="selct"  value="' + ci_field4 + '" style ="margin-left:2%;margin-bottom:5%"/>');
        var newSelectRole2= $('</select>');

        var removeButton = $('<br id="brb' + next + '"><button id="remove-' + next + '" class="btn btn-danger remove-me" >-</button>');

        $("#field_contains").append(removeButton);
        $("#field_contains").append(newInputField1);
        $("#field_contains").append(newInputField2);
        $("#field_contains").append(newInputField3);
        $("#field_contains").append(newSelectRole1);
        $("#field4"+ next).append(select_options);
        $("#field_contains").append(newSelectRole2);


        //when pressing the remove button it deletes both input fields and the button
        $('.remove-me').click(function(e){
            e.preventDefault();
            var fieldNum = this.id.substr(this.id.indexOf("-") + 1);
            var f1ID = "#field1" + fieldNum;
            var f2ID = "#field2" + fieldNum;
            var f3ID = "#field3" + fieldNum;
            var f4ID = "#field4" + fieldNum;

            var lf1ID = "#label-field1" + fieldNum;
            var lf2ID = "#label-field2" + fieldNum;
            var lf3ID = "#label-field3" + fieldNum;
            var lf4ID = "#label-field4" + fieldNum;

            var brn = "#brn" + fieldNum;
            var brm = "#brm" + fieldNum;
            var brs = "#brs" + fieldNum;
            var brd = "#brd" + fieldNum;
            var brb = "#brb" + fieldNum;

            $(this).remove();
            $(f1ID).remove();
            $(f2ID).remove();
            $(f3ID).remove();
            $(f4ID).remove();
            $(lf1ID).remove();
            $(lf2ID).remove();
            $(lf3ID).remove();
            $(lf4ID).remove();
            $(brn).remove();
            $(brd).remove();
            $(brm).remove();
            $(brs).remove();
            $(brb).remove();
          });
  }
};
});
