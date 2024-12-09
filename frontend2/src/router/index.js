// src/router.js

import { createRouter, createWebHistory } from "vue-router";
import PresentationView from "../views/Presentation/PresentationView.vue";
import AboutView from "../views/LandingPages/AboutUs/AboutView.vue";
import InterfaceView from "../views/Interface.vue";
import Login from "../views/Login.vue"; // Import Login component
import Register from "../views/Register.vue"; // Import Register component
import Admin from "../views/Admin.vue"; // Import Admin component (to be created)
import Dashboard from "../views/Dashboard.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "presentation",
      component: PresentationView,
    },
    {
      path: "/pages/landing-pages/about-us",
      name: "about",
      component: AboutView,
    },
    {
      path: "/pages/interface",
      name: "interface",
      component: InterfaceView,
    },
    {
      path: "/login",
      name: "login",
      component: Login,
    },
    {
      path: "/register",
      name: "register",
      component: Register,
    },
    {
      path: "/admin",
      name: "admin",
      component: Admin,
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: Dashboard,
    },
    // Add more routes as needed
  ],
});

// Navigation Guard to protect routes
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');
  const isAdmin = localStorage.getItem('is_staff') === 'true'; // localStorage stores everything as strings

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // Redirect to login if not authenticated
  } else if (to.meta.requiresAdmin && !isAdmin) {
    next('/dashboard'); // Redirect to dashboard if not admin
  } else {
    next(); // Proceed to the route
  }
});

export default router;
