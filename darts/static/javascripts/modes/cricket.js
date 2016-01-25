$(function(){

	var complete = $("input[name=complete]").val() == "1";
	if(complete){
		$(".game-option.new-game").on("click", function(){
			window.location = "/";
		});
		return;
	}

	var player = $(".player.active");
	var gameId = $("input[name=gameId]").val();
	var team1Id = $(".score").first().data("teamid");
	var team2Id = $(".score").last().data("teamid");
	var nextRoundModal = $(".modal-next-round");
	var newGameModal = $(".modal-new-game");
	var game = parseInt($("input[name=game]").val());
	var numPlayers = parseInt($("input[name=players]").val());
	var round = parseInt($("input[name=round]").val());

	var turnTeam = player.parents(".players").data("order");
	var turnPlayer = parseInt(player.data("order"));
	var turnTimeout;
	var turnDelay = 5000;

	setActivePlayer();

	$(".game-option.new-game").on("click", function(){
		newGameModal.show();
	});
	$(".new-game-yes").on("click", function(){
		window.location = "/";
	});
	$(".new-game-no").on("click", function(){
		newGameModal.hide();
	});

	$(".game-option .undo").on("click", function(){
		window.location = "/games/" + gameId + "/undo/";
	});

	$(".game-option .miss").on("click", function(){
		var teamId =  $(".player.active").data("teamid");
		var playerId = $(".player.active").data("playerid");
		$.post("/games/" + gameId + "/teams/" + teamId + "/players/" + playerId + "/games/" + game + "/rounds/" + round + "/marks/0/").done(nextTurn);
	});

	$(".awarded").on("click", function(){

		var source = $(this);
		var hits = parseInt(source.attr("data-hits"));
		var point = source.data("points");
		var teamId = source.data("teamid");
		var playerId = $(".player.active").data("playerid");

		if($(".player.active[data-teamid=" + teamId + "]").length == 0){
			return;
		}

		var points = 0;
		var closed = $(".awarded[data-points=" + point + "]:not([data-teamid=" + teamId + "])").attr("data-hits") >= 3;

		if( hits < 3 || !closed ){
			source.attr("data-hits", hits + 1);
			$.post("/games/" + gameId + "/teams/" + teamId + "/players/" + playerId + "/games/" + game + "/rounds/" + round + "/marks/" + point + "/");
		}

		if( hits >= 3 && !closed ){
			points += source.data("points");
		}

		if(!closed){
			var current = $('.score[data-teamid="' + teamId + '"]');
			current.data("score", current.data("score") + points);
			current.find(".current-round-points").html(current.data("score"));
		}

		var team1Closed = isClosed(team1Id);
		var team2Closed = isClosed(team2Id);
		var team1Score = getScore(team1Id);
		var team2Score = getScore(team2Id);

		if(team1Closed && team1Score >= team2Score){
			win(team1Id);
			loss(team2Id);
			nextRound(1, team1Id, team2Id);
		} else if(team2Closed && team2Score >= team1Score){
			win(team2Id);
			loss(team1Id);
			nextRound(2, team2Id, team1Id);
		}

		clearTimeout(turnTimeout);
		turnTimeout = setTimeout(nextTurn, turnDelay);

	});

	function isClosed(teamId){
		var closed = true;
		$(".awarded[data-teamid=" + teamId + "]").each(function(){
			if($(this).attr("data-hits") < 3){
				closed = false;
			}
		});
		return closed;
	}

	function getScore(teamId){
		return parseInt($(".score[data-teamid=" + teamId + "]").data("score"));
	}

	function setActivePlayer(){
		$(".player").removeClass("active");
		$(".players").eq(turnTeam).find(".player").eq(turnPlayer).addClass("active");

		$(".player-row, .awarded").removeClass("highlight");
		var teamId =  $(".player.active").data("teamid");
		$(".player-row[data-teamid=" + teamId + "]").addClass("highlight");
		$(".awarded[data-teamid=" + teamId + "]").addClass("highlight");

	}

	function getActivePlayer(){
		return parseInt($(".players").find(".active").data("playerid"));
	}

	function nextTurn(){
		if(numPlayers == 4 && turnTeam == 1){
			turnPlayer = turnPlayer == 1 ? 0 : 1;
		}

		turnTeam = turnTeam == 1 ? 0 : 1;

		setActivePlayer();

		var playerId = getActivePlayer();

		$.post("/games/" + gameId + "/players/" + playerId + "/turn/");

		if(turnTeam == 0 && turnPlayer == 0){
			round++;
		}
	}

	function win(id){
		$.post("/games/" + gameId + "/teams/" + id + "/game/" + game + "/score/" + getScore(id) + "/win/");
	}

	function loss(id){
		$.post("/games/" + gameId + "/teams/" + id + "/game/" + game + "/score/" + getScore(id) + "/loss/");
	}

	function gameWin(id){
		$.post("/games/" + gameId + "/teams/" + id + "/win/");
	}

	function gameLoss(id){
		$.post("/games/" + gameId + "/teams/" + id + "/loss/");
	}

	function nextRound(num, winnerId, loserId){

		nextRoundModal.show();

		if($("input[name=result][data-win=1][data-teamid=" + winnerId + "]").length >= 1){
			nextRoundModal.find("h1").html("Team " + num + "<br />Wins The Game!");
			nextRoundModal.find("button").html("Done");
			gameWin(winnerId);
			gameLoss(loserId);
		} else {
			nextRoundModal.find("h1").html("Team " + num + "<br />Wins Round " + game + "!");
		}

	}

});
