<template>
  <div class="main-box">
    <!-- Profile Button -->
    <button v-if="!company_data" class="create-btn" @click="showForm = true">
      + New Profile
    </button>
    <button v-if="company_data" class="create-btn" @click="showForm = true">
      + Update Profile
    </button>

    <!-- Profile Form -->
    <div v-if="showForm" class="form-box">
      <h3>
        {{ company_data ? "Update Company Profile" : "Create Company Profile" }}
      </h3>

      <input v-model="profile.company_name" placeholder="Company Name" />
      <input v-model="profile.industry" placeholder="Industry" />
      <input v-model="profile.website" placeholder="Website" />
      <input v-model="profile.location" placeholder="Location" />
      <input v-model="profile.company_size" placeholder="Company Size" />

      <button v-if="!company_data" @click="submitProfile">Submit</button>
      <button v-if="company_data" @click="editProfile">Update Profile</button>
      <button class="cancel-btn" @click="showForm = false">Cancel</button>
    </div>

    <!-- Profile Display -->
    <div v-if="company_data" class="profile-box">
      <h3>Company Profile</h3>

      <p><b>Name:</b> {{ company_data.company_name }}</p>
      <p><b>Industry:</b> {{ company_data.industry }}</p>
      <p><b>Website:</b> {{ company_data.website }}</p>
      <p><b>Location:</b> {{ company_data.location }}</p>
      <p><b>Size:</b> {{ company_data.company_size }}</p>
    </div>

    <!-- Job Button -->
    <button class="create-btn" @click="showJobForm = true">+ Post Job</button>

    <!-- Job Form -->
    <div v-if="showJobForm" class="form-box">
      <h3>Post Job</h3>

      <input v-model="jobForm.title" placeholder="Job Title" />
      <input v-model="jobForm.description" placeholder="Description" />
      <input v-model="jobForm.skills" placeholder="Skills" />
      <input v-model="jobForm.experience" placeholder="Experience" />
      <input v-model="jobForm.salary" placeholder="Salary" />
      <input v-model="jobForm.location" placeholder="Location" />

      <button @click="postJob">Post</button>
      <button class="cancel-btn" @click="showJobForm = false">Cancel</button>
    </div>

    <!-- Jobs List -->
    <div v-if="jobs.length > 0" class="job-list">
      <h3>Your Jobs</h3>

      <div v-for="job in jobs" :key="job.id" class="job-card">
        <p>
          <b>{{ job.title }}</b>
        </p>
        <p>{{ job.description }}</p>
        <p><b>Skills:</b> {{ job.skills }}</p>
        <p><b>Salary:</b> {{ job.salary }}</p>
        <p><b>Location:</b> {{ job.location }}</p>

        <button
          class="danger-btn"
          v-if="job.is_closed === false"
          @click="closeJob(job.id)"
        >
          Close Job
        </button>

        <button
          class="view-btn"
          v-if="job.is_closed === true"
          @click="openJob(job.id)"
        >
          Reopen Job
        </button>
        <button
          @click="$router.push(`/job/${job.id}/applicants`)"
          class="view-btn"
        >
          View Applicants
        </button>
        <p>
  <b>Status:</b>
  <span
    :style="{
      color: !job.is_approved ? 'orange' : job.is_closed ? 'red' : 'green',
    }"
  >
    {{ !job.is_approved ? "Pending" : job.is_closed ? "Closed" : "Open" }}
  </span>
</p>
      </div>
      
    </div>
    
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      showForm: false,
      showJobForm: false,
      company_data: null,
      profile: {
        company_name: "",
        industry: "",
        website: "",
        location: "",
        company_size: "",
      },
      jobForm: {
        title: "",
        description: "",
        skills: "",
        experience: "",
        salary: "",
        location: "",
        job_type: "Full-time",
      },
      jobs: [],
    };
  },

  methods: {
    submitProfile() {
      const token = localStorage.getItem("token");

      api
        .post("/company/create_profile", this.profile, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(() => {
          alert("Profile Created Successfully");
          this.showForm = false;
          this.fetch_company_profile(); // refresh
        })
        .catch((err) => {
          alert(err.response?.data?.message || "Profile creation failed");
        });
    },

    editProfile() {
      const token = localStorage.getItem("token");

      api
        .post("/edit_company_profile", this.profile, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(() => {
          alert("Profile Updated");
          this.showForm = false;
          this.fetch_company_profile();
        });
    },

    fetch_company_profile() {
      const token = localStorage.getItem("token");

      api
        .get("/get_company_profie", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.company_data = res.data;
        })
        .catch(() => {
          console.log("error getting profile");
        });
    },

    postJob() {
      const token = localStorage.getItem("token");

      api
        .post("/company/post_job", this.jobForm, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(() => {
          alert("Job posted");
          this.showJobForm = false;
          this.fetchJobs(); // refresh jobs
        })
        .catch((err) => {
          console.log("post the job");
          alert(err.response.data.message);
        });
    },

    fetchJobs() {
      const token = localStorage.getItem("token");

      api
        .get("/company/my_jobs", {
          headers: { Authorization: `Bearer ${token}` },
        })

        .then((res) => {
          this.jobs = res.data;
        })
        .catch(() => {
          console.log("error fetching jobs");
        });
    },

    closeJob(jobId) {
      console.log("close job hit");
      const token = localStorage.getItem("token");

      if (!confirm("Are you sure you want to close this job?")) return;

      api
        .post(
          `/company/close_job/${jobId}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then(() => {
          alert("Job closed");
          this.fetchJobs(); // refresh list
        })
        .catch((err) => {
          alert(err.response.message || "Error closing job");
        });
    },
    openJob(jobId) {
      console.log("open job hit");
      const token = localStorage.getItem("token");

      api
        .post(
          `/company/open_job/${jobId}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        )
        .then(() => {
          alert("Job reopened");
          this.fetchJobs();
        })
        .catch((err) => {
          alert(err.response?.data?.message || "Error reopening job");
        });
    },
  },

  mounted() {
    this.fetch_company_profile();
    this.fetchJobs();
  },
};
</script>

<style>
.main-box {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.create-btn {
  background: #4caf50;
  color: white;
  padding: 10px;
  margin: 10px 5px;
  border: none;
  cursor: pointer;
}

.form-box {
  margin-top: 20px;
  border: 1px solid #ccc;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.profile-box {
  margin-top: 20px;
  border: 1px solid #444;
  padding: 15px;
}

.job-card {
  border: 1px solid #555;
  padding: 10px;
  margin: 10px 0;
}

.cancel-btn {
  background: gray;
  color: white;
  padding: 8px;
}

.danger-btn {
  background: red;
  color: white;
  margin-right: 10px;
}

.view-btn {
  background: #2196f3;
  color: white;
}
</style>