$("#bushingSubmit").click(function(e) {
	e.preventDefault();
	var weight = $("#weight").val();
	var weightType = $("#weightType").val();
	var truck = $("#trucks").val();
	var url = "query?weight="+weight+"&weight_type=" + weightType + "&truck="+truck;

	$("#content").load(url + " #content");
});