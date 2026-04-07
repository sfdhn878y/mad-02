<template>
  <div class="main-box" v-if="job">
    <h2>Job Detail</h2>

    <!-- ===== JOB INFO ===== -->
    <div class="card">
      <h3>{{ job.title }}</h3>
      <p><b>Description:</b> {{ job.description }}</p>
      <p><b>Skills:</b> {{ job.skills }}</p>
      <p><b>Experience:</b> {{ job.experience }}</p>
      <p><b>Salary:</b> {{ job.salary }}</p>
      <p><b>Benefits:</b> {{ job.benefits }}</p>
      <p><b>Location:</b> {{ job.location }}</p>
      <p><b>Type:</b> {{ job.job_type }}</p>
      <p><b>Approved:</b> {{ job.is_approved }}</p>
      <p><b>Closed:</b> {{ job.is_closed }}</p>
      <p><b>Blacklisted:</b> {{ job.is_blacklisted }}</p>
    </div>

    <!-- ===== COMPANY INFO ===== -->
    <h3>Company Detail</h3>
    <div class="card">
      <p><b>Name:</b> {{ company.company_name }}</p>
      <p><b>Industry:</b> {{ company.industry }}</p>
      <p><b>Website:</b> {{ company.website }}</p>
      <p><b>Location:</b> {{ company.location }}</p>
      <p><b>Size:</b> {{ company.company_size }}</p>
      <p><b>Email:</b> {{ company.email }}</p>
      <p><b>Phone:</b> {{ company.phone }}</p>
      <p><b>Active:</b> {{ company.is_active }}</p>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      job: null,
      company: null,
    };
  },

  mounted() {
    const token = localStorage.getItem("token");
    const id = this.$route.params.id;

    api
      .get(`/admin/job/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        this.job = res.data.job;
        this.company = res.data.company;
      });
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
  padding: 15px;
  margin: 15px 0;
}
</style>