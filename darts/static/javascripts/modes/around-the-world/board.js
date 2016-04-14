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

	$(".ctrl.undo").on("click", function(){
		$.post("/matches/" + matchId + "/modes/around-the-world/undo/", score);
	});

	function score(response){
		var player = $(".player[data-playerid=" + response.playerId + "]");
		var points = response.mark;
		player.data("point", points);
		player.find(".point").html(points);
	}

	$(".ctrl.triple").on("click", function(){
		$(".name").addClass("selectable");
	});

	$(".name").on("click", function(){
		var source = $(this);
		if(!source.hasClass("selectable")) return;
		var player = source.parent(".player");

		$.post("/matches/" + matchId + "/modes/around-the-world/players/" + player.data("playerid") + "/triple/", score);
		$(".name").removeClass("selectable");
	});
});
