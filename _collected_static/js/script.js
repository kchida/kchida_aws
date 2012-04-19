/* Author: 

*/


// Begin: SimpleModal Login/Register Form
jQuery(function ($) {
	
	var logreg_modal = {
		
		init: function () {
			
			$('#login-link, #register-link').click(function (ev_obj) {
				
				var link_id = ev_obj.target.id,
				    general_options = {
				    	opacity: 80,
	    				overlayId: 'modal-overlay',
			    		containerId: 'modal-container',
	    				closeHTML: "<a href='#' id='modal-close' title='Close'>x</a>",
		    			overlayClose: true,
			    		position: ["25%",],
    					onOpen: logreg_modal.open,
	    				onShow: logreg_modal.show,
		    			onClose: logreg_modal.close
				    };
				    
				ev_obj.preventDefault();
				
				if (link_id === 'login-link') {
 				    $('#login-panel').modal(general_options);
				};
				
				if (link_id === 'register-link') {
 				    $('#register-panel').modal(general_options);
				};
			});
		},
		
		open: function ($dialog) {
			// Note:  $dialog.container === $('#modal-container')
			// Note:  $dialog.data === $('#login-panel')
			
			var h = 350;
			//var h = $('#modal-container').height();
			$dialog.overlay.fadeIn(200, function () {
				$dialog.container.fadeIn(200, function () {
					$(this).animate({height: h}, function () {
						$dialog.data.fadeIn(function () {
							$(this).find('input:first').focus();
						});
					});
				});
			});
		},
		
		show: function ($dialog) {
			// Note:  $dialog.data === $('#login-panel')
			
		    if ($dialog.data.is('#login-panel')) {
		    
			    var $twitter_icon = $dialog.data.find('.icon-twitter'),
			        $google_icon = $dialog.data.find('.icon-google-oauth'),
			        $twitter_shadow = $('#twitter-shadow'),
			        $google_shadow = $('#google-oauth-shadow');
			    
			    $twitter_icon.hover(
				    function () {
				    	$twitter_shadow.stop().animate({opacity: 1}, 'fast');
				    },
				    function () {
				    	$twitter_shadow.stop().animate({opacity: 0}, 'slow');
				    }
			    );
			    
			    $google_icon.hover(
				    function () {
				    	$google_shadow.stop().animate({opacity: 1}, 'fast');
				    },
				    function () {
				    	$google_shadow.stop().animate({opacity: 0}, 'slow');
				    }
			    );
			    
			    $twitter_icon.click(
				    function () {$twitter_shadow.stop(true, true);}
			    );
			    $google_icon.click(
				    function () {$google_shadow.stop(true, true);}
			    );
			};
		},
		
		close: function ($dialog) {
			// Note:  $dialog.container === $('#modal-container')
			// Note:  $dialog.data === $('#login-panel')
		    
		    $dialog.data.fadeOut(function () {
		    	$dialog.container.animate({height: 40}, function () {
		    		$(this).fadeOut(200, function () {
		    			$dialog.overlay.fadeOut(200, function () {
		    				$.modal.close();
		    			});
		    		});
		    	});
		    });
		}
	};
	
    logreg_modal.init();
});

