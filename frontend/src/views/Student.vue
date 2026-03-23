<template>
  <div class="main-box">
    <div class="welcome-bar">
      <span>Welcome {{ user_name }}</span>
      <div class="top-links">
        <a @click="showProfileForm = true">edit profile</a> |
      
     
      </div>
    </div>

    <!-- Edit Profile Form -->
    <div v-if="showProfileForm" class="form-box">
      <h3>{{ student_profile ? "Update Profile" : "Create Profile" }}</h3>

      <input v-model="profileForm.department" placeholder="Department" />
      <input v-model="profileForm.year" placeholder="Year" type="number" />
      <input v-model="profileForm.cgpa" placeholder="CGPA" type="number" step="0.01" />
      <input v-model="profileForm.skills" placeholder="Skills (comma-separated)" />

      <button v-if="!student_profile" @click="submitProfile">Submit</button>
      <button v-if="student_profile" @click="updateProfile">Update Profile</button>
      <button class="cancel-btn" @click="showProfileForm = false">Cancel</button>
    </div>

    <!-- Profile Display -->
    <div v-if="student_profile" class="profile-box">
      <h3>My Profile</h3>
      <p><b>Department:</b> {{ student_profile.department }}</p>
      <p><b>Year:</b> {{ student_profile.year }}</p>
      <p><b>CGPA:</b> {{ student_profile.cgpa }}</p>
      <p><b>Skills:</b> {{ student_profile.skills }}</p>
      <p><b>Placement Status:</b> {{ student_profile.placement_status }}</p>
    </div>

    <!-- Organizations Section -->
    <div class="section-box">
      <h3>Organizations</h3>

      <div v-for="company in companies" :key="company.id" class="list-row">
        <span>{{ company.company_name }}</span>
        <button class="view-btn" @click="$router.push(`/company/${company.id}`)">view details</button>
      </div>

      <p v-if="companies.length === 0" class="empty-msg">No companies available.</p>
    </div>

    <!-- Applied Drives Section -->
    <div class="section-box">
      <h3>Applied Drives</h3>

      <table v-if="applications.length > 0" class="drives-table">
        <thead>
          <tr>
            <th>Sr No.</th>
            <th>Drive Name</th>
            <th>Company</th>
            <th>Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(app, index) in applications" :key="app.id">
            <td>{{ index + 1 }}.</td>
            <td>{{ app.job_title }}</td>
            <td>{{ app.company_name }}</td>
            <td>{{ app.applied_at }}</td>
            <td>{{ app.status }}</td>
            <td>
              <button class="view-btn" @click="viewApplication(app)">view details</button>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-if="applications.length === 0" class="empty-msg">No applications yet.</p>
    </div>

    <!-- Application Detail Modal -->
    <div v-if="selectedApplication" class="modal-overlay" @click.self="selectedApplication = null">
      <div class="modal-box">

        <div class="modal-header">
          <h3>Application Details</h3>
          <button class="close-btn" @click="selectedApplication = null">✕</button>
        </div>

        <p><b>Job:</b> {{ selectedApplication.job_title }}</p>
        <p><b>Company:</b> {{ selectedApplication.company_name }}</p>
        <p><b>Status:</b> {{ selectedApplication.status }}</p>
        <p><b>Applied At:</b> {{ selectedApplication.applied_at }}</p>
        <p v-if="selectedApplication.remarks"><b>Remarks:</b> {{ selectedApplication.remarks }}</p>
        <p v-if="selectedApplication.interview_datetime"><b>Interview:</b> {{ selectedApplication.interview_datetime }}</p>
        <p v-if="selectedApplication.interview_mode"><b>Mode:</b> {{ selectedApplication.interview_mode }}</p>
        <p v-if="selectedApplication.interview_link"><b>Link:</b> {{ selectedApplication.interview_link }}</p>
        <p v-if="selectedApplication.interview_location"><b>Venue:</b> {{ selectedApplication.interview_location }}</p>
        <p v-if="selectedApplication.feedback"><b>Feedback:</b> {{ selectedApplication.feedback }}</p>

      </div>
    </div>

  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      user_name: "",
      showProfileForm: false,
      showHistory: false,
      student_profile: null,
      profileForm: {
        department: "",
        year: "",
        cgpa: "",
        skills: "",
      },
      companies: [],
      applications: [],
      selectedApplication: null,
    };
  },

  methods: {
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },

    submitProfile() {
      const token = localStorage.getItem("token");

      api
        .post("/student/create_profile", this.profileForm, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(() => {
          alert("Profile Created Successfully");
          this.showProfileForm = false;
          this.fetchStudentProfile();
        })
        .catch((err) => {
          alert(err.response?.data?.message || "Profile creation failed");
        });
    },

    updateProfile() {
      const token = localStorage.getItem("token");

      api
        .post("/student/edit_profile", this.profileForm, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(() => {
          alert("Profile Updated");
          this.showProfileForm = false;
          this.fetchStudentProfile();
        })
        .catch((err) => {
          alert(err.response?.data?.message || "Update failed");
        });
    },

    fetchStudentProfile() {
      const token = localStorage.getItem("token");

      api
        .get("/student/get_profile", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.student_profile = res.data;
          this.user_name = res.data.user_name || "";
          this.profileForm = {
            department: res.data.department || "",
            year: res.data.year || "",
            cgpa: res.data.cgpa || "",
            skills: res.data.skills || "",
          };
        })
        .catch(() => {
          console.log("No student profile found");
        });
    },

    fetchCompanies() {
      const token = localStorage.getItem("token");

      api
        .get("/student/companies", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.companies = res.data;
        })
        .catch(() => {
          console.log("Error fetching companies");
        });
    },

    fetchApplications() {
      const token = localStorage.getItem("token");

      api
        .get("/student/my_applications", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => {
          this.applications = res.data;
        })
        .catch(() => {
          console.log("Error fetching applications");
        });
    },

    viewApplication(app) {
      this.selectedApplication = app;
    },
  },

  mounted() {
    this.fetchStudentProfile();
    this.fetchCompanies();
    this.fetchApplications();
  },
};
</script>

<style>
.main-box {
  max-width: 700px;
  margin: auto;
  padding: 20px;
}

.welcome-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  padding: 10px 15px;
  margin-bottom: 20px;
  font-weight: bold;
}

.top-links a {
  color: #2196f3;
  cursor: pointer;
  font-weight: normal;
  font-size: 14px;
  margin: 0 2px;
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

.list-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ddd;
  padding: 8px 12px;
  margin-bottom: 8px;
}

.drives-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.drives-table th,
.drives-table td {
  border: 1px solid #ddd;
  padding: 8px 10px;
  text-align: left;
}

.drives-table th {
  background: #f5f5f5;
}

.form-box {
  margin-top: 20px;
  border: 1px solid #ccc;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.form-box input {
  padding: 8px;
  border: 1px solid #ccc;
}

.profile-box {
  border: 1px solid #444;
  padding: 15px;
  margin-bottom: 20px;
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
  border: none;
  cursor: pointer;
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

/* Application modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 60px;
  z-index: 999;
}

.modal-box {
  background: white;
  width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  padding: 25px;
  border: 1px solid #ccc;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #555;
}
</style>