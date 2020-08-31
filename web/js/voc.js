var jsonUrl = "voc.json";
var vocUrl;// = "http://localhost:9000/lookup";
var port;
var jsonData;
var $vocListContainer = $("#vocListContainer");
var $vocForm = $("#vocForm");
var $voc_template = $(".voc_template").clone();
var $def_template = $(".def_template").clone();
$(".voc_template").remove();
$(".def_template").remove();
$vocListContainer.height(window.innerHeight-100);
var simpleBar = new SimpleBar($vocListContainer[0]);
simpleBar.recalculate();
$vocContainer = $vocListContainer.find(".simplebar-content");

$.getJSON("../../config/config.json", function(data){
	port = data["port"].toString();
	vocUrl = "http://"+window.location.host + "/lookup";
});

function getData(url, func=null){
	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",
		success: function(data){
			jsonData = data;
			if(func != null){
				func(data);
			}
		},
		error: function(){
			alertmsg("Server Error!");
		}
	});
}

function genDiv(res){
	var data = res["voc"];
	var sc = res["sc"];
	var orm = res["orm"];
	var $voc = $voc_template.clone();
	var word;
	if(data!=null){
		word = data["word"];
		var audio = data["audio"];
		console.log(audio);
		var defs = data["defs"];
		var stems = data["stems"];
		var syns = data["syns"];
		var ants = data["ants"];
		$voc.find(".word").text(word);
		if(data.hasOwnProperty("audio")){
			var $audioBtn = $('<span><i class="fas fa-volume-up"></span>').attr("data-audio", data["audio"]).css("cursor", "pointer");
			//$voc.find(".word").parent().append($i);
			$voc.find(".audio").after($audioBtn);
			$voc.find(".audio").find("source").attr("src", audio).closest(".audio")[0].play();
			$audioBtn.click(function(){
				$voc.find(".audio")[0].play();
			});
		}
		//$voc.find(".audio").find("source").attr("src", audio).closest(".audio")[0].play();
		genDefs($voc.find(".defs"), data["defs"]);
		$voc.find(".stems").text(stems);
		if(data["syns"]) $voc.find(".syns").text(syns.join(", "));
		if(data["ants"]) $voc.find(".ants").text(ants.join(", "));
	}
	if(sc!=null)
		$voc.find(".sc .content").html(sc['error'] + "Possible Candidates: <strong>" + sc["candi"] + "</strong>");

	$voc.find(".orm .mdcontent").html(marked(orm["note"]));
	$voc.find(".orm .last_update").html(orm["last_update"]);
	$voc.find(".orm .editBtn").attr("data-note", orm["note"]).attr("data-word", word);

	$vocContainer.prepend($voc);
	anime({
	  targets: $voc[0],
	  backgroundColor: "#a3a3ff",
	  direction: 'alternate',
	});
	simpleBar.getScrollElement().scrollTop = 0;
}

function genDefs($ul, data){
	data.forEach(function(item, idx){
		var $def = $def_template.clone();
		$def.find(".fl").text(item["fl"]);
		$def.find(".text").text(item["text"]);
		if(item.hasOwnProperty("vis"))
			$def.find(".vis").text(item["vis"]);
		$ul.append($def);
	});
	colorify($ul);
}

function clearDiv(){
	anime({
	  targets: ".voc_template",
	  backgroundColor: "#ffa3a3",
	  direction: 'alternate',
	  complete: function(anime){
	  	$(".voc_template").remove();
	  }
	});
}

function colorify($ele){
	$.each($ele.find(".fl"), function(idx, item){
		//console.log(item);
		if($(item).text() == "adverb"){
			$(item).css("background-color", "green");
		}else if($(item).text() == "adjective"){
			$(item).css("background-color", "red");
		}else if($(item).text() == "noun"){
			$(item).css("background-color", "blue");
		}else if($(item).text() == "verb"){
			$(item).css("background-color", "purple");
		}else if($(item).text() == "preposition"){
			$(item).css("background-color", "chocolate");
		}else if($(item).text() == "conjunction"){
			$(item).css("background-color", "pink");
		}
	});
}

function submitform(e){
	console.log("submit!");
	var word = $vocForm.find('input[name="word"]').val();
	var url = vocUrl + "?word=" + word;
	getData(url, genDiv);
	return false;
}

$(function(){
	$vocForm.on("submit", submitform);
	$("#voc_clear").on("click", clearDiv);
});