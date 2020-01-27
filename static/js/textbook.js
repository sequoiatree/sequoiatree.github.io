// Render

function renderContent() {
    $('body').css('padding-top', $('#navbar').height());
}

window.addEventListener('load', function() {
    renderContent();
});

// Navbar

function toggleClass(id, baseClass, extension) {
    var element = document.getElementById(id);
    if (element.className === baseClass) {
        element.className += ' ' + extension;
    } else {
        element.className = baseClass;
    }
}

// Dropdown

window.addEventListener('resize', function(event) {
    setDisplayAll('dropdown-content', 'none');
    renderContent();
});

window.addEventListener('click', function(event) {
    if (!event.target.matches('.dropbtn')) {
        setDisplayAll('dropdown-content', 'none');
    }
    renderContent();
});
