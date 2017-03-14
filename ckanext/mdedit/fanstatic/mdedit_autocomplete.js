/* An auto-complete module for select and input elements that can pull in
 * a list of terms from an API endpoint (provided using data-module-source).
 *
 * source   - A url pointing to an API autocomplete endpoint.
 * interval - The interval between requests in milliseconds (default: 1000).
 * items    - The max number of items to display (default: 10)
 * tags     - Boolean attribute if true will create a tag input.
 * key      - A string of the key you want to be the form value to end up on
 *            from the ajax returned results
 * label    - A string of the label you want to appear within the dropdown for
 *            returned results
 *
 * Examples
 *
 *   // <input name="tags" data-module="autocomplete" data-module-source="http://" />
 *
 */
this.ckan.module('mdedit_autocomplete', function (jQuery, _) {
  return {
    /* Options for the module */
    options: {
      tags: false,
      key: false,
      label: false,
      items: 10,
      source: null,
      interval: 1000,
      taxonomy_name: '',
      dropdownClass: '',
      containerClass: '',
      i18n: {
        noMatches: _('No matches found'),
        emptySearch: _('Start typing…'),
        inputTooShort: function (data) {
          return _('Input is too short, must be at least one character')
          .ifPlural(data.min, 'Input is too short, must be at least %(min)d characters');
        }
      }
    },

    /* Sets up the module, binding methods, creating elements etc. Called
     * internally by ckan.module.initialize();
     *
     * Returns nothing.
     */
    initialize: function () {
      jQuery.proxyAll(this, /_on/, /format/);
      this.setupAutoComplete();
    },

    /* Sets up the auto complete plugin.
     *
     * Returns nothing.
     */
    setupAutoComplete: function () {
      var settings = {
        width: 'resolve',
        formatResult: this.formatResult,
        formatNoMatches: this.formatNoMatches,
        formatInputTooShort: this.formatInputTooShort,
        dropdownCssClass: this.options.dropdownClass,
        containerCssClass: this.options.containerClass
      };

      // Different keys are required depending on whether the select is
      // tags or generic completion.
      if (!this.el.is('select')) {
        if (this.options.tags) {
          settings.tags = this._onQuery;
        } else {
          settings.query = this._onQuery;
          settings.createSearchChoice = this.formatTerm;
        }
        settings.initSelection = this.formatInitialValue;
      }
      else {
        if (/MSIE (\d+\.\d+);/.test(navigator.userAgent)) {
            var ieversion=new Number(RegExp.$1);
            if (ieversion<=7) {return}
         }
      }

      var select2 = this.el.select2(settings).data('select2');

      if (this.options.tags && select2 && select2.search) {
        // find the "fake" input created by select2 and add the keypress event.
        // This is not part of the plugins API and so may break at any time.
        select2.search.on('keydown', this._onKeydown);
      }

      // This prevents Internet Explorer from causing a window.onbeforeunload
      // even from firing unnecessarily
      $('.select2-choice', select2.container).on('click', function() {
        return false;
      });

      this._select2 = select2;

      // adding of thesaurus

      var target = document.querySelector('ul.select2-choices');

      // create an observer instance
      var observer = new MutationObserver(function(mutations) {
          mutations.forEach(function(mutation) {
            // do stuff when
            // `childList`, `subtree` of `#myTable` modified
            usedThesauri = $('#field-thesaurusName').val();

            if(mutation.addedNodes.length > 0){
                var keyword = mutation.addedNodes[0].children[0].innerHTML;

                thesaurus = $('#field-selectThesaurus').val()

                if(thesaurus == ""){
                    var data = new FormData();
                    data.append('label', keyword);

                    $.ajax({
                        url: '/get_taxonomy_title_from_keyword',
                        data: data,
                        cache: false,
                        contentType: false,
                        processData: false,
                        type: 'POST',
                        success: function(response){
                            thesaurus = response;
                        },
                        async: false
                    });
                }

                var inputThesaurus = $('<input value="'+ thesaurus +'" type="hidden"/>');
                mutation.addedNodes[0].append(inputThesaurus[0]);

                var thesaurusAlreadyUsed = false;
                for(t of usedThesauri.split(", ")){
                    if(t == thesaurus){
                        thesaurusAlreadyUsed = true;
                    }
                }
                if(thesaurusAlreadyUsed == false){
                    if(usedThesauri.split(", ").length == 1 && usedThesauri.split(", ")[0] == ''){
                        $('#field-thesaurusName').val(thesaurus);
                    }else{
                      $('#field-thesaurusName').val(usedThesauri + ', ' + thesaurus);
                    }
                }
            }else if(mutation.removedNodes.length > 0){
                var removedElement = mutation.removedNodes[0];
                var thesaurus = mutation.removedNodes[0].children[2].value;
                var listElements = mutation.target.children;
                var deleteThesaurus = true;
                for (var i = 0; i < listElements.length -1; i++) {
                    if(listElements[i]!=removedElement){
                        if(thesaurus == listElements[i].children[2].value){
                            deleteThesaurus = false;
                        }
                    }
                }
                if(deleteThesaurus){
                    usedThesauri = usedThesauri.split(", ");
                    var index = usedThesauri.indexOf(thesaurus);
                    usedThesauri.splice(index, 1);
                    $('#field-thesaurusName').val(usedThesauri.join(", "));
                }
            }
          });
      });

        // configuration of the observer:
      var config = { attributes: true, childList: true, characterData: true };

        // pass in the target node, as well as the observer options
      observer.observe(target, config);

    },

    /* Looks up the completions for the current search term and passes them
     * into the provided callback function.
     *
     * The results are formatted for use in the select2 autocomplete plugin.
     *
     * string - The term to search for.
     * fn     - A callback function.
     *
     * Examples
     *
     *   module.getCompletions('cake', function (results) {
     *     results === {results: []}
     *   });
     *
     * Returns a jqXHR promise.
     */
    getCompletions: function (string, fn) {
      var taxName = $( "#field-selectThesaurus" ).val();
      var parts  = this.options.source.split('?');
      var end    = parts.pop();
      // var source = parts.join('?') + encodeURIComponent(string) + end + "&tax_name=" + this.options.taxonomy_name;
      var source = parts.join('?') + encodeURIComponent(string) + end + "&tax_name=" + taxName;
      var client = this.sandbox.client;
      var options = {
        format: function(data) {
          var completion_options = jQuery.extend(options, {objects: true});
          return {
            results: client.parseCompletions(data, completion_options)
          }
        },
        key: this.options.key,
        label: this.options.label
      };

      return client.getCompletions(source, options, fn);
    },

    /* Looks up the completions for the provided text but also provides a few
     * optimisations. If there is no search term it will automatically set
     * an empty array. Ajax requests will also be debounced to ensure that
     * the server is not overloaded.
     *
     * string - The term to search for.
     * fn     - A callback function.
     *
     * Returns nothing.
     */
    lookup: function (string, fn) {
      var module = this;
      // Cache the last searched term otherwise we'll end up searching for
      // old data.
      this._lastTerm = string;

      // Kills previous timeout
      clearTimeout(this._debounced);

      // OK, wipe the dropdown before we start ajaxing the completions
      fn({results:[]});

      if (string) {
        // Set a timer to prevent the search lookup occurring too often.
        this._debounced = setTimeout(function () {
          var term = module._lastTerm;

          // Cancel the previous request if it hasn't yet completed.
          if (module._last && typeof module._last.abort == 'function') {
            module._last.abort();
          }

          module._last = module.getCompletions(term, fn);
        }, this.options.interval);

        // This forces the ajax throbber to appear, because we've called the
        // callback already and that hides the throbber
        $('.select2-search input', this._select2.dropdown).addClass('select2-active');
      }
    },

    /* Formatter for the select2 plugin that returns a string for use in the
     * results list with the current term emboldened.
     *
     * state     - The current object that is being rendered.
     * container - The element the content will be added to (added in 3.0)
     * query     - The query object (added in select2 3.0).
     *
     *
     * Returns a text string.
     */
    formatResult: function (state, container, query) {
      var term = this._lastTerm || null; // same as query.term
      if (container) {
        // Append the select id to the element for styling.
        container.attr('data-value', state.id);
      }

      return state.text.split(term).join(term && term.bold());
    },

    /* Formatter for the select2 plugin that returns a string used when
     * the filter has no matches.
     *
     * Returns a text string.
     */
    formatNoMatches: function (term) {
      return !term ? this.i18n('emptySearch') : this.i18n('noMatches');
    },

    /* Formatter used by the select2 plugin that returns a string when the
     * input is too short.
     *
     * Returns a string.
     */
    formatInputTooShort: function (term, min) {
      return this.i18n('inputTooShort', {min: min});
    },

    /* Takes a string and converts it into an object used by the select2 plugin.
     *
     * term - The term to convert.
     *
     * Returns an object for use in select2.
     */
    formatTerm: function (term) {
      term = jQuery.trim(term || '');

      // Need to replace comma with a unicode character to trick the plugin
      // as it won't split this into multiple items.
      return {id: term.replace(/,/g, '\u002C'), text: term};
    },

    /* Callback function that parses the initial field value.
     *
     * element  - The initialized input element wrapped in jQuery.
     * callback - A callback to run once the formatting is complete.
     *
     * Returns a term object or an array depending on the type.
     */
    formatInitialValue: function (element, callback) {
      var value = jQuery.trim(element.val() || '');
      console.log(value);
      var formatted;

      if (this.options.tags) {
        formatted = jQuery.map(value.split(","), this.formatTerm);
      } else {
        formatted = this.formatTerm(value);
      }

      // Select2 v3.0 supports a callback for async calls.
      if (typeof callback === 'function') {
        callback(formatted);
      }

      return formatted;
    },

    /* Callback triggered when the select2 plugin needs to make a request.
     *
     * Returns nothing.
     */
    _onQuery: function (options) {
      if (options) {
        this.lookup(options.term, options.callback);
      }
    },

    /* Called when a key is pressed.  If the key is a comma we block it and
     * then simulate pressing return.
     *
     * Returns nothing.
     */
    _onKeydown: function (event) {
      if (event.which === 188) {
        event.preventDefault();
        setTimeout(function () {
          var e = jQuery.Event("keydown", { which: 13 });
          jQuery(event.target).trigger(e);
        }, 10);
      }
    }
  };
});
