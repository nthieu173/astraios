$(document).ready(function() {
	var ship = document.getElementById("shipImg");
	var scale = document.getElementById("scale").getAttribute("data-scale");
	var ast_list = JSON.parse(document.getElementById("ast_list").getAttribute("data-ast-list"));
	var ship_list = JSON.parse(document.getElementById("ship_list").getAttribute("data-ship-list"));
	var ctx = document.getElementById("radarCanvas").getContext("2d");
	var width = Number(document.getElementById("radarCanvas").getAttribute("width").slice(0,-2));
	var height = Number(document.getElementById("radarCanvas").getAttribute("height").slice(0,-2));
	var de = $("#de-input").val();
	var dt = $("#dt-input").val();
	var ship_name = $("#ship-name").text();
	$("#info").val("{'ship':'"+ship_name+"','de':"+de+",'dt':"+dt+"}");
	draw_all_ship(ship_list);
	draw_field(ast_list);
	ctx.strokeStyle = "white";
	ctx.stroke();
	
	function cen_polygon(cen_obj,plist_array) {
		ctx.moveTo((cen_obj["x"]+plist_array[0]["x"])*scale,(cen_obj["y"]-plist_array[0]["y"])*scale)
		for (let i=1; i<plist_array.length; i++) {
			ctx.lineTo((cen_obj["x"]+plist_array[i]["x"])*scale,(cen_obj["y"]-plist_array[i]["y"])*scale);
		}
		ctx.lineTo((cen_obj["x"]+plist_array[0]["x"])*scale,(cen_obj["y"]-plist_array[0]["y"])*scale);
	}
	
	function polygon(plist_array) {
		ctx.moveTo(plist_array[0]["x"],plist_array[0][1]);
		for (let i=1; i<plist_array.length; i++) {
			ctx.lineTo(plist_array[i][0],plist_array[i][1]);
		}
		ctx.lineTo(plist_array[0][0],plist_array[0][1]);
	}

	function draw_field(ast_field_array) {
		ast_field_array.forEach(function(ast_obj){
			cen_obj = ast_obj["cen"]
			plist_array = ast_obj["plist"]
			cen_polygon(cen_obj,plist_array);
		});
	}
	
	function draw_ship(x,y,angle) {
		ctx.translate(x*scale,y*scale);
		ctx.rotate(-Math.PI/2+angle*Math.PI/180);
		ctx.drawImage(ship,-2*scale,-2*scale,4*scale,4*scale);
		ctx.rotate(+Math.PI/2-angle*Math.PI/180);
		ctx.translate(-x*scale,-y*scale);
	}
	
	function draw_all_ship(ship_array) {
		ship_array.forEach(function(ship){
			draw_ship(ship["x"],ship["y"],ship["o"]);
		})
	}
});

function physics_step() {
	console.log("stepped");
};
