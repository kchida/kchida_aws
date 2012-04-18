/* Author: Ken Chida 

*/

jQuery(function ($) {
	
    // Logo Container Hover Highlight #################################
    (function logo_highlight ($) {
        $('#logo-container').hover(
		    function () {
		        $(this).stop().animate({opacity: 1}, 'fast');
		    },
		    function () {
		        $(this).stop().animate({opacity: 0.7}, 'slow');
		    }
        );
    })($); 
    
    // Main Nav Menu Hover Highlight ##################################
    //
    // Note: jQuery color transition plugin is much better option!!
    (function menu_highlight ($, window) {
        // Cache menu button jQuery object.
    	var $menu = $('#main-nav li');
        // Settings:
        //    REFRESH_INTERVAL -- Elapsed time between CSS color updates to button.
        //    ON_DURATION -- Elapsed time for mouse-over color transitions.
        //    OFF_DURATION -- Elapsed time for mouse-exit color transitions.
        //    START_COLOR -- Original unhighlighted menu color per CSS stylesheet. 
        //    END_COLOR -- Respective highlight colors from left-to-right; rgb string.
        // Note:
        //    Duration divided by refresh interval should ideally yield whole number.
    	var REFRESH_INTERVAL = 25,
    	    ON_DURATION = 200,
    	    OFF_DURATION = 400,
    	    START_COLOR = $menu.css('background-color'),
    	    END_COLOR = ['rgb(255,144,0)','rgb(0,143,210)','rgb(215,0,22)','rgb(245,195,0)','rgb(0,0,0)'];
    	    
        function rgbParse (color) { 
   	    // Takes a rgb color string and returns an object with rgb int values.
   	    // Param: color -- must be a string 'rgb(xx, xx, xx)'
   	    // Output: parsed -- Ex. {red: 3, green: 4, blue: 33}
   	        var parsed = {red: '', green: '', blue: ''},
   	            comp_list = ['blue', 'green', 'red'];    // color components
   	            
   	    	for (var i = 0, comp = comp_list.pop(); i < color.length; i++) {
   	    		if ( color[i] === ',' || (i + 1) === color.length) {
   	    			parsed[comp] = parseInt(parsed[comp], 10);
   	    		    comp = comp_list.pop();
   	    		}
   	    		else if ( parseInt(color[i], 10) || color[i] === '0' ) {
   	    		    parsed[comp] = parsed[comp].concat(color[i]);
   	    		};
   	    	};
   	    	return parsed;
   	    };
   	    
        function colorFader ($button, target_color, duration) {
    	// Takes a jQuery object and performs color transition.
    	// Params:
    	//    $button -- Cached button jQuery object that was hovered over.
    	//    target_color -- Target color in 'rgb(xx,xx,xx)' string format.
    	//    duration -- Duration of color transition in milliseconds. 
    	    var initial = rgbParse($button.css('background-color')),
    	        target = rgbParse(target_color),
    	        refresh_interval = REFRESH_INTERVAL,
    	        // Color delta for each refresh cycle.
    	        step = {red: 0, green: 0, blue: 0},
    	        // Cache for current color value.
    	        curval = {red: 0, green: 0, blue: 0},
    	         // Color component list and temp cache.
    	        comp_list = ['blue', 'green', 'red'],
    	        comp = '',
    	        // Index to track number of calls to refresh_color().
    	        refresh_count = 0,
    	        // Flag to stop color animation if mouseleave event is detected.
    	        stop_refresh = false,
    	        is_mouseleave = (target_color === START_COLOR) ? true : false;
    	     
    	    var total_refreshes = Math.floor(duration / refresh_interval);
    	    
            // Multiply 'step' and 'curval' by 1000 so Math.floor doesn't obliterate precision.
            while (comp_list.length) {
                comp = comp_list.pop();
                step[comp] = ( (target[comp] - initial[comp]) * 1000 ) / total_refreshes;
                curval[comp] = initial[comp]*1000
            };
            
		    // When new mouse event is detected, stop animation.
		    var mouse_event = (is_mouseleave) ? 'mouseenter' : 'mouseleave';
		    function stop_cursor() {stop_refresh = true;};
		    $button.one(mouse_event, stop_cursor);
		    //$button.click(stop_cursor);
		    
            // Callback function for setInterval().
            // Each call increments the color value and refreshes CSS color value.
            function refresh_color () {
    	        // 'hex_color' used to set CSS color attribute at end of each refresh cycle.
    	        var hex_color = '#',
    	            comp_int = 0;	
    	            
    	        comp_list = ['blue', 'green', 'red'];
    	        
                refresh_count = refresh_count + 1;
                
                if ((refresh_count >= total_refreshes) || stop_refresh ) {
    	            window.clearInterval(id); 
                };
                
   		        while (comp_list.length) {
	                comp = comp_list.pop();
    	            curval[comp] = curval[comp] + step[comp];
    	            // Scale back down by factor of 1000 and ready to convert to hex.
    	            comp_int = Math.floor(curval[comp] / 1000);
    	            // Make sure each color gets two hex digits.
    	            if (comp_int < 16) {
    	                hex_color = hex_color.concat('0');
    	            };
    	            hex_color = hex_color.concat( comp_int.toString(16) );
                };
                $button.css('background-color', hex_color);
            };
    	    // Each refresh is 'refresh_interval' milliseconds long. 
            var id = window.setInterval(refresh_color, refresh_interval);
        };      
    	
    	// MAIN
        $menu.hover(
        	// Mouseenter callback
		    function () {
		    	  // Note: $(this) !== $menu === $('#main-nav li'). 'this' is
		    	  // the single button element that triggered the event.
		        var $this = $(this);
		          // Cached cursor jQuery object and sentinel to signal when
		          // to stop cursor blinking.
		        var stop_blink = 0;
		          // Tells us which button triggered event; for color assignment. 
		        var button_index = $menu.index(this);
		            
		        colorFader($this, END_COLOR[button_index], ON_DURATION);
		        
		        // When mouse exits menu, cursor must stop blinking.
		        function stop_cursor() {stop_blink = 1;};
		        $this.mouseleave(stop_cursor);
		        
		        // Recursive setTimeout call to create blinking effect.
		        function cursor_blink () {
		        	var id = 0;
		        	if (stop_blink === 0) {
		                $this.find('.cursor').stop().animate({opacity: 0.7}, 50)
		                     .delay(400).animate({opacity: 0}, 50);
		                id = window.setTimeout(cursor_blink, 1000);
		            }
		            else {
		                window.clearTimeout(id);
		            };
		        };
		        cursor_blink();
		    },
		    // Mouseleave callback
		    function () {
		        var $this = $(this);
		        $this.find('.cursor').stop().css('opacity', 0);
		        colorFader($this, START_COLOR, OFF_DURATION);
		    }
        );
    })($, window); 
    
    // Begin: SimpleModal Login/Register Form ################################
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
    // End: SimpleModal Login/Register Form ##################################
    
});

