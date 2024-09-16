let tickets = document.getElementById('tickets')

function cambiar() {
    let disponibles = document.getElementsByClassName('disponible')
    for (const esto of disponibles) {
        esto.addEventListener('click', async () => {
            const url = "/rifas/revision/" + codigo.value;
            try {
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Access-Control-Allow-Origin': '*'
                    },
                });
                if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
                }
                const json = await response.json();
            } catch (error) {
                console.error(error.message);
            }
        })
    }

}