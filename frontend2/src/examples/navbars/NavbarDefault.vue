<!-- DefaultNavbar.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark-daw py-3">
    <div class="container">
      <RouterLink
        class="navbar-brand text-light font-weight-bolder ms-sm-3"
        :to="{ name: 'presentation' }"
      >
        Airdrum System
      </RouterLink>
      <button
        class="navbar-toggler shadow-none ms-2"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navigation"
        aria-controls="navigation"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon mt-2">
          <span class="navbar-toggler-bar bar1"></span>
          <span class="navbar-toggler-bar bar2"></span>
          <span class="navbar-toggler-bar bar3"></span>
        </span>
      </button>
      <div class="collapse navbar-collapse w-100 pt-3 pb-2 py-lg-0" id="navigation">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item dropdown mx-2">
            <a
              class="nav-link d-flex align-items-center text-light dropdown-toggle"
              href="#"
              id="navbarDropdownMenuLink"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="fa fa-list me-2 opacity-8"></i>
              Paginas
            </a>
            <ul
              class="dropdown-menu dropdown-menu-dark border-0 shadow-sm"
              aria-labelledby="navbarDropdownMenuLink"
            >
              <li>
                <RouterLink
                  :to="{ name: 'about' }"
                  class="dropdown-item"
                >
                  Porque usar AirDrum?
                </RouterLink>
              </li>
              <li>
                <RouterLink
                  :to="{ name: 'interface' }"
                  class="dropdown-item"
                >
                  Prueba demo
                </RouterLink>
              </li>
            </ul>
          </li>

          <!-- Logout Button -->
          <li class="nav-item ms-3">
            <RouterLink
              :to="{ name: 'login' }"
              class="btn btn-logout d-flex align-items-center"
            >
              <i class="fa fa-sign-out-alt me-2"></i>
              Logout
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

.navbar {
  background: #2c2c2c !important;
  border-bottom: 1px solid #333;
}

.bg-dark-daw {
  background: #2c2c2c !important;
}

.navbar-brand {
  font-size: 16px;
}

.navbar-dark .navbar-nav .nav-link {
  color: #ccc;
  font-size: 14px;
  transition: color 0.2s;
}

.navbar-dark .navbar-nav .nav-link:hover {
  color: #fff;
}

.dropdown-menu {
  background: #2c2c2c;
  border-radius: 4px;
  min-width: 180px;
  padding: 0.5rem 0;
}

.dropdown-menu .dropdown-item {
  color: #ccc;
  font-size: 13px;
  transition: background 0.2s, color 0.2s;
}

.dropdown-menu .dropdown-item:hover {
  background: #3a3a3a;
  color: #fff;
}

.navbar-toggler {
  border:none;
}

.navbar-toggler:hover .navbar-toggler-icon {
  filter: brightness(1.2);
}

.navbar-toggler-icon {
  color: #ccc;
}

/* Logout Button Styles */
.btn-logout {
  background: #e74c3c;
  color: #fff;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  transition: background 0.2s;
}

.btn-logout:hover {
  background: #c0392b;
  text-decoration: none;
  color: #fff;
}
</style>
