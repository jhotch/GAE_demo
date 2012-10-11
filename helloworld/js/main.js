function visitorFormSubmit(){
	var params = new Array("AddVisitor");
	var formFieldValues = $("#visitorForm").serializeArray();
	params.push(formFieldValues);
	// console.log(params);
	$.ajax({
	   type: "post",
	   url: "/rpc",
	   data: JSON.stringify(params),
	   dataType: "json",
	   success: function(response){
		 console.log(response);
	   }
	});
};

function getVisitors(){
	var params = new Array("GetAllVisitors");
	$.ajax({
	   type: "post",
	   url: "/rpc",
	   data: JSON.stringify(params),
	   dataType: "json",
	   success: function(response){
		 console.log(response);
	   }
	});
};

$(document).ready(function(){
	
	//get all visitors
	getVisitors();
	
	// visitor form behaviours
	$("#visitorForm").on("click", "#btnSubmit", function(event){
		event.preventDefault();
		visitorFormSubmit();
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