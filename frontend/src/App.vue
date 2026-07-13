<template>
  <div>

    <Navbar v-if="showNavbar" />

    <div class="container mt-4 mb-5">
      <router-view />
    </div>

  </div>
</template>

<script>
import Navbar from "./Navbar.vue";

export default {
  name: "App",

  components: {
    Navbar,
  },

  computed: {
    showNavbar() {
      return !["/login", "/register"].includes(this.$route.path);
    },
  },
};
</script>