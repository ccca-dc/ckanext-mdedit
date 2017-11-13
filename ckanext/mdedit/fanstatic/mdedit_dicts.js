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
        // auto collapse all panels
        $(".panel-collapse").hide();

        var wrapper = $("#fs-"+options.field_name); //Fields wrapper

        $('#add-'+options.field_name).click(function(e){ //on add input button click
            e.preventDefault();

            // Grab the ID from last node
            var x = $(".inp-"+options.field_name)[$(".inp-"+options.field_name).length - 1].attributes.id.value.match(/\d+$/);

            // Get first node (no remove button there)
            var NewElement=$(".inp-"+options.field_name)[0].cloneNode(true);  
            // Increment the ID
            NewElement.attributes.id.value = NewElement.attributes.id.value.replace(0,parseInt(x)+1);

            // Create remove field and append to modified Node
            var remove_button = $('<a>',{
              class: 'rm-'+options.field_name,
              text: 'Remove',
              href: '#'
            }).appendTo(NewElement);


            // Append node on wrapper
            $(wrapper).append(NewElement);

            // Increment ID
        });

        $(wrapper).on("click",".rm-"+options.field_name, function(e){ //user click on remove text
            e.preventDefault(); $(this).parent('div').remove();
        });

        $(".panel-heading").click(function () {
          // toggle current
          $(this).parent().find(".panel-collapse").toggle();
        });


        $( "form" ).submit(function( event ) {
            // Define empty array
            var outList = [];
            // Loop over all input collections
            $(".inp-"+options.field_name).each(function (i,el) {
              var inputFields = el.getElementsByTagName('input');
              // Define emtpy dict
              var dict = {};
              // Add all inputFields from collection to dict
              for (var i = 0; i < inputFields.length; i++) {
                dict[inputFields[i].name.split("-").pop()] = inputFields[i].value;
              };
              // Add dict from input collection to array 
              outList.push(dict);
            });
            console.log(JSON.stringify(outList));
            //event.preventDefault();
            var outpField = $('#fs-'+options.field_name);

            // Remove input field with json data if user came with back button in browser
//            if (document.contains(document.getElementById(options.field_name))) {
//              document.getElementById(options.field_name).remove();
//            };  

            // Append one input field with json data
            var jsonInp = $('<input>',{
              name: options.field_name,
              id: options.field_name,
              type: 'hidden',
              value: JSON.stringify(outList),
            }).insertAfter(outpField);
        });

    }//initialize
  }; // return
}); // module
