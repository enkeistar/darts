$(function(){

	var player;
	var gameId = $("input[name=gameId]").val();

	$(".game-option.new-game").on( 'click', function(){
		if(confirm( 'Are you sure you want to start a new game?' )){
			window.location = '/games/new/';
		}
	});

	var undo = false;

	$(".player").on("click", function(){
		$(".player").removeClass("active");
		$(this).addClass("active");
	});

	$( '.game-option.undo' ).on( 'click', function(){

		var source = $( this );
		source.toggleClass( 'active' );
		undo = source.hasClass( 'active' );
		source.html("Click<br />Score");

	});

	$( '.awarded' ).on( 'click', function(){

		var source = $( this );
		var points = 0;
		var hits = parseInt( source.attr( 'data-hits' ) );

		var teamId = source.data("team");
		var playerId = $(".player").first().addClass("active").data("player");
		var point = source.data("points");
		var closed = $('.awarded[data-points="' + point + '"]:not([data-team="' + teamId + '"]' ).attr("data-hits") >= 3;

		if( undo ){

			if( hits > 0 ){

				source.attr("data-hits", hits - 1 );

			}

			if( hits > 3 ){

				points -= source.data("points");

			}

			$(".game-option.undo").click().html("Remove<br />Score");

		} else {

			if( hits < 3 || !closed ){

				source.attr("data-hits", hits + 1 );

				var data =  {
					teamId: teamId,
					playerId: playerId,
					points: point,
					round: 1
				};

				$.post("/games/" + gameId + "/score", data, function(data){
					console.log(data);
				});

			}

			if( hits >= 3 && !closed ){

				points += source.data("points");

			}

		}

		if( !closed ){

			var current = $('.score[data-team="' + teamId + '"]');
			current.data("score", current.data("score") + points );
			current.html( current.data("score") );

		}

	});

});
