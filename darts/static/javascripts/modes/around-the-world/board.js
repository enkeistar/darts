$(function(){


	var matchId = $(".around-the-world-board").data("matchid");


	$(".ctrl.home").on("click", function(){
		$(".modal-home").show();
	});
	$(".home-yes").on("click", function(){
		window.location = "/";
	});
	$(".home-no").on("click", function(){
		$(".modal-home").hide();
	});


	$(".point").on("click", function(){
		var player = $(this).parent(".player");
		var teamId = player.data("teamid");
		var playerId = player.data("playerid");
		var point = parseInt(player.data("point"));

		$.post("/matches/" + matchId + "/modes/around-the-world/teams/" + teamId + "/players/" + playerId + "/marks/" + point + "/", score);
	});


	function score(response){
		var player = $(".player[data-playerid=" + response.playerId + "]");
		var points = response.mark;
		player.data("point", points);
		player.find(".point").html(points);
	}


	$(".ctrl.undo").on("click", function(){
		$.post("/matches/" + matchId + "/modes/around-the-world/undo/", score);
	});

	function undo(response){

	}

});
