$(document).ready(function(){
	$.getJSON("json/notes.json", function(data){
		$.each(data.items, function(i,item){
			obj = JSON.parse(item);
			document.getElementById("testfield").innerHTML = obj.name + " " + obj.sex;
		});
	});

	$("button").click(function(){
		id = "#" + $(this).attr('id').slice(0, -6);
		$(id).slideToggle();
	});
});