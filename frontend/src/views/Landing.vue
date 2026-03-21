<template>
  <div class="main">

    <!-- Header -->
    <div class="header">
      <h1>Placement Portal</h1>
      <p>Empowering Students for Better Careers</p>
    </div>

    

    <!-- Banner -->
    <div class="banner">
      <img src="https://images.unsplash.com/photo-1523240795612-9a054b0db644" />
    </div>

    <!-- About Section -->
    <div class="about">
      <h2>About Us</h2>
      <p>
        Our Placement Cell organizes campus drives, career guidance sessions,
        aptitude training, and interview preparation programs. Every year,
        hundreds of students get placed in reputed companies.
      </p>
    </div>

    <!-- Companies -->
    <div class="companies">
      <h2>Top Recruiting Companies</h2>

      <div class="company-list">
        <div>
          <img src="https://images.unsplash.com/photo-1492724441997-5dc865305da7" />
          <p>ABC Technologies</p>
        </div>

        <div>
          <img src="https://images.unsplash.com/photo-1551434678-e076c223a692" />
          <p>FutureSoft Pvt Ltd</p>
        </div>

        <div>
          <img src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d" />
          <p>NextGen Solutions</p>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats">
      <h2>Placement Statistics</h2>
      <p>Total Students Placed: 320+</p>
      <p>Highest Package: 12 LPA</p>
      <p>Average Package: 5.5 LPA</p>
    </div>

    <!-- Footer -->
    <div class="footer">
      © 2026 Placement Portal | All Rights Reserved
    </div>

  </div>
</template>

<script>
export default {
  name: "App"
}
</script>

<style>
.main {
  margin: 0;
  font-family: Arial;
  background-color: #f3e2d4;
}

.header {
  background-color: #5a3825;
  color: white;
  text-align: center;
  padding: 20px;
}

.nav {
  background-color: #c47a44;
  text-align: center;
  padding: 12px;
}

.nav span {
  margin: 15px;
  color: white;
  cursor: pointer;
}

.banner {
  text-align: center;
  margin-top: 20px;
}

.banner img {
  width: 80%;
  border-radius: 8px;
}

.about {
  padding: 40px;
  text-align: center;
}

.companies {
  background-color: #ead1bc;
  padding: 40px;
  text-align: center;
}

.company-list {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 20px;
}

.company-list img {
  width: 200px;
  height: 130px;
  object-fit: cover;
  border-radius: 6px;
}

.stats {
  padding: 40px;
  text-align: center;
}

.footer {
  background-color: #5a3825;
  color: white;
  text-align: center;
  padding: 15px;
}
</style>