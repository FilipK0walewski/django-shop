const bigImage = document.getElementById('big-image')
const nextImage = document.getElementById('next-image')
const previousImage = document.getElementById('previous-image')
const decrementQuantity = document.getElementById('decrement-quantity')
const incrementQuantity = document.getElementById('increment-quantity')
const productQuantity = document.getElementById('product-quantity')
const maxProductQuantity = parseInt(productQuantity.getAttribute('max'))

let imageIndex = 0
const imageList = document.getElementById('image-list')

const resetFocus = () => {
    for (let imageContainer of imageList.children) {
        imageContainer.classList.remove('image-focused')
    }
}

for (let i = 0; i < imageList.children.length; i++) {
    const imageContainer = imageList.children[i]
    imageContainer.addEventListener('click', () => {
        imageIndex = i
        resetFocus()
        imageContainer.classList.add('image-focused')
        imageList.scrollLeft = i * imageList.children[i].offsetWidth
        imageContainer.style.left = '100px'
        bigImage.src = imageContainer.children[0].src
    })
}

nextImage.addEventListener('click', () => {
    imageIndex = Math.min(...[imageList.children.length - 1, imageIndex + 1])
    resetFocus()
    imageList.children[imageIndex].classList.add('image-focused')
    imageList.scrollLeft = imageIndex * imageList.children[imageIndex].offsetWidth
    bigImage.src = imageList.children[imageIndex].children[0].src
})

previousImage.addEventListener('click', () => {
    imageIndex = Math.max(...[0, imageIndex - 1])
    resetFocus()
    imageList.children[imageIndex].classList.add('image-focused')
    imageList.scrollLeft = imageIndex * imageList.children[imageIndex].offsetWidth
    bigImage.src = imageList.children[imageIndex].children[0].src
})

decrementQuantity.addEventListener('click', (e) => {
    e.preventDefault()
    productQuantity.value = Math.max(...[1, parseInt(productQuantity.value) - 1])
})

incrementQuantity.addEventListener('click', (e) => {
    e.preventDefault()
    productQuantity.value = Math.min(...[maxProductQuantity, parseInt(productQuantity.value) + 1])
})