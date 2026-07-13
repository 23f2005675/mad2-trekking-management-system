<template>
  <div class="row justify-content-center">

    <div class="col-md-5">

      <div class="card shadow">

        <div class="card-body">

          <h3 class="text-center mb-4">
            Trekking Management System
          </h3>

          <h5 class="mb-4">
            Login
          </h5>

          <div
            v-if="error"
            class="alert alert-danger"
          >
            {{ error }}
          </div>

          <form @submit.prevent="login">

            <div class="mb-3">
              <label class="form-label">
                Email
              </label>

              <input
                v-model="email"
                type="email"
                class="form-control"
                required
              >
            </div>

            <div class="mb-3">

              <label class="form-label">
                Password
              </label>

              <input
                v-model="password"
                type="password"
                class="form-control"
                required
              >

            </div>

            <button
              class="btn btn-primary w-100"
              :disabled="loading"
            >
              {{ loading ? "Logging in..." : "Login" }}
            </button>

          </form>

          <div class="mt-3">

            Don't have an account?

            <router-link to="/register">
              Register
            </router-link>

          </div>

          <hr>

          <small class="text-muted">

            Admin Login

            <br>

            Email :
            admin@trek.com

            <br>

            Password :
            admin123

          </small>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import api from "./api";

export default {

  name: "Login",

  data() {

    return {

      email: "",

      password: "",

      error: "",

      loading: false

    };

  },

  methods: {

    async login() {

      this.error = "";

      this.loading = true;

      try {

        const response = await api.post(
          "/auth/login",
          {

            email: this.email,

            password: this.password

          }
        );

        localStorage.setItem(
          "token",
          response.data.access_token
        );

        localStorage.setItem(
          "role",
          response.data.role
        );

        localStorage.setItem(
          "name",
          response.data.user.name
        );

        localStorage.setItem(
          "user_id",
          response.data.user.id
        );

        if (response.data.role === "Admin") {

          this.$router.push("/admin");

        }

        else if (response.data.role === "Trek Staff") {

          this.$router.push("/staff");

        }

        else {

          this.$router.push("/dashboard");

        }

      }

      catch (error) {

        this.error =
          error.response?.data?.message ||
          "Invalid email or password.";

      }

      finally {

        this.loading = false;

      }

    }

  }

};
</script>