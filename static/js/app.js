// Script js para o app

var isOpen = false

function change_overlay() {
    let overlay = document.querySelector("#overlay")

    overlay.classList.toggle("ative")
    isOpen = !isOpen

    if (isOpen) {
        overlay.innerHTML = ""
    }

    console.log(isOpen)
}


function tocarMusicaDuasVezes(src) {
    const audio = new Audio(src);

    function tocar() {
        audio.play().catch((error) => {
            console.log("Autoplay bloqueado pelo navegador");
            document.addEventListener("click", function(){
                audio.play()
            }, {once: true})
        });
    }

    document.addEventListener("load", ()=>{tocar()})


    
}