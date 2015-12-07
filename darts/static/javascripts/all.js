$(function(){

	$(".btn.delete").on("click", function(){
		var source = $(this);
		return confirm(source.data("message"));
	})

	var usersList = $( '.users-list' );
	var usersForm = $( '.users-form' );
	var search = $( '.player-search' );
	var player;

	$( '.back' ).on( 'click', function(){
		usersList.fadeOut( 200 );
	});

	$( '.new' ).on( 'click', function(){
		usersForm.show();
		usersList.hide();
	});

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

	search.on( 'input', function(){

		var terms = $( this ).val().toLowerCase().replace(/\s/g, "").split("");

		$( '.user' ).show().each( function(){

			var source = $( this ).hide();
			var name = source.data("name");
			var search = name.trim().toLowerCase();
			var letters = name.split("");

			var found = true;
			for(var i = 0; i < terms.length; i++){
				var letter = terms[i];
				if(search.indexOf(letter) == -1){
					found = false;
				}
			}

			var html = "";
			for(var i = 0; i < letters.length; i++){
				var letter = letters[i];
				if(terms.indexOf(letter.toLowerCase()) == -1){
					html += letter;
				} else {
					html += "<strong>" + letter + "</strong>";
				}
			}
			if(found){
				source.show().html(html);
			}
		});

	});


	$( '.game-option.new-game' ).on( 'click', function(){
		if(confirm( 'Are you sure you want to start a new game?' )){
			window.location = '/';
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

		var otherTeam = source.data( 'team' ) == 1 ? 2 : 1;
		var closed = ( $( '.awarded[data-team="' + otherTeam + '"][data-points="' + source.data( 'points' ) + '"]' ).attr( 'data-hits' ) >= 3 );

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


	/*


	var callbacks = {

		users: {

			list: function(users){

				var container = $(".view-user-list").html("");

				for(var i = 0; i < users.length; i++){
					var user = users[i];
					container.append($("<div />").html(user.firstName + " " + user.lastName));
				}

			},
			create: function(id){
				console.log(id);
			}
		}
	};



	$(".js-action").on("click", function(){
		var source = $(this);

		$(".view").hide();

		if(source.data("request")){

			$.get(source.data("request"), function(data){

				if(source.data("view")){
					$(".view-" + source.data("view")).show();
					if(source.data("renderer")){
						var parts = source.data("renderer").split(".");
						callbacks[parts[0]][parts[1]](data);
					}
				}

			});

		} else if(source.data("view")){

			$(".view-" + source.data("view")).show();

		}

	});


	$("form").on("submit", function(){
		var source = $(this);

		$.post(source.attr("action"), source.serialize(), function(data){

			var parts = source.data("renderer").split(".");
			callbacks[parts[0]][parts[1]](data);

		});

		return false;
	});

	*/

});
