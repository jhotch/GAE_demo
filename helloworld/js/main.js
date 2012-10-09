$(document).ready(function(){
	var params = new Array('getAllGreetings');
	// ajax test
	$.ajax({
	   type: "post",
	   url: "/rpc",
	   data: JSON.stringify(params),
	   dataType: "json",
	   success: function(response){
		 console.log(response);
	   }
	 });

	// summary list behaviour 
	$("#summaryContainer li").children(".arrivalToggle").hide();	
	$("#summaryContainer li").on({
		mouseenter: function() {
			$(this).addClass("highlight").children(".arrivalToggle").fadeToggle("fast");
	   },
		mouseleave: function() {
			$(this).removeClass("highlight").children(".arrivalToggle").hide();
	   } 
	});
	
});