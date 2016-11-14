/* Extensions necessary because tab #tags do not show up in the url
   reload always jumps to first tab

   ergoogelt - Anja 20.10.
*/


/*

$('#myPills a').click(function(e) {
e.preventDefault();
$(this).pill('show');
});

// store the currently selected tab in the hash value
$("ul.nav-pills > li > a").on("shown.bs.pill", function(e) {
var id = $(e.target).attr("href").substr(1);
window.location.hash = id;
});

// on load of the page: switch to the currently selected tab
var hash = window.location.hash;
$('#myPills a[href="' + hash + '"]').pill('show');

*/

/*
// Jump back to top
var scrollmem = $('body').scrollTop() || $('html').scrollTop();
window.location.hash = this.hash;
$('html,body').scrollTop(scrollmem);
*/
// Javascript to enable link to tab

var url = document.location.toString();
console.log(url)
if (url.match('#')) {
    $('.nav-pills a[href="#' + url.split('#')[1] + '"]').tab('show');
     window.scrollTo(0, 0);
}

// Change hash for page-reload
$('.nav-pills a').on('shown.bs.tab', function (e) {
    window.location.hash = e.target.hash;
    window.scrollTo(0, 0);
    window.refresh();
})

// Note last position
/*
var scrollmem = $('body').scrollTop() || $('html').scrollTop();
   window.location.hash = this.hash;
   $('html,body').scrollTop(scrollmem);
   */
