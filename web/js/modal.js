var $msgbox = $("#msgbox");
var $msg = $("#msg");
var $msgCloseBtn = $("#msgCloseBtn");
var $editBtn = $(".editBtn");
var $modal = $("#modal");
var $modalCloseBtn = $(".modalCloseBtn");
var $confirm = $(".confirm");
var $cancel = $(".cancel");
var word;
var $cur_edit_btn;
var $cur_note_content;
var $cur_orm;

var $editor = $("#editor");
var $codemirror = $('#codemirror');
var quill = new Quill('#editor', {theme: 'snow', formats:[]});
var codemirror = CodeMirror.fromTextArea($("#codemirror")[0],{
                mode:"markdown", 
                lineNumbers:true,
                theme: "monokai"
        });
//var $
$("body").on("click",".editBtn", function(){
	word = $(this).attr("data-word");
	//quill.setText($(this).attr("data-note"));
	codemirror.setValue($(this).attr("data-note"));
	$cur_edit_btn = $(this);
	$cur_note_content = $(this).closest(".orm").find(".mdcontent");
	$cur_orm = $(this).closest(".orm");
	$modal.fadeIn();
});

$modalCloseBtn.click(function(){
	$modal.fadeOut();
});

$confirm.click(function(){
	$modal.fadeOut();
	$.ajax({
		type: "POST",
		url: "/update",
		dataType: "json",
		data: "word=" + word + "&note=" + codemirror.getValue(),//quill.getText(),
		success: function(data){
			console.log(data);
			if(data["res"] == true){
				$cur_orm.find(".editBtn").attr("data-note", data["note"]);
				$cur_orm.find(".mdcontent").html(marked(data["note"]));
				$cur_orm.find(".last_update").html(data["last_update"]);
				infomsg("Successfully update!");
			}else{
				alertmsg("Update Failed!");
			}
		},
		error: function(){
			alertmsg("Server Error!");
		} 
	});
});

function alertmsg(msg){
	$msgbox.addClass("msgalert");
	$msg.html(msg);
	$msgbox.slideDown();
}

function infomsg(msg){
	$msgbox.addClass("msginfo");
	$msg.html(msg);
	$msgbox.slideDown();
}

$cancel.click(function(){
	$modal.fadeOut();
});

$msgCloseBtn.click(function(){
	$msgbox.slideUp(function(){
		$msgbox.removeClass();
	});
});

