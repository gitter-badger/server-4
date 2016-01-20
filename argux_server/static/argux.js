$("#toggle-fullscreen").click(function(e) {
    $("body").toggleClass("fs");
    $("body").toggleClass("no-fs");
    $("#toggle-fullscreen > span").toggleClass("glyphicon-fullscreen");
    $("#toggle-fullscreen > span").toggleClass("glyphicon-resize-small");
});
