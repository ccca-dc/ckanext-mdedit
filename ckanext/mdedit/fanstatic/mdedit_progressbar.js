// Enable JavaScript's strict mode. Strict mode catches some common
// programming errors and throws exceptions, prevents some unsafe actions from
// being taken, and disables some confusing and bad JavaScript features.
"use strict";


ckan.module('mdedit_progressbar', function ($, _) {
  var filled = 0;
  var this_module;
  var total_elements=0;

  return {
    initialize: function () {
        console.log("Data initialized for element: ", this.el, this.options,this.sandbox);
        this_module = this; //save for later (on) calls
        total_elements= this.init_total(); // Check number of elements to consider for progressbar;
        filled = this.check_filled();
        var percent = filled +'%';
        if (filled == 100)
             percent = "100% Great! :-)";
        $("#progressbar")
            .progressbar({ value: parseInt(filled), max:100})
            .children('.ui-progressbar-value')
            .html(percent)
            .css("display", "block");

        $.proxyAll(this, /_on/);

        $('#progresselements').on('input textarea select', function (e) {
    //      e.preventDefault(); // Does not take input anymore

           //console.log("********* CHANGE*******");
           if (e.target.name == "contact_info")
                //total_elements = this_module.init_total();
                return; //better :-)

           filled = this_module.check_filled();
           var percent = filled + '%';
           if (filled == 100)
                percent = "100% Great! :-)";

            $( "#progressbar" )
          	 .progressbar({value: parseInt(filled)})
          	 .children('.ui-progressbar-value')
          	 .html(percent)
          	 .css("display", "block");

          });

    }, // initialize
    init_total: function (){

  	     var elements = $('#progresselements input');
         var number = 0;
         // search readonly elements
         for (var i=0; i< elements.length;i++){
            if (!elements[i].id.startsWith ('field-') )
                continue; // Some crazy fields from ckanext-spatial...
            if (!elements[i].readOnly && !elements[i].hidden){
               //console.log(elements[i].id);
                number++;
              }
          }

          elements = $('#progresselements select');
          for (var i=0; i< elements.length;i++){
            // console.log(elements[i].target);
            //  if (elements[i].target.find ('select-field-spatial') > -1)
            //  continue; // Some  fields from ckanext-spatial...

            if (!elements[i].id.startsWith ('field-') )
               continue; // Some crazy fields from ckanext-spatial...

            if (!elements[i].readOnly && !elements[i].hidden){
               //console.log(elements[i].id);
                number++;
              }
           }

          elements = $('#progresselements textarea');
          for (var i=0; i< elements.length;i++){
            //console.log(elements[i].target);
            if (!elements[i].id.startsWith ('field-') )
              continue; // Some crazy fields from ckanext-spatial...
            if (!elements[i].readOnly && !elements[i].hidden){
               //console.log(elements[i].id);
                number++;
              }
           }

           this_module.total_elements = number;
           //console.log("Total elements: " + number);


    },

    check_filled: function (event){

          var filled =0;

        	var total = $('#progresselements input');
          //console.log("Total ", total);

          filled = this_module.calc_filled(total);

          total = $('#progresselements select');
          //console.log("Total ", total);

          filled += this_module.calc_filled(total);

          total = $('#progresselements textarea');
          //console.log("Total ", total);

          filled += this_module.calc_filled(total);

          //console.log("Filled elements: " + filled);
          //console.log("Total elements: " + this_module.total_elements);

          filled = (filled * 100 / this_module.total_elements);
          filled = filled.toPrecision(3);
         	return filled;

    },//check_filled

    calc_filled:   function (elements){
       var number =0;
       //console.log(elements);
        //console.log(elements.length);
        for (var i=0; i< elements.length;i++){
          //console.log(elements[i].value);

          // select-field-spatial, field11, filed21, field31,field41, s2id: somehow from spatial -: ignore
          // our fields start with field- ... hopefully
          if (!elements[i].id.startsWith ('field-') )
            continue; // Some crazy fields from ckanext-spatial or others ...

          if (elements[i].hidden)
              continue; // spatial ..
          if (elements[i].readOnly)
              continue; // automatically filled - not counted
          if (elements[i].value.length != 0){
                 number++;
              //   console.log(elements[i].id);
          }
           else {
            // console.log("Empty: "+ elements[i].id + " Name: " + elements[i].name);
            // console.log(elements[i]);

           }
        }
        return number;
    } // calc_filled

  }; // return

}); //ckan_module
