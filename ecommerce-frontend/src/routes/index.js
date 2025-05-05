import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomePage.vue' 
import UserLogin from '../views/UserLogin.vue'
import UserRegister from '../views/UserRegister.vue'
import ProductList from '../components/ProductList.vue'
import Cart from '../components/ShoppingCart.vue'
import OrderHistory from '../views/OrderHistory.vue'
import CheckoutMonitor from '../components/AdminProductManagement.vue'
import MonitorProducts from '../components/AdminProductInventory.vue'
import AddProduct from '../components/AddProduct.vue'
import AdminProductView from '../components/AdminProductView.vue'
import AdminTransactionHistory from '../components/AdminTransactionHistory.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: UserLogin },
  { path: '/register', component: UserRegister },
  { path: '/products', component: ProductList },
  { path: '/cart', component: Cart },
  { path: '/orders', component: OrderHistory },
  { path: '/monitor', component: CheckoutMonitor },
  { path: '/monitor-products', component: MonitorProducts },
  { path: '/add-product', component: AddProduct },
  { path: '/admin-product-view', component: AdminProductView },
  { path: '/admin-transaction-history', component: AdminTransactionHistory },

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🔐 GLOBAL GUARD FOR ALL NAVIGATION
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access')
  const isStaff = localStorage.getItem('is_staff') === 'true'

  const guestOnly = ['/login', '/register']
  const staffOnly = ['/monitor']
  const customerOnly = ['/products', '/cart', '/orders']

  // Not logged in → block access to all protected routes
  if (!isLoggedIn && !guestOnly.includes(to.path) && to.path !== '/') {
    return next('/login')
  }

  // Logged in → block guest pages
  if (isLoggedIn && guestOnly.includes(to.path)) {
    return next(isStaff ? '/monitor' : '/products')
  }

  // Staff cannot access customer pages
  if (isLoggedIn && isStaff && customerOnly.includes(to.path)) {
    return next('/monitor')
  }

  // Customer cannot access admin pages
  if (isLoggedIn && !isStaff && staffOnly.includes(to.path)) {
    return next('/products')
  }

  next()
})

export default router
