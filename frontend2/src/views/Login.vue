<!-- src/views/Login.vue -->

<template>
    <div class="container">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="loguearUsuario">
        <input
          type="email"
          v-model="email"
          placeholder="Correo electrónico"
          required
        />
        <input
          type="password"
          v-model="password"
          placeholder="Contraseña"
          required
        />
        <button type="submit">Iniciar Sesión</button>
      </form>
      <div class="link">
        <p>
          ¿No tienes una cuenta?
          <router-link to="/register">Regístrate aquí</router-link>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import authService from './utils/authService';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'Login',
    data() {
      return {
        email: '',
        password: '',
        error: '',
      };
    },
    setup() {
      const router = useRouter();
      return { router };
    },
    methods: {
      async loguearUsuario() {
        try {
          const data = await authService.login(this.email, this.password);
          // Store relevant data in localStorage
          localStorage.setItem('email', data.email);
          localStorage.setItem('token', data.token);
          localStorage.setItem('is_staff', data.is_staff); // Store is_staff in localStorage
  
          // Redirect based on user role
          if (data.is_staff) {
            this.$router.push('/admin'); // Redirect to admin if staff
          } else {
            this.$router.push('/pages/interface'); // Redirect to client if not staff
          }
        } catch (error) {
          console.error('Error en el login:', error);
          if (error.response && error.response.data && error.response.data.detail) {
            this.error = error.response.data.detail;
          } else {
            this.error = 'Error en el login. Por favor, intenta nuevamente.';
          }
          alert(this.error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
.LoginContainer {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #71a1d0;
}
  .container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 100%;
  }
  h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  form {
    display: flex;
    flex-direction: column;
  }
  input {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  button {
    padding: 10px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  button:hover {
    background-color: #218838;
  }
  .link {
    text-align: center;
    margin-top: 10px;
  }
  .link a {
    color: #007bff;
    text-decoration: none;
  }
  .link a:hover {
    text-decoration: underline;
  }
  </style>
  