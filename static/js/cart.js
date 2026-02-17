// ========================================
// CART JAVASCRIPT
// Shopping Cart Operations
// ========================================

// Update cart item quantity
function updateCartQuantity(productId, quantity) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch(`/cart/update/${productId}/`, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error updating cart:', error);
        });
}

// Remove item from cart
function removeFromCart(productId) {
    if (!confirm('Are you sure you want to remove this item from your cart?')) {
        return;
    }

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch(`/cart/remove/${productId}/`, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        })
        .catch(error => {
            console.error('Error removing from cart:', error);
        });
}

// Add to cart with animation
function addToCart(productId, quantity = 1) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Show success message
            showNotification('Item added to cart!', 'success');

            // Update cart count in navbar
            updateCartBadge();

            // Add animation to cart icon
            animateCartIcon();
        })
        .catch(error => {
            console.error('Error adding to cart:', error);
            showNotification('Error adding item to cart', 'error');
        });
}

// Update cart badge count
function updateCartBadge() {
    fetch('/cart/count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.cart-badge');
            if (badge) {
                badge.textContent = data.count;
                badge.classList.add('pulse');
                setTimeout(() => badge.classList.remove('pulse'), 600);
            }
        })
        .catch(error => console.error('Error updating cart badge:', error));
}

// Animate cart icon
function animateCartIcon() {
    const cartIcon = document.querySelector('.cart-icon');
    if (cartIcon) {
        cartIcon.classList.add('bounce');
        setTimeout(() => cartIcon.classList.remove('bounce'), 500);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">${type === 'success' ? '✓' : '!'}</span>
            <span class="notification-message">${message}</span>
        </div>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Quantity input handlers
const quantityInputs = document.querySelectorAll('.quantity-input');
quantityInputs.forEach(input => {
    const decreaseBtn = input.previousElementSibling;
    const increaseBtn = input.nextElementSibling;

    if (decreaseBtn) {
        decreaseBtn.addEventListener('click', () => {
            const currentValue = parseInt(input.value);
            if (currentValue > 1) {
                input.value = currentValue - 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    }

    if (increaseBtn) {
        increaseBtn.addEventListener('click', () => {
            const currentValue = parseInt(input.value);
            const maxValue = parseInt(input.max) || 99;
            if (currentValue < maxValue) {
                input.value = currentValue + 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    }

    input.addEventListener('change', () => {
        const productId = input.dataset.productId;
        const quantity = parseInt(input.value);
        if (productId && quantity > 0) {
            updateCartQuantity(productId, quantity);
        }
    });
});

// Calculate and display cart total
function calculateCartTotal() {
    const cartItems = document.querySelectorAll('.cart-item');
    let total = 0;

    cartItems.forEach(item => {
        const price = parseFloat(item.dataset.price);
        const quantity = parseInt(item.querySelector('.quantity-input').value);
        total += price * quantity;
    });

    const totalElement = document.getElementById('cartTotal');
    if (totalElement) {
        totalElement.textContent = '₹' + total.toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }
}

// Initialize cart on page load
document.addEventListener('DOMContentLoaded', () => {
    calculateCartTotal();
    updateCartBadge();
});

// Apply promo code
const promoForm = document.getElementById('promoForm');
if (promoForm) {
    promoForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const promoCode = document.getElementById('promoCode').value;

        fetch('/cart/apply-promo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ code: promoCode })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Promo code applied successfully!', 'success');
                    calculateCartTotal();
                } else {
                    showNotification(data.message || 'Invalid promo code', 'error');
                }
            })
            .catch(error => {
                console.error('Error applying promo:', error);
                showNotification('Error applying promo code', 'error');
            });
    });
}

console.log('🛒 Cart operations initialized!');
