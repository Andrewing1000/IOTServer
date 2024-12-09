<!-- src/views/Admin.vue -->

<template>
    <div class="dashboard-container">
      <button class="logout-button" @click="logout">Cerrar Sesión</button>
      <h1>Dashboard de Admin - Estado de las vaquetas</h1>

      <div>
    <h1>Tracks</h1>
    <button @click="loadTracks">Cargar Tracks</button>
    <ul v-if="tracks.length">
      <li v-for="track in tracks" :key="track.id">
        {{ track.name }}
        <button @click="decodeTrackFile(track.file)">Decodificar y Graficar</button>
      </li>
    </ul>

    <div v-if="decodedData && decodedData.length">
      <h2>Datos Decodificados</h2>
      <table border="1">
        <tr><th>Tiempo</th><th>Vol</th><th>Sound_ID</th></tr>
        <tr v-for="(row,i) in decodedData" :key="i">
          <td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td>
        </tr>
      </table>
    </div>

    <!-- Contenedor para la gráfica -->
    <div ref="chartDiv" style="width:600px; height:400px; margin-top:20px;"></div>
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
        tracks: [],
        decodedData: []
      };
    },
    methods: {
      async logout() {
        localStorage.clear();
        this.$router.push('/login');
      },
      async loadTracks() {
        try {
          const response = await api.get('http://localhost:8080/airdrum/track/');
          this.tracks = response.data;
        } catch (error) {
          console.error('Error loading tracks:', error);
        }
      },
      async decodeTrackFile(fileUrl) {
        this.decodedData = [];
        try {
          const response = await fetch(fileUrl);
          const arrayBuffer = await response.arrayBuffer();
          const dataView = new DataView(arrayBuffer);

          let offset = 0;
          const count = dataView.getUint32(offset, false);
          offset += 4;

          const data = [];
          for (let i = 0; i < count; i++) {
            const time = dataView.getFloat32(offset, false); 
            offset += 4;
            const vol = dataView.getFloat32(offset, false);
            offset += 4;
            const sound_id = dataView.getUint32(offset, false);
            offset += 4;
            data.push([time, vol, sound_id]);
          }

          this.decodedData = data;
          this.plotData();
        } catch (error) {
          console.error('Error decoding track file:', error);
        }
      },
      plotData() {
        // Extraer arrays de tiempo y sound_id
        const times = this.decodedData.map(d => d[0]);
        const sound_ids = this.decodedData.map(d => d[2]);

        const trace = {
          x: times,
          y: sound_ids,
          mode: 'lines+markers',
          type: 'scatter',
          name: 'Track Data',
          marker: { size: 6, color: 'blue' }
        };

        const layout = {
          title: 'Time vs Sound_ID',
          xaxis: { title: 'Tiempo (seg)' },
          yaxis: { title: 'Sound_ID' }
        };

        Plotly.newPlot(this.$refs.chartDiv, [trace], layout);
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
    },
  };
  </script>
  
  <style scoped>
  .dashboard-container {
  background: #1e1e1e; /* Fondo oscuro simulando un estudio con iluminación baja */
  color: #f5f5f5;
  font-family: 'Roboto', sans-serif;
  padding: 20px;
  min-height: 100vh;
}

/* Botón de cerrar sesión */
.logout-button {
  background: #c0392b;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  float: right;
  margin: 10px;
  transition: background 0.3s;
}

.logout-button:hover {
  background: #e74c3c;
}

/* Títulos */
h1, h2 {
  margin-top: 0;
  font-weight: 300;
  color: #f5f5f5;
}

/* Contenedor principal */
.dashboard-container > h1 {
  margin-bottom: 30px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

/* Botones de acción */
button {
  background: #3a3a3a;
  border: none;
  color: #f5f5f5;
  padding: 8px 12px;
  border-radius: 4px;
  margin: 5px 0;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 14px;
}

button:hover {
  background: #505050;
}

/* Sección de Tracks */
ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 20px;
}

li {
  background: #2a2a2a;
  margin-bottom: 5px;
  padding: 10px;
  border-radius: 4px;
}

li:hover {
  background: #333333;
}

/* Tablas */
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background: #2a2a2a;
  color: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
}

th, td {
  border: 1px solid #3a3a3a;
  padding: 10px;
  text-align: left;
}

th {
  background: #1a1a1a;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 1px;
}

tr:nth-child(even) {
  background: #252525;
}

/* Gráfica */
[ref="chartDiv"] {
  background: #1a1a1a;
  border: 1px solid #333333;
  border-radius: 4px;
}

/* Ajustes de tipografía */
body, button, input, select {
  font-family: 'Roboto', sans-serif;
}

/* Pequeño efecto luminoso simulado (opcional) */
.dashboard-container {
  box-shadow: 0 0 20px rgba(0,0,0,0.7) inset;
}

/* Estilo al título principal, recordando levemente un neón suave */
.dashboard-container > h1 {
  color: #c0c0c0;
  text-shadow: 0 0 10px #c0c0c0;
}

/* Cuando se haga hover en el botón 'Decodificar y Graficar' 
   cambiamos el color a uno más vibrante para enfatizar */
button:hover:contains("Decodificar y Graficar") {
  background: #8e44ad;
  color: #fff;
}

  </style>
  