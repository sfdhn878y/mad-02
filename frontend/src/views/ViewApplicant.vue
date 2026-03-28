<template>
  <div class="main-box">
    <h2>Applicants</h2>

    <div v-if="applicants.length === 0">
      No applicants yet 😴
    </div>

    <div v-for="app in applicants" :key="app.application_id" class="card">
      <p><b>Name:</b> {{ app.name }}</p>
      <p><b>Email:</b> {{ app.email }}</p>
      <p><b>Phone:</b> {{ app.phone }}</p>
      <p><b>Skills:</b> {{ app.skills }}</p>
      <p><b>CGPA:</b> {{ app.cgpa }}</p>
      <p><b>Status:</b> {{ app.status }}</p>

      <a :href="app.resume" target="_blank">View Resume</a>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      applicants: [],
    };
  },

  methods: {
    fetchApplicants() {
      const token = localStorage.getItem("token");
      const jobId = this.$route.params.jobId;

      api
        .get(`/company/job/${jobId}/applicants`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.applicants = res.data;
        })
        .catch(() => {
          alert("Error fetching applicants");
        });
    },
  },

  mounted() {
    this.fetchApplicants();
  },
};
</script>

<style>
.main-box {
  max-width: 700px;
  margin: auto;
  padding: 20px;
}

.card {
  border: 1px solid #444;
  padding: 10px;
  margin: 10px 0;
}
</style>