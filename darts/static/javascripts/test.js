$(function(){

	setTimeout(function(){

		var playersPattern = new RegExp("\/games\/[0-9]+\/players\/");
		var gamePattern = new RegExp("\/games\/[0-9]+\/");

		if(window.location.pathname == "/"){

			window.location = "/games/new/";

		} else if(window.location.pathname == "/games/new/"){

		 	$(".number-of-players").eq(randRange(0,1)).click();

		} else if(playersPattern.test(window.location)){

			function clickPlayer(num){

				$(".player").eq(randRange(0, $(".player").length - 1)).click();

				setTimeout(function(){
					if(num > 0){
						clickPlayer(num - 1);
					} else {
						$(".play").click();
					}
				}, 200);

			}

			clickPlayer($(".selected").length - 1);

		} else if(gamePattern.test(window.location)){

			var items = $(".awarded");

			function mark(num){

				if($(".modal-box.modal-next-round").is(":visible") || $(".modal-box.modal-new-game").is(":visible")){
					setTimeout(function(){
						$(".btn-next-round").click();
					}, 500);
					return;
				}

				if(num < 0){
					$(".miss").click();
					mark(items.length - 1);
					return;
				}

				var item = items[num];

				function markItem(itemNum){

					if(itemNum < 0){
						mark(num - 1);
						return;
					}

					if(randRange(0,5) == 0){
						item.click();
						setTimeout(function(){
							markItem(itemNum - 1);
						}, 20);
					} else {
						markItem(itemNum - 1);
					}

				}

				markItem(2);

			}

			mark(items.length - 1);

		}

		function randRange(min, max) {

			return Math.floor(Math.random() * (max - min + 1)) + min;

		}

		var running = true;

		$(document).ajaxStart(function(){
			running = true;
		});
		$(document).ajaxStop(function(){
			running = false;
		});

	}, 500);

});