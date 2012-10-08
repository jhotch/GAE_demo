$(document).ready(function(){

	// ajax test
	$.ajax({
	   type: "GET",
	   url: "/rpc",
	   data: "",
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