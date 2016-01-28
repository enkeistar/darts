$(function(){

	var ajaxRequest;
	var leaderboard = $("#leaderboard");
	var column, direction;

	$.post("/leaderboard/", { "start": "", "end": "" }).done(updateTable);

	function updateTable(html){
		leaderboard.html(html).find("table").stupidtable();


		leaderboard.find("table").bind("aftertablesort", function(el, data){
			column = data.column;
			direction = data.direction;
		});

		$("th").eq(column).stupidsort(direction);
	}

	$(".input-daterange").datepicker({

		clearBtn: true,
		autoclose: true,
		todayHighlight: true,
		format: "yyyy-mm-dd"

	}).on("change.dp", function(){

		if(ajaxRequest){
			ajaxRequest.abort();
		}
		ajaxRequest = $.post("/leaderboard/", { "start": $("input[name=start]").val(), "end": $("input[name=end]").val() }).done(updateTable);

	});

});