<template>
  <div v-if="trek" class="row justify-content-center">

    <div class="col-md-8">

      <div class="card shadow-sm">

        <div class="card-body">

          <h2>{{ trek.name }}</h2>

          <h5 class="text-muted">
            {{ trek.location }}
          </h5>

          <hr>

          <p>
            {{ trek.description }}
          </p>

          <ul class="list-group list-group-flush mb-4">

            <li class="list-group-item">
              <strong>Difficulty:</strong>
              {{ trek.difficulty }}
            </li>

            <li class="list-group-item">
              <strong>Duration:</strong>
              {{ trek.duration_days }} Days
            </li>

            <li class="list-group-item">
              <strong>Price:</strong>
              ₹{{ trek.price }}
            </li>

            <li class="list-group-item">
              <strong>Available Slots:</strong>
              {{ trek.available_slots }}
            </li>

            <li class="list-group-item">
              <strong>Status:</strong>
              {{ trek.status }}
            </li>

            <li
              v-if="trek.staff_name"
              class="list-group-item"
            >
              <strong>Assigned Staff:</strong>
              {{ trek.staff_name }}
            </li>

          </ul>

          <div
            v-if="message"
            class="alert alert-info"
          >
            {{ message }}
          </div>

          <button
            v-if="isUser && trek.status === 'Open'"
            class="btn btn-success"
            :disabled="trek.available_slots <= 0"
            @click="book"
          >
            Book Trek
          </button>

          <button
            class="btn btn-secondary ms-2"
            @click="$router.push('/treks')"
          >
            Back
          </button>

          <p
            v-if="!isUser"
            class="text-muted mt-3"
          >
            Login as a User to book this trek.
          </p>

        </div>

      </div>

    </div>

  </div>
</template>

<script>
import api from "./api";

export default {

  name: "TrekDetails",

  props: ["id"],

  data() {

    return {

      trek: null,

      message: "",

      isUser: (localStorage.getItem("role") || "").toLowerCase() === "user"

    };

  },

  async mounted() {

    await this.loadTrek();

  },

  methods: {

    async loadTrek() {

      try {

        const response = await api.get(`/treks/${this.id}`);

        this.trek = response.data;

      }

      catch {

        alert("Failed to load trek details.");

      }

    },

    async book() {

      this.message = "";

      try {

        await api.post("/bookings", {

          trek_id: this.trek.id

        });

        this.message = "Trek booked successfully.";

        await this.loadTrek();

      }

      catch (err) {

        this.message =
          err.response?.data?.msg ||
          "Booking failed.";

      }

    }

  }

};
</script>