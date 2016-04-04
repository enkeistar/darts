$(function(){


	var layers = [];

	var canvas = this.__canvas = new fabric.Canvas("mark-style", {
		isDrawingMode: true,
		selection: false
	});

	fabric.Object.prototype.transparentCorners = false;

	var $drawingColor = $("#drawing-color");
	var $drawingLineWidth = $("#drawing-line-width");



	canvas.freeDrawingBrush = new fabric['PencilBrush'](canvas);

	$drawingColor.on("change", function(){
		canvas.freeDrawingBrush.color = this.value;
	});

	$drawingLineWidth.on("change", function() {
		canvas.freeDrawingBrush.width = parseInt(this.value, 10) || 1;
		$("#drawing-line-width-info").html(this.value);
	}).trigger("change");

	if (canvas.freeDrawingBrush) {
		canvas.freeDrawingBrush.color = $drawingColor.val();
		canvas.freeDrawingBrush.width = parseInt($drawingLineWidth.val(), 10) || 1;
	}

	$("#clear-canvas").on("click", function(){
		canvas.clear();
		layers = [];
		enableDrawing();
		renderLayers();
	});

	canvas.on("mouse:down", function(options){
		return false;
	});

	canvas.on("mouse:up", function(){
		alert("mouse:up");
	});
	canvas.on("mouse:out", function(){
		alert("mouse:out");
	});

	canvas.on("mouse:up", function(options) {
		console.log(this);
		layers.push({
			png: canvas.toDataURL(),
			svg: canvas.toSVG()
		});
		if(layers.length >= 3){
			disableDrawing();
		}
		renderLayers();
	});

	function renderLayers(){
		$(".layers").empty();
		for(var idx in layers){
			$("#layer-" + idx).html($("<img />").attr("src", layers[idx]["png"]));
		}
	}

	function disableDrawing(){
		canvas.isDrawingMode = false;
		canvas.deactivateAll();
		canvas.forEachObject(function(o) {
			o.selectable = false;
		});
		$("form").find("button[type=submit]").prop("disabled", false);
	}

	function enableDrawing(){
		canvas.isDrawingMode = true;
		$("form").find("button[type=submit]").prop("disabled", true);
	}


	$("form").on("submit", function(){
		if(layers.length != 3){
			return false;
		}

		var source = $(this);
		source.find("input[name=one]").val(layers[0]["svg"]);
		source.find("input[name=two]").val(layers[1]["svg"]);
		source.find("input[name=three]").val(layers[2]["svg"]);
	});

});