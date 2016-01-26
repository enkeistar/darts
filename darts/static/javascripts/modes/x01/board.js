$(function(){

	var complete = $("input[name=complete]").val() == "1";
	if(complete){
		$(".home").on("click", function(){
			window.location = "/";
		});
		return;
	}

	var gameId = $("input[name=gameId]").val();
	var baseUrl = "/games/" + gameId + "/modes/x01";
	var players = $(".player");
	var numPlayers = players.length;
	var round = parseInt($("input[name=round").val());
	var turn = parseInt($("input[name=turn").val());
	var game = parseInt($("input[name=game").val());
	var quiteGameModal = $(".modal-quit-game");

	var turnTimeout;
	var turnDelay = 5000;

	var order = players.filter("[data-playerid=" + turn + "]").addClass("active").index();


	$(".score-button").on("click", function(){
		var source = $(this);
		var points = parseInt(source.data("points"));
		var activePlayer = $(".player.active");
		var playerId = activePlayer.data("playerid");
		var teamId = activePlayer.data("teamid");
		var currentPoints = parseInt(activePlayer.attr("data-score"));

		$.post(baseUrl + "/teams/" + teamId + "/players/" + playerId + "/games/" + game + "/rounds/" + round + "/marks/" + points + "/");

		currentPoints -= points;
		activePlayer.find(".score").html(currentPoints);
		activePlayer.attr("data-score", currentPoints);

		clearTimeout(turnTimeout);
		turnTimeout = setTimeout(nextTurn, turnDelay);
	});

	function nextTurn(){
		order++;
		if(order >= numPlayers){
			order = 0;
		}

		players.removeClass("active");
		var playerId = players.eq(order).addClass("active").data("playerid");

		$.post(baseUrl + "/players/" + playerId + "/turn/");
	}

	$(".miss").on("click", function(){
		var activePlayer = $(".player.active");
		var playerId = activePlayer.data("playerid");
		var teamId = activePlayer.data("teamid");
		$.post(baseUrl + "/teams/" + teamId + "/players/" + playerId + "/games/" + game + "/rounds/" + round + "/marks/0/").done(nextTurn);
	});

	$(".undo").on("click", function(){
		window.location = baseUrl + "/undo/";
	});

	$(".home").on("click", function(){
		quiteGameModal.show();
	});
	$(".quit-game-yes").on("click", function(){
		window.location = "/";
	});
	$(".quit-game-no").on("click", function(){
		quiteGameModal.hide();
	});

});
