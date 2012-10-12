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

function getVisitors(category){
	var params = ['GetVisitors',category];
	$.ajax({
	   type: "post",
	   url: "/rpc",
	   data: JSON.stringify(params),
	   dataType: "json",
	   success: function(response){
		 console.log(response);
		 // refreshVisitors(response, category);
	   }
	});
};

function refreshVisitors(arrObjects, category){
	var arrDue = [];
	var arrOnsite = [];
	var arrDeparted = [];
	// determine proper category
	$.each(arrObjects, function(index, obj){
		if(obj.actualArrivalTime == '' && obj.actualDepartureTime == ''){
			arrDue.push(obj);
		} else {
			if(obj.actualDepartureTime == ''){
				arrOnsite.push(obj);
			} else {
				arrDeparted.push(obj);
			};
		};
	});	
	// clear existing display
	$('#arrivalDueContainer, #onsiteContainer, #departedContainer').html('<h4>Loading...</h4>');
	// rebuild displays
	rebuildDisplays(arrDue, arrOnsite, arrDeparted);
};

function rebuildDisplays(){
	
};

function formatDateAsString(d){
	var d_names = new Array('Sunday', 'Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday');
	var m_names = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');
	var curr_day = d.getDay();
	var curr_date = d.getDate();
	var sup = '';
	if (curr_date == 1 || curr_date == 21 || curr_date ==31) {
		sup = 'st';
	} else {
		if (curr_date == 2 || curr_date == 22) {
			sup = 'nd';
		} else {
			if (curr_date == 3 || curr_date == 23) {
				sup = 'rd';
			} else {
				sup = 'th';
			};
		};
	};
	var curr_month = d.getMonth();
	var curr_year = d.getFullYear();
	return (d_names[curr_day] + ', ' + m_names[curr_month] + ' ' + curr_date + '<SUP>' + sup + '</SUP>' + ', ' + curr_year);	
};

$(document).ready(function(){

	//set current Date
	var now = new Date();
	$('#currentDateContainer').html(formatDateAsString(now));
	
	//get all visitors
	getVisitors('all');
	
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