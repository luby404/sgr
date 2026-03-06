var buttons = document.querySelectorAll("#content_menu_btns .iten_menu")


buttons.forEach(element => {
    const path = window.location.pathname
    let el_path = element.getAttribute("href")
    if (path == el_path) {
        element.classList.add("ative")
    }

});


