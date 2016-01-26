$(function(){

	var gameId = $("input[name=gameId]").val();
	var baseUrl = "/games/" + gameId + "/modes/x01";
	var players = $(".player");
	var numPlayers = players.length;
	var round = parseInt($("input[name=round").val());
	var turn = parseInt($("input[name=turn").val());
	var game = parseInt($("input[name=game").val());

	var turnTimeout;
	var turnDelay = 5000;

	var order = 0;

	players.first().addClass("active");


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
		players.eq(order).addClass("active");
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
		if(confirm("Are you sure?")){
			window.location = "/";
		}
	});

});