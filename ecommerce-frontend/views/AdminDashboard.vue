<template>
  <div>
    <h1>Admin Dashboard</h1>
    <AdminProductManagement />
  </div>
</template>

<script>
import AdminProductManagement from '@/components/AdminProductManagement.vue';

export default {
  components: {
    AdminProductManagement,
  },
};
</script>
