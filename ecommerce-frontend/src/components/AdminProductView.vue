
<template>
    <div class="container mt-4">
        <h3>Product Inventory</h3>

        <div v-if="paginated.length === 0" class="no-products">No products found.</div>
        <div v-else class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Price</th>
                        <th>Stock</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="product in paginated" :key="product.id" class="product-row">
                        <td class="image-cell">
                            <img v-if="product.image" :src="fullImageUrl(product.image)" alt="Product image"
                                class="product-image" />
                            <div v-else class="no-image">No image</div>
                        </td>
                        <td class="name-cell">{{ product.name }}</td>
                        <td class="description-cell">{{ product.description }}</td>
                        <td class="price-cell">₱{{ product.price }}</td>
                        <td class="stock-cell">{{ product.stock }}</td>
                        <td class="actions-cell">

                            <button class="btn-elegant-secondary btn-sm me-1" @click="openEditModal(product)">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn-elegant-danger btn-sm" @click="confirmDelete(product)">
                                <i class="bi bi-trash"></i>
                            </button>

                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Pagination -->
        <nav v-if="totalPages > 1">
            <ul class="pagination justify-content-center mt-3">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <a class="page-link" href="#" @click.prevent="currentPage--">Previous</a>
                </li>
                <li v-for="n in totalPages" :key="n" class="page-item" :class="{ active: currentPage === n }">
                    <a class="page-link" href="#" @click.prevent="currentPage = n">{{ n }}</a>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                    <a class="page-link" href="#" @click.prevent="currentPage++">Next</a>
                </li>
            </ul>
        </nav>

        <!-- Edit Modal -->
        <div class="modal fade" ref="editModal" id="editModal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <form @submit.prevent="submitEdit">
                        <div class="modal-header">
                            <h5 class="modal-title">Edit Product</h5>
                            <button type="button" class="btn-close" @click="closeEditModal"></button>
                        </div>
                        <div class="modal-body">
                            <input v-model="editProduct.name" class="form-control mb-2" placeholder="Name" required />
                            <input v-model="editProduct.description" class="form-control mb-2" placeholder="Description"
                                required />
                            <input type="number" v-model.number="editProduct.price" class="form-control mb-2"
                                placeholder="Price" required />
                            <input type="number" v-model.number="editProduct.stock" class="form-control mb-2"
                                placeholder="Stock" required />
                            <input type="file" @change="handleEditImage" class="form-control mb-2" accept="image/*" />
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" @click="closeEditModal">Cancel</button>
                            <button type="submit" class="btn btn-success">Save</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div class="modal fade" ref="deleteModal" id="deleteModal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Confirm Delete</h5>
                        <button type="button" class="btn-close" @click="closeDeleteModal"></button>
                    </div>
                    <div class="modal-body">
                        Are you sure you want to delete this product?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Cancel</button>
                        <button type="button" class="btn btn-danger" @click="deleteProduct(productToDelete?.id)">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from '../axios'
import * as bootstrap from 'bootstrap'

export default {
    data() {
        return {
            products: [],
            currentPage: 1,
            perPage: 5,
            editProduct: { id: null, name: '', description: '', price: 0, stock: 0 },
            editImage: null,
            modalInstance: null,
            productToDelete: null,
            deleteModalInstance: null
        }
    },
    computed: {
        totalPages() {
            return Math.ceil(this.products.length / this.perPage)
        },
        paginated() {
            const start = (this.currentPage - 1) * this.perPage
            return this.products.slice(start, start + this.perPage)
        }
    },
    methods: {
        fullImageUrl(path) {
            if (path.startsWith('http')) return path
            return `http://127.0.0.1:8000${path.startsWith('/') ? path : '/media/' + path}`
        },
        async fetchProducts() {
            try {
                const res = await axios.get('products/')
                this.products = res.data
            } catch {
                alert('❌ Failed to load products.')
            }
        },
        confirmDelete(product) {
            this.productToDelete = product
            this.deleteModalInstance = new bootstrap.Modal(this.$refs.deleteModal)
            this.deleteModalInstance.show()
        },
        closeDeleteModal() {
            if (this.deleteModalInstance) this.deleteModalInstance.hide()
            this.productToDelete = null
        },
        async deleteProduct(id) {
            if (!id) return

            try {
                await axios.delete(`products/${id}/`)
                this.showToast('Product deleted successfully', 'success')
                this.fetchProducts()
                this.closeDeleteModal()
            } catch (err) {
                console.error('Delete error:', err)
                alert('❌ Cannot delete. Product may be in an order.')
                this.closeDeleteModal()
            }
        },
        openEditModal(product) {
            this.editProduct = { ...product }
            this.editImage = null
            this.modalInstance = new bootstrap.Modal(this.$refs.editModal)
            this.modalInstance.show()
        },
        closeEditModal() {
            if (this.modalInstance) this.modalInstance.hide()
        },
        handleEditImage(e) {
            this.editImage = e.target.files[0]
        },
        async submitEdit() {
            const formData = new FormData()
            for (let key in this.editProduct) {
                if (key !== 'image') {
                    formData.append(key, this.editProduct[key])
                }
            }
            if (this.editImage) {
                formData.append('image', this.editImage)
            }

            try {
                await axios.patch(`products/${this.editProduct.id}/`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                })
                alert('✅ Product updated!')
                this.fetchProducts()
                this.closeEditModal()
            } catch (err) {
                alert('❌ Failed to update product.')
            }
        },
        showToast(message = 'info') {
            // If you have a toast component, use it here
            // Otherwise fall back to alert
            alert(message)
        }
    },
    mounted() {
        const token = localStorage.getItem('access')
        const isStaff = localStorage.getItem('is_staff') === 'true'
        if (!token || !isStaff) {
            alert('⛔ Access denied. Staff only.')
            this.$router.push('/login')
            return
        }
        this.fetchProducts()
    }
}
</script>

<style>
/* Refined Brown and neutral color palette */
:root {
    --brown-primary: #8D7158;
    --brown-dark: #6A5340;
    --brown-light: #A68D76;
    --brown-lighter: #C5B4A0;
    --brown-lightest: #E5DCD0;
    --neutral-100: #FAF8F5;
    --neutral-200: #F0EBE3;
    --neutral-300: #DFD8CE;
    --neutral-400: #B8AEA1;
    --neutral-500: #847D73;
    --text-dark: #3F3830;
    --text-medium: #6E665D;
    --text-light: #9E968D;
    --color-text-light: #9E968D;
    --color-text: #3F3830;
    --color-accent: #8D7158;
    --color-accent-danger: #a16955;
    --border-radius: 6px;
    --transition: all 0.2s ease;
}

/* Global styles for refined elegance */
body {
    background-color: var(--neutral-100);
    color: var(--text-dark);
    font-family: 'Inter', 'Segoe UI', sans-serif;
    line-height: 1.6;
    letter-spacing: 0.01em;
}

.container {
    background-color: white;
    padding: 32px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

/* Typography enhancements */
h1,
h2,
h3,
h4,
h5 {
    font-family: 'Playfair Display', 'Times New Roman', serif;
    font-weight: 500;
    color: var(--brown-dark);
}

h3 {
    font-size: 1.75rem;
    margin-bottom: 28px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--neutral-200);
    position: relative;
}

h3:after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 80px;
    height: 3px;
    background-color: var(--brown-primary);
    border-radius: 3px;
}

/* Table refinements */
.table {
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 3px 15px rgba(139, 110, 78, 0.05);
    margin-bottom: 2rem;
}

.table thead th {
    background-color: var(--brown-primary);
    background: linear-gradient(to right, var(--brown-primary), var(--brown-dark));
    color: white;
    font-weight: 500;
    padding: 14px 18px;
    border: none;
    text-transform: uppercase;
    font-size: 0.85rem;
    letter-spacing: 0.07em;
}

.table tbody tr {
    transition: all 0.25s ease;
    border-bottom: 1px solid var(--neutral-200);
}

.table tbody tr:last-child {
    border-bottom: none;
}

.table tbody tr:hover {
    background-color: var(--neutral-100);
    transform: translateY(-1px);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
}

.table td {
    padding: 18px;
    vertical-align: middle;
    color: var(--text-medium);
    font-size: 0.95rem;
}

.name-cell {
    font-weight: 600;
    color: var(--brown-dark);
    font-size: 1rem;
}

.description-cell {
    max-width: 280px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--text-medium);
    font-weight: 400;
}

.price-cell,
.stock-cell {
    font-weight: 600;
    text-align: center;
    font-variant-numeric: tabular-nums;
}

.price-cell {
    color: var(--brown-dark);
    font-size: 1.05rem;
}

.stock-cell {
    color: var(--text-medium);
}

.image-cell {
    width: 100px;
}

.product-image {
    max-height: 80px;
    max-width: 100px;
    object-fit: contain;
    border-radius: 6px;
    border: 1px solid var(--neutral-200);
    padding: 4px;
    background-color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
    transition: transform 0.2s ease;
}

.product-image:hover {
    transform: scale(1.05);
}

.no-image {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 80px;
    width: 80px;
    background-color: var(--neutral-200);
    color: var(--text-light);
    font-size: 0.75rem;
    font-style: italic;
    border-radius: 6px;
}

.actions-cell {
    text-align: right;
    white-space: nowrap;
}


.btn-elegant-secondary {
    background-color: transparent;
    border: 1px solid var(--color-text-light);
    color: var(--color-text);
    padding: 0.5rem 1.5rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    border-radius: var(--border-radius);
    transition: var(--transition);
}

.btn-elegant-secondary:hover {
    border-color: var(--color-accent);
    color: var(--color-accent);
    background-color: rgba(200, 169, 126, 0.05);
}

.btn-elegant-danger {
    background-color: transparent;
    border: 1px solid var(--color-accent-danger);
    color: var(--color-accent-danger);
    padding: 0.5rem 1.5rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    border-radius: var(--border-radius);
    transition: var(--transition);
}

.btn-elegant-danger:hover {
    background-color: var(--color-accent-danger);
    color: white;
}

.no-products {
    text-align: center;
    padding: 48px 24px;
    background-color: var(--neutral-100);
    border-radius: 10px;
    color: var(--text-light);
    font-style: italic;
    font-size: 1.1rem;
}

/* Button refinements */
.btn {
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    letter-spacing: 0.02em;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
    transition: all 0.2s ease;
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn:active {
    transform: translateY(1px);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.btn-sm {
    font-size: 0.8rem;
    padding: 0.35rem 0.8rem;
}

.btn-primary {
    background-color: var(--brown-primary);
    border-color: var(--brown-primary);
}

.btn-primary:hover {
    background-color: var(--brown-dark);
    border-color: var(--brown-dark);
}

.btn-danger {
    background-color: #a16955;
    border-color: #a16955;
}

.btn-danger:hover {
    background-color: #8c5a49;
    border-color: #8c5a49;
}

.btn-success {
    background-color: #7e9169;
    border-color: #7e9169;
}

.btn-success:hover {
    background-color: #6a7b58;
    border-color: #6a7b58;
}

.btn-secondary {
    background-color: var(--neutral-400);
    border-color: var(--neutral-400);
    color: white;
}

.btn-secondary:hover {
    background-color: var(--neutral-500);
    border-color: var(--neutral-500);
}

/* Pagination refinements */
.pagination {
    margin-top: 2rem;
}

.pagination .page-link {
    color: var(--brown-primary);
    background-color: white;
    border-color: var(--neutral-200);
    padding: 0.6rem 1rem;
    font-weight: 500;
}

.pagination .page-item.active .page-link {
    background-color: var(--brown-primary);
    border-color: var(--brown-primary);
    box-shadow: 0 2px 5px rgba(139, 110, 78, 0.3);
}

.pagination .page-item.disabled .page-link {
    color: var(--text-light);
}

.pagination .page-item:not(.active) .page-link:hover {
    background-color: var(--neutral-100);
    border-color: var(--neutral-300);
}

/* Modal refinements */
.modal-content {
    border: none;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    overflow: hidden;
}

.modal-header {
    background: linear-gradient(to right, var(--brown-primary), var(--brown-dark));
    color: white;
    border-bottom: none;
    padding: 1.5rem;
}

.modal-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 500;
}

.modal-body {
    padding: 1.8rem;
}

.modal-footer {
    background-color: var(--neutral-100);
    border-top: none;
    padding: 1.2rem 1.8rem;
}

.form-control {
    border-color: var(--neutral-300);
    background-color: white;
    padding: 0.7rem 1rem;
    border-radius: 6px;
    transition: all 0.25s ease;
}

.form-control:focus {
    border-color: var(--brown-light);
    box-shadow: 0 0 0 0.20rem rgba(139, 110, 78, 0.15);
}

/* Subtle animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.product-row {
    animation: fadeIn 0.3s ease-out forwards;
}

/* Additional helper classes */
.text-brown {
    color: var(--brown-primary);
}

.bg-neutral {
    background-color: var(--neutral-100);
}

/* Font imports */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600&display=swap');
</style>