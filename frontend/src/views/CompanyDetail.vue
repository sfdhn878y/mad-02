<template>
  <div class="main-box">

    <button class="back-btn" @click="$router.back()">← Back</button>

    <!-- Company Profile -->
    <div v-if="company" class="profile-box">
      <h3>{{ company.company_name }}</h3>
      <p><b>Industry:</b> {{ company.industry }}</p>
      <p><b>Website:</b> {{ company.website }}</p>
      <p><b>Location:</b> {{ company.location }}</p>
      <p><b>Size:</b> {{ company.company_size }}</p>
    </div>

    <!-- Jobs -->
    <div class="section-box">
      <h3>Jobs Posted</h3>

      <p v-if="jobs.length === 0" class="empty-msg">No jobs posted by this company.</p>

      <div v-for="job in jobs" :key="job.id" class="job-card">
        <p><b>{{ job.title }}</b></p>
        <p>{{ job.description }}</p>
        <p><b>Skills:</b> {{ job.skills }}</p>
        <p v-if="job.experience"><b>Experience:</b> {{ job.experience }}</p>
        <p><b>Salary:</b> {{ job.salary }}</p>
        <p><b>Location:</b> {{ job.location }}</p>
        <p><b>Job Type:</b> {{ job.job_type }}</p>

        
      </div>
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
      myApplications: [],
    };
  },

  methods: {
    fetchCompanyDetails() {
      const token = localStorage.getItem("token");
      const companyId = this.$route.params.id;

      api
        .get(`/student/company_details/${companyId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.company = res.data.company;
          this.jobs = res.data.jobs;
        })
        .catch(() => {
          console.log("Error fetching company details");
        });
    },

    fetchMyApplications() {
      const token = localStorage.getItem("token");

      api
        .get("/student/my_applications", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.myApplications = res.data;
        })
        .catch(() => {
          console.log("Error fetching applications");
        });
    },

    hasApplied(jobId) {
      return this.myApplications.some((app) => app.job_id === jobId);
    },

    applyJob(jobId) {
      const token = localStorage.getItem("token");

      if (!confirm("Apply for this job?")) return;

      api
        .post(
          `/student/apply/${jobId}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then(() => {
          alert("Applied successfully");
          this.fetchMyApplications(); // refresh so button turns to Applied
        })
        .catch((err) => {
          alert(err.response?.data?.message || "Error applying");
        });
    },
  },

  mounted() {
    this.fetchCompanyDetails();
    this.fetchMyApplications();
  },
};
</script>

<style>
.main-box {
  max-width: 700px;
  margin: auto;
  padding: 20px;
}

.back-btn {
  background: none;
  border: none;
  color: #2196f3;
  font-size: 15px;
  cursor: pointer;
  margin-bottom: 15px;
  padding: 0;
}

.profile-box {
  border: 1px solid #444;
  padding: 15px;
  margin-bottom: 20px;
}

.section-box {
  border: 1px solid #ccc;
  padding: 15px;
  margin-bottom: 20px;
}

.section-box h3 {
  margin-top: 0;
  margin-bottom: 12px;
}

.job-card {
  border: 1px solid #555;
  padding: 10px;
  margin: 10px 0;
}

.job-actions {
  margin-top: 8px;
}

.closed-badge {
  background: #ccc;
  color: #555;
  padding: 4px 10px;
  font-size: 13px;
}

.view-btn {
  background: #2196f3;
  color: white;
  border: none;
  padding: 6px 12px;
  cursor: pointer;
}

.view-btn:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.empty-msg {
  color: #888;
  font-size: 14px;
}
</style>