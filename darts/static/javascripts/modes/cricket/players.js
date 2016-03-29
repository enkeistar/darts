$(function(){

	var current = -1;
	var matchId = $("#matchId").val();
	var instructions = $(".select-player-instruction")
	var teamPlayers = $(".team-player");
	var existingPlayers = $(".existing-players");
	var players = $(".player");

	next();

	players.on("click", function(){
		var source = $(this);

		var data = {
			teamId: teamPlayers.eq(current).data("teamid"),
			playerId: source.data("playerid")
		};

		players.prop("disabled", true);

		$.post("/matches/" + matchId + "/modes/cricket/players/", data, function(data){
			selectPlayer(source);
			players.prop("disabled", false);
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

		if(current >= teamPlayers.length){
			$(".play").show();
			$(".player-list").hide();
			$(".add-player").hide();
		}
	}

});
