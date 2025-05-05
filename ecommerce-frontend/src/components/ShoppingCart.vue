<template>
    <div>
        <h1>Shopping Cart</h1>
        <ul>
        <li v-for="item in cart" :key="item.id">
            {{ item.name }} - ${{ item.price }} (Quantity: {{ item.quantity }})
            <button @click="removeItem(item.id)">Remove</button>
        </li>
        </ul>
    </div>
</template>

<script>
    import { ref } from "vue";

        export default {
        setup() {
            const cart = ref([
            { id: 1, name: "Headphones", price: 150, quantity: 1 },
            { id: 2, name: "Keyboard", price: 100, quantity: 2 },
            ]);

            const removeItem = (id) => {
            cart.value = cart.value.filter((item) => item.id !== id);
            };

            return { cart, removeItem };
        },
    };
</script>

<style scoped>
    h1 {
        color: #28a745;
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