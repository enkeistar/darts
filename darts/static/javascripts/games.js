$(function(){

	var currentPlayer = 1;
	var numberOfPlayers = parseInt($("#number-of-players").val());

	$(".player").on("click", function(){
		var source = $(this);

		var player = (currentPlayer + 1) % 2 + 1;
		var team = Math.floor((currentPlayer - 1) / 2) % 2 + 1;

		$('.value[data-team="' + team + '"][data-player="' + player + '"]').val(source.data("id"));
		$('.selected[data-team="' + team + '"][data-player="' + player + '"]').html(source.html());

		source.remove();

		$(".select-player-instruction").hide();
		$('.select-player-instruction[data-team="' + team + '"][data-player="' + player + '"]').show();

		currentPlayer++;

		if(currentPlayer > numberOfPlayers){
			$(".select-player-instruction").hide();
			$(".player-list").hide();
			$(".done, .redo").show();
		}
	});

	$(".add-player").on("click", function(){

		console.log("click");

	});

});
