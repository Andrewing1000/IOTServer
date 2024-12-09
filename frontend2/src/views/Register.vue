<!-- src/views/Register.vue -->

<template>
    <div class="container">
      <h2>Registro de Usuario</h2>
      <form @submit.prevent="registrarUsuario">
        <input
          type="text"
          v-model="name"
          placeholder="Nombre"
          required
        />
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
        <button type="submit">Registrarse</button>
      </form>
      <div class="link">
        <p>
          ¿Ya tienes una cuenta?
          <router-link to="/login">Inicia sesión aquí</router-link>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import authService from './utils/authService';
  
  export default {
    name: 'Register',
    data() {
      return {
        name: '',
        email: '',
        password: '',
        error: '',
      };
    },
    methods: {
      async registrarUsuario() {
        try {
          await authService.register(this.name, this.email, this.password);
          alert('Usuario registrado exitosamente');
          this.$router.push('/login'); // Redirect to login after successful registration
        } catch (error) {
          console.error('Error en el registro:', error);
          if (error.response && error.response.data && error.response.data.detail) {
            this.error = error.response.data.detail;
          } else {
            this.error = 'Error en el registro. Por favor, intenta nuevamente.';
          }
          alert(this.error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
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
  