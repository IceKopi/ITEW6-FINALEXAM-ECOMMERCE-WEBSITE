<template>
    <div class="container py-5 main-container">
      <!-- Header Section -->
      <div class="row mb-5">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <h2 class="font-weight-bold text-brown mb-0">Maisanova Collection</h2>
            <div class="search-container position-relative">
              <input
                v-model="searchQuery"
                type="text"
                class="form-control search-input pl-4 pr-5 rounded-pill border-0 shadow-sm"
                placeholder="Search our collection..."
              />
              <span class="position-absolute search-icon">
                <i class="fas fa-search text-brown-light"></i>
              </span>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Product Grid -->
      <div v-if="filteredProducts.length === 0" class="text-center py-5">
        <p class="text-brown-light">No products match your search criteria.</p>
      </div>
      
      <div class="row">
        <div v-for="product in filteredProducts" :key="product.id" class="col-md-4 mb-4">
          <div class="card product-card h-100 border-0 shadow-sm">
            <div class="product-image-container">
              <img
                v-if="product.image"
                :src="fullImageUrl(product.image)"
                class="card-img-top product-image-list"
                alt="Product"
              />
              <div v-else class="no-image-placeholder">
                <i class="fas fa-image text-brown-light"></i>
              </div>
              <div v-if="product.stock === 0" class="out-of-stock-badge">
                Out of Stock
              </div>
            </div>
            
            <div class="card-body d-flex flex-column bg-beige">
              <h5 class="card-title font-weight-bold text-brown-dark">{{ product.name }}</h5>
              <p class="card-text text-brown-medium product-description">{{ product.description }}</p>
              <div class="mt-auto">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <span class="product-price text-brown-dark">₱{{ product.price.toLocaleString() }}</span>
                  <span class="stock-indicator" :class="{'text-accent': product.stock < 5 && product.stock > 0}">
                    {{ product.stock > 0 ? `${product.stock} in stock` : '' }}
                  </span>
                </div>
                <button
                  class="btn btn-add-to-cart-list w-100"
                  @click="addToCart(product)"
                  :disabled="product.stock === 0 || hasReachedLimit(product)"
                  :class="{'btn-brown-light': product.stock === 0 || hasReachedLimit(product)}"
                >
                  <i class="fas fa-shopping-cart mr-2"></i>
                  {{ buttonText(product) }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios'
  
  export default {
    data() {
      return {
        products: [],
        cart: [], // ✅ Initialized as array
        searchQuery: ''
      }
    },
    computed: {
      filteredProducts() {
        if (!this.searchQuery) return this.products
        const q = this.searchQuery.toLowerCase()
        return this.products.filter(p =>
          p.name.toLowerCase().includes(q) ||
          p.description.toLowerCase().includes(q)
        )
      }
    },
    methods: {
      buttonText(product) {
        if (product.stock === 0) return 'Out of Stock'
        if (this.hasReachedLimit(product)) return 'Max Quantity Reached'
        return 'Add to Cart'
      },
      fullImageUrl(path) {
        if (!path) return ''
        return path.startsWith('http') ? path : `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
      },
      loadCart() {
        try {
          const stored = localStorage.getItem('cart')
          this.cart = stored ? JSON.parse(stored) : []
        } catch (err) {
          console.error('Error loading cart:', err)
          this.cart = []
        }
      },
      saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart))
  
        // Display cart items in console for debugging
        console.log("Current cart items:", this.cart)
      },
      addToCart(product) {
        if (!Array.isArray(this.cart)) {
          this.cart = []
        }
  
        // Format item for backend compatibility
        const cartItem = {
          id: product.id,        // For local storage reference
          product: product.id,   // For backend API
          product_name: product.name, // For display in cart
          price: product.price,  // For price calculations
          quantity: 1,           // Initial quantity
          name: product.name,    // For compatibility with previous code
          description: product.description // Additional info that might be useful
        }
  
        const existing = this.cart.find(item => item.product === product.id)
  
        if (existing) {
          if (existing.quantity < product.stock) {
            existing.quantity += 1
          } else {
            alert(`You've reached the maximum available quantity for this item.`)
            return
          }
        } else {
          if (product.stock === 0) {
            alert('This item is currently out of stock.')
            return
          }
          this.cart.push(cartItem)
        }
  
        this.saveCart()
        
        // // Show success toast with link to cart
        // const toastHtml = `
        //   <div>
        //     <strong>${product.name}</strong> added to your cart.
        //     <br>
        //     <a href="/cart" class="mt-2 d-inline-block">View Cart</a>
        //   </div>
        // `
        // If you have a toast library, use it here
        // Otherwise fall back to alert
        alert(`${product.name} added to your cart.`)
      },
      hasReachedLimit(product) {
        if (!Array.isArray(this.cart)) return false
        const found = this.cart.find(item => item.product === product.id)
        return found ? found.quantity >= product.stock : false
      },
      async fetchProducts() {
        try {
          const res = await axios.get('products/')
          this.products = res.data
        } catch (err) {
          alert('Failed to fetch products. Please try again later.')
          console.error(err)
        }
      }
    },
    mounted() {
      this.loadCart()
      this.fetchProducts()
    }
  }
  </script>
  
  <style scoped>
  /* Brown Neutral Color Palette */
  :root {
    --brown-dark: #5D4037;
    --brown-medium: #7D5A50;
    --brown-light: #A98274;
    --beige: #F5F5DC;
    --cream: #FFFBEB;
    --accent: #8D6E63;
    --neutral-dark: #4E342E;
    --neutral-light: #D7CCC8;
  }
  
  .main-container {
    background-color: var(--cream);
  }
  
  .search-container {
    width: 300px;
  }
  
  .search-input {
    background-color: #F9F4E8;
    transition: all 0.3s;
    border: 1px solid var(--neutral-light);
  }
  
  .search-input:focus {
    background-color: white;
    box-shadow: 0 0 10px rgba(93, 64, 55, 0.1);
    border-color: var(--brown-light);
  }
  
  .search-icon {
    top: 10px;
    right: 15px;
  }
  
  .product-card {
    transition: transform 0.3s, box-shadow 0.3s;
    overflow: hidden;
    border-radius: 8px;
  }
  
  .product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(93, 64, 55, 0.15) !important;
  }
  
  .product-image-container {
    height: 220px;
    overflow: hidden;
    position: relative;
    background-color: #F9F4E8;
  }
  
  .product-image-list {
    height: 100%;
    width: 100%;
    object-fit: cover;
  }
  
  .no-image-placeholder {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .no-image-placeholder i {
    font-size: 3rem;
  }
  
  .bg-beige {
    background-color: var(--beige);
  }
  
  .text-brown {
    color: var(--brown-medium);
  }
  
  .text-brown-dark {
    color: var(--brown-dark);
  }
  
  .text-brown-medium {
    color: var(--brown-medium);
  }
  
  .text-brown-light {
    color: var(--brown-light);
  }
  
  .product-description {
    font-size: 0.9rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    min-height: 60px;
  }
  
  .product-price {
    font-size: 1.25rem;
    font-weight: bold;
  }
  
  .stock-indicator {
    font-size: 0.85rem;
    color: var(--brown-medium);
  }
  
  .text-accent {
    color: var(--accent);
    font-weight: 600;
  }
  
  .btn-add-to-cart-list {
    background-color: var(--brown-medium);
    color: rgb(37, 30, 30);
    border: 1px var(--brown-medium);
    transition: all 0.3s;
    border-radius: 6px;
    font-weight: 500;
    letter-spacing: 0.5px;
  }
  
  .btn-add-to-cart-list:hover:not(:disabled) {
    background-color: var(--brown-dark);
  }
  
  .btn-brown-light {
    background-color: var(--neutral-light);
    color: var(--neutral-dark);
  }
  
  .out-of-stock-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: rgba(125, 90, 80, 0.9);
    color: white;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
  }
  </style>