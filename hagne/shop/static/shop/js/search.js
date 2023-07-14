document.getElementById('order').addEventListener('change', () => {
    document.getElementById('order-form').submit()
})

for (let i of document.getElementsByClassName('page-input')) {
    i.addEventListener('blur', () => {
        i.parentElement.submit()
    })
}