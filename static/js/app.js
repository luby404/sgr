// Script js para o app

var isOpen = false

function change_overlay(){
    let overlay = document.querySelector("#overlay")

    overlay.classList.toggle("ative")
    isOpen = !isOpen

    if (isOpen){
        overlay.innerHTML = ""
    }

    console.log(isOpen)
}




