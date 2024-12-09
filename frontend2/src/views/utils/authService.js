// src/services/authService.js

import api from './api';

const authService = {
  register: async (name, email, password) => {
    try {
      const response = await api.post('tienda/user/', {
        name,
        email,
        password,
        is_active: true,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  login: async (email, password) => {
    try {
      const response = await api.post('user/token/', {
        email,
        password,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getUserData: async () => {
    try {
      const response = await api.get('user/me/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  fetchAllUsers: async () => {
    try {
      const response = await api.get('tienda/user/');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    localStorage.removeItem('is_staff');
  },
};

export default authService;
