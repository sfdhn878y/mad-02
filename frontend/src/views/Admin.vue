<template>
  <div class="main-box">
    <h2>Admin Dashboard</h2>

    <!-- ===== STATS ===== -->
    <div class="stats-box">
      <div class="stat">Companies: {{ stats.companies }}</div>
      <div class="stat">Students: {{ stats.students }}</div>
      <div class="stat">Jobs: {{ stats.jobs }}</div>
      <div class="stat">Applications: {{ stats.applications }}</div>
    </div>

    <!-- ===== PENDING COMPANIES ===== -->
    <h3>Pending Companies</h3>
    <div v-if="pendingCompanies.length === 0">No pending companies</div>

    <div v-for="c in pendingCompanies" :key="c.id" class="card">
      <p>
        <b>{{ c.name }}</b>
      </p>
      <p>{{ c.email }}</p>

      <button class="approve-btn" @click="approveCompany(c.id)">Approve</button>
    </div>

    <!-- ===== APPROVED COMPANIES ===== -->
    <h3>Companies</h3>

    <input
      v-model="companySearch"
      @input="searchCompanies"
      placeholder="Search by name or industry..."
    />
    <div v-for="c in companies" :key="c.id" class="card">
      <p>
        <b>{{ c.company_name }}</b>
      </p>
      <p>Jobs: {{ c.jobs_count }}</p>

      <button class="view-btn" @click="viewCompany(c.id)">View</button>
      <button class="danger-btn" @click="blockCompany(c.id)">
        {{ c.is_blocked ? "Unblock" : "Block" }}
      </button>
    </div>

    <!-- ===== STUDENTS ===== -->
    <h3>Students</h3>

    <input
      v-model="studentSearch"
      @input="searchStudents"
      placeholder="Search by name, ID, email, or phone..."
    />
    <div v-for="s in students" :key="s.id" class="card">
      <p>
        <b>{{ s.name }}</b>
      </p>
      <p>Applications: {{ s.applications }}</p>

      <button class="view-btn" @click="viewStudent(s.user_id)">View</button>

      <button class="danger-btn" @click="toggleStudent(s.user_id)">
        {{ s.is_active ? "Block" : "Unblock" }}
      </button>
    </div>

    <!-- ===== PENDING JOBS ===== -->
    <h3>Pending Drives</h3>
    <div v-if="pendingJobs.length === 0">No pending jobs</div>

    <div v-for="j in pendingJobs" :key="j.id" class="card">
      <p>
        <b>{{ j.title }}</b>
      </p>
      <p>{{ j.company }}</p>

      <button class="approve-btn" @click="approveJob(j.id)">Approve</button>
    </div>

    <!-- ===== ALL JOBS ===== -->
    <h3>All Drives</h3>
    <div v-for="j in jobs" :key="j.id" class="card">
      <p>
        <b>{{ j.title }}</b>
      </p>
      <p>{{ j.company }}</p>
      <button class="view-btn" @click="viewJob(j.id)">View</button>
      <button class="danger-btn" @click="blockJob(j.id)">
        {{ j.is_blacklisted ? "Unblock" : "Block" }}
      </button>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      stats: {},
      pendingCompanies: [],
      companies: [],
      students: [],
      pendingJobs: [],
      jobs: [],
    };
  },

  methods: {
    // ===== LOAD ALL DATA =====

    loadStats() {
      const token = localStorage.getItem("token");

      api
        .get("/admin/stats", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.stats = res.data;
        });
    },

    loadPendingCompanies() {
      const token = localStorage.getItem("token");

      api
        .get("/admin/pending_companies", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.pendingCompanies = res.data;
        });
    },

    loadCompanies() {
      const token = localStorage.getItem("token");

      api
        .get("/admin/all_companies", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.companies = res.data;
        });
    },

    loadStudents() {
      const token = localStorage.getItem("token");

      api
        .get("/admin/all_students", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.students = res.data;
        });
    },

    loadPendingJobs() {
      const token = localStorage.getItem("token");

      api
        .get("/admin/pending_jobs", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.pendingJobs = res.data;
        });
    },

    loadJobs() {
      const token = localStorage.getItem("token");

      api
        .get("/admin/all_jobs", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.jobs = res.data;
        });
    },

    // ===== ACTIONS =====

    approveCompany(id) {
      const token = localStorage.getItem("token");

      api
        .post(
          `/admin/approve_company/${id}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then(() => {
          alert("Company Approved");
          this.loadPendingCompanies();
          this.loadCompanies();
        });
    },

    blockCompany(id) {
      const token = localStorage.getItem("token");

      api
        .post(
          `/admin/toggle_company_block/${id}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then(() => {
          // 🔥 instant toggle in UI
          const company = this.companies.find((c) => c.id === id);
          if (company) {
            company.is_blocked = !company.is_blocked;
          }
        });
    },
    approveJob(id) {
      const token = localStorage.getItem("token");

      api
        .put(
          `/admin/approve_job/${id}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then(() => {
          alert("Job Approved");
          this.loadPendingJobs();
          this.loadJobs();
        });
    },

    blockJob(id) {
      const token = localStorage.getItem("token");

      api
        .post(
          `/admin/toggle_job_block/${id}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then(() => {
          // 🔥 instant UI update (IMPORTANT)
          const job = this.jobs.find((j) => j.id === id);
          if (job) {
            job.is_blacklisted = !job.is_blacklisted;
          }
        })
        .catch((err) => {
          console.log(err);
          alert("error blocking job");
        });
    },

    viewCompany(id) {
      this.$router.push(`/admin/company/${id}`);
    },

    viewStudent(id) {
      this.$router.push(`/admin/student/${id}`);
    },
    toggleStudent(id) {
      const token = localStorage.getItem("token");

      api
        .post(
          `/admin/toggle_student_block/${id}`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        )
        .then(() => {
          // 🔥 instant UI update
          const student = this.students.find((s) => s.user_id === id);
          if (student) {
            student.is_active = !student.is_active;
          }
        })
        .catch(() => {
          alert("Error updating student status");
        });
    },
    viewJob(id) {
      this.$router.push(`/admin/job/${id}`);
    },
    searchStudents() {
      const token = localStorage.getItem("token");

      if (this.studentSearch.trim() === "") {
        this.loadStudents();
        return;
      }

      api
        .get(`/admin/search_students?q=${this.studentSearch}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.students = res.data;
        });
    },

    searchCompanies() {
      const token = localStorage.getItem("token");

      if (this.companySearch.trim() === "") {
        this.loadCompanies();
        return;
      }

      api
        .get(`/admin/search_companies?q=${this.companySearch}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.companies = res.data;
        });
    },
  },

  mounted() {
    // load everything
    this.loadStats();
    this.loadPendingCompanies();
    this.loadCompanies();
    this.loadStudents();
    this.loadPendingJobs();
    this.loadJobs();
  },
};
</script>

<style>
.main-box {
  max-width: 750px;
  margin: auto;
  padding: 20px;
}

.stats-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.stat {
  background: #eee;
  padding: 10px;
}

.card {
  border: 1px solid #444;
  padding: 10px;
  margin: 10px 0;
}

.approve-btn {
  background: green;
  color: white;
  margin-right: 10px;
}

.danger-btn {
  background: red;
  color: white;
}

.view-btn {
  background: #2196f3;
  color: white;
  margin-right: 10px;
}
</style>