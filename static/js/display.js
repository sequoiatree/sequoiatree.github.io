function setDisplay(element, state) {
    element.style.display = state;
}

function setDisplayAll(className, state) {
    var elements = document.getElementsByClassName(className);
    var i;
    for (i = 0; i < elements.length; i += 1) {
        setDisplay(elements[i], state);
    }
}

function toggleDisplay(id, state0, state1) {
    var element = document.getElementById(id);
    if (element.style.display === state0) {
    	setDisplay(element, state1);
    } else {
    	setDisplay(element, state0);
    }
}
