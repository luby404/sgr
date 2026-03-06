var isOpen = false

function change_overlay(){
    document.querySelector("#overlay").classList.toggle("ative")
    isOpen = !isOpen

    if (isOpen){
        document.querySelector("#overlay").innerHTML = ""
    }
}


