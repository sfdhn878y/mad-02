<template>
  <div class="main-box">
    <h2>Applicants</h2>

    <div v-if="applicants.length === 0">
      No applicants yet 😴
    </div>

    <!-- Applicants List -->
    <div
      v-for="app in applicants"
      :key="app.application_id"
      class="card"
    >
      <p><b>Name:</b> {{ app.name }}</p>
      <p><b>Email:</b> {{ app.email }}</p>
      <p><b>Phone:</b> {{ app.phone }}</p>
      <p><b>Skills:</b> {{ app.skills }}</p>
      <p><b>CGPA:</b> {{ app.cgpa }}</p>
      <p><b>Status:</b> {{ app.status }}</p>

      <a :href="app.resume" target="_blank">View Resume</a>

      <br /><br />

      <!-- Interview Details -->
      <div v-if="app.status === 'shortlist' && app.interview_datetime">
        <p>
          <b>Interview Date:</b>
          {{ formatDate(app.interview_datetime) }}
        </p>

        <p>
          <b>Interview Link:</b>
          <a :href="app.interview_link" target="_blank">
            Join Interview
          </a>
        </p>
      </div>

      <!-- Offer Letter -->
      <div v-if="app.status === 'select' && app.offer_letter">
        <p><b>Offer Letter:</b></p>
        <a :href="app.offer_letter" target="_blank">
          View Offer Letter
        </a>
      </div>

      <br />

      <!-- Action Buttons -->
      <button
        @click="openShortlist(app)"
        :disabled="app.status === 'select'"
      >
        Shortlist
      </button>

      <button
        @click="openReject(app)"
        :disabled="app.status === 'select'"
      >
        Reject
      </button>

      <button
        @click="openSelect(app)"
        :disabled="app.status === 'select'"
      >
        Select
      </button>
    </div>

    <!-- MODAL -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>{{ modalTitle }}</h3>

        <!-- Shortlist -->
        <div v-if="actionType === 'shortlist'">
          <input
            type="datetime-local"
            v-model="form.interview_datetime"
          />
          <input
            type="text"
            placeholder="Meet Link"
            v-model="form.interview_link"
          />
        </div>

        <!-- Reject -->
        <div v-if="actionType === 'reject'">
          <textarea
            placeholder="Provide feedback..."
            v-model="form.feedback"
          ></textarea>
        </div>

        <!-- Select -->
        <div v-if="actionType === 'select'">
          <input type="file" @change="handleFileUpload" />
        </div>

        <br />

        <button @click="submitAction">Submit</button>
        <button @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      applicants: [],
      showModal: false,
      actionType: "",
      selectedApp: null,
      modalTitle: "",
      form: {
        interview_datetime: "",
        interview_link: "",
        feedback: "",
        offer_letter: null,
      },
    };
  },

  methods: {
    formatDate(date) {
      if (!date) return "";

      const d = new Date(date);

      return d.toLocaleString("en-IN", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

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

    openShortlist(app) {
      this.actionType = "shortlist";
      this.modalTitle = "Schedule Interview";
      this.selectedApp = app;
      this.showModal = true;
    },

    openReject(app) {
      this.actionType = "reject";
      this.modalTitle = "Provide Feedback";
      this.selectedApp = app;
      this.showModal = true;
    },

    openSelect(app) {
      this.actionType = "select";
      this.modalTitle = "Upload Offer Letter";
      this.selectedApp = app;
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.resetForm();
    },

    resetForm() {
      this.form = {
        interview_datetime: "",
        interview_link: "",
        feedback: "",
        offer_letter: null,
      };
    },

    handleFileUpload(e) {
      this.form.offer_letter = e.target.files[0];
    },

    submitAction() {
      const token = localStorage.getItem("token");
      const id = this.selectedApp.application_id;

      const formData = new FormData();
      formData.append("status", this.actionType);

      if (this.actionType === "shortlist") {
        formData.append("interview_datetime", this.form.interview_datetime);
        formData.append("interview_link", this.form.interview_link);
      }

      if (this.actionType === "reject") {
        formData.append("feedback", this.form.feedback);
      }

      if (this.actionType === "select") {
        formData.append("offer_letter", this.form.offer_letter);
      }

      api
        .put(`/company/application/${id}/status`, formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        })
        .then(() => {
          // update local status
          this.selectedApp.status = this.actionType;

          // refresh full list from backend
          this.fetchApplicants();

          this.closeModal();
        })
        .catch(() => {
          alert("Update failed");
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

button {
  margin-right: 8px;
  padding: 6px 12px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  width: 400px;
  border-radius: 8px;
}
</style>