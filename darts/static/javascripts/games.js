$(function(){

	var current = -1;
	var gameId = $("#gameId").val();
	var instructions = $(".select-player-instruction")
	var teamPlayers = $(".team-player");
	var existingPlayers = $(".existing-players");

	next();

	$(".player").on("click", function(){
		var source = $(this);

		var data = {
			teamId: teamPlayers.eq(current).data("teamid"),
			playerId: source.data("playerid")
		};

		$.post("/games/" + gameId + "/players/", data, function(data){
			selectPlayer(source);
		});

	});

	existingPlayers.each(function(){
		var playerId = $(this).val();
		selectPlayer($(".player[data-playerid=" + playerId + "]"));
	});

	function selectPlayer(player){
		player.remove();
		teamPlayers.eq(current).find(".selected").html(player.html());
		next();
	}

	function next(){
		current++;

		teamPlayers.removeClass("active");
		teamPlayers.eq(current).addClass("active");

		instructions.hide();
		instructions.eq(current).show();
	}

});
