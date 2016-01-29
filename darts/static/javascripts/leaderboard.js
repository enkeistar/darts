$(function(){

	var ajaxRequest;
	var leaderboard = $("#leaderboard");
	var column, direction;

	function updateTable(html){
		leaderboard.html(html);
		bindSort();
	}

	function bindSort(){
		leaderboard.find("table").stupidtable().bind("aftertablesort", function(el, data){
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
		ajaxRequest = $.get("/leaderboard/", { "start": $("input[name=start]").val(), "end": $("input[name=end]").val() }).done(updateTable);

	});

	bindSort();

});