let codigo = document.getElementById('codigo')
let rifar = document.getElementById('rifar')

async function revisar() {
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
        if (json === true) rifar.setAttribute('disabled', '')
        else rifar.removeAttribute('disabled')
    } catch (error) {
        console.error(error.message);
    }
}