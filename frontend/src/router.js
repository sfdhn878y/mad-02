import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    component: () => import("./views/Landing.vue"),
  },
  {
    path: "/login",
    component: () => import("./views/Login.vue"),
  },
  {
    path: "/register",
    component: () => import("./views/Reg.vue"),
  },

 {
    path: "/company_dashboard",
    component: () => import("./views/Company.vue"),
    
  },
 {
    path: "/student-dashboard",
    component: () => import("./views/Student.vue"),
    
  },
  {
      path: "/company/:id",
      component: () => import("./views/CompanyDetail.vue"),
  },
   {
  path: "/job/:jobId/applicants",
  component: () => import("./views/ViewApplicant.vue"),
},
   {
  path: "/admin",
  component: () => import("./views/Admin.vue"),
},
{
  path: "/admin/company/:id",
  component: () => import("./views/CompanyDetailAdmin.vue"),
},

{
  path: "/admin/student/:id",
  component: () => import("./views/StudentDetail.vue"),
},

{
  path: "/admin/job/:id",
  component: () => import("./views/AdminJobDetail.vue")
}
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;