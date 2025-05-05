<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <h3 class="mb-4 fw-light text-center display-6">
          <i class="bi bi-bag-check"></i> My Order History
        </h3>
        
        <!-- Date Filter -->
        <div class="card shadow-sm border-0 mb-4">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-md-5">
                <div class="form-group">
                  <label for="startDate" class="form-label text-brown">From Date</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    id="startDate" 
                    v-model="filters.startDate" 
                    @change="applyFilters"
                  >
                </div>
              </div>
              <div class="col-md-5">
                <div class="form-group">
                  <label for="endDate" class="form-label text-brown">To Date</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    id="endDate" 
                    v-model="filters.endDate" 
                    @change="applyFilters"
                  >
                </div>
              </div>
              <div class="col-md-2 d-flex align-items-end">
                <button 
                  class="btn btn-light w-100" 
                  @click="resetFilters"
                >
                  Reset
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- No Orders Message -->
        <div class="card shadow-sm border-0 mb-4" v-if="filteredOrders.length === 0">
          <div class="card-body text-center p-5 text-muted">
            <i class="bi bi-bag-x fs-1"></i>
            <p class="mt-3">No orders found.</p>
            <button class="btn btn-light mt-2" @click="$router.push('/shop')">
              Start Shopping
            </button>
          </div>
        </div>
        
        <!-- Order Cards -->
        <div v-for="order in filteredOrders" :key="order.id" class="card mb-3 shadow-sm border-0">
          <div class="card-header bg-transparent border-bottom-0 pt-3">
            <div class="d-flex justify-content-between align-items-center">
              <h6 class="fw-normal text-brown mb-0">
                Order #{{ order.id }}
              </h6>
              <div>
                <span class="badge bg-soft-brown text-brown">
                  {{ formatDate(order.date_ordered) }}
                </span>
              </div>
            </div>
          </div>
          <div class="card-body pt-0">
            
            <div class="items-list mb-3">
              <div v-for="item in order.items" :key="item.id" class="d-flex justify-content-between align-items-center py-2 border-bottom border-light">
                <div>
                  <span class="fw-medium">{{ item.product_name || 'Unknown Product' }}</span>
                  <span class="text-muted ms-2">× {{ item.quantity || 0 }}</span>
                </div>
                <span class="text-brown">₱{{ parseFloat(item.price || 0).toFixed(2) }}</span>
              </div>
            </div>
            
            <div class="d-flex justify-content-between align-items-center">
              <span class="fw-bold">Total: <span class="text-brown">₱{{ calculateTotal(order.items).toFixed(2) }}</span></span>
              <button class="btn btn-outline-brown px-4" @click="openOrderDetailModal(order)">
                <i class="bi bi-info-circle me-1"></i> View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Order Detail Modal -->
    <div class="modal fade" id="orderDetailModal" tabindex="-1" aria-labelledby="orderDetailModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0">
          <div class="modal-header border-0">
            <h5 class="modal-title fw-light text-brown" id="orderDetailModalLabel">
              Order #{{ selectedOrder?.id }} Details
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedOrder">
            <div class="order-detail-container p-4">
              <div class="text-center mb-4">
                <h4 class="fw-light text-uppercase mb-2">ORDER DETAILS</h4>
                <p class="mb-1 small">Order #{{ selectedOrder.id }}</p>
                <p class="small text-muted">{{ formatDate(selectedOrder.date_ordered) }}</p>
                <div class="separator my-3 mx-auto"></div>
              </div>
              
              <div class="order-info mb-4">
                <div class="row">
                  <div class="col-md-6">
                    <p class="fw-medium mb-1">Order Date</p>
                    <p class="mb-3">{{ formatDate(selectedOrder.date_ordered) }}</p>
                  </div>
                </div>
              </div>
              
              <div class="separator my-3 mx-auto"></div>
              
              <h5 class="fw-light mb-3">Items</h5>
              <table class="table receipt-table">
                <thead class="table-light">
                  <tr class="text-brown">
                    <th class="fw-medium">Item</th>
                    <th class="fw-medium">Qty</th>
                    <th class="text-end fw-medium">Price</th>
                    <th class="text-end fw-medium">Total</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in selectedOrder.items" :key="item.id">
                    <td>{{ item.product_name || 'Unknown Product' }}</td>
                    <td>{{ item.quantity || 0 }}</td>
                    <td class="text-end">₱{{ parseFloat(item.price || 0).toFixed(2) }}</td>
                    <td class="text-end">₱{{ (parseFloat(item.price || 0) * parseFloat(item.quantity || 0)).toFixed(2) }}</td>
                  </tr>
                  <tr>
                    <td colspan="3" class="text-end border-0">Subtotal</td>
                    <td class="text-end border-0">₱{{ calculateTotal(selectedOrder.items).toFixed(2) }}</td>
                  </tr>
                  <tr class="border-top">
                    <td colspan="3" class="text-end"><strong>Total</strong></td>
                    <td class="text-end">
                      <strong class="text-brown">
                        ₱{{ (calculateTotal(selectedOrder.items) + (selectedOrder.shipping_cost || 0) + (selectedOrder.tax || 0)).toFixed(2) }}
                      </strong>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="modal-footer border-0">
            <button type="button" class="btn btn-light" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios'
import { Modal } from 'bootstrap'

export default {
  data() {
    return {
      orders: [],
      filteredOrders: [],
      selectedOrder: null,
      orderDetailModal: null,
      filters: {
        startDate: null,
        endDate: null
      }
    }
  },
  methods: {
    async fetchMyOrders() {
      try {
        const res = await axios.get('orders/')
        console.log('API Response:', res.data)
        
        // Process the data to ensure we have product names and prices
        this.orders = res.data.map(order => {
          // Process items to include product names if not already provided
          const items = order.items.map(item => {
            let productName = 'Unknown Product'
            let productPrice = 0
            
            // Handle different product data structures
            if (typeof item.product === 'object' && item.product !== null) {
              productName = item.product.name || `Product #${item.product.id}`
              productPrice = parseFloat(item.product.price) || 0
            } else if (typeof item.product === 'string') {
              productName = item.product
              productPrice = parseFloat(item.price || 0)
            } else if (typeof item.product === 'number') {
              productName = `Product #${item.product}`
              productPrice = parseFloat(item.price || 0)
            }
            
            // Ensure price is always a number
            const finalPrice = typeof item.price !== 'undefined' ? 
              parseFloat(item.price) : productPrice
            
            return {
              ...item,
              product_name: item.product_name || productName,
              price: isNaN(finalPrice) ? 0 : finalPrice
            }
          })
          
          // Add default values for optional fields
          return {
            ...order,
            status: order.status || 'processing',
            shipping_address: order.shipping_address || null,
            payment_method: order.payment_method || null,
            shipping_cost: order.shipping_cost || 0,
            tax: order.tax || 0,
            items: items
          }
        })
        
        this.filteredOrders = [...this.orders]
        console.log('Processed Orders:', this.orders)
      } catch (error) {
        console.error('Error fetching orders:', error)
        alert('❌ Failed to load your orders.')
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    },
    
    formatStatus(status) {
      if (!status) return 'Processing'
      
      // Capitalize first letter
      return status.charAt(0).toUpperCase() + status.slice(1)
    },
    
    getStatusBadgeClass(status) {
      switch (status?.toLowerCase()) {
        case 'completed':
          return 'bg-success'
        case 'processing':
          return 'bg-primary'
        case 'shipped':
          return 'bg-info'
        case 'cancelled':
          return 'bg-danger'
        case 'pending':
          return 'bg-warning'
        default:
          return 'bg-secondary'
      }
    },
    
    openOrderDetailModal(order) {
      this.selectedOrder = order
      this.orderDetailModal.show()
    },
    
    calculateTotal(items) {
      return items.reduce((sum, item) => {
        const price = parseFloat(item.price || 0)
        const quantity = parseFloat(item.quantity || 0)
        return sum + (price * quantity)
      }, 0)
    },
    
    applyFilters() {
      if (!this.filters.startDate && !this.filters.endDate) {
        this.filteredOrders = [...this.orders]
        return
      }
      
      const startDate = this.filters.startDate ? new Date(this.filters.startDate) : null
      const endDate = this.filters.endDate ? new Date(this.filters.endDate) : null
      
      // If endDate is provided, set it to end of day (23:59:59)
      if (endDate) {
        endDate.setHours(23, 59, 59, 999)
      }
      
      this.filteredOrders = this.orders.filter(order => {
        const orderDate = new Date(order.date_ordered)
        
        // Check if the order date is within the filter range
        if (startDate && orderDate < startDate) {
          return false
        }
        
        if (endDate && orderDate > endDate) {
          return false
        }
        
        return true
      })
    },
    
    resetFilters() {
      this.filters.startDate = null
      this.filters.endDate = null
      this.filteredOrders = [...this.orders]
    },
    
    printOrderDetails() {
      const printContents = document.querySelector('.order-detail-container').innerHTML
      const originalContents = document.body.innerHTML
      
      document.body.innerHTML = `
        <div style="padding: 20px;">
          ${printContents}
        </div>
      `
      
      window.print()
      document.body.innerHTML = originalContents
      
      // Re-initialize the modal and other components
      this.$nextTick(() => {
        this.initializeModal()
      })
    },
    
    initializeModal() {
      const orderDetailModalElement = document.getElementById('orderDetailModal')
      if (orderDetailModalElement) {
        this.orderDetailModal = new Modal(orderDetailModalElement)
      }
    }
  },
  mounted() {
    const token = localStorage.getItem('access')
    if (!token) {
      alert('⛔ You need to be logged in to view your orders.')
      this.$router.push('/login')
      return
    }
    
    this.fetchMyOrders()
    this.$nextTick(() => {
      this.initializeModal()
    })
  }
}
</script>

<style scoped>
/* Brown and neutral color palette */
:root {
  --primary-brown: #8B6E4E;
  --light-brown: #A68C69;
  --dark-brown: #6F563D;
  --soft-brown: #F2EAE1;
  --light-beige: #F9F6F2;
  --dark-beige: #E6DFD5;
}

.text-brown {
  color: var(--primary-brown);
}

.bg-brown {
  background-color: var(--primary-brown);
}

.bg-soft-brown {
  background-color: var(--soft-brown);
}

.btn-brown {
  background-color: var(--primary-brown);
  color: white;
  border: none;
  transition: all 0.3s ease;
}

.btn-brown:hover {
  background-color: var(--dark-brown);
  color: white;
}

.btn-outline-brown {
  color: var(--primary-brown);
  border-color: var(--primary-brown);
  background-color: transparent;
  transition: all 0.3s ease;
}

.btn-outline-brown:hover {
  background-color: var(--primary-brown);
  color: white;
}

/* Typography Enhancements */
h3, h4, h5, h6 {
  font-family: 'Playfair Display', Georgia, serif;
}

body {
  font-family: 'Lato', 'Helvetica Neue', Arial, sans-serif;
}

.order-detail-container {
  font-family: 'Lato', 'Helvetica Neue', Arial, sans-serif;
  border: 1px solid var(--dark-beige);
  border-radius: 8px;
  background-color: var(--light-beige);
}

.receipt-table th, .receipt-table td {
  padding: 0.75rem;
}

.separator {
  height: 1px;
  width: 70%;
  background-color: var(--dark-beige);
}

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  background-color: var(--light-beige);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(139, 110, 78, 0.1) !important;
}

/* Print Styles */
@media print {
  body * {
    visibility: hidden;
  }
  .order-detail-container, .order-detail-container * {
    visibility: visible;
  }
  .order-detail-container {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    background-color: white !important;
  }
}
</style>