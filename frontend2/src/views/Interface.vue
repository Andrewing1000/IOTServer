<script>
import * as THREE from 'three';
import DefaultNavbar from "../examples/navbars/NavbarDefault.vue";
import DefaultFooter from "../examples/footers/FooterDefault.vue";
import Controls from './sections/controls.vue';
import { setupSocket } from './utils/socket'; // Gestión global del socket
import { Howl } from 'howler';
import MyGraphics from './sections/graphics.vue';

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
    };
  },
  mounted() {
    this.initialize3DScene();
    this.setupSocketHandlers();
    let homeButton = document.getElementById("homebutton");

    homeButton.addEventListener("click", e => {
      console.log("Homed");
      this.yawZero = this.yaw;
      this.pitchZero = this.pitch;
      this.rollZero = this.roll;
    });
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
    loadSounds() {
      import('@/assets/audio/mi-sonido2.mp3').then((module) => {
        this.sound = new Howl({
          src: [module.default],
          volume: 1.0,
          loop: false
        });
      });

      import('@/assets/audio/kick_sound.mp3').then((module) => {
        this.kickSound = new Howl({
          src: [module.default],
          volume: 1.0,
          loop: false
        });
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

      let tip = baqueta1.getObjectByName("tip");
      const tipGlobalPosition = new THREE.Vector3();
      tip.getWorldPosition(tipGlobalPosition);

      if (this.active) {
        if (tipGlobalPosition.y <= -1) {
          this.playSound();
          this.active = false;
        }
      } else {
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
      socket.binaryType = "arraybuffer";
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
  },
};
</script>

<template>
  <div id="app" class="background">
    <DefaultNavbar
      :action="{
        route: 'javascript:;',
        color: 'btn-white',
      }"  
    />
    <div id="main-content">
      <div id="sidebar">
        <h3>Controles de Animación para Baqueta 1</h3>
        <button id="homebutton" class="btn">Home</button>
        <Controls/>
        <button @click="playSound" class="btn">Play Sound</button>
        <button @click="playKickSound" class="btn">Play Kick Sound</button>
      </div>
      <div id="scene-container"></div>
    </div>
    <MyGraphics/>
    <DefaultFooter />
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
  font-family: 'Roboto', sans-serif;
}

.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #6dd5ed, #2193b0);
  background-size: cover;
  z-index: -1;
  animation: backgroundAnimation 10s infinite alternate;
}

@keyframes backgroundAnimation {
  0% { background-position: 0% 50%; }
  100% { background-position: 100% 50%; }
}

#main-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: calc(100% - 100px);
  padding: 20px;
  animation: fadeIn 1s ease-in-out;
}

#scene-container {
  flex: 1;
  position: relative;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  animation: fadeIn 1s ease-in-out;
}

#sidebar {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  animation: slideIn 1s ease-in-out;
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
}

label, input, button {
  display: block;
  margin-bottom: 10px;
}

button {
  cursor: pointer;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #2193b0;
  color: white;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #6dd5ed;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}
</style>