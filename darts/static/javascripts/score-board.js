$(function(){

	var player;
	var gameId = $("input[name=gameId]").val();
	var team1Id = $(".score").first().data("team");
	var team2Id = $(".score").last().data("team");
	var nextRoundModal = $(".modal-next-round");
	var newGameModal = $(".modal-new-game");
	var round = $("input[name=round]");

	var undo = false;

	var turnTeam = 0;
	var turnPlayer = 0;
	var turnTimeout;
	var turnDelay = 5000;

	setActivePlayer();
	setPlayerForRound();

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
		var source = $( this );
		source.toggleClass("active");
		undo = source.hasClass("active");
		source.html("Click<br />Score");
	});

	$(".awarded").on("click", function(){

		var source = $( this );
		var points = 0;
		var hits = parseInt(source.attr("data-hits"));

		var teamId = source.data("team");
		var playerId = $(".player.active").data("playerid");
		var point = source.data("points");
		var closed = $(".awarded[data-points=" + point + "]:not([data-team=" + teamId + "])").attr("data-hits") >= 3;

		var data =  {
			teamId: teamId,
			playerId: playerId,
			points: point,
			round: round.val()
		};

		if( undo ){

			if( hits > 0 ){
				source.attr("data-hits", hits - 1 );

				$.post("/games/" + gameId + "/undo", data, function(data){
					console.log(data);
				});
			}

			if( hits > 3 ){
				points -= source.data("points");
			}

			$(".game-option.undo").click().html("Remove<br />Score");

		} else {

			if( hits < 3 || !closed ){

				source.attr("data-hits", hits + 1 );

				$.post("/games/" + gameId + "/score", data, function(data){
					console.log(data);
				});

			}

			if( hits >= 3 && !closed ){
				points += source.data("points");
			}

		}

		if(!closed){
			var current = $('.score[data-team="' + teamId + '"]');
			current.data("score", current.data("score") + points );
			current.html(current.data("score"));
		}

		var team1Closed = isClosed(team1Id);
		var team2Closed = isClosed(team2Id);
		var team1Score = getScore(team1Id);
		var team2Score = getScore(team2Id);
		var nextRound = parseInt(round.val()) + 1;

		if(team1Closed && team1Score >= team2Score){
			nextRoundModal.show();
			nextRoundModal.find("h1").html("Team 1 Wins Round " + round.val() + "!!");
			nextRoundModal.find(".round-number").html(nextRound);
		} else if(team2Closed && team2Score >= team1Score){
			nextRoundModal.show();
			nextRoundModal.find("h1").html("Team 2 Wins Round " + round.val() + "!!");
			nextRoundModal.find(".round-number").html(nextRound);
		}

		clearTimeout(turnTimeout);
		turnTimeout = setTimeout(nextPlayer, turnDelay);

	});

	$(".btn-next-round").on("click", function(){
		var nextRound = parseInt(round.val()) + 1;
		$.post("/games/" + gameId + "/round", { round: nextRound }, function(data){
			nextRoundModal.hide();
			$(".awarded").attr("data-hits", 0).attr("data-points", 0);
			$(".score").attr("data-score", 0).html(0);
			round.val(nextRound);
			setActivePlayer();
		});
	});

	$(".player").on("click", function(){
		var source = $(this);
		$(".player").removeClass("active");

		source.addClass("active");
		turnTeam = parseInt(source.parent(".players").data("order"));
		turnPlayer = parseInt(source.data("order"));
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
		if(turnTeam == 1){
			turnPlayer = turnPlayer == 1 ? 0 : 1;
		}

		turnTeam = turnTeam == 1 ? 0 : 1;

		setActivePlayer();
	}

	function setPlayerForRound(){
		var thisRound = parseInt(round.val());

		if(thisRound >= 2){
			nextPlayer();
		}
		if(thisRound == 3){
			nextPlayer();
		}
	}

});
