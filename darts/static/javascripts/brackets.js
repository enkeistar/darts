$(function(){

	$(".col2 .bracket-player").each(function(){
		var playerid = $(this).data("playerid");
		if(playerid){
			$(".col1 .bracket-player[data-playerid=" + playerid + "]").css("font-weight", "bold");
		}
	});

	$(".col3 .bracket-player").each(function(){
		var playerid = $(this).data("playerid");
		if(playerid){
			$(".col2 .bracket-player[data-playerid=" + playerid + "]").css("font-weight", "bold");
		}
	});

	$(".col4 .bracket-player").each(function(){
		var playerid = $(this).data("playerid");
		if(playerid){
			$(".col3 .bracket-player[data-playerid=" + playerid + "]").css("font-weight", "bold");
		}
	});


	var players;
	var bracketType;

	$("#brackets-details").on("submit", function(){
		$("#bracket-form").addClass("hidden");
		$("#bracket-grid").removeClass("hidden");

		players = parseInt($("select[name=players]").val());
		bracketType = $("select[name=bracketType]").val();

		$("input[name=players]").val(players);
		$("input[name=bracketType]").val(bracketType);

		if(players == 8){
			$(".col1 .bracket-player").each(function(i, el){
				if(i >= 8){
					$(el).remove();
				}
			});
			$(".col2 .bracket-player").each(function(i, el){
				if(i >= 4){
					$(el).remove();
				}
			});
			$(".col3 .bracket-player").each(function(i, el){
				if(i >= 2){
					$(el).remove();
				}
			});
			$(".col4").remove();
		}

		if(bracketType == "single"){
			$(".bracket-player-select").each(function(i, el){
				if(i % 2 == 1){
					$(el).remove();
				}
			});
		}

		return false;
	});


	$(".bracket-player-select").val("").find("option").prop("disabled", false);

	$(".bracket-player-select").on("change", function(){
		var source = $(this);
		var currentValue = source.val();
		var previousValue = source.data("prev");
		if(previousValue){
			$(".bracket-player-select").not(source).find("option[value=" + previousValue + "]").prop("disabled", false).show();
		}
		if(currentValue){
			$(".bracket-player-select").not(source).find("option[value=" + currentValue + "]").prop("disabled", true).hide();
		}
		source.data("prev", currentValue);
	});

});