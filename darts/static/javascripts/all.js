$(function(){

	$(".btn.delete").on("click", function(){
		var source = $(this);
		return confirm(source.data("message"));
	});

});
