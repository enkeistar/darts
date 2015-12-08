$(function(){

	var player;
	var gameId = $("input[name=gameId]").val();
	console.log(gameId);

	$( '.player' ).on( 'click', function(){

		usersList.fadeIn( 200 );
		player = $( this ).data( 'player' );
		search.val( '' );

		var container = $("#user-list");
		container.html("");

		var template = $("<div />").addClass("user");

		$.get("/users/", function(data){

			for(var i = 0; i < data.length; i++){
				var user = data[i];
				var name = user.firstName + " " + user.lastName;
				container.append(template.clone().html(name).data("name", name).data("id", user.id));
			}
		});

		search.focus();

	});

	$( "#user-list" ).on( 'click', '.user', function(){

		var source = $( this );
		var name = source.data("name");
		var $player = $( '.player[data-player="' + player + '"]' );

		$player.addClass( 'set' );
		$player.find( '.initial' ).html( name.substring( 0, 1 ) );
		$player.find( '.name' ).html( name );

		usersList.fadeOut( 200 );

	});

	$( '.game-option.new-game' ).on( 'click', function(){
		if(confirm( 'Are you sure you want to start a new game?' )){
			window.location = '/games/new/';
		}
	});

	var undo = false;

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
		var playerId = $(".player").first().data("player");
		var point = source.data("points");

		// var otherTeam = source.data( 'team' ) == 1 ? 2 : 1;
		// var closed = ( $( '.awarded[data-team="' + otherTeam + '"][data-points="' + source.data( 'points' ) + '"]' ).attr( 'data-hits' ) >= 3 );
		var closed = false;

		if( undo ){

			if( hits > 0 ){

				source.attr( 'data-hits', hits - 1 );

			}

			if( hits > 3 ){

				points -= source.data( 'points' );

			}

			$( '.game-option.undo' ).click().html("Remove<br />Score");

		} else {

			if( hits < 3 || !closed ){

				source.attr( 'data-hits', hits + 1 );

			}

			if( hits >= 3 && !closed ){

				points += source.data( 'points' );

			}

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

		if( !closed ){

			var current = $( '.score[data-team="' + source.data( 'team' ) + '"]' );
			current.data( 'score', current.data( 'score' ) + points );
			current.html( current.data( 'score' ) );

		}

	});

	$("#user-form").on("submit", function(e){

		e.preventDefault();
		var source = $(this);

		$.post("/users/", source.serialize(), function(data){

			var name = data.firstName + " " + data.lastName;
			var $player = $( '.player[data-player="' + player + '"]' );

			$player.addClass( 'set' );
			$player.find( '.initial' ).html( name.substring( 0, 1 ) );
			$player.find( '.name' ).html( name );

			usersForm.fadeOut( 200 );

			source.trigger("reset");

		});

	});

	$(".users-form .cancel").on("click", function(e){
		e.preventDefault();
		usersForm.fadeOut(200);
	});

});
