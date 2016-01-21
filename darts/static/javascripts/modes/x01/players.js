$(function(){

	var current = 0;
	var gameId = $("#gameId").val();
	var teams = $(".team");
	var players = $(".player");

	players.on("click", function(){

		var source = $(this);

		var data = {
			teamId: teams.eq(current).data("teamid"),
			playerId: source.data("playerid")
		};

		players.prop("disabled", true);

		$.post("/games/" + gameId + "/players/", data, function(data){
			players.prop("disabled", false);
			source.remove();
			teams.eq(current).show().append(source.html());
			current++;

			if(current >= teams.length){
				$(".play").show();
				$(".redo").css("display", "block");
				$(".player-list").hide();
				$(".add-player").hide();
			}
		});


	});

});