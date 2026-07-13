<template>
  <div class="row justify-content-center">

    <div class="col-md-5">

      <div class="card shadow">

        <div class="card-body">

          <h3 class="text-center mb-4">
            Create Account
          </h3>

          <div
            v-if="error"
            class="alert alert-danger"
          >
            {{ error }}
          </div>

          <div
            v-if="success"
            class="alert alert-success"
          >
            {{ success }}
          </div>

          <form @submit.prevent="register">

            <div class="mb-3">
              <label class="form-label">Name</label>
              <input
                v-model="name"
                type="text"
                class="form-control"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Email</label>
              <input
                v-model="email"
                type="email"
                class="form-control"
                required
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Phone</label>
              <input
                v-model="phone"
                type="text"
                class="form-control"
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Password</label>
              <input
                v-model="password"
                type="password"
                class="form-control"
                required
              >
            </div>

            <button
              class="btn btn-success w-100"
              :disabled="loading"
            >
              {{ loading ? "Registering..." : "Register" }}
            </button>

          </form>

          <div class="mt-3">

            Already have an account?

            <router-link to="/login">
              Login
            </router-link>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import api from "./api";

export default {

  name: "Register",

  data() {

    return {

      name: "",
      email: "",
      phone: "",
      password: "",

      loading: false,

      error: "",
      success: ""

    };

  },

  methods: {

    async register() {

      this.loading = true;

      this.error = "";
      this.success = "";

      try {

        await api.post("/auth/register", {

          name: this.name,
          email: this.email,
          phone: this.phone,
          password: this.password

        });

        this.success = "Registration successful. Redirecting to login...";

        setTimeout(() => {

          this.$router.push("/login");

        }, 1500);

      }

      catch (error) {

        this.error =
          error.response?.data?.message ||
          "Registration failed.";

      }

      finally {

        this.loading = false;

      }

    }

  }

};
</script>