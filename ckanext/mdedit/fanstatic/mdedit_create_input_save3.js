"use strict";

ckan.module('mdedit_create_input', function ($, _) {
    var next = 0;
    var origin;
    var count;
    var max = 5;
    var values=["", "", "","","",""];
    var labels=["", "", "","","",""];
    var pholder=["", "", "","","",""];
    var field_name;
    var selectoptions="";
    var str_sep = '';
    var white_space = '';

  return {
    initialize: function () {
         console.log("Data initialized for element: ", this.el);
        $.proxyAll(this, /_on/);
        this.el.on('click', this._onClick);
        origin = this.options.origin;
        field_name = this.options.field_name;
        var strcount = this.options.count;
        count = parseInt (strcount);
        str_sep = this.options.strsep;
        white_space = this.options.whitespace;

        selectoptions = this.options.stroptions;

        switch (count)
        {
          case 5:
                values[5] = this.options.field5;
                labels[5] = this.options.label5;
                pholder[5] = this.options.pholder5;
          case 4:
                values[4] = this.options.field4;
                labels[4] = this.options.label4;
                pholder[4] = this.options.pholder4;
          case 3:
                values[3] = this.options.field3;
                labels[3] = this.options.label3;
                pholder[3] = this.options.pholder3;
          case 2:
                values[2] = this.options.field2;
                labels[2] = this.options.label2;
                pholder[2] = this.options.pholder2;

          case 1:
                values[1] = this.options.field1;
                labels[1] = this.options.label1;
                pholder[1] = this.options.pholder1;
        }


        if (origin != "button"){
          // Wird schon durch click initiiert
            this.createInput();
        }
    },

    _onClick: function(event) {

        for (var i = 1; i<=count; i++)
        {
          values[i] = "";
        }

        this.createInput();
    },

    createInput: function () {
        next = next + 1;
        console.log ("CreateInpput");
        // when field or imagename was not filled out last time, it gets filled out with 'true' and therefore it is here set to '' again

        for (var i = 1; i<=count; i++)
        {
          if (values[i]==true)
            values[i] = "";
          if (labels[i]==true)
            labels[i] = "";
          if (pholder[i]==true)
            pholder[i] = "";
        }

      /***************************** new Input and ggf select  ****************************************/

        var newInput = [$(),$(),$(),$(),$(),$()];

        var removeButton = $('<br id="brb' + next + '"><button id="remove-' + next + '" class="btn btn-danger remove-me" >-</button>');


        /**************************************************************/
        //check whether we have a select and convert optionsstring
        var checkselect = selectoptions.toString();

        console.log("*************checkselect:" + checkselect);

        var selectinput = false;

        var corrected_count = count;

        if (checkselect.indexOf('<option') > -1) {

          // NOPE: otpions already transformed
          selectinput = true;
          console.log ("NOPE");

        }
        else if (checkselect.indexOf(str_sep) > -1) {

            selectinput = true;

            // Whitespaces from template string turn into cr here - replaced by ~;
            // reinsert whitespaces here
            var so = selectoptions.replace(/~/g, " ");

            // Separated options via # see mdedit_contains.html!
            so = so.split(/#/);

            // Build options string
            var sostring ="";
            for (var i=0; i< so.length; i+=2){

                sostring+='<option value="';
                sostring+= so[i];

                if (so[i] === values[count])
                    sostring+='" selected>';
                else
                    sostring+='">';
                sostring+= so[i+1];
                sostring+='</option>';
                console.log(so[i]);
                console.log(values[count]);
            }

            console.log(sostring);
            selectoptions = sostring;
        }
        else { // No select field: One more input field
          corrected_count +=1;
        }

        /**************************************************************/

        if (corrected_count > 0)
            $("#field_contains").append(removeButton);

        for (var i = 1; i< corrected_count; i++)
        {
          newInput[i]= $('<br id="br' + i + next + '" ><label id="label-field' + i + next + '" class="control-label" for="field'+ i + next + '">' + labels[i]+ '</label><input  class="input form-control" id="field' + i + next + '" name="'+ field_name + '" type="text" placeholder="'+  pholder[i] + ' "  value="' + values[i] + '" style ="margin-left:2%;margin-bottom:5%"/></input>');
          console.log(newInput[i]);
          $("#field_contains").append(newInput[i]);
        }

        if (selectinput) {
          var newSelect1= $('<br id="br' + count + next + '" ><label id="label-field'+ count + next + '" class="control-label" for="field'+ count + next + '">' + labels[count]+ '</label><select id="field' + count + next + '" name="'+ field_name + '" type="select"  selected="' + values[count] + '" style ="margin-left:2%;margin-bottom:5%"/>');
          var newSelect2= $('</select>');
          var select_options =$(selectoptions);

            if (count > 0) {
              $("#field_contains").append(newSelect1);
              $("#field" + count + next).append(select_options);
              $("#field_contains").append(newSelect2);
            }
         }

        $('.remove-me').click(function(e){
            e.preventDefault();

            var fieldNum = this.id.substr(this.id.indexOf("-") + 1);

            var fieldId, labelId, brId;
            var brb = "#brb" + fieldNum;

            $(this).remove();
            $(brb).remove();

            for (var i = 1; i<= corrected_count; i++){

              fieldId = "#field" +i+ fieldNum;
              labelId = "#label-field" +i+ fieldNum;
              brId = "#br" +i+ fieldNum;
              $(fieldId).remove();
              $(labelId).remove();
              $(brId).remove();

            }

          });

    } // create_input


  }; // return
}); // module
