<template>
  <div>
    <h3 class="mb-4">Admin Dashboard</h3>

    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h6 class="card-title text-muted">Total Users</h6>
            <h2 class="card-text">{{ dashboard.total_users }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h6 class="card-title text-muted">Total Staff</h6>
            <h2 class="card-text">{{ dashboard.total_staff }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h6 class="card-title text-muted">Total Treks</h6>
            <h2 class="card-text">{{ dashboard.total_treks }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h6 class="card-title text-muted">Total Bookings</h6>
            <h2 class="card-text">{{ dashboard.total_bookings }}</h2>
          </div>
        </div>
      </div>
    </div>

    <ul class="nav nav-tabs mb-3">
      <li class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'treks' }"
          @click="activeTab = 'treks'"
        >
          Treks
        </button>
      </li>
      <li class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'staff' }"
          @click="activeTab = 'staff'"
        >
          Staff
        </button>
      </li>
      <li class="nav-item">
        <button
          class="nav-link"
          :class="{ active: activeTab === 'users' }"
          @click="activeTab = 'users'"
        >
          Users
        </button>
      </li>
    </ul>

    <!-- TREKS TAB -->
    <div v-if="activeTab === 'treks'">
      <div class="card mb-4">
        <div class="card-body">
          <h5 class="card-title">Create Trek</h5>
          <form @submit.prevent="createTrek">
            <div class="row g-2">
              <div class="col-md-4">
                <label class="form-label">Name</label>
                <input v-model="newTrek.name" type="text" class="form-control" required />
              </div>
              <div class="col-md-4">
                <label class="form-label">Location</label>
                <input v-model="newTrek.location" type="text" class="form-control" required />
              </div>
              <div class="col-md-4">
                <label class="form-label">Difficulty</label>
                <select v-model="newTrek.difficulty" class="form-select">
                  <option value="Easy">Easy</option>
                  <option value="Moderate">Moderate</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>
              <div class="col-md-3">
                <label class="form-label">Duration (days)</label>
                <input
                  v-model.number="newTrek.duration_days"
                  type="number"
                  min="1"
                  class="form-control"
                  required
                />
              </div>
              <div class="col-md-3">
                <label class="form-label">Price</label>
                <input
                  v-model.number="newTrek.price"
                  type="number"
                  min="0"
                  class="form-control"
                  required
                />
              </div>
              <div class="col-md-3">
                <label class="form-label">Available Slots</label>
                <input
                  v-model.number="newTrek.available_slots"
                  type="number"
                  min="0"
                  class="form-control"
                  required
                />
              </div>
              <div class="col-md-3">
                <label class="form-label">Start Date</label>
                <input v-model="newTrek.start_date" type="date" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">End Date</label>
                <input v-model="newTrek.end_date" type="date" class="form-control" />
              </div>
              <div class="col-md-12">
                <label class="form-label">Description</label>
                <textarea v-model="newTrek.description" class="form-control" rows="2"></textarea>
              </div>
              <div class="col-md-12">
                <button type="submit" class="btn btn-primary mt-2">Create Trek</button>
              </div>
            </div>
          </form>
        </div>
      </div>

      <table class="table table-bordered align-middle">
        <thead>
          <tr>
            <th>Name</th>
            <th>Location</th>
            <th>Difficulty</th>
            <th>Status</th>
            <th>Available Slots</th>
            <th>Assigned Staff</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trek in treks" :key="trek.id">
            <td>{{ trek.name }}</td>
            <td>{{ trek.location }}</td>
            <td>{{ trek.difficulty }}</td>
            <td>{{ trek.status }}</td>
            <td>{{ trek.available_slots }}</td>
            <td>
              <select
                v-model="trek.assigned_staff_id"
                class="form-select form-select-sm"
                @change="assignStaff(trek)"
              >
                <option :value="null">-- None --</option>
                <option v-for="staff in staffList" :key="staff.id" :value="staff.id">
                  {{ staff.name }}
                </option>
              </select>
            </td>
            <td>
              <div class="d-flex flex-wrap gap-1">
                <button
                  v-if="trek.status === 'Pending'"
                  class="btn btn-sm btn-success"
                  @click="approveTrek(trek)"
                >
                  Approve Trek
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteTrek(trek)">Delete</button>
              </div>
            </td>
          </tr>
          <tr v-if="treks.length === 0">
            <td colspan="7" class="text-center text-muted">No treks found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- STAFF TAB -->
    <div v-if="activeTab === 'staff'">
      <div class="card mb-4">
        <div class="card-body">
          <h5 class="card-title">Create Trek Staff</h5>
          <form @submit.prevent="createStaff">
            <div class="row g-2">
              <div class="col-md-4">
                <label class="form-label">Name</label>
                <input v-model="newStaff.name" type="text" class="form-control" required />
              </div>
              <div class="col-md-4">
                <label class="form-label">Email</label>
                <input v-model="newStaff.email" type="email" class="form-control" required />
              </div>
              <div class="col-md-4">
                <label class="form-label">Phone</label>
                <input v-model="newStaff.phone" type="text" class="form-control" />
              </div>
              <div class="col-md-4">
                <label class="form-label">Contact</label>
                <input v-model="newStaff.contact" type="text" class="form-control" />
              </div>
              <div class="col-md-4">
                <label class="form-label">Password</label>
                <input v-model="newStaff.password" type="password" class="form-control" required />
              </div>
              <div class="col-md-12">
                <button type="submit" class="btn btn-primary mt-2">Create Staff</button>
              </div>
            </div>
          </form>
        </div>
      </div>

      <table class="table table-bordered align-middle">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Blacklisted</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="staff in staffList" :key="staff.id">
            <td>{{ staff.name }}</td>
            <td>{{ staff.email }}</td>
            <td><span :class="staff.is_active ? 'badge bg-success' : 'badge bg-secondary'">{{ staff.is_active ? 'Active' : 'Suspended' }}</span></td>
            <td>{{ staff.is_blacklisted ? "Yes" : "No" }}</td>
            <td>
              <div class="d-flex flex-wrap gap-1">
                <button class="btn btn-sm btn-outline-secondary" @click="toggleStaffStatus(staff)">
                  {{ staff.is_active ? "Suspend" : "Activate" }}
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="toggleStaffBlacklist(staff)">
                  {{ staff.is_blacklisted ? "Un-blacklist" : "Blacklist" }}
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="staffList.length === 0">
            <td colspan="5" class="text-center text-muted">No staff found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- USERS TAB -->
    <div v-if="activeTab === 'users'">
      <table class="table table-bordered align-middle">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Blacklisted</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.phone }}</td>
            <td>{{ user.is_blacklisted ? "Yes" : "No" }}</td>
            <td>
              <button class="btn btn-sm btn-outline-danger" @click="toggleUserBlacklist(user)">
                {{ user.is_blacklisted ? "Un-blacklist" : "Blacklist" }}
              </button>
            </td>
          </tr>
          <tr v-if="users.length === 0">
            <td colspan="5" class="text-center text-muted">No users found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from "./api";

export default {
  name: "AdminDashboard",
  data() {
    return {
      activeTab: "treks",
      dashboard: {
        total_users: 0,
        total_staff: 0,
        total_treks: 0,
        total_bookings: 0
      },
      treks: [],
      staffList: [],
      users: [],
      newTrek: {
        name: "",
        location: "",
        difficulty: "Easy",
        duration_days: null,
        price: null,
        available_slots: null,
        start_date: "",
        end_date: "",
        description: ""
      },
      newStaff: {
        name: "",
        email: "",
        phone: "",
        contact: "",
        password: ""
      }
    };
  },
  async mounted() {
    await this.loadAllData();
  },
  methods: {
    async loadAllData() {
      try {
        const [dashboardRes, treksRes, staffRes, usersRes] = await Promise.all([
          api.get("/admin/dashboard"),
          api.get("/admin/treks"),
          api.get("/admin/staff"),
          api.get("/admin/users")
        ]);
        this.dashboard = dashboardRes.data;
        this.treks = treksRes.data;
        this.staffList = staffRes.data;
        this.users = usersRes.data;
      } catch (err) {
        alert("Failed to load dashboard data.");
      }
    },
    resetTrekForm() {
      this.newTrek = {
        name: "",
        location: "",
        difficulty: "Easy",
        duration_days: null,
        price: null,
        available_slots: null,
        start_date: "",
        end_date: "",
        description: ""
      };
    },
    resetStaffForm() {
      this.newStaff = {
        name: "",
        email: "",
        phone: "",
        contact: "",
        password: ""
      };
    },
    async createTrek() {
      try {
        await api.post("/admin/treks", this.newTrek);
        this.resetTrekForm();
        await this.loadAllData();
      } catch (err) {
        alert("Failed to create trek.");
      }
    },
    async approveTrek(trek) {
      try {
        await api.put(`/admin/treks/${trek.id}`, { status: "Open" });
        await this.loadAllData();
      } catch (err) {
        alert("Failed to approve trek.");
      }
    },
    async assignStaff(trek) {
      try {
        await api.put(`/admin/treks/${trek.id}`, {
          assigned_staff_id: trek.assigned_staff_id
        });
        await this.loadAllData();
      } catch (err) {
        alert("Failed to assign staff.");
      }
    },
    async deleteTrek(trek) {
      if (!confirm(`Are you sure you want to delete "${trek.name}"?`)) return;
      try {
        await api.delete(`/admin/treks/${trek.id}`);
        await this.loadAllData();
      } catch (err) {
        alert("Failed to delete trek.");
      }
    },
    async createStaff() {
      try {
        await api.post("/admin/staff", this.newStaff);
        this.resetStaffForm();
        await this.loadAllData();
      } catch (err) {
        alert("Failed to create staff.");
      }
    },
    async toggleStaffStatus(staff) {

      try {

          await api.put(`/admin/staff/${staff.id}`, {

              is_active: !staff.is_active

          });

          await this.loadAllData();

      }

      catch {

          alert("Failed to update staff status.");

      }

    },
    async toggleStaffBlacklist(staff) {
      try {
        await api.put(`/admin/staff/${staff.id}`, {
          is_blacklisted: !staff.is_blacklisted
        });
        await this.loadAllData();
      } catch (err) {
        alert("Failed to update staff blacklist status.");
      }
    },
    async toggleUserBlacklist(user) {
      try {
        await api.put(`/admin/users/${user.id}`, {
          is_blacklisted: !user.is_blacklisted
        });
        await this.loadAllData();
      } catch (err) {
        alert("Failed to update user blacklist status.");
      }
    }
  }
};
</script>