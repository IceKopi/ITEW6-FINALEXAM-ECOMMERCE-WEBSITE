<template>
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="elegant-card card shadow-sm border-0">
            <div class="card-header py-2">
              <h3 class="elegant-heading text-brown mb-0">
                Add New Product
              </h3>
            </div>
            <div class="card-body p-3">
              <form @submit.prevent="submitProduct" enctype="multipart/form-data">
                <div class="mb-2">
                  <label class="elegant-label form-label fw-medium">
                    <i class="bi bi-tag-fill me-2"></i>Product Name
                  </label>
                  <input 
                    v-model="product.name" 
                    class="elegant-input form-control form-control-sm" 
                    placeholder="Enter product name" 
                    required 
                  />
                </div>
  
                <div class="mb-2">
                  <label class="elegant-label form-label fw-medium">
                    <i class="bi bi-card-text me-2"></i>Description
                  </label>
                  <textarea 
                    v-model="product.description" 
                    class="elegant-input form-control elegant-text" 
                    placeholder="Enter product description" 
                    rows="3" 
                    required
                  ></textarea>
                </div>
  
                <div class="row mb-2">
                  <div class="col-md-6">
                    <label class="elegant-label form-label fw-medium">
                      <i class="bi bi-currency-dollar me-2"></i>Price
                    </label>
                    <div class="input-group">
                      <span class="input-group-text text-white" style="background-color: #5D4037; border-color: #5D4037;">$</span>
                      <input 
                        type="number" 
                        v-model.number="product.price" 
                        class="elegant-input form-control elegant-text" 
                        placeholder="0.00" 
                        min="0" 
                        step="0.01" 
                        required 
                      />
                    </div>
                  </div>
  
                  <div class="col-md-6">
                    <label class="elegant-label form-label fw-medium">
                      <i class="bi bi-box-seam me-2"></i>Stock
                    </label>
                    <input 
                      type="number" 
                      v-model.number="product.stock" 
                      class="elegant-input form-control elegant-text" 
                      placeholder="Quantity available" 
                      min="0" 
                      required 
                    />
                  </div>
                </div>
  
                <div class="mb-3">
                  <label class="elegant-label form-label fw-medium">
                    <i class="bi bi-image me-2"></i>Product Image
                  </label>
                  <div class="image-upload-container p-2 text-center">
                    <template v-if="imagePreview">
                      <div class="position-relative mb-2">
                        <img :src="imagePreview" class="img-preview img-fluid rounded" alt="Product preview" />
                        <button type="button" @click="removeImage" class="btn btn-sm btn-danger position-absolute top-0 end-0 rounded-circle">
                          <i class="bi bi-x"></i>
                        </button>
                      </div>
                    </template>
                    <template v-else>
                      <i class="bi bi-cloud-arrow-up display-6 mb-2"></i>
                      <p class="elegant-text text-muted small">Drag and drop your image here or click to browse</p>
                    </template>
                    <input 
                      type="file" 
                      id="fileInput" 
                      @change="handleImage" 
                      class="elegant-input form-control mt-1" 
                      accept="image/*" 
                    />
                  </div>
                </div>
  
                <button type="submit" class="btn-elegant btn btn-sm w-100 text-brown fw-medium">
                  <i class="bi bi-plus-circle me-2"></i>Add Product
                </button>
              </form>
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
        product: { name: '', description: '', price: 0, stock: 0 },
        image: null,
        imagePreview: null
      }
    },
    methods: {
      handleImage(e) {
        this.image = e.target.files[0]
        if (this.image) {
          const reader = new FileReader()
          reader.onload = (e) => {
            this.imagePreview = e.target.result
          }
          reader.readAsDataURL(this.image)
        }
      },
      removeImage() {
        this.image = null
        this.imagePreview = null
        document.getElementById('fileInput').value = ''
      },
      async submitProduct() {
        const formData = new FormData()
        for (let key in this.product) {
          formData.append(key, this.product[key])
        }
        if (this.image) formData.append('image', this.image)
  
        try {
          await axios.post('products/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          alert('✅ Product added successfully.')
          this.$router.push('/monitor-products')
        } catch (err) {
          alert('❌ Failed to add product.')
        }
      }
    }
  }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600&display=swap');
  @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css");
  
  :root {
    --color-primary: #453a2d;
    --color-secondary: #5a4d3e;
    --color-accent: #c8a97e;
    --color-accent-light: #dbc6a6;
    --color-accent-danger: #c45440;
    --color-light: #f9f7f4;
    --color-white: #ffffff;
    --color-text: #453a2d;
    --color-text-light: #7d7164;
    --border-radius: 8px;
    --box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    --transition: all 0.3s ease;
  }
  
  .elegant-heading {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 700;
    color: var(--color-primary);
    font-size: 2rem;
    letter-spacing: -0.3px;
    color: #453a2d;
  }
  
  .elegant-label {
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    color: var(--color-primary);
    font-size: 0.85rem;
    margin-bottom: 0.3rem;
    color: #453a2d;
  }
  
  .elegant-text {
    font-family: 'Montserrat', sans-serif;
    color: var(--color-text-light);
    font-weight: 400;
    line-height: 1.5;
    font-size: 0.875rem;
  }
  
  .btn-elegant {
    background-color: var(--color-accent);
    border: 1px solid rgb(30, 11, 11);
    color: var(--color-primary);
    padding: 0.4rem 1.2rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    border-radius: var(--border-radius);
    font-size: 0.95rem;
    transition: var(--transition);
  }
  
  .btn-elegant:hover {
    background-color: #b59669;
    color: var(--color-primary);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(200, 169, 126, 0.3);
  }
  
  .elegant-card {
    border-radius: var(--border-radius);
    overflow: hidden;
    background-color: var(--color-white);
  }
  
  .elegant-input {
    border: 1px solid #e0e0e0;
    border-radius: var(--border-radius);
    padding: 0.5rem 0.75rem;
    font-family: 'Montserrat', sans-serif;
    font-size: 0.9rem;
    transition: var(--transition);
  }
  
  .elegant-input:focus {
    border-color: var(--color-accent-light);
    box-shadow: 0 0 0 3px rgba(200, 169, 126, 0.1);
  }
  
  .image-upload-container {
    border: 1px dashed var(--color-accent-light);
    border-radius: var(--border-radius);
    background-color: var(--color-light);
    cursor: pointer;
  }
  
  .img-preview {
    max-height: 200px;
    object-fit: contain;
    border-radius: var(--border-radius);
    border: 1px solid #e0e0e0;
  }
  </style>
  