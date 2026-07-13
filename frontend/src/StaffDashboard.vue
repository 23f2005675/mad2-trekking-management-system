<template>
  <div>
    <h3 class="mb-4">Staff Dashboard</h3>

    <table class="table table-bordered align-middle">
      <thead>
        <tr>
          <th>Trek</th>
          <th>Status</th>
          <th>Available Slots</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="trek in treks" :key="trek.id">
          <td>
            <strong>{{ trek.name }}</strong>
            <br>
            <small class="text-muted">{{ trek.location }}</small>
          </td>

          <td>
            <span class="badge bg-info text-dark">
              {{ trek.status }}
            </span>
          </td>

          <td style="width:150px">
            <input
              type="number"
              min="0"
              class="form-control form-control-sm"
              v-model.number="trek.available_slots"
            >
          </td>

          <td>

            <div class="d-flex flex-wrap gap-2">

              <button
                class="btn btn-primary btn-sm"
                @click="saveSlots(trek)"
              >
                Save Slots
              </button>

              <select
                class="form-select form-select-sm w-auto"
                v-model="trek.status"
                @change="updateStatus(trek)"
              >
                <option value="Open">Open</option>
                <option value="Closed">Closed</option>
                <option value="Started">Started</option>
                <option value="Completed">Completed</option>
              </select>

              <button
                class="btn btn-outline-secondary btn-sm"
                @click="viewParticipants(trek)"
              >
                Participants
              </button>

            </div>

          </td>
        </tr>

        <tr v-if="treks.length===0">
          <td colspan="4" class="text-center text-muted">
            No treks assigned yet.
          </td>
        </tr>

      </tbody>

    </table>

    <div
      class="card mt-4"
      v-if="selectedTrek"
    >

      <div class="card-body">

        <h5 class="card-title">
          Participants - {{ selectedTrek.name }}
        </h5>

        <ul class="list-group">

          <li
            class="list-group-item"
            v-for="participant in participants"
            :key="participant.booking_id"
          >

            {{ participant.user_name }}

            ({{ participant.user_email }})

          </li>

          <li
            class="list-group-item text-muted"
            v-if="participants.length===0"
          >
            No participants yet.
          </li>

        </ul>

      </div>

    </div>

  </div>
</template>

<script>
import api from "./api";

export default {

  name: "StaffDashboard",

  data() {

    return {

      treks: [],

      selectedTrek: null,

      participants: []

    };

  },

  async mounted() {

    await this.loadTreks();

  },

  methods: {

    async loadTreks() {

      try {

        const response = await api.get("/staff/treks");

        this.treks = response.data;

      }

      catch {

        alert("Failed to load treks.");

      }

    },

    async saveSlots(trek) {

      try {

        await api.put(`/staff/treks/${trek.id}`, {

          available_slots: trek.available_slots

        });

        alert("Slots updated successfully.");

      }

      catch {

        alert("Failed to update slots.");

      }

    },

    async updateStatus(trek) {

      try {

        await api.put(`/staff/treks/${trek.id}`, {

          status: trek.status

        });

        alert("Status updated successfully.");

      }

      catch {

        alert("Failed to update trek status.");

      }

    },

    async viewParticipants(trek) {

      try {

        this.selectedTrek = trek;

        const response = await api.get(`/staff/participants/${trek.id}`);

        this.participants = response.data;

      }

      catch {

        alert("Failed to load participants.");

      }

    }

  }

};
</script>