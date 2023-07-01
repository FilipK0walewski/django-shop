const bigImage = document.getElementById('big-image')
const nextImage = document.getElementById('next-image')
const previousImage = document.getElementById('previous-image')

let imageIndex = 0
const imageList = document.getElementById('image-list')

for (let imageContainer of imageList.children) {
    imageContainer.addEventListener('click', () => {
        bigImage.src = imageContainer.children[0].src
    })
}

nextImage.addEventListener('click', () => {
    imageIndex = Math.min(...[imageList.children.length - 1, imageIndex + 1])
    bigImage.src = imageList.children[imageIndex].children[0].src
})

previousImage.addEventListener('click', () => {
    imageIndex = Math.max(...[0, imageIndex - 1])
    bigImage.src = imageList.children[imageIndex].children[0].src
})

// const addToCart = document.getElementById('add-to-cart')

// addToCart.addEventListener('click', () => {
//     const segments = window.location.href.split('/')
//     const productId = segments[segments.length - 2]

//     const csrftoken = document.cookie.split('csrftoken=')[1].split(';')[0]
//     console.log(csrftoken)
//     fetch('/cart/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken
//         },
//         body: JSON.stringify({ quantity: 1, id: productId })
//     })
// })