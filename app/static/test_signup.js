const form = document.querySelector('.form form');

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formdata = {
        name: form[0].value,
        nickname: form[1].value,
        id: form[2].value,
        password: form[3].value,
        email: form[4].value
    }
    fetch('',{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formdata)
    })
})