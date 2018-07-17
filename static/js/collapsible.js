var collapsibles = document.getElementsByClassName("collapsible");
var i;
for (i = 0; i < collapsibles.length; i += 1) {
    collapsibles[i].addEventListener("click", function() {
        this.classList.toggle("active-collapsible");
        var content = this.nextElementSibling;
        if (content.style.maxHeight){
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
}
