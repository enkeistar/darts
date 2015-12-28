$(function(){

	var player;
	var gameId = $("input[name=gameId]").val();
	var team1Id = $(".score").first().data("team");
	var team2Id = $(".score").last().data("team");
	var nextRoundModal = $(".modal-next-round");
	var newGameModal = $(".modal-new-game");
	var game = $("input[name=game]");
	var numPlayers = parseInt($("input[name=players]").val());
	var round = $("input[name=round]");

	var undo = false;

	var turnTeam = 0;
	var turnPlayer = 0;
	var turnTimeout;
	var turnDelay = 5000;

	setActivePlayer();
	setPlayerForGame();

	$(".game-option.new-game").on("click", function(){
		newGameModal.show();
	});
	$(".new-game-yes").on("click", function(){
		window.location = "/";
	});
	$(".new-game-no").on("click", function(){
		newGameModal.hide();
	});

	$(".game-option.undo").on("click", function(){

		console.log("UNDO");

	});

	$(".awarded").on("click", function(){

		var source = $(this);
		var hits = parseInt(source.attr("data-hits"));
		var point = source.data("points");
		var teamId = source.data("team");
		var playerId = $(".player.active").data("playerid");

		if($(".player.active[data-teamid=" + teamId + "]").length == 0){
			return;
		}


		var points = 0;
		var closed = $(".awarded[data-points=" + point + "]:not([data-team=" + teamId + "])").attr("data-hits") >= 3;

		if( hits < 3 || !closed ){
			source.attr("data-hits", hits + 1);
			$.post("/games/" + gameId + "/teams/" + teamId + "/players/" + playerId + "/games/" + game.val() + "/rounds/" + round.val() + "/marks/" + point + "/");
		}

		if( hits >= 3 && !closed ){
			points += source.data("points");
		}

		if(!closed){
			var current = $('.score[data-team="' + teamId + '"]');
			current.data("score", current.data("score") + points);
			current.find(".current-round-points").html(current.data("score"));
		}

		var team1Closed = isClosed(team1Id);
		var team2Closed = isClosed(team2Id);
		var team1Score = getScore(team1Id);
		var team2Score = getScore(team2Id);
		var nextRound = parseInt(game.val()) + 1;

		if(team1Closed && team1Score >= team2Score){
			nextRoundModal.show();
			nextRoundModal.find("h1").html("Team 1 Wins Game " + game.val() + "!!");
		} else if(team2Closed && team2Score >= team1Score){
			nextRoundModal.show();
			nextRoundModal.find("h1").html("Team 2 Wins Game " + game.val() + "!!");
		}

		clearTimeout(turnTimeout);
		turnTimeout = setTimeout(nextPlayer, turnDelay);


	});

	function isClosed(teamId){
		var closed = true;
		$(".awarded[data-team=" + teamId + "]").each(function(){
			if($(this).attr("data-hits") < 3){
				closed = false;
			}
		});
		return closed;
	}

	function getScore(teamId){
		return parseInt($(".score[data-team=" + teamId + "]").data("score"));
	}

	function setActivePlayer(){
		$(".player").removeClass("active");
		$(".players").eq(turnTeam).find(".player").eq(turnPlayer).addClass("active");
	}

	function nextPlayer(){
		if(numPlayers == 4 && turnTeam == 1){
			turnPlayer = turnPlayer == 1 ? 0 : 1;
		}

		turnTeam = turnTeam == 1 ? 0 : 1;

		setActivePlayer();
	}

	function setPlayerForGame(){
		var thisGame = parseInt(game.val());

		if(thisGame > 1){
			nextPlayer();
			if(thisGame > 2){
				nextPlayer();
			}
		}
	}

});
