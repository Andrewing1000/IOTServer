<!-- App.vue -->
<template>
  <div class="app-container">
    <DefaultNavbar :action="{ route: 'javascript:;', color: 'btn-white' }" class="top-navbar" />

    <div class="main-content">
      <aside class="left-panel">
        <div class="nav-icons">
          <button class="icon-nav" @click="homeClicked" :title="'Home'">
            <i class="fa fa-home"></i>
          </button>
          <button class="icon-nav" @click="showModal=true" :title="'Sound Settings'">
            <i class="fa fa-cog"></i>
          </button>
        </div>
        <div class="section-title">Controls</div>
        <Controls class="controls-section" />
        <div class="section-title">Player</div>
        <Controller />
      </aside>
      <div id="scene-container" class="scene-container"></div>
    </div>

    <footer class="bottom-bar">
      <button class="btn-bottom record" @click="toggleRecording" :title="isRecording ? 'Stop Recording' : 'Record'">
        <i class="fa" :class="isRecording ? 'fa-stop-circle' : 'fa-circle'"></i>
      </button>
      <button class="btn-bottom action" @click="playSound" :title="'Play Snare'">
        <i class="fa fa-drum"></i>
      </button>
      <button class="btn-bottom action" @click="playKickSound" :title="'Play Kick'">
        <i class="fa fa-drum-steelpan"></i>
      </button>
    </footer>

    <transition name="fade">
      <div class="modal-overlay" v-if="showModal" @click.self="showModal=false">
        <div class="modal-content">
          <h3>Sound Settings</h3>
          <h4>Seleccionar sonido principal</h4>
          <select v-model="selectedSoundIndex" @change="assignSelectedSounds">
            <option v-for="(s, index) in allSounds" :key="s.id" :value="index">{{ s.name }}</option>
          </select>

          <h4>Seleccionar sonido de kick</h4>
          <select v-model="selectedKickSoundIndex" @change="assignSelectedSounds">
            <option v-for="(s, index) in allSounds" :key="s.id" :value="index">{{ s.name }}</option>
          </select>

          <h3>Agregar un nuevo sonido</h3>
          <form @submit.prevent="postSound">
            <div class="form-group">
              <label>Nombre:</label>
              <input type="text" v-model="newSound.name" required />
            </div>
            <div class="form-group">
              <label>Archivo de sonido:</label>
              <input type="file" @change="handleFileUpload" accept="audio/*" required />
            </div>
            <div class="form-group-inline">
              <input type="checkbox" v-model="newSound.private" />
              <span>Privado</span>
            </div>
            <button class="submit-btn" type="submit">Enviar</button>
          </form>
          <p v-if="serverResponse" class="response-text">{{ serverResponse }}</p>

          <div class="modal-actions">
            <button class="close-btn" @click="showModal=false">
              <i class="fa fa-times"></i> Close
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import * as THREE from 'three';
import DefaultNavbar from "../examples/navbars/NavbarDefault.vue";
import DefaultFooter from "../examples/footers/FooterDefault.vue";
import Controls from './sections/controls.vue';
import { setupSocket } from './utils/socket';
import { Howl } from 'howler';
import api from './utils/api';

export default {
  components: {
    DefaultNavbar,
    DefaultFooter,
    Controls,
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
      active: true,
      isRecording: false,
      allSounds: [],
      selectedSoundIndex: 0,
      selectedKickSoundIndex: 1,
      newSound: {
        name: '',
        private: true
      },
      selectedFile: null,
      serverResponse: null,
      showModal: false,
    };
  },
  mounted() {
    this.initialize3DScene();
    this.setupSocketHandlers();

    let homeButton = document.getElementById("homebutton");
    homeButton.addEventListener("click", () => {
      this.yawZero = this.yaw;
      this.pitchZero = this.pitch;
      this.rollZero = this.roll;
    });

    this.loadSounds();
  },
  methods: {
    homeClicked() {
      this.yawZero = this.yaw;
      this.pitchZero = this.pitch;
      this.rollZero = this.roll;
    },
    initialize3DScene() {
      const scene = this.createScene();
      const camera = this.createCamera();
      const renderer = this.createRenderer();
      this.scene = scene;
      this.camera = camera;
      this.renderer = renderer;
      this.setupLighting(scene);
      this.addObjects(scene);
      this.setupAnimationLoop(scene, camera, renderer);
      this.setupResizeHandler(camera, renderer);
    },
    createScene() {
      return new THREE.Scene();
    },
    createCamera() {
      const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 1000);
      camera.position.set(0, 5, 20);
      camera.lookAt(0, 0, 0);
      return camera;
    },
    createRenderer() {
      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      const container = document.getElementById('scene-container');
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(window.devicePixelRatio);
      renderer.setClearColor(0x1e1e1e, 1);
      container.appendChild(renderer.domElement);
      return renderer;
    },
    setupLighting(scene) {
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
      scene.add(ambientLight);
      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.9);
      directionalLight.position.set(10, 20, 10);
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
      this.assignSelectedSounds();
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
    async postSound() {
      try {
        const formData = new FormData();
        formData.append('name', this.newSound.name);
        formData.append('private', this.newSound.private);
        formData.append('sound', this.selectedFile);
        await api.post('/airdrum/sound/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        });
        this.serverResponse = 'Sonido subido exitosamente.';
        this.newSound = { name: '', private: true };
        this.selectedFile = null;
        this.loadSounds();
      } catch (error) {
        this.serverResponse = error.response ? error.response.data : 'Error al subir el sonido.';
      }
    },
    async loadSounds() {
      try {
        const response = await api.get('/airdrum/sound/');
        this.allSounds = response.data;
        this.assignSelectedSounds();
      } catch (error) {}
    },
    playSound() {
      if (this.sound) this.sound.play();
    },
    playKickSound() {
      if (this.kickSound) this.kickSound.play();
    },
    toggleRecording() {
      this.isRecording = !this.isRecording;
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
      if (!baqueta1) return;
      const tip = baqueta1.getObjectByName("tip");
      if (!tip) return;
      const tipGlobalPosition = new THREE.Vector3();
      tip.getWorldPosition(tipGlobalPosition);
      if (this.active && tipGlobalPosition.y <= -1) {
        this.playSound();
        this.active = false;
      } else if (!this.active && tipGlobalPosition.y > -1) {
        this.active = true;
      }
      baqueta1.rotation.x = (this.pitch - this.pitchZero) - Math.PI / 2;
      baqueta1.rotation.y = (this.yaw - this.yawZero);
      baqueta1.rotation.z = -(this.roll - this.rollZero);
    },
    setupResizeHandler(camera, renderer) {
      const onResize = () => {
        const container = document.getElementById('scene-container');
        const width = container.clientWidth;
        const height = container.clientHeight;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
      };
      window.addEventListener('resize', onResize);
      onResize();
    },
    setupSocketHandlers() {
      const socket = setupSocket();
      socket.binaryType = "arraybuffer";
      socket.onmessage = (e) => {
        if (e.data instanceof ArrayBuffer) {
          const dataView = new DataView(e.data);
          this.roll = dataView.getFloat64(0, false);
          this.pitch = dataView.getFloat64(8, false);
          this.yaw = dataView.getFloat64(16, false);
        } else {
          const data = JSON.parse(e.data);
          if (data.command === "kick") this.playKickSound();
        }
      };
    },
    assignSelectedSounds() {
      if (this.allSounds[this.selectedSoundIndex]) {
        const soundUrl = this.allSounds[this.selectedSoundIndex].sound;
        this.sound = new Howl({ src: [soundUrl], volume: 1.0, loop: false });
      }
      if (this.allSounds[this.selectedKickSoundIndex]) {
        const kickSoundUrl = this.allSounds[this.selectedKickSoundIndex].sound;
        this.kickSound = new Howl({ src: [kickSoundUrl], volume: 1.0, loop: false });
      }
    }
  },
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

.app-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #1e1e1e;
  overflow: hidden;
  font-family: sans-serif;
  color: #ccc;
}

.top-navbar {
  flex: 0 0 60px;
  background: #2c2c2c;
  border-bottom: 1px solid #333;
  z-index: 10;
}

.main-content {
  flex: 1 1 auto;
  display: flex;
  overflow: hidden;
}

.left-panel {
  flex: 0 0 400px;
  background: #2c2c2c;
  border-right: 1px solid #333;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
}

.nav-icons {
  display: flex;
  gap:10px;
  margin-bottom:20px;
}

.icon-nav {
  width:40px;
  height:40px;
  border:none;
  background:#3a3a3a;
  border-radius:4px;
  display:flex;
  align-items:center;
  justify-content:center;
  color:#eee;
  cursor:pointer;
  font-size:16px;
  transition: background 0.2s;
}
.icon-nav:hover {
  background:#4a4a4a;
}

.section-title {
  margin-top:20px;
  margin-bottom:10px;
  font-size:14px;
  color:#aaa;
  text-transform:uppercase;
  letter-spacing:1px;
}

.btn.btn-block {
  display: block;
  width: 100%;
  margin-bottom: 20px;
  background: #4a90e2;
  color: #fff;
  text-align: center;
  border: none;
  border-radius: 4px;
  padding: 10px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn.btn-block:hover {
  background: #357ab8;
}

.controls-section {
  margin-bottom:20px;
}

.scene-container {
  flex: 1;
  position: relative;
  background: #1e1e1e;
  overflow: hidden;
}

.scene-container canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.bottom-bar {
  flex: 0 0 80px;
  background: #2c2c2c;
  border-top:1px solid #333;
  box-sizing: border-box;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  padding:10px 20px;
}

.btn-bottom {
  width:40px; height:40px;
  border:none;
  border-radius:4px;
  background:#3a3a3a;
  display:flex;
  align-items:center;
  justify-content:center;
  color:#eee;
  cursor:pointer;
  font-size:18px;
  transition: background 0.2s;
}

.btn-bottom:hover {
  background:#4a4a4a;
}

.record {
  color:#e74c3c;
}
.record:hover {
  background:#5a5a5a;
}

.action {
  color:#4a90e2;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.modal-overlay {
  position: fixed;
  top:0;
  left:0;
  width:100%;
  height:100%;
  background:rgba(0,0,0,0.6);
  z-index:9999;
  display:flex;
  justify-content:center;
  align-items:center;
}

.modal-content {
  background:#2c2c2c;
  padding:20px;
  border-radius:8px;
  width:400px;
  max-width:90%;
  box-sizing:border-box;
  color:#ccc;
  font-size:14px;
}

.modal-content h3 {
  margin-top:0;
  margin-bottom:10px;
  color:#fff;
}

.modal-content h4 {
  margin-bottom:10px;
  margin-top:20px;
  color:#ccc;
}

.form-group,
.form-group-inline {
  margin-bottom:10px;
  display:flex;
  flex-direction:column;
  color:#ccc;
  font-size:13px;
}

.form-group-inline {
  flex-direction:row;
  align-items:center;
  gap:5px;
}

input[type="text"],
input[type="file"],
select {
  width:100%;
  padding:8px;
  border:1px solid #555;
  border-radius:4px;
  margin-bottom:10px;
  box-sizing:border-box;
  background:#333;
  color:#ccc;
  font-size:13px;
}

input[type="checkbox"] {
  margin-right:5px;
}

.submit-btn {
  background:#27ae60;
  color:#fff;
  border:none;
  padding:8px 12px;
  border-radius:4px;
  font-size:14px;
  cursor:pointer;
  transition:background 0.2s;
}

.submit-btn:hover {
  background:#1e8449;
}

.response-text {
  margin-top:10px;
  color:#2ecc71;
  font-size:13px;
}

.modal-actions {
  margin-top:20px;
  display:flex;
  justify-content:flex-end;
}

.close-btn {
  background:#7f8c8d;
  color:#fff;
  border:none;
  padding:8px 12px;
  border-radius:4px;
  font-size:14px;
  cursor:pointer;
  transition:background 0.2s;
  display:flex;
  align-items:center;
  gap:5px;
}

.close-btn:hover {
  background:#707b7c;
}

@media (max-width: 768px) {
  .left-panel {
    width:100%;
    border-right:none;
    border-bottom:1px solid #333;
  }

  .main-content {
    flex-direction:column;
  }

  .scene-container {
    height: calc(100vh - 60px - 80px);
  }

  .bottom-bar {
    flex-wrap:wrap;
    justify-content:center;
  }
}

@media (max-width:480px) {
  .modal-content {
    width:90%;
    padding:10px;
  }

  .submit-btn, .close-btn {
    width:100%;
  }
}
</style>
