<template>
  <DefaultNavbar
    :action="{ route: 'javascript:;', color: 'btn-white' }"
    class="top-navbar"
  />
  <div class="dashboardContainer">
    <b-container fluid class="p-3">
      <b-row>
        <b-col>
          <b-card class="text-center animated-card">
            <b-card-header>
              <h3 class="header-title">
                Visualización de Datos en Tiempo Real
              </h3>
            </b-card-header>
            <b-card-body>
              <p class="description-text">
                Este panel muestra datos en tiempo real de los parámetros de
                orientación del dispositivo. Los gráficos interactivos permiten
                un análisis detallado de los movimientos, facilitando la toma de
                decisiones informadas.
              </p>
              <div id="chart-container" class="chart-container">
                <canvas id="myChart"></canvas>
              </div>
            </b-card-body>
            <b-card-footer class="text-muted">
              <p>Actualizado a cada segundo con nuevos datos.</p>
            </b-card-footer>
          </b-card>
        </b-col>
      </b-row>
      <b-row class="mt-4">
        <b-col>
          <b-card class="info-card">
            <b-card-header>
              <h5>Información Adicional</h5>
            </b-card-header>
            <b-card-body>
              <ul>
                <li><strong>Yaw:</strong> Rotación sobre el eje vertical.</li>
                <li>
                  <strong>Pitch:</strong> Inclinación sobre el eje lateral.
                </li>
                <li>
                  <strong>Roll:</strong> Inclinación sobre el eje longitudinal.
                </li>
              </ul>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col>
          <b-card class="info-card">
            <b-card-header>
              <h5>Estadísticas</h5>
            </b-card-header>
            <b-card-body>
              <p>Últimos 10 segundos de datos:</p>
              <ul>
                <li>Yaw promedio: {{ getAverageYaw() }}</li>
                <li>Pitch promedio: {{ getAveragePitch() }}</li>
                <li>Roll promedio: {{ getAverageRoll() }}</li>
              </ul>
            </b-card-body>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import { setupSocket } from "./utils/socket";
import DefaultNavbar from "../examples/navbars/NavbarDefault.vue";

Chart.register(...registerables);

export default {
  components: {
    DefaultNavbar,
  },
  data() {
    return {
      yaw: 0,
      pitch: 0,
      roll: 0,
      chart: null,
      chartData: {
        labels: [],
        datasets: [
          {
            label: "Yaw",
            data: [],
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 2,
            fill: false,
          },
          {
            label: "Pitch",
            data: [],
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 2,
            fill: false,
          },
          {
            label: "Roll",
            data: [],
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 2,
            fill: false,
          },
        ],
      },
    };
  },
  mounted() {
    this.setupSocketHandlers();
    this.initializeChart();
  },
  methods: {
    setupSocketHandlers() {
      const socket = setupSocket();
      socket.binaryType = "arraybuffer";
      socket.onmessage = (e) => {
        if (e.data instanceof ArrayBuffer) {
          const dataView = new DataView(e.data);
          this.roll = dataView.getFloat64(0, false);
          this.pitch = dataView.getFloat64(8, false);
          this.yaw = dataView.getFloat64(16, false);
          this.updateChartData();
        } else {
          const data = JSON.parse(e.data);
          if (data.command === "kick") {
            // Handle kick command if needed
          }
        }
      };
    },
    initializeChart() {
      const ctx = document.getElementById("myChart").getContext("2d");
      this.chart = new Chart(ctx, {
        type: "line",
        data: this.chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: "linear",
              position: "bottom",
            },
            y: {
              beginAtZero: true,
              ticks: {
                callback: function (value) {
                  return value.toFixed(2);
                },
              },
            },
          },
        },
      });
    },
    updateChartData() {
      const timestamp = Date.now();
      this.chartData.labels.push(timestamp);
      this.chartData.datasets[0].data.push({ x: timestamp, y: this.yaw });
      this.chartData.datasets[1].data.push({ x: timestamp, y: this.pitch });
      this.chartData.datasets[2].data.push({ x: timestamp, y: this.roll });

      if (this.chartData.labels.length > 50) {
        this.chartData.labels.shift();
        this.chartData.datasets.forEach((dataset) => dataset.data.shift());
      }

      this.chart.update();
    },
    getAverageYaw() {
      return this.calculateAverage(this.chartData.datasets[0].data);
    },
    getAveragePitch() {
      return this.calculateAverage(this.chartData.datasets[1].data);
    },
    getAverageRoll() {
      return this.calculateAverage(this.chartData.datasets[2].data);
    },
    calculateAverage(data) {
      if (data.length === 0) return 0;
      const sum = data.reduce((acc, point) => acc + point.y, 0);
      return (sum / data.length).toFixed(2);
    },
  },
};
</script>

<style scoped>
.dashboardContainer {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  flex-direction: column;
  background: linear-gradient(to right, #b9d7f5, #a1c4fd);
  animation: backgroundAnimation 10s ease infinite alternate;
}

@keyframes backgroundAnimation {
  from {
    background: #b9d7f5;
  }
  to {
    background: #a1c4fd;
  }
}

.animated-card {
  transition: transform 0.3s ease;
}

.animated-card:hover {
  transform: scale(1.02);
}

.header-title {
  color: #ffffff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.description-text {
  color: #ffffff;
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.chart-container {
  width: 100%;
  max-width: 800px;
  height: 400px;
  margin: 0 auto;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  padding: 20px;
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
}

.b-card {
  background-color: #343a40;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
}

.b-card-header {
  background-color: #007bff;
  color: white;
}

.b-card-body {
  padding: 1.25rem;
}

.info-card {
  margin-top: 20px;
  background-color: #f8f9fa;
  color: #343a40;
  border: 1px solid #ced4da;
}
</style>
