<template>
  <div class="page">
    <div class="box">
      <h2>Login</h2>

      <form @submit.prevent="loginUser">
        <label>Email</label>
        <input type="email" v-model="email" required />

        <label>Password</label>
        <input type="password" v-model="password" required />

        <button>Login</button>
      </form>

      <p class="link">
        New user?
        <router-link to="/register">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {

      email: "",      // user email input
      password: ""    // user password input

    };
  },

  methods: {
    loginUser() {
      // basic check
      if (!this.email || !this.password) {
        alert("Please enter email and password");
        return;
      }
      // send login request to backend
      api.post("/login", {
        email: this.email,
        password: this.password
      })
      .then(response => {
        console.log("login success", response.data);

        // ✅ SAVE TOKEN
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("role", response.data.role);
        console.log(response.data.token);
        

        if (response.data.role === "company") {
          this.$router.push("/company_dashboard");
        } else if (response.data.role === "student") {
          this.$router.push("/student-dashboard");
        } else if (response.data.role === "admin") {
          this.$router.push("/admin");
        }
      })
      .catch(error => {
        console.log("login error", error);

        // backend sent an error message
        if (error.response && error.response.data) {
          alert(error.response.data.msg);
        } 
        else {
          // server not running / network issue
          alert("Server not reachable. Is Flask running?");
        }
      });
    }
  }
};
</script>
<style scoped>
/* Full screen background */
.page {
  min-height: 100vh;
  width: 100%;
  background-color: #f3e2d4;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Login card */
.box {
  width: 380px;
  background: #ffffff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(90, 56, 37, 0.2);
  border-top: 6px solid #c47a44;
  font-family: Arial, sans-serif;
}

/* Title */
h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #5a3825;
}

/* Labels */
label {
  color: #5a3825;
  display: block;
  margin-top: 14px;
  font-size: 14px;
}

/* Inputs */
input {
  width: 100%;
  padding: 10px;
  margin-top: 6px;
  border-radius: 6px;
  border: 1px solid #d7b49e;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: #c47a44;
}

/* Button */
button {
  width: 100%;
  margin-top: 24px;
  padding: 10px;
  background-color: #5a3825;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

button:hover {
  background-color: #c47a44;
}

/* Link */
.link {
  margin-top: 18px;
  text-align: center;
  font-size: 14px;
  color: #5a3825;
}

.link a {
  color: #c47a44;
  text-decoration: none;
}

.link a:hover {
  text-decoration: underline;
}
</style>