"use strict";

ckan.module('mdedit_dicts', function ($, _) {
  return {
    /* options object can be extended using data-module-* attributes */
    options: {
        field_name: 'field_name',
        field_dict: 'field_dict', 
    },

    initialize: function () {
        $.proxyAll(this, /_on/);
        var options = this.options;
        //var field_dict = JSON.parse(options.field_dict);

        console.log("Data initialized for element: ", this.el);

        var wrapper         = $("#input_fields"); //Fields wrapper
        var add_button      = $(".add_field_button"); //Add button ID
       
        var x = 1; //initial text box count
        $('#addbtn').click(function(e){ //on add input button click
            e.preventDefault();
            x++; //text box increment
            $(wrapper).append('<div><input type="text" name="mytext[' + x + ']"/><a href="#" class="remove_field">Remove</a></div>'); //add input box
        });
        $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
            e.preventDefault(); $(this).parent('div').remove(); x--;
        })

        $( "form" ).submit(function( event ) {
            console.log( $( this ).serializeArray() );
            console.log( JSON.stringify($('#input_fields :input').serializeArray()) );
            event.preventDefault();
        });

    }//initialize
  }; // return
}); // module
