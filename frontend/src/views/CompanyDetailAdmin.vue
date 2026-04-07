<template>
  <div class="main-box">
    <button class="back-btn" @click="$router.back()">← Back</button>

    <h2>Company Details (Admin)</h2>

    <!-- ===== COMPANY INFO ===== -->
    <div v-if="company" class="profile-box">
      <p><b>Company Name:</b> {{ company.company_name }}</p>
      <p><b>Email:</b> {{ company.email }}</p>
      <p><b>Industry:</b> {{ company.industry }}</p>
      <p><b>Website:</b> {{ company.website }}</p>
      <p><b>Location:</b> {{ company.location }}</p>
      <p><b>Company Size:</b> {{ company.company_size }}</p>
      <p><b>Status:</b> {{ company.is_blocked ? "Blocked" : "Active" }}</p>
      <p><b>Joined On:</b> {{ company.created_at }}</p>

      <button class="danger-btn" @click="toggleCompany">
        {{ company.is_blocked ? "Unblock Company" : "Block Company" }}
      </button>
    </div>

    <!-- ===== JOBS ===== -->
    <h3>Jobs Posted</h3>

    <div v-if="jobs.length === 0">No jobs posted</div>

    <div v-for="job in jobs" :key="job.id" class="card">
      <p><b>{{ job.title }}</b></p>
      <p>{{ job.description }}</p>
      <p><b>Salary:</b> {{ job.salary }}</p>
      <p><b>Applications:</b> {{ job.applications_count }}</p>
      <p><b>Status:</b> {{ job.is_blacklisted ? "Blocked" : "Active" }}</p>

      <button class="danger-btn" @click="toggleJob(job.id)">
        {{ job.is_blacklisted ? "Unblock Job" : "Block Job" }}
      </button>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      company: null,
      jobs: [],
    };
  },

  methods: {
    loadCompany() {
      const token = localStorage.getItem("token");
      const id = this.$route.params.id;

      api.get(`/admin/company_details/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        this.company = res.data.company;
        this.jobs = res.data.jobs;
      })
      .catch(() => {
        alert("Error loading company");
      });
    },

    toggleCompany() {
      const token = localStorage.getItem("token");

      api.post(`/admin/toggle_company_block/${this.company.id}`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(() => {
        this.company.is_blocked = !this.company.is_blocked;
      });
    },

    toggleJob(jobId) {
      const token = localStorage.getItem("token");

      api.post(`/admin/toggle_job_block/${jobId}`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(() => {
        const job = this.jobs.find(j => j.id === jobId);
        if (job) job.is_blacklisted = !job.is_blacklisted;
      });
    }
  },

  mounted() {
    this.loadCompany();
  },
};
</script>

<style>
.main-box {
  max-width: 750px;
  margin: auto;
  padding: 20px;
}

.profile-box {
  border: 1px solid #444;
  padding: 15px;
  margin-bottom: 20px;
}

.card {
  border: 1px solid #555;
  padding: 10px;
  margin: 10px 0;
}

.danger-btn {
  background: red;
  color: white;
  padding: 6px 12px;
  border: none;
  cursor: pointer;
  margin-top: 5px;
}

.back-btn {
  background: none;
  border: none;
  color: #2196f3;
  cursor: pointer;
  margin-bottom: 15px;
}
</style>