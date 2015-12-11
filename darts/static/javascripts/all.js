$(function(){

	var deleteModal = $(".modal-delete");
	var deleteForm;

	$(".btn.delete").on("click", function(){
		var source = $(this);

		deleteModal.find(".message").html(source.data("message"));
		deleteModal.show();

		deleteForm = $("#" + source.data("form"));

		return false;
	});

	$(".modal-delete").find(".action-yes").on("click", function(){
		deleteForm.submit();
	});

	$(".modal-delete").find(".action-no").on("click", function(){
		deleteModal.hide();
	});

});
