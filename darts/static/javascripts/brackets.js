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



	$("form").on("submit", function(){
		$("#bracket-form").addClass("hidden");
		$("#bracket-grid").removeClass("hidden");
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