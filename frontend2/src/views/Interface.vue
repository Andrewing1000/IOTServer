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
      active : true,
      allSounds: [],
      selectedSoundIndex: 0,
      selectedKickSoundIndex: 1
    };
  },
  mounted() {
    this.initialize3DScene();
    this.setupSocketHandlers();
    let homeButton = document.getElementById("homebutton")
    

    homeButton.addEventListener("click", e=>{
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
    async loadSounds() {
      let url = 'http://localhost:8080'

      let admin={
        email: 'admin@example.com',
        password: 'admin'
      }
      let tokenS;
      await axios.post(url+'/user/token/',admin).then((response) => {
        tokenS = response.data.token;
        console.log(tokenS);
        
      });
      

      let config = {
        headers: {
          Authorization: 'Token '+tokenS,
        }
      }
      await axios.get('http://localhost:8080/airdrum/sound/',config)
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

      if(this.active){
        if (tipGlobalPosition.y  <= -1) {
          this.playSound()
          this.active = false;
        }
      }
      else{
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
          if (data.command === "kick" ) {
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
    <DefaultNavbar
      :action="{
        route: 'javascript:;',
        color: 'btn-white',
      }"  
    />
    <div id="main-content">
      <div id="sidebar">
        <h3>Controles de Animación para Baqueta 1</h3>
        <button id="homebutton">Home</button>
        <Controls/>

        <h4>Seleccionar sonido principal</h4>
        <select v-model="selectedSoundIndex" @change="assignSelectedSounds">
          <option v-for="(s,index) in allSounds" :key="s.id" :value="index">{{ s.name }}</option>
        </select>

        <h4>Seleccionar sonido de kick</h4>
        <select v-model="selectedKickSoundIndex" @change="assignSelectedSounds">
          <option v-for="(s,index) in allSounds" :key="s.id" :value="index">{{ s.name }}</option>
        </select>

        <button @click="playSound">Play Sound</button>
        <button @click="playKickSound">Play Kick Sound</button>
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
  /* background: url("src/assets/img/escenario.jpg") no-repeat center center fixed; */
  background-color: aqua;
  background-size: cover;
  z-index: -1; /* Ensure it is behind other content */
}

#main-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: calc(100% - 100px); /* Adjust based on navbar and footer height */
  padding: 20px;
}

#scene-container {
  flex: 1;
  position: relative;
  background-color: #67676739;
}

#sidebar {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 8px;
  width: 300px;
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
}

label, input, button {
  display: block;
  margin-bottom: 5px;
}

button {
  cursor: pointer;
}
</style>