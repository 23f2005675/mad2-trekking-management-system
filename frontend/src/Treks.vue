<template>
  <div>

    <h3 class="mb-4">Available Treks</h3>

    <div class="row g-2 mb-4">

      <div class="col-md-4">
        <input
          v-model="search"
          @keyup.enter="loadTreks"
          class="form-control"
          placeholder="Search Trek"
        >
      </div>

      <div class="col-md-3">
        <input
          v-model="location"
          @keyup.enter="loadTreks"
          class="form-control"
          placeholder="Location"
        >
      </div>

      <div class="col-md-3">

        <select
          v-model="difficulty"
          class="form-select"
        >
          <option value="">All Difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Moderate">Moderate</option>
          <option value="Hard">Hard</option>
        </select>

      </div>

      <div class="col-md-2">

        <button
          class="btn btn-primary w-100"
          @click="loadTreks"
        >
          Search
        </button>

      </div>

    </div>

    <div
      v-if="treks.length===0"
      class="alert alert-info"
    >
      No open treks available.
    </div>

    <div class="row">

      <div
        class="col-md-4 mb-4"
        v-for="trek in treks"
        :key="trek.id"
      >

        <div class="card h-100 shadow-sm">

          <div class="card-body d-flex flex-column">

            <h5 class="card-title">

              {{ trek.name }}

            </h5>

            <h6 class="text-muted">

              {{ trek.location }}

            </h6>

            <hr>

            <p>

              <strong>Difficulty:</strong>

              {{ trek.difficulty }}

            </p>

            <p>

              <strong>Duration:</strong>

              {{ trek.duration_days }} days

            </p>

            <p>

              <strong>Price:</strong>

              ₹{{ trek.price }}

            </p>

            <p>

              <strong>Available Slots:</strong>

              {{ trek.available_slots }}

            </p>

            <p>

              <strong>Status:</strong>

              {{ trek.status }}

            </p>

            <router-link
              class="btn btn-outline-primary mt-auto"
              :to="`/treks/${trek.id}`"
            >

              View Details

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

  name: "Treks",

  data() {

    return {

      treks: [],

      search: "",

      location: "",

      difficulty: ""

    };

  },

  async mounted() {

    await this.loadTreks();

  },

  methods: {

    async loadTreks() {

      try {

        const params = {};

        if (this.search)
          params.search = this.search;

        if (this.location)
          params.location = this.location;

        if (this.difficulty)
          params.difficulty = this.difficulty;

        const response = await api.get("/treks", {

          params

        });

        this.treks = response.data;

      }

      catch {

        alert("Failed to load treks.");

      }

    }

  }

};
</script>