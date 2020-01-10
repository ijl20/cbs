		$(document).ready(function(){
 			$("label.inlined + .input-text").each(function (type) {
		     	$(this).focus(function () {
		      		$(this).prev("label.inlined").addClass("focus");
		     	});
		     	$(this).keypress(function () {
		      		$(this).prev("label.inlined").addClass("has-text").removeClass("focus");
		     	});
		     	$(this).blur(function () {
		      		if($(this).val() == "") {
		      			$(this).prev("label.inlined").removeClass("has-text").removeClass("focus");
		      		}
		     	});
		    });
		});
