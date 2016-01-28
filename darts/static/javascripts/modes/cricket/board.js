$(function(){

	var complete = $("input[name=complete]").val() == "1";
	if(complete){
		$(".game-option .home").on("click", function(){
			window.location = "/";
		});
		return;
	}

	var gameId = $("input[name=gameId]").val();
	var team1Id = $(".score").first().data("teamid");
	var team2Id = $(".score").last().data("teamid");
	var nextRoundModal = $(".modal-next-round");
	var homeModal = $(".modal-home");
	var game = parseInt($("input[name=game]").val());
	var numPlayers = parseInt($("input[name=players]").val());
	var round = parseInt($("input[name=round]").val());

	var turnTimeout;
	var turnDelay = 500;

	var baseUrl = "/games/" + gameId + "/modes/cricket";

	highlightTeam();

	$(".game-option .home").on("click", function(){
		homeModal.show();
	});
	$(".home-yes").on("click", function(){
		window.location = "/";
	});
	$(".home-no").on("click", function(){
		homeModal.hide();
	});

	$(".game-option .undo").on("click", undo);

	$(".game-option .turn").on("click", nextTurn);

	$(".game-option .miss").on("click", function(){
		var teamId =  $(".player.active").data("teamid");
		var playerId = $(".player.active").data("playerid");
		$.post(baseUrl + "/teams/" + teamId + "/players/" + playerId + "/games/" + game + "/rounds/" + round + "/marks/0/").done(nextTurn);
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
			$.post(baseUrl + "/teams/" + teamId + "/players/" + playerId + "/games/" + game + "/rounds/" + round + "/marks/" + point + "/");
		}

		if( hits >= 3 && !closed ){
			points += source.data("points");
		}

		if(!closed){
			var current = $('.score[data-teamid="' + teamId + '"]');
			current.data("score", current.data("score") + points);
			current.find(".current-round-points").html(current.data("score"));
		}

		determineWinner();

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

	function highlightTeam(){
		$(".player-row, .awarded").removeClass("highlight");
		var teamId =  $(".player.active").data("teamid");
		$(".player-row[data-teamid=" + teamId + "]").addClass("highlight");
		$(".awarded[data-teamid=" + teamId + "]").addClass("highlight");

	}

	function getActivePlayer(){
		return parseInt($(".players").find(".active").data("playerid"));
	}

	function nextTurn(){

		var players = $(".player");

		var position = 0;
		for( var i = 0; i < players.length; i++){
			var player = $(players[i]);
			if(player.hasClass("active")){
				position = i;
				break;
			}
		}

		players.removeClass("active");


		if(players.length == 4){

			var index = 0;
			switch(position){
				case 0:
					index = 2;
					break;
				case 1:
					index = 3;
					break;
				case 2:
					index = 1;
					break;
				case 3:
					index = 0;
					break;
			}

		} else {

			var index = position == 0 ? 1 : 0;

		}

		if(index == 0){
			round++;
		}

		var playerId = $(players[index]).addClass("active").data("playerid");
		$.post(baseUrl + "/players/" + playerId + "/turn/");
		highlightTeam();
	}

	function win(id){
		$.post(baseUrl + "/teams/" + id + "/game/" + game + "/score/" + getScore(id) + "/win/");
	}

	function loss(id){
		$.post(baseUrl + "/teams/" + id + "/game/" + game + "/score/" + getScore(id) + "/loss/");
	}

	function gameWin(id){
		$.post(baseUrl + "/teams/" + id + "/win/");
	}

	function gameLoss(id){
		$.post(baseUrl + "/teams/" + id + "/loss/");
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

	function determineWinner(){

		var team1Closed = isClosed(team1Id);
		var team2Closed = isClosed(team2Id);
		var team1Score = getScore(team1Id);
		var team2Score = getScore(team2Id);

		var team1Wins = team1Closed && team1Score >= team2Score;
		var team2Wins = team2Closed && team2Score >= team1Score;

		if(team1Wins){
			win(team1Id);
			loss(team2Id);
			nextRound(1, team1Id, team2Id);
		} else if(team2Wins){
			win(team2Id);
			loss(team1Id);
			nextRound(2, team2Id, team1Id);
		}

	}

	function undo(){
		return $.post(baseUrl + "/undo/", function(response){
			if(response.valid){

				if(response.redirect){
					window.location = baseUrl + "/play/";
					return;
				}

				$(".player").removeClass("active");
				$(".player[data-playerid=" + response.playerId + "]").addClass("active");
				highlightTeam();

				var awarded = $(".awarded[data-teamid=" + response.teamId + "][data-points=" + response.value + "]");
				var hits = parseInt(awarded.attr("data-hits")) - 1;
				awarded.attr("data-hits", hits);

				if(hits >= 3){
					var current = $(".score[data-teamid=" + response.teamId + "]");
					current.data("score", current.data("score") - response.value);
					current.find(".current-round-points").html(current.data("score"));
				}
			}
		});
	}

});
