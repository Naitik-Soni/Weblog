function boldSelectedText() {
    var textarea = document.getElementById("blogcontent");
    var selectedText = window.getSelection().toString();
    var boldText = "<b>" + selectedText + "</b>";
    document.execCommand('insertHTML', false, boldText);
}

function italicSelectedText() {
    var textarea = document.getElementById("blogcontent");
    var selectedText = window.getSelection().toString();
    var iText = "<i>" + selectedText + "</i>";
    document.execCommand('insertHTML', false, iText);
}

function underlineSelectedText() {
    var textarea = document.getElementById("blogcontent");
    var selectedText = window.getSelection().toString();
    var ulText = "<u>" + selectedText + "</u>";
    document.execCommand('insertHTML', false, ulText);
}

function biggerSelectedText() {
    var textarea = document.getElementById("blogcontent");
    var selectedText = window.getSelection().toString();
    var bigText = "<big>" + selectedText + "</big>";
    document.execCommand('insertHTML', false, bigText);
}

function smallerSelectedText() {
    var textarea = document.getElementById("blogcontent");
    var selectedText = window.getSelection().toString();
    var smallText = "<small>" + selectedText + "</small>";
    document.execCommand('insertHTML', false, smallText);
}

function changeColor() {
    var textarea = document.getElementById("blogcontent");
    var color = document.getElementById("colorpicker").value;

    var selection = window.getSelection();
    if (selection.rangeCount > 0) {
      var range = selection.getRangeAt(0);
      var span = document.createElement("span");
      span.style.color = color;
      range.surroundContents(span);
    }
}

function imageAdded(){
    console.log(document.getElementById("imageinput").files[0]);
    document.getElementById("imageicon").src = "/static/media/tick.png";
}


function postBlog() {
    var title = document.getElementById("title").value;
    var image = document.getElementById("imageinput").value;
    var content = document.getElementById("blogcontent").innerHTML;

    if(
        title == "" ||
        content.length < 1 ||
        image.value == ""
    ){
        swal("Empty Fields", "All fields are compulsory", "error");
    }
    else{
        document.getElementById("textarea").value = document.getElementById("blogcontent").innerHTML;
        document.getElementById("userform").submit();
    }
}

function clearInitial(){
    var divi = document.getElementById("blogcontent").innerHTML;
    if(divi.trim() == "Start Writing From here..."){
        document.getElementById("blogcontent").innerHTML = "";
    }
}
