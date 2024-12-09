<!-- src/views/Admin.vue -->

<template>
    <div class="dashboard-container">
      <button class="logout-button" @click="logout">Cerrar Sesión</button>
      <h1>Dashboard de Admin - Estado de las vaquetas</h1>
  
      <div class="input-container">
        <label for="filter-pk">Filtrar por PK de usuario:</label>
        <select id="filter-pk" v-model="currentPk">
          <option value="">Todos</option>
          <option v-for="usuario in usuarios" :key="usuario.pk" :value="usuario.pk">
            PK: {{ usuario.pk }} - {{ usuario.email }}
          </option>
        </select>
  
        <label for="filter-ip">Filtrar por IP de usuario:</label>
        <select id="filter-ip" v-model="currentIp">
          <option value="">Todos</option>
          <option v-for="usuario in usuarios" :key="usuario.pk" :value="usuario.ip">
            {{ usuario.ip ? `IP: ${usuario.ip}` : 'IP: ""' }}
          </option>
        </select>
      </div>
  
      <!-- Actividad de Usuarios Section -->
      <div class="grafico">
        <h2>Actividad de Usuarios</h2>
        <div id="grafico_actividad" style="width:100%;height:300px;"></div>
      </div> 
  
      <!-- DrumHit Section -->
      <div class="fibonacii">
        <h2>DrumHit</h2>
        <div class="input-container">
          <button class="fibonacci-button delete" @click="deleteFibonacci">Eliminar Todos</button>
        </div>
        <div id="grafico_fibonacii" style="width:100%;height:300px;"></div>
      </div>
    </div>
  </template>
  
  <script>
  import api from './utils/api';
  import Plotly from 'plotly.js-dist-min';
  
  export default {
    name: 'Admin',
    data() {
      return {
        usuarios: [],
        currentPk: '',
        currentIp: '',
        activityDataFull: [],
        fibonacciDataFull: [],
        pollingInterval: null,
      };
    },
    methods: {
      async logout() {
        localStorage.clear();
        this.$router.push('/login');
      },
  
      async obtenerUsuarios() {
        try {
          const response = await api.get('tienda/user/');
          this.usuarios = response.data;
        } catch (error) {
          console.error('Error al obtener usuarios:', error);
          alert('Error al obtener usuarios.');
        }
      },
  
      async obtenerSeries() {
        try {
          const response = await api.get('tienda/activity/');
          this.activityDataFull = response.data;
          this.generarGraficoActividad('grafico_actividad', this.activityDataFull, 'Actividad de usuarios');
        } catch (error) {
          console.error('Error al obtener las series:', error);
        }
      },
  
      async obtenerFibonacii() {
        try {
          const response = await api.get('tienda/drum/');
          this.fibonacciDataFull = response.data;
          this.generarGraficoFibonacii(this.fibonacciDataFull);
        } catch (error) {
          console.error('Error al obtener Fibonacii:', error);
        }
      },
  
      async deleteFibonacci() {
        if (!confirm('¿Está seguro de que desea eliminar todas las entradas de Fibonacii?')) {
          return;
        }
  
        try {
          const response = await api.delete('tienda/drum/1/');
          if (response.status === 204 || response.status === 200) {
            await this.obtenerFibonacii();
            alert('Todas las entradas de Fibonacii han sido eliminadas.');
          } else {
            throw new Error('Error al eliminar entradas de Fibonacii.');
          }
        } catch (error) {
          console.error('Error al eliminar Fibonacii:', error);
          alert('Error al eliminar Fibonacii.');
        }
      },
  
      generarGraficoActividad(id, data, titulo) {
        const labels = data.map(item => item.ip);
        const activity = data.map(item => item.actividad);
  
        const layout = {
          title: titulo,
          xaxis: { title: 'IP' },
          yaxis: { title: '#Registros' },
          showlegend: true,
        };
  
        const trace1 = {
          x: labels,
          y: activity,
          type: "bar",
          name: "Actividad",
        };
  
        Plotly.react(id, [trace1], layout);
      },
  
      generarGraficoFibonacii(data, titulo = 'Toques') {
        const ips = new Set(data.map(item => item.ip));
        let time = data.map(item => item.time);
        const fibonacciValues = data.map(item => item.value);
        let first = time[0];
        time = time.map(item => (item - first) / 60);
  
        const layout = {
          title: titulo,
          xaxis: {
            title: 'Tiempo',
            range: [0, 4],
          },
          yaxis: { title: 'Intensidad del golpe' },
          showlegend: true
        };
  
        const traces = [];
        ips.forEach(ip => {
          const filteredData = data.filter(item => item.ip === ip);
          const t = filteredData.map(item => (item.time - first) / 60);
          const v = filteredData.map(item => item.value);
          traces.push({
            x: t,
            y: v,
            mode: 'lines+markers',
            name: `${ip}`
          });
        });
  
        Plotly.react('grafico_fibonacii', traces, layout);
      },
  
      aplicarFiltros() {
        const pk = this.currentPk;
        const ip = this.currentIp;
  
        const activityDataFiltered = this.activityDataFull.filter(item =>
          (!pk || item.user.pk == pk) && (!ip || item.user.ip == ip)
        );
  
        const fibonacciDataFiltered = this.fibonacciDataFull.filter(item =>
          (!pk || (item.ip && this.usuarios.find(u => u.pk == pk && u.ip == item.ip))) &&
          (!ip || item.ip == ip)
        );
  
        this.generarGraficoActividad('grafico_actividad', activityDataFiltered, 'Actividad de usuarios');
        this.generarGraficoFibonacii(fibonacciDataFiltered);
      },
    },
    watch: {
      currentPk() {
        this.aplicarFiltros();
      },
      currentIp() {
        this.aplicarFiltros();
      }
    },
    mounted() {
      this.obtenerUsuarios();
      this.obtenerSeries();
      this.obtenerFibonacii();
  
      this.pollingInterval = setInterval(() => {
        this.obtenerSeries();
        this.obtenerFibonacii();
        this.aplicarFiltros();
      }, 500);
    },
    beforeUnmount() {
      clearInterval(this.pollingInterval);
    }
  };
  </script>
  
  <style scoped>
  .dashboard-container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    max-width: 1200px;
    width: 100%;
    margin: 20px auto;
  }
  
  h1, h2 {
    text-align: center;
    color: #333;
  }
  
  .grafico, .fibonacii {
    margin: 20px 0;
  }
  
  .logout-button {
    background-color: #dc3545;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-bottom: 20px;
  }
  
  .logout-button:hover {
    background-color: #c82333;
  }
  
  .input-container {
    margin-bottom: 20px;
    text-align: center;
  }
  
  .input-container select, .fibonacci-input {
    padding: 10px;
    width: 150px;
    margin-right: 10px;
  }
  
  .input-container button, .fibonacci-button {
    padding: 10px 20px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .input-container button:hover, .fibonacci-button:hover {
    background-color: #218838;
  }
  
  .fibonacci-button.delete {
    background-color: #dc3545;
  }
  
  .fibonacci-button.delete:hover {
    background-color: #c82333;
  }
  </style>
  