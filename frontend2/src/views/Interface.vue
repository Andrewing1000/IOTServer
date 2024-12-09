<script>
import * as THREE from 'three';
import DefaultNavbar from "../examples/navbars/NavbarDefault.vue";
import DefaultFooter from "../examples/footers/FooterDefault.vue";
import Controls from './sections/controls.vue';
import { setupSocket } from './utils/socket'; // Gestión global del socket
import { Howl } from 'howler';
import MyGraphics from './sections/graphics.vue';
import axios from 'axios';


export default {
  components: {
    DefaultNavbar,
    DefaultFooter,
    Controls,
    MyGraphics,
  },
  data() {
    return {
      yaw: 0,
      pitch: 0,
      roll: 0,
      yawZero: 0,
      pitchZero: 0,
      rollZero: 0,
      sound: null,
      kickSound: null,
      scene: null,
      camera: null,
      renderer: null,
      baqueta1: null,
      baqueta2: null,
      stream: null,
      active: true,
      allSounds: [],
      selectedSoundIndex: 0,
      selectedKickSoundIndex: 1,
      showSidebar: true,
      showSoundSidebar: false,
      selectedSoundToDelete: '',
      newSound: {
        name: '',
        private: true
      },
      selectedFile: null,
      serverResponse: null,
    };
  },
  mounted() {
    this.initialize3DScene();
    this.setupSocketHandlers();
    let homeButton = document.getElementById("homebutton")


    homeButton.addEventListener("click", e => {
      console.log("Homed")
      this.yawZero = this.yaw
      this.pitchZero = this.pitch
      this.rollZero = this.roll
    })
  },
  methods: {
    initialize3DScene() {
      const scene = this.createScene();
      const camera = this.createCamera();
      const renderer = this.createRenderer();

      this.setupLighting(scene);
      this.addObjects(scene);

      this.setupAnimationLoop(scene, camera, renderer);
      this.setupResizeHandler(camera, renderer);
    },
    createScene() {
      return new THREE.Scene();
    },
    createCamera() {
      const camera = new THREE.PerspectiveCamera(80, window.innerWidth / window.innerHeight, 1, 1000);
      camera.position.z = 17;
      return camera;
    },
    createRenderer() {
      const renderer = new THREE.WebGLRenderer({ alpha: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setClearColor(0x000000, 0);
      document.getElementById('scene-container').appendChild(renderer.domElement);
      return renderer;
    },
    toggleSidebars() {
      this.showSidebar = !this.showSidebar;
      this.showSoundSidebar = !this.showSoundSidebar;
    },
    setupLighting(scene) {
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
      directionalLight.position.set(10, 10, 10);
      scene.add(directionalLight);
    },
    addObjects(scene) {
      const drum = this.createDrum();
      scene.add(drum);

      const baqueta1 = this.createBaqueta();
      baqueta1.name = "baqueta1";
      const baqueta2 = this.createBaqueta();
      baqueta2.name = "baqueta2";
      baqueta2.position.x = 5;

      scene.add(baqueta1, baqueta2);

      this.loadSounds();
    },
    createDrum() {
      const material = new THREE.MeshStandardMaterial({ color: 0xf09569 });
      const geometry = new THREE.CylinderGeometry(5, 5, 2, 32);
      const drum = new THREE.Mesh(geometry, material);
      drum.position.y = -2;
      return drum;
    },
    createBaqueta() {
      const material = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
      const bodyGeometry = new THREE.CylinderGeometry(0.1, 0.1, 8, 32);
      const body = new THREE.Mesh(bodyGeometry, material);
      body.rotation.x = Math.PI / 2;

      const tipGeometry = new THREE.SphereGeometry(0.2, 32, 32);
      const tip = new THREE.Mesh(tipGeometry, material);
      tip.name = "tip";
      tip.position.set(0, 4, 0);

      body.add(tip);
      return body;
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async deleteSelectedSound() {
      if (!this.selectedSoundToDelete) return;
      try {
        let url = 'http://localhost:8080'

        let admin = {
          email: 'admin@example.com',
          password: 'admin'
        }
        let tokenS;
        await axios.post(url + '/user/token/', admin).then((response) => {
          tokenS = response.data.token;
          console.log(tokenS);

        });


        let config = {
          headers: {
            Authorization: 'Token ' + tokenS,
          }
        }
        await axios.delete(`http://localhost:8080/airdrum/sound/${this.selectedSoundToDelete}/`,config);
        // Filtramos el sonido eliminado de la lista local
        this.allSounds = this.allSounds.filter(sound => sound.id !== this.selectedSoundToDelete);
        // Reiniciamos la selección
        this.selectedSoundToDelete = '';
        this.loadSounds();
      } catch (error) {
        console.error('Error deleting sound:', error);
      }
    },
    async postSound() {
      let url = 'http://localhost:8080'

      let admin = {
        email: 'admin@example.com',
        password: 'admin'
      }
      let tokenS;
      await axios.post(url + '/user/token/', admin).then((response) => {
        tokenS = response.data.token;
        console.log(tokenS);

      });


      let config = {
        headers: {
          Authorization: 'Token ' + tokenS,
        }
      }
      try {
        const formData = new FormData();
        formData.append('name', this.newSound.name);
        formData.append('private', this.newSound.private);
        formData.append('sound', this.selectedFile); // Aquí adjuntamos el archivo

        const response = await axios.post('http://localhost:8080/airdrum/sound/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Token ' + tokenS
          }
        });

        this.serverResponse = response.data;
        // Limpiar el formulario
        this.newSound = { name: '', private: true };
        this.selectedFile = null;
        this.loadSounds();
      } catch (error) {
        console.error('Error posting sound:', error);
        this.serverResponse = error.response ? error.response.data : error.message;
      }
    },
    async loadSounds() {
      let url = 'http://localhost:8080'

      let admin = {
        email: 'admin@example.com',
        password: 'admin'
      }
      let tokenS;
      await axios.post(url + '/user/token/', admin).then((response) => {
        tokenS = response.data.token;
        console.log(tokenS);

      });


      let config = {
        headers: {
          Authorization: 'Token ' + tokenS,
        }
      }
      await axios.get('http://localhost:8080/airdrum/sound/', config)
        .then((response) => {
          this.allSounds = response.data; // Guardamos todos los sonidos obtenidos

          // Asignar el primer sonido (por ejemplo) a this.sound si existe
          if (this.allSounds[this.selectedSoundIndex]) {
            const soundUrl = this.allSounds[this.selectedSoundIndex].sound;
            this.sound = new Howl({
              src: [soundUrl],
              volume: 1.0,
              loop: false
            });
          }

          // Asignar el segundo sonido (por ejemplo) a this.kickSound si existe
          if (this.allSounds[this.selectedKickSoundIndex]) {
            const kickSoundUrl = this.allSounds[this.selectedKickSoundIndex].sound;
            this.kickSound = new Howl({
              src: [kickSoundUrl],
              volume: 1.0,
              loop: false
            });
          }
        })
        .catch((error) => {
          console.error("Error loading sounds:", error);
        });
    },
    playSound() {
      if (this.sound) {
        this.sound.play();
      }
    },
    playKickSound() {
      if (this.kickSound) {
        this.kickSound.play();
      }
    },
    setupAnimationLoop(scene, camera, renderer) {

      const animate = () => {
        requestAnimationFrame(animate);

        this.updateBaquetaRotations(scene);

        renderer.render(scene, camera);
      };
      animate();
    },
    updateBaquetaRotations(scene) {

      const baqueta1 = scene.children.find((obj) => obj.name === "baqueta1");

      let tip = baqueta1.getObjectByName("tip")
      const tipGlobalPosition = new THREE.Vector3();
      tip.getWorldPosition(tipGlobalPosition)

      if (this.active) {
        if (tipGlobalPosition.y <= -1) {
          this.playSound()
          this.active = false;
        }
      }
      else {
        if (tipGlobalPosition.y > -1) {
          this.active = true;
        }
      }


      baqueta1.rotation.x = (this.pitch - this.pitchZero) - Math.PI / 2;
      baqueta1.rotation.y = (this.yaw - this.yawZero);
      baqueta1.rotation.z = -(this.roll - this.rollZero);

    },
    setupResizeHandler(camera, renderer) {
      window.addEventListener('resize', () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
      });
    },
    setupSocketHandlers() {
      const socket = setupSocket();
      socket.binaryType = "arraybuffer"
      socket.onmessage = (e) => {

        if (e.data instanceof ArrayBuffer) {
          const buffer = e.data;
          const dataView = new DataView(buffer);

          this.roll = dataView.getFloat64(0, false);
          this.pitch = dataView.getFloat64(8, false);
          this.yaw = dataView.getFloat64(16, false);
        } else {
          const data = JSON.parse(e.data);
          this.playKickSound();
          if (data.command === "kick") {
            this.playKickSound();
          }
        }
      };
    },
    assignSelectedSounds() {
      if (this.allSounds[this.selectedSoundIndex]) {
        this.sound = new Howl({
          src: [this.allSounds[this.selectedSoundIndex].sound],
          volume: 1.0,
          loop: false
        });
      }

      if (this.allSounds[this.selectedKickSoundIndex]) {
        this.kickSound = new Howl({
          src: [this.allSounds[this.selectedKickSoundIndex].sound],
          volume: 1.0,
          loop: false
        });
      }
    }
  },
};
</script>

<template>
  <div id="app" class="background">
    <DefaultNavbar :action="{ route: 'javascript:;', color: 'btn-white' }" />
    <div id="main-content">
      <!-- Barra lateral izquierda -->
      <div id="sidebar" v-show="showSidebar">
        <h3>Controles de Animación para Baqueta 1</h3>
        <button id="homebutton">Home</button>
        <Controls/>

        <!-- Botón para ocultar este sidebar y mostrar el otro -->
        <button @click="toggleSidebars">Ir a Ajustes de Sonido</button>
      </div>

      <!-- Barra lateral derecha -->
      <div id="sound-sidebar" v-show="showSoundSidebar">
        <h4>Seleccionar sonido principal</h4>
        <select v-model="selectedSoundIndex" @change="assignSelectedSounds">
          <option v-for="(s, index) in allSounds" :key="s.id" :value="index">{{ s.name }}</option>
        </select>

        <h4>Seleccionar sonido de kick</h4>
        <select v-model="selectedKickSoundIndex" @change="assignSelectedSounds">
          <option v-for="(s, index) in allSounds" :key="s.id" :value="index">{{ s.name }}</option>
        </select>

        <div>
          <h3>Agregar un nuevo sonido</h3>
          <form @submit.prevent="postSound">
            <div>
              <label for="name">Nombre:</label>
              <input type="text" id="name" v-model="newSound.name" required />
            </div>
            <div>
              <label for="sound">URL/Path:</label>
              <input type="file" id="sound" @change="handleFileUpload" required />
            </div>
            <div>
              <label for="private">Privado:</label>
              <input type="checkbox" id="private" v-model="newSound.private" />
            </div>
            <button type="submit">Enviar</button>
          </form>
        </div>

        <!-- Nueva sección para listar y eliminar sonidos -->
        <h4>Eliminar un sonido</h4>
        <select v-model="selectedSoundToDelete">
          <option disabled value="">Selecciona un sonido</option>
          <option v-for="sound in allSounds" :key="sound.id" :value="sound.id">
            {{ sound.name }}
          </option>
        </select>
        <button @click="deleteSelectedSound" :disabled="!selectedSoundToDelete">Eliminar</button>

        <button @click="playSound">Play Sound</button>
        <button @click="playKickSound">Play Kick Sound</button>

        <!-- Botón para ocultar este sidebar y mostrar el otro -->
        <button @click="toggleSidebars">Volver a Controles</button>
      </div>

      <div id="scene-container"></div>
    </div>

    <MyGraphics/>
    <DefaultFooter />
  </div>
</template>


<style>
.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #ADD8E6;
  /* un tono de azul claro */
  background-size: cover;
  z-index: -1;
  /* detrás de los elementos */
  font-family: Arial, sans-serif;
  color: #333;
}

#main-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: calc(100% - 100px);
  /* Ajustado según navbar y footer */
  padding: 20px;
  gap: 20px;
  /* Espacio entre columnas */
}

#scene-container {
  flex: 1;
  position: relative;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 8px;
  max-height: 100%;
}

#sidebar {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
  border: 1px solid #ddd;
}
#sound-sidebar {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
  border: 1px solid #ddd;
}

#sidebar h3,
#sound-sidebar h3,
#sidebar h4,
#sound-sidebar h4 {
  margin-top: 0;
  margin-bottom: 10px;
}

label {
  font-weight: bold;
  margin-bottom: 3px;
}

input[type="text"],
input[type="file"],
select,
textarea {
  width: 100%;
  padding: 5px 8px;
  margin-bottom: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input[type="checkbox"] {
  margin-right: 5px;
}

button {
  display: inline-block;
  background-color: #3498db;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  margin-bottom: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 14px;
}

button:hover {
  background-color: #2980b9;
}

pre {
  background: #eee;
  padding: 10px;
  border-radius: 4px;
  overflow: auto;
  font-size: 13px;
}
</style>