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

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;