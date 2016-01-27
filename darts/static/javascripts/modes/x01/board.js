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
	var players = $(".player:not(.winner)");
	var numPlayers = players.length;
	var round = parseInt($("input[name=round").val());
	var game = parseInt($("input[name=game").val());
	var quiteGameModal = $(".modal-quit-game");
	var turns = 0;

	var turnTimeout;
	var turnDelay = 5000;


	$(".score-button").on("click", function(){
		var source = $(this);
		var points = parseInt(source.data("points"));
		var activePlayer = $(".player.active");
		var playerId = activePlayer.data("playerid");
		var teamId = activePlayer.data("teamid");

		turns++;

		$.post(baseUrl + "/teams/" + teamId + "/players/" + playerId + "/games/" + game + "/rounds/" + round + "/marks/" + points + "/");

		changeScore(activePlayer, -points);

		if(getPoints(activePlayer) < 0){
			retractThrows();
		}

		clearTimeout(turnTimeout);
		turnTimeout = setTimeout(nextTurn, turnDelay);
	});

	$(".miss").on("click", miss);

	$(".turn").on("click", nextTurn);

	$(".undo").on("click", undo);

	$(".home").on("click", function(){
		quiteGameModal.show();
	});
	$(".quit-game-yes").on("click", function(){
		window.location = "/";
	});
	$(".quit-game-no").on("click", function(){
		quiteGameModal.hide();
	});

	function nextTurn(){
		determineWinners();
		clearTimeout(turnTimeout);
		turns = 0;

		var index = 0;
		for(var i = 0; i < players.length; i++){
			if($(players[i]).hasClass("active")){
				index = i + 1;
				break;
			}
		}
		if(index >= players.length){
			index = 0;
		}
		$(".player").removeClass("active");
		var playerId = $(players[index]).addClass("active").data("playerid");

		$.post(baseUrl + "/players/" + playerId + "/turn/");
	}

	function miss(){
		var activePlayer = $(".player.active");
		var playerId = activePlayer.data("playerid");
		var teamId = activePlayer.data("teamid");
		$.post(baseUrl + "/teams/" + teamId + "/players/" + playerId + "/games/" + game + "/rounds/" + round + "/marks/0/").done(nextTurn);
	}

	function undo(){
		return $.post(baseUrl + "/undo/", function(response){
			if(response.valid){
				$(".player").removeClass("active");
				var player = $(".player[data-playerid=" + response.playerId + "]").addClass("active");
				changeScore(player, response.value);
			}
		});
	}

	function changeScore(player, points){
		points = getPoints(player) + points;
		player.find(".score").html(points);
		player.attr("data-score", points);
	}

	function getPoints(player){
		return parseInt(player.attr("data-score"));
	}

	function retractThrows(){
		if(turns > 0){
			undo().done(function(){
				turns--;
				retractThrows();
			});
		} else {
			miss();
		}
	}

	function determineWinners(){
		var winners = $(".player:not(.winner)[data-score=0]");
		if(winners.length > 0){
			winners.addClass("winner");
			players = players.filter(":not(.winner)");
		}
	}

});
