$(function(){

	var current = 0;
	var gameId = $("#gameId").val();
	var teams = $(".team");
	var existingPlayers = $(".existing-players");
	var players = $(".player");

	var baseUrl = "/games/" + gameId + "/modes/x01";

	players.on("click", function(){

		var source = $(this);

		var data = {
			teamId: teams.eq(current).data("teamid"),
			playerId: source.data("playerid")
		};

		players.prop("disabled", true);

		$.post(baseUrl + "/players/", data, function(data){
			players.prop("disabled", false);
			selectPlayer(source);
		});


	});

	existingPlayers.each(function(){
		var playerId = $(this).val();
		selectPlayer($(".player[data-playerid=" + playerId + "]"));
	});

	function selectPlayer(player){
		player.remove();
		teams.eq(current).show().append(player.html());
		current++;

		if(current >= teams.length){
			$(".play").show();
			$(".redo").css("display", "block");
			$(".player-list").hide();
			$(".add-player").hide();
		}
	}

});