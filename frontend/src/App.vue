<template>
  <div class="main">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo">Placement Portal</div>

      <div class="nav-links">
        <router-link to="/">Home</router-link>
        <div v-if="!checkJWT()">
          <router-link to="/login" class="btn">Login</router-link>
          <router-link to="/register" class="btn">Register</router-link>
        </div>
        <div v-if="checkJWT()">
          <button class="btn" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <!-- Page Content -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",

  methods: {
    checkJWT() {
      const token = localStorage.getItem("token");
      if (token) {
        return true;
      }
      return false;
    },
    logout() {
      localStorage.removeItem("token");
      this.token = null;
      this.$router.push("/login");
    },
  },
};
</script>

<style>
.main {
  margin: 0;
  font-family: Arial;
  background-color: #f3e2d4;
}

/* Navbar */
.navbar {
  background-color: #5a3825;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
}

.logo {
  font-size: 15px;
}

.nav-links a {
  margin-left: 20px;
  text-decoration: none;
  color: white;
}

.btn {
  background-color: #c47a44;
  padding: 6px 12px;
  border-radius: 4px;
}

/* Router active link */
.router-link-active {
  font-weight: bold;
}
</style>