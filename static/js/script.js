$(function(){

    // Chama um evento do Analytics em caso de clique em links externos.
    $("a[rel*='external']").click(function(){
      trackEvent('Destino externo', this.href, this.href);
    });

    $(".header").click(function(e) {  if (e.shiftKey) $(".footerFrame, .contentFrame, .headerFrame").toggleClass("debug"); });

	if ( $('.homeSignup').length ) {

		$(window).resize(function() {
			bodyhomeImgPos();
		});

		bodyhomeImgPos();

	}

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

function bodyhomeImgPos() {

	offsetSignupButton = $('.homeSignup').offset();

	bodyHome_img_pos_x = Math.floor( offsetSignupButton.left - 721 );
	bodyHome_img_pos_y = Math.floor( offsetSignupButton.top  - 240 );

	bodyHome_img_pos = bodyHome_img_pos_x + "px " + bodyHome_img_pos_y + "px";

	$('.bodyHome').css('backgroundPosition', bodyHome_img_pos );

}
