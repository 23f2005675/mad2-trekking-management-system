<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">

    <div class="container">

      <router-link
        class="navbar-brand"
        to="/treks"
      >
        Trekking Management
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div
        class="collapse navbar-collapse"
        id="navbarNav"
      >

        <ul class="navbar-nav me-auto">

          <li class="nav-item">
            <router-link
              class="nav-link"
              to="/treks"
            >
              Treks
            </router-link>
          </li>

          <li
            class="nav-item"
            v-if="role === 'Admin'"
          >
            <router-link
              class="nav-link"
              to="/admin"
            >
              Admin Dashboard
            </router-link>
          </li>

          <li
            class="nav-item"
            v-if="role === 'Trek Staff'"
          >
            <router-link
              class="nav-link"
              to="/staff"
            >
              Staff Dashboard
            </router-link>
          </li>

          <li
            class="nav-item"
            v-if="role === 'User'"
          >
            <router-link
              class="nav-link"
              to="/dashboard"
            >
              My Dashboard
            </router-link>
          </li>

        </ul>

        <ul class="navbar-nav">

          <template v-if="!isLoggedIn">

            <li class="nav-item">
              <router-link
                class="nav-link"
                to="/login"
              >
                Login
              </router-link>
            </li>

            <li class="nav-item">
              <router-link
                class="nav-link"
                to="/register"
              >
                Register
              </router-link>
            </li>

          </template>

          <template v-else>

            <li class="nav-item">

              <span class="nav-link text-light">

                {{ userName }}

                <small class="text-warning">
                  ({{ role }})
                </small>

              </span>

            </li>

            <li class="nav-item">

              <button
                class="btn btn-outline-light btn-sm ms-2"
                @click="logout"
              >
                Logout
              </button>

            </li>

          </template>

        </ul>

      </div>

    </div>

  </nav>
</template>

<script>
export default {

  name: "Navbar",

  data() {

    return {

      isLoggedIn: !!localStorage.getItem("token"),

      role: localStorage.getItem("role"),

      userName: localStorage.getItem("name")

    };

  },

  methods: {

    logout() {

      localStorage.removeItem("token");
      localStorage.removeItem("role");
      localStorage.removeItem("name");
      localStorage.removeItem("user_id");

      this.$router.push("/login");

    }

  }

};
</script>