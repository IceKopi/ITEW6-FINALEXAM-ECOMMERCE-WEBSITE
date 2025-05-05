<template>
    <div>
        <h1>Admin Product Management</h1>
        <ul>
        <li v-for="product in products" :key="product.id">
            {{ product.name }} - ${{ product.price }}
            <button @click="deleteProduct(product.id)">Delete</button>
        </li>
        </ul>
    </div>
</template>

<script>
    import { ref } from "vue";

        export default {
        setup() {
            const products = ref([
            { id: 1, name: "Laptop", price: 1500 },
            { id: 2, name: "Smartphone", price: 800 },
            ]);

            const deleteProduct = (id) => {
            products.value = products.value.filter((product) => product.id !== id);
            };

            return { products, deleteProduct };
        },
    };
</script>

<style scoped>
    h1 {
        color: #007bff;
        }
    ul {
        list-style: none;
        padding: 0;
        }
    li {
        margin: 10px 0;
        }
    button {
        margin-left: 10px;
        background-color: red;
        color: white;
        border: none;
        padding: 5px;
        }
</style>