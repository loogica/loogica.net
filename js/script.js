$(function(){

    // Chama um evento do Analytics em caso de clique em links externos.
    $("a[rel*='external']").click(function(){
      trackEvent('Destino externo', this.href, this.href);
    });

    $(".header").click(function(e) {  if (e.shiftKey) $(".footerFrame, .contentFrame, .headerFrame").toggleClass("debug"); });

    $('article').click(function() {
    	$(this).find('.videoMain').toggle();
	});

});


/**
 * Aciona um registro no Google Analytics
 * Registra e identifica um clique no Google Analytics via evento de JavaScript
 *
 */
function trackEvent(category, action, redirectTo)
{
    try {
      _gaq.push(['_trackEvent', category, action]);
      // alert( 'tracked event: ' + category + ', ' + action)
    }catch(err){}
}
