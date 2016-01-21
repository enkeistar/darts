$(function(){

	$("#leaderboard").stupidtable();
	var sorting =
		'<div class="sorting-container">' +
			'<span class="glyphicon glyphicon-chevron-up"></span>' +
			'<span class="glyphicon glyphicon-chevron-down"></span>' +
		'</div>'
	;
	$("th[data-sort]").append(sorting);

});