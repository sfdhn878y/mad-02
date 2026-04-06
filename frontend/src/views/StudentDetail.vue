<template>
  <div class="main-box">
    <h2>Student Details</h2>

    <div v-if="data">

      <p><b>Name:</b> {{ data.name }}</p>
      <p><b>Department:</b> {{ data.department }}</p>
      <p><b>CGPA:</b> {{ data.cgpa }}</p>
      <p><b>Total Applications:</b> {{ data.applications_count }}</p>

      <h3>Applications</h3>

      <div v-if="data.applications.length === 0">
        No applications
      </div>

      <div
        v-for="app in data.applications"
        :key="app.job"
        class="card"
      >
        <p><b>{{ app.job }}</b></p>
        <p>Company: {{ app.company }}</p>
        <p>Status: {{ app.status }}</p>
      </div>

    </div>

    <div v-else>
      Loading...
    </div>

  </div>
</template>
<script>
import api from "../services/api";

export default {
  data() {
    return {
      data: null,
    };
  },

  methods: {
    getStudentDetails() {
      const token = localStorage.getItem("token");
      const id = this.$route.params.id;

      api
        .get(`/admin/student_details/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.data = res.data;
        })
        .catch(() => {
          alert("Error loading student");
        });
    },
  },

  mounted() {
    this.getStudentDetails();
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