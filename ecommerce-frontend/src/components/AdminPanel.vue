<template>
    <div class="container py-6 px-4 mx-auto max-w-4xl">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-serif text-gray-800 mb-2">Admin Product Management</h2>
        <div class="w-24 h-1 bg-indigo-500 mx-auto rounded"></div>
      </div>
  
      <!-- Add Product Form -->
      <div class="bg-white shadow-lg rounded-lg p-6 mb-8">
        <h3 class="text-xl font-serif text-gray-700 mb-4">Add New Product</h3>
        <form @submit.prevent="addProduct">
          <div class="grid md:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Product Name</label>
              <input 
                v-model="newProduct.name" 
                placeholder="Enter product name" 
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-300 focus:outline-none transition"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Price (₱)</label>
              <input 
                v-model.number="newProduct.price" 
                placeholder="0.00" 
                type="number" 
                step="0.01"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-300 focus:outline-none transition"
              />
            </div>
          </div>
  
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea 
              v-model="newProduct.description" 
              placeholder="Product description" 
              rows="2"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-300 focus:outline-none transition"
            ></textarea>
          </div>
  
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-1">Stock Quantity</label>
            <input 
              v-model.number="newProduct.stock" 
              placeholder="0" 
              type="number"
              class="w-full md:w-1/3 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-300 focus:outline-none transition"
            />
          </div>
  
          <button 
            type="submit" 
            class="px-5 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition"
          >
            Add Product
          </button>
        </form>
      </div>
  
      <!-- Product List -->
      <div class="bg-white shadow-lg rounded-lg p-6">
        <h3 class="text-xl font-serif text-gray-700 mb-6">Product Inventory</h3>
        
        <div v-if="products.length === 0" class="text-center py-8 text-gray-500 italic">
          No products available yet.
        </div>
        
        <div class="grid gap-6 md:grid-cols-2">
          <div 
            v-for="product in products" 
            :key="product.id" 
            class="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition"
          >
            <div class="p-5">
              <div class="flex justify-between items-start">
                <h4 class="text-lg font-medium text-gray-800">{{ product.name }}</h4>
                <span class="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full font-medium">₱{{ product.price.toFixed(2) }}</span>
              </div>
              
              <p class="text-gray-600 mt-2 text-sm">{{ product.description }}</p>
              
              <div class="flex items-center mt-4 text-sm text-gray-500">
                <span class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0v10a2 2 0 01-2 2H4a2 2 0 01-2-2V7a2 2 0 012-2h12a2 2 0 012 2z" />
                  </svg>
                  Stock: {{ product.stock }}
                </span>
              </div>
              
              <div class="flex mt-4 pt-3 border-t border-gray-100">
                <button 
                  @click="editProduct(product)" 
                  class="flex items-center text-sm text-blue-600 hover:text-blue-800 mr-4"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  Edit
                </button>
                <button 
                  @click="deleteProduct(product.id)" 
                  class="flex items-center text-sm text-red-600 hover:text-red-800"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Delete
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
        newProduct: {
          name: '',
          description: '',
          price: 0,
          stock: 0
        }
      }
    },
    methods: {
      async fetchProducts() {
        try {
          const res = await axios.get('products/')
          this.products = res.data
        } catch (error) {
          console.error('Error fetching products:', error)
        }
      },
      async addProduct() {
        try {
          await axios.post('products/', this.newProduct)
          this.newProduct = { name: '', description: '', price: 0, stock: 0 }
          this.fetchProducts()
        } catch (error) {
          console.error('Error adding product:', error)
        }
      },
      async deleteProduct(id) {
        if (confirm('Are you sure you want to delete this product?')) {
          try {
            await axios.delete(`products/${id}/`)
            this.fetchProducts()
          } catch (error) {
            console.error('Error deleting product:', error)
          }
        }
      },
      async editProduct(product) {
        const name = prompt('New name:', product.name)
        if (name) {
          try {
            await axios.put(`products/${product.id}/`, {
              ...product,
              name
            })
            this.fetchProducts()
          } catch (error) {
            console.error('Error updating product:', error)
          }
        }
      }
    },
    mounted() {
      this.fetchProducts()
    }
  }
  </script>