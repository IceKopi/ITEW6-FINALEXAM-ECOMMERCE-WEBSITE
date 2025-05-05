<template>
  <nav class="navbar navbar-expand-lg luxury-navbar">
    <div class="container-fluid px-4">
      <router-link
        class="navbar-brand"
        :to="auth.isLoggedIn ? (auth.isStaff ? '/monitor' : '/products') : '/login'"
      >
      <img src="@/assets/logo.png" alt="Maisonova Logo" class="me-2" height="32" onerror="this.onerror=null; this.src='https://via.placeholder.com/32'; this.style.opacity=0.7;">
      <span class="luxury-brand">Maisonova</span>
      </router-link>

      <button 
        class="navbar-toggler border-0" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarContent"
        aria-controls="navbarContent"
        aria-expanded="false" 
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <!-- NON-LOGGED IN NAVIGATION -->
          <li class="nav-item" v-if="!auth.isLoggedIn">
            <router-link class="nav-link luxury-link" to="/shop">
              Shop
            </router-link>
          </li>

          <!-- STAFF NAVIGATION -->
          <li class="nav-item" v-if="auth.isLoggedIn && auth.isStaff">
            <router-link class="nav-link luxury-link" to="/monitor">
              Admin Panel
            </router-link>
          </li>
          <li class="nav-item" v-if="auth.isLoggedIn && auth.isStaff">
            <router-link class="nav-link luxury-link" to="/admin-product-view">
              Products
            </router-link>
          </li>
          <li class="nav-item" v-if="auth.isLoggedIn && auth.isStaff">
            <router-link class="nav-link luxury-link" to="/add-product">
              Add Product
            </router-link>
          </li>
          <li class="nav-item" v-if="auth.isLoggedIn && auth.isStaff">
            <router-link class="nav-link luxury-link" to="/admin-transaction-history">
              Orders
            </router-link>
          </li>


          <!-- CUSTOMER NAVIGATION -->
          <li class="nav-item" v-if="auth.isLoggedIn && !auth.isStaff">
            <router-link class="nav-link luxury-link" to="/products">
              Home
            </router-link>
          </li>
          <li class="nav-item" v-if="auth.isLoggedIn && !auth.isStaff">
            <router-link class="nav-link luxury-link" to="/cart">
              Cart
            </router-link>
          </li>
          <li class="nav-item" v-if="auth.isLoggedIn && !auth.isStaff">
            <router-link class="nav-link luxury-link" to="/orders">
              My Orders
            </router-link>
          </li>
        </ul>

        <ul class="navbar-nav ms-auto">
          <!-- Show Login/Register only if LOGGED OUT -->
          <li class="nav-item" v-if="!auth.isLoggedIn">
            <router-link class="nav-link luxury-link" to="/login">
              Login
            </router-link>
          </li>
          <li class="nav-item" v-if="!auth.isLoggedIn">
            <router-link class="nav-link-register" to="/register">
              Register
            </router-link>
          </li>

          <!-- Show Logout if LOGGED IN -->
          <li class="nav-item" v-if="auth.isLoggedIn">
            <button class="logout-btn" @click="logout">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="nav-shadow"></div>
  <router-view />
</template>

<script>
import { auth } from './auth'

export default {
  setup() {
    return { auth }
  },
  methods: {
    logout() {
      const cart = localStorage.getItem('cart')
      localStorage.clear()
      localStorage.setItem('cart', cart)

      auth.isLoggedIn = false        // Reset reactivity
      auth.isStaff = false

      this.$router.push('/login')
    }
  }
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&display=swap');

.navbar {
  background-color: rgba(249, 246, 240, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: none;
  padding: 1.2rem 0;
  font-family: 'Montserrat', sans-serif;
  position: relative;
  z-index: 1000;
}

.nav-shadow {
  height: 1px;
  width: 100%;
  background: linear-gradient(to right, transparent 5%, rgba(212, 201, 190, 0.5) 50%, transparent 95%);
  position: relative;
  z-index: 999;
  margin-bottom: 4px; /* Creating slight separation */
}

.navbar-brand {
  padding: 0;
  margin-right: 2rem;
  letter-spacing: 1.2px;
}

.luxury-brand {
  font-family: 'Playfair Display', serif;
  font-weight: 500;
  letter-spacing: 2px;
  color: #2c2a29;
  font-size: 1.25rem;
}

.navbar-nav {
  gap: 0.2rem;
}

.nav-link {
  color: #2c2a29;
  font-weight: 400;
  letter-spacing: 1px;
  text-transform: uppercase;
  font-size: 0.8rem;
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #8a7c6d;
}

.router-link-active {
  color: #8a7c6d !important;
  font-weight: 500;
}

.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 1rem;
  right: 1rem;
  height: 1px;
  background-color: #8a7c6d;
  transform: scaleX(0.8);
  transition: transform 0.3s ease;
}

.router-link-active:hover::after {
  transform: scaleX(1);
}

.nav-link-register {
  color: #fff;
  background-color: #8a7c6d;
  font-weight: 500;
  letter-spacing: 1px;
  text-transform: uppercase;
  font-size: 0.8rem;
  padding: 0.5rem 1.25rem;
  transition: all 0.3s ease;
  display: inline-block;
  text-decoration: none;
  margin-left: 0.5rem;
  border-radius: 0;
}

.nav-link-register:hover {
  background-color: #2c2a29;
  transform: translateY(-2px);
}

/* Search Bar Styling */
.search-form {
  margin: 0 1rem;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  border: 1px solid #d4c9be;
  border-radius: 0;
  padding: 8px 40px 8px 15px;
  font-size: 0.85rem;
  font-family: 'Montserrat', sans-serif;
  background-color: rgba(255, 255, 255, 0.5);
  transition: all 0.3s ease;
  width: 220px;
  letter-spacing: 0.5px;
}

.search-input:focus {
  outline: none;
  background-color: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
  width: 260px;
  border-color: #8a7c6d;
}

.search-input::placeholder {
  color: #8a7c6d;
  opacity: 0.7;
  font-style: italic;
  font-size: 0.8rem;
}

.search-button {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8a7c6d;
  transition: color 0.2s ease;
}

.search-button:hover {
  color: #2c2a29;
}

.logout-btn {
  border: 1px solid #d4c9be;
  background: transparent;
  color: #2c2a29;
  letter-spacing: 1px;
  text-transform: uppercase;
  font-size: 0.8rem;
  padding: 0.5rem 1.5rem;
  transition: all 0.3s ease;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #8a7c6d;
  color: #fff;
  border-color: #8a7c6d;
}

.custom-toggler {
  border: 1px solid #d4c9be;
  padding: 0.25rem 0.5rem;
}

.custom-toggler:focus {
  box-shadow: none;
  outline: none;
}

@media (max-width: 991px) {
  .search-form {
    margin: 1rem 0;
    width: 100%;
  }
  
  .search-input {
    width: 100%;
  }
  
  .search-input:focus {
    width: 100%;
  }
  
  .navbar-nav {
    margin: 1rem 0;
  }
  
  .nav-link-register {
    margin: 0.5rem 0 0.5rem 0;
    text-align: center;
    display: block;
  }
  
  .logout-btn {
    margin-top: 0.5rem;
    width: 100%;
  }
}
</style>