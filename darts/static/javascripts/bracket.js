$(function(){

	$(".col2 .bracket-player").each(function(){
		var playerid = $(this).data("playerid");
		if(playerid){
			$(".col1 .bracket-player[data-playerid=" + playerid + "]").css("font-weight", "bold");
		}
	});

	$(".col3 .bracket-player").each(function(){
		var playerid = $(this).data("playerid");
		if(playerid){
			$(".col2 .bracket-player[data-playerid=" + playerid + "]").css("font-weight", "bold");
		}
	});

	$(".col4 .bracket-player").each(function(){
		var playerid = $(this).data("playerid");
		if(playerid){
			$(".col3 .bracket-player[data-playerid=" + playerid + "]").css("font-weight", "bold");
		}
	});

});