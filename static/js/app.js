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
    audio.muted = true;
    let contador = 0;

    function tocar() {
        audio.muted = false;
        audio.play().catch(() => {
            console.log("Autoplay bloqueado pelo navegador");
        });
    }

    audio.addEventListener("ended", () => {
        contador++;
        if (contador < 2) {
            audio.currentTime = 0;
            tocar();
        }
    });

    window.addEventListener("load", () => {
        tocar();
    });
}