let tickets = document.getElementById('tickets')
let numero = document.getElementById('numero')
let cedula = document.getElementById('cedula')
let final = document.getElementById('final')
let elegido = 23

async function cambiar() {
    let aviso = document.getElementById('aviso')
    let tiempo = await fetch('/rifas/tiempo/' + final.value)
    if (tiempo.status == 404) {
        location.href = '/'
        return
    }
    console.log(tiempo);
    tiempo = await tiempo.json()
    console.log(tiempo);
    aviso.innerText = 'Esta rifa termina en ' + tiempo + ' ¡Que no se te acabe el tiempo!'
    if (!cedula) return
    let disponibles = document.getElementsByClassName('disponible')
    let codigo = document.getElementById('codigo')
    for (const esto of disponibles) {
        esto.addEventListener('click', async () => {
            let uno = document.getElementsByClassName('elegido')
            for (const este of uno) {
                este.classList.remove('elegido')
            }
            esto.classList.add('elegido')
            numero.value = esto.id
        })
        esto.addEventListener('dblclick', async () => {
            let uno = document.getElementsByClassName('elegido')
            for (const este of uno) {
                este.classList.remove('elegido')
            }
            numero.value = ''
        })
    }

}

cambiar()