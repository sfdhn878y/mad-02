<template>
  <button v-if="!company_data" class="create-btn" @click="showForm = true">+ New Profile</button>
    <button v-if="company_data" class="create-btn" @click="showForm = true">+ Update Profile</button>


  <div
    v-if="showForm"
    style="margin-top: 20px; border: 1px solid #ccc; padding: 20px"
  >
    <h3>Create Company Profile</h3>

    <input v-model="profile.company_name" placeholder="Company Name" /><br /><br />
    <input v-model="profile.industry" placeholder="Industry" /><br /><br />
    <input v-model="profile.website" placeholder="Website" /><br /><br />
    <input v-model="profile.location" placeholder="Location" /><br /><br />
    <input v-model="profile.company_size" placeholder="Company Size" /><br /><br />
    <data value=""></data>

    <button  v-if="!company_data"  @click="submitProfile" >Submit</button>
    <button  v-if="company_data"  @click="editProfile"  >Update Profile</button>
  </div>
  <div>
    <div v-if="company_data" style="margin-top:20px; border:1px solid #444; padding:15px;">
      <h3>Company Profile</h3>

      <p><b>Name:</b> {{ company_data.company_name }}</p>
      <p><b>Industry:</b> {{ company_data.industry }}</p>
      <p><b>Website:</b> {{ company_data.website }}</p>
      <p><b>Location:</b> {{ company_data.location }}</p>
      <p><b>Size:</b> {{ company_data.company_size }}</p>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      showForm: false,
      company_data:null,
      profile: {
        company_name: "",
        industry: "",
        website: "",
        location: "",
        company_size: "",
        
        
      }
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
        })
        .catch((err) => {
          alert(err.response?.data?.message || "Profile creation failed");
        });
    },
    editProfile(){
        const token = localStorage.getItem("token");
        api.post('/edit_company_profile',this.profile,{
          headers: { Authorization: `Bearer ${token}` },
          
        })
    },
    fetch_company_profile(){
      const token = localStorage.getItem("token");

      api.get('/get_company_profie',{
         headers: { Authorization: `Bearer ${token}` },
      })
      .then((res)=>{
        this.company_data = res.data

      }
    )
    .catch(()=>{
      console.log("error getting profile ")
    })
    }
    
  },
    mounted() {
    this.fetch_company_profile();
  }
}
</script>