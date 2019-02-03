var sliderIDs = getSliderIDs();

var MAX_SLIDE_HEIGHT = 400;

initializeSliders();

function getSliderIDs() {
    var sliders = document.getElementsByClassName("slider");
    var sliderIDs = new Array(sliders.length);
    var i;
    for (i = 0; i < sliderIDs.length; i += 1) {
        sliderIDs[i] = getID(sliders[i], "slider");
    }
    return sliderIDs;
}

function initializeSliders() {
    var i;
    for (i = 0; i < sliderIDs.length; i += 1) {
        var id = sliderIDs[i];
        initializeSlides(id); // Keep the diagram window the same height.
        getSlider(id).oninput = function() {
            setSlider(getID(this, "slider"), this.value);
        }
        setSlider(id, 0);
    }
}

function initializeSlides(id) {
    var slides = getSlides(id);
    var heights = new Array(slides.length);
    var i;
    for (i = 0; i < slides.length; i += 1) {
        setSlider(id, i);
        heights[i] = $(slides[i]).height();
    }
    var maxHeight = Math.max.apply(Math, heights);
    if (maxHeight < MAX_SLIDE_HEIGHT) {
        for (i = 0; i < slides.length; i += 1) {
            slides[i].style.height = maxHeight + "px";
        }
    }
}

function setSlider(id, n) {
    var slider = getSlider(id);
    var slides = getSlides(id);
    var captions = getCaptions(id);
    var i;
    for (i = 0; i <= parseInt(slider.max); i += 1) {
        slides[i].style.display = "none";
        captions[i].style.display = "none";
    }
    slides[n].style.display = "block";
    captions[n].style.display = "block";
    slider.value = n;
}

function incrementSlider(id, n) {
    var slider = getSlider(id);
    var length = parseInt(slider.max) + 1
    var n = (parseInt(slider.value) + n) % length;
    if (n < 0) {
        n += length;
    }
    setSlider(id, n);
}

function getSlider(id) {
    return document.getElementById("slider-".concat(id));
}

function getSlides(id) {
    return document.getElementsByClassName("slide-".concat(id));
}

function getCaptions(id) {
    return document.getElementsByClassName("caption-".concat(id));
}

function getID(element, base) {
    return element.id.substr(base.length + 1);
}
