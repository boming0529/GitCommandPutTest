$(function () {
    var thHeight = $(".table th:first").height();
    $(".table th").resizable({
        handles: "e",
        minHeight: thHeight,
        maxHeight: thHeight,
        minWidth: 40,
        resize: function (event, ui) {
            var sizerID = ".table" + "-sizer";
            $(sizerID).width(ui.size.width);
        }
    });
});