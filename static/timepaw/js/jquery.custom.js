/*-----------------------------------------------------------------------------------

 	Custom JS - All front-end jQuery
 
-----------------------------------------------------------------------------------*/
 
 
/*-----------------------------------------------------------------------------------*/
/*	Superfish Settings - http://users.tpg.com.au/j_birch/plugins/superfish/
/*-----------------------------------------------------------------------------------*/

jQuery(document).ready(function() {

/*-----------------------------------------------------------------------------------*/
/*	Menu Drops
/*-----------------------------------------------------------------------------------*/

	jQuery('#primary-nav ul').superfish({
		delay: 200,
		animation: {opacity:'show', height:'show'},
		speed: 'fast',
		autoArrows: false,
		dropShadows: false
	}); 

/*-----------------------------------------------------------------------------------*/
/*	Back to Top
/*-----------------------------------------------------------------------------------*/

	var topLink = jQuery('#back-to-top');

	function tz_backToTop(topLink) {

		if(jQuery(window).scrollTop() > 0) {
			topLink.fadeIn(200);
		} else {
			topLink.fadeOut(200);
		}
	}

	jQuery(window).scroll( function() {
		tz_backToTop(topLink);
	});

	topLink.click( function() {
		jQuery('html, body').stop().animate({scrollTop:0}, 500);
		return false;
	});
	
/*-----------------------------------------------------------------------------------*/
/*	Like Script
/*-----------------------------------------------------------------------------------*/

	function tz_reloadLikes(who) {
		var text = jQuery("#" + who).html();
		var patt= /(\d)+/;

		var num = patt.exec(text);
		num[0]++;
		text = text.replace(patt,num[0]);
		jQuery("#" + who).html('<span class="count">' + text + '</span>');
	} //reloadLikes


	function tz_likeInit() {
		jQuery(".likeThis").click(function() {
			var classes = jQuery(this).attr("class");
			classes = classes.split(" ");

			if(classes[1] == "active") {
				return false;
			}
			var classes = jQuery(this).addClass("active");
			var id = jQuery(this).attr("id");
			id = id.split("like-");
			jQuery.ajax({
			  type: "POST",
			  url: "index.php",
			  data: "likepost=" + id[1],
			  success: tz_reloadLikes("like-" + id[1])
			}); 


			return false;
		});
	}

	tz_likeInit();


});