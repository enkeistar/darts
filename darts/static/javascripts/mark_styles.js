$(function(){

	var layers = [];
	var history = [];
	var addHistory = true;

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

	$drawingLineWidth.on("input", function() {
		canvas.freeDrawingBrush.width = parseInt(this.value, 10) || 1;
		$("#drawing-line-width-info").html(this.value);
	}).trigger("input");

	if (canvas.freeDrawingBrush) {
		canvas.freeDrawingBrush.color = $drawingColor.val();
		canvas.freeDrawingBrush.width = parseInt($drawingLineWidth.val(), 10) || 1;
	}

	$("#clear-canvas").on("click", function(){
		canvas.clear();
		layers = [];
		enableDrawing();
		renderLayers();
		history = [];
	});

	$("#clear-layer").on("click", function(){
		canvas.clear();
		history.push(JSON.stringify(canvas));
	});

	$("#add-layer").on("click", function() {
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
		$("#mark-style-form").find("button[type=submit]").prop("disabled", false);
		$("#add-layer, #clear-layer").prop("disabled", true);
	}

	function enableDrawing(){
		canvas.isDrawingMode = true;
		$("#mark-style-form").find("button[type=submit]").prop("disabled", true);
		$("#add-layer, #clear-layer").prop("disabled", false);
	}


	$("#mark-style-form").on("submit", function(){
		if(layers.length != 3){
			return false;
		}

		var source = $(this);
		source.find("input[name=one]").val(layers[0]["svg"]);
		source.find("input[name=two]").val(layers[1]["svg"]);
		source.find("input[name=three]").val(layers[2]["svg"]);
	});

	$(".form-delete").on("submit", function(){
		return confirm("Are you sure you want to delete this mark style?");
	});


	canvas.on("object:added", function(){
		if(!addHistory) return;
		history.push(JSON.stringify(canvas));
	});

	$("#undo-btn").on("click", function(){
		addHistory = false;
		history.pop();
		if(history.length > 0){
			canvas.loadFromJSON(history[history.length - 1]);
		} else {
			canvas.clear();
		}
		canvas.renderAll();
		addHistory = true;
	});

});
