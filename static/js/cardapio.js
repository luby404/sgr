var isOpen = false

function change_overlay(){
    document.querySelector("#overlay").classList.toggle("ative")
    isOpen = !isOpen

    if (isOpen){
        document.querySelector("#overlay").innerHTML = ""
    }
}


function alert_not_produto() {
    alert("O produto selecionado não está disponivel no momento.")
}
