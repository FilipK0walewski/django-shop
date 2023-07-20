let cartData = null
const cartList = document.getElementById('cart-list')

const getCsrfToken = () => {
    return document.cookie.split('csrftoken=')[1].split(';')[0]
}

const getCart = async () => {
    const res = await fetch('/cart/items/', { method: 'GET', headers: { 'X-CSRFToken': getCsrfToken() } })
    const data = await res.json()

    if (data.cart.length === 0) {
        cartList.innerHTML = '<p>koszyk jest pusty.</p>'
        document.getElementById('cart-sum').classList.add('hidden')
        return
    }

    cartData = {}
    cartList.innerHTML = ''

    let totalPrice = 0
    for (let item of data.cart) {
        const itemSum = (parseInt(item.price * item.quantity * 100) / 100).toFixed(2)
        const itemHtml = `
            <li id="${item.id}" class="cart-item">
                <div class="cart-item-image-name space-x">
                    <div class="image-container image-small">
                        <img src="${item.image}" alt="${item.name}" class="product-image">
                    </div>
                    <a href="/product/${item.id}">${item.name}</a>
                </div>
                <div class="cart-item-buttons">
                    <div class="quantity-control">
                        <button ${item.quantity === 1 ? 'disabled' : null} onclick="decrementQuantity(${item.id})" class="decrement">-</button>
                        <div>
                            <span class="quantity">${item.quantity}</span>
                        </div>
                        <button ${item.stock === item.quantity ? 'disabled' : null} onclick="incrementQuantity(${item.id})" class="increment">+</button>
                    </div>
                    <div class="product-price">
                        <span><span class="multi-price">${itemSum}</span> zl</span>
                        <span class="single-price">${item.price.toFixed(2)} zl</span>
                    </div>
                    <button onclick="deleteProduct(${item.id})" class="delete-btn btn-0">&#9851;</button>
                </div>
            </li>
        `
        cartList.insertAdjacentHTML('beforeend', itemHtml)
        cartData[item.id] = item
        totalPrice += item.quantity * item.price
    }
    document.getElementById('total-price').innerHTML = (parseInt(totalPrice * 100) / 100).toFixed(2)
}

const deleteProduct = async (id) => {
    await fetch(`/cart/${id}/delete/`, { method: 'DELETE', headers: { 'X-CSRFToken': getCsrfToken() } })
    await getCart()
}

const decrementQuantity = async (id) => {
    if (cartData[id].quantity === 1) return
    const res = await fetch(`/cart/${id}/decrement/`, { method: 'POST', headers: { 'X-CSRFToken': getCsrfToken() } })
    if (!res.ok) return
    await getCart()
}

const incrementQuantity = async (id) => {
    if (cartData[id].quantity === cartData[id].stock) return
    const res = await fetch(`/cart/${id}/increment/`, { method: 'POST', headers: { 'X-CSRFToken': getCsrfToken() } })
    if (!res.ok) return
    await getCart()
}

const submitCart = async () => {
    await fetch('/cart/submit/', { method: 'POST', headers: { 'X-CSRFToken': getCsrfToken() } })
}

window.onload = () => {
    getCart()
}