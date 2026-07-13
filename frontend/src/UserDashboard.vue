<template>
  <div>

    <h3 class="mb-4">My Dashboard</h3>

    <div class="row">

      <div class="col-md-5 mb-4">

        <div class="card">

          <div class="card-body">

            <h5 class="card-title">
              My Profile
            </h5>

            <div
              v-if="profileMsg"
              class="alert alert-success"
            >
              {{ profileMsg }}
            </div>

            <form @submit.prevent="updateProfile">

              <div class="mb-3">

                <label class="form-label">
                  Name
                </label>

                <input
                  v-model="profile.name"
                  class="form-control"
                >

              </div>

              <div class="mb-3">

                <label class="form-label">
                  Phone
                </label>

                <input
                  v-model="profile.phone"
                  class="form-control"
                >

              </div>

              <div class="mb-3">

                <label class="form-label">
                  Email
                </label>

                <input
                  :value="profile.email"
                  class="form-control"
                  disabled
                >

              </div>

              <button
                class="btn btn-primary"
              >
                Save Changes
              </button>

            </form>

          </div>

        </div>

      </div>

      <div class="col-md-7">

        <div class="d-flex justify-content-between align-items-center mb-3">

          <h5>
            My Bookings
          </h5>

          <button
            class="btn btn-outline-secondary btn-sm"
            @click="downloadCSV"
          >
            Download CSV
          </button>

        </div>

        <table class="table table-bordered">

          <thead>

            <tr>

              <th>Trek</th>

              <th>Date</th>

              <th>Status</th>

              <th>Payment</th>

              <th>Action</th>

            </tr>

          </thead>

          <tbody>

            <tr
              v-for="booking in bookings"
              :key="booking.id"
            >

              <td>
                {{ booking.trek_name }}
              </td>

              <td>
                {{ formatDate(booking.booking_date) }}
              </td>

              <td>

                <span
                  :class="booking.status==='confirmed'
                    ? 'badge bg-success'
                    : 'badge bg-secondary'"
                >

                  {{ booking.status }}

                </span>

              </td>

              <td>

                {{ booking.payment_status }}

              </td>

              <td>

                <button
                  v-if="booking.status==='confirmed'"
                  class="btn btn-danger btn-sm"
                  @click="cancelBooking(booking.id)"
                >
                  Cancel
                </button>

              </td>

            </tr>

            <tr v-if="bookings.length===0">

              <td
                colspan="5"
                class="text-center text-muted"
              >

                No bookings yet.

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>
</template>

<script>
import api from "./api";

export default {

  name: "UserDashboard",

  data() {

    return {

      profile: {

        name: "",

        phone: "",

        email: ""

      },

      bookings: [],

      profileMsg: ""

    };

  },

  async mounted() {

    await Promise.all([

      this.loadProfile(),

      this.loadBookings()

    ]);

  },

  methods: {

    async loadProfile() {

      try {

        const response = await api.get("/auth/me");

        this.profile = response.data;

      }

      catch {

        alert("Failed to load profile.");

      }

    },

    async loadBookings() {

      try {

        const response = await api.get("/bookings/history");

        this.bookings = response.data;

      }

      catch {

        alert("Failed to load bookings.");

      }

    },

    async updateProfile() {

      try {

        await api.put("/profile", {

          name: this.profile.name,

          phone: this.profile.phone

        });

        localStorage.setItem(

          "name",

          this.profile.name

        );

        this.profileMsg = "Profile updated successfully.";

      }

      catch {

        alert("Failed to update profile.");

      }

    },

    async cancelBooking(id) {

      if (!confirm("Cancel this booking?"))
        return;

      try {

        await api.delete(`/bookings/${id}`);

        await this.loadBookings();

      }

      catch {

        alert("Failed to cancel booking.");

      }

    },

    downloadCSV() {

      const token = localStorage.getItem("token");

      window.open(

        `http://localhost:5000/api/bookings/export?token=${token}`,

        "_blank"

      );

    },

    formatDate(date) {

      if (!date)
        return "";

      return new Date(date).toLocaleString();

    }

  }

};
</script>