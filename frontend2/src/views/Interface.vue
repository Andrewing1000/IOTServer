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
        <div class="section-title">Controls & Player</div>
        <Controls class="controls-section" 
          @sound-played="onSoundPlayed" 
          @kick-played="onKickPlayed"
        />
        <!-- We assume Controls emits events 'sound-played' and 'kick-played' 
             whenever a sound is played in Controls.vue -->
      </aside>
      <div id="scene-container" class="scene-container"></div>
    </div>

    <footer class="bottom-bar" :class="{recording:isRecording}">
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

    <DefaultFooter />

    <transition name="fade">
      <div class="modal-overlay" v-if="showModal" @click.self="showModal=false">
        <div class="modal-content">
          <div class="modal-tabs">
            <button 
              class="tab-btn"
              :class="{active: activeTab==='selection'}" 
              @click="activeTab='selection'">Selection</button>
            <button 
              class="tab-btn" 
              :class="{active: activeTab==='management'}" 
              @click="activeTab='management'">Management</button>
          </div>

          <div class="modal-body">
            <div v-show="activeTab==='selection'" class="tab-section">
              <h3>Sound Selection</h3>
              <div class="form-group">
                <label>Principal Sound:</label>
                <select v-model="selectedSoundIndex" @change="assignSelectedSounds">
                  <option v-for="(s, index) in allSounds" :key="index" :value="index">{{ s.name }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Kick Sound:</label>
                <select v-model="selectedKickSoundIndex" @change="assignSelectedSounds">
                  <option v-for="(s, index) in allSounds" :key="index" :value="index">{{ s.name }}</option>
                </select>
              </div>
            </div>

            <div v-show="activeTab==='management'" class="tab-section">
              <h3>Upload New Sound</h3>
              <form @submit.prevent="postSound" class="upload-form">
                <div class="form-group">
                  <label>Name:</label>
                  <input type="text" v-model="newSound.name" required />
                </div>
                <div class="form-group">
                  <label>Sound File:</label>
                  <input type="file" @change="handleFileUpload" accept="audio/*" required />
                </div>
                <div class="form-group-inline">
                  <input type="checkbox" v-model="newSound.private" />
                  <span>Private</span>
                </div>
                <button class="submit-btn" type="submit">Upload</button>
              </form>
              <p v-if="serverResponse" class="response-text">{{ serverResponse }}</p>

              <h3>User Uploaded Sounds</h3>
              <div class="uploaded-list" v-if="uploadedSounds.length > 0">
                <div class="uploaded-item" v-for="sound in uploadedSounds" :key="sound.id">
                  <span class="sound-name">{{ sound.name }}</span>
                  <button class="delete-btn" @click="deleteSound(sound.id)">Delete</button>
                </div>
              </div>
              <p v-else class="no-sounds">No uploaded sounds found</p>
            </div>
          </div>

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
import './App.css';
import mainSoundUrl from '@/assets/audio/mi-sonido2.mp3';
import kickSoundUrl from '@/assets/audio/kick_sound.mp3';

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
      recordingStartTime: null,
      recordedEvents: [], // store tuples (timestamp, 1.0, sound_id)
      defaultSounds: [
        { name: 'Default Snare', sound: mainSoundUrl },
        { name: 'Default Kick', sound: kickSoundUrl }
      ],
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
      activeTab: 'selection'
    };
  },
  computed: {
    uploadedSounds() {
      return this.allSounds.filter(s => s.id !== undefined);
    }
  },
  mounted() {
    this.initialize3DScene();
    this.setupSocketHandlers();
    this.loadSounds();
    let homeButton = document.getElementById("homebutton");
    if (homeButton) {
      homeButton.addEventListener("click", () => {
        this.yawZero = this.yaw;
        this.pitchZero = this.pitch;
        this.rollZero = this.roll;
      });
    }
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
        await this.loadSounds();
      } catch (error) {
        this.serverResponse = error.response ? error.response.data : 'Error al subir el sonido.';
      }
    },
    async loadSounds() {
      try {
        const response = await api.get('/airdrum/sound/');
        const serverSounds = response.data || [];
        // Merge defaults and server sounds
        this.allSounds = [...this.defaultSounds, ...serverSounds];
        this.assignSelectedSounds();
      } catch (error) {
        // If server fails, still show default sounds
        this.allSounds = [...this.defaultSounds];
        this.assignSelectedSounds();
      }
    },
    async deleteSound(id) {
      try {
        await api.delete(`/airdrum/sound/${id}`);
        this.allSounds = this.allSounds.filter(s => s.id !== id);
        this.assignSelectedSounds();
      } catch (error) {
        console.error('Error deleting sound:', error);
      }
    },
    playSound() {
      if (this.sound) {
        this.sound.play();
        // If recording, record event
        this.recordEventForSound(this.allSounds[this.selectedSoundIndex]);
      }
    },
    playKickSound() {
      if (this.kickSound) {
        this.kickSound.play();
        // If recording, record event
        this.recordEventForSound(this.allSounds[this.selectedKickSoundIndex]);
      }
    },
    toggleRecording() {
      if (this.isRecording) {
        // Stopping recording
        this.isRecording = false;
        // Prompt for track name
        const trackName = prompt("Enter a name for this track:");
        if (trackName) {
          this.saveRecording(trackName);
        }
      } else {
        // Starting recording
        this.isRecording = true;
        this.recordingStartTime = performance.now();
        this.recordedEvents = [];
      }
    },
    recordEventForSound(soundObj) {
      if (!this.isRecording) return;
      const timestamp = (performance.now() - this.recordingStartTime) / 1000.0;
      const fixedID = soundObj.id !== undefined ? soundObj.id : 1; // default to 1 if no id
      // Tuple: (timestamp(float), 1.0, sound_id(int))
      this.recordedEvents.push([timestamp, 1.0, fixedID]);
    },
    saveRecording(trackName) {
      // Convert recordedEvents to binary
      const length = this.recordedEvents.length;
      // Each event: 2 floats + 1 int = (4 + 4 + 4) = 12 bytes per event
      // Plus 4 bytes for length
      const bufferSize = 4 + (length * 12);
      const buffer = new ArrayBuffer(bufferSize);
      const view = new DataView(buffer);

      let offset = 0;
      // Write length (unsigned int, big-endian)
      view.setUint32(offset, length, false); // false = big-endian
      offset += 4;

      for (let i = 0; i < length; i++) {
        const [timestamp, constantOne, sound_id] = this.recordedEvents[i];
        // Timestamp float big-endian
        this.writeFloatBE(view, timestamp, offset); offset += 4;
        // ConstantOne float big-endian
        this.writeFloatBE(view, constantOne, offset); offset += 4;
        // sound_id unsigned int big-endian
        this.writeUint32BE(view, sound_id, offset); offset += 4;
      }

      const blob = new Blob([buffer], { type: 'application/octet-stream' });

      // Upload to /airdrum/track/
      const formData = new FormData();
      formData.append('name', trackName);
      formData.append('file', blob);

      api.post('/airdrum/track/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        console.log("Track saved:", response.data);
      }).catch(err => {
        console.error("Error saving track:", err);
      });
    },
    writeFloatBE(view, value, offset) {
      // Helper to write float big-endian
      const tempBuffer = new ArrayBuffer(4);
      const tempView = new DataView(tempBuffer);
      tempView.setFloat32(0, value, false);
      view.setUint8(offset, tempView.getUint8(0));
      view.setUint8(offset+1, tempView.getUint8(1));
      view.setUint8(offset+2, tempView.getUint8(2));
      view.setUint8(offset+3, tempView.getUint8(3));
    },
    writeUint32BE(view, value, offset) {
      // Helper to write uint32 big-endian
      view.setUint32(offset, value, false);
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
        if (this.sound) this.sound.play();
        // If recording, record event
        if (this.isRecording) this.recordEventForSound(this.allSounds[this.selectedSoundIndex]);
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
          if (data.command === "kick" && this.kickSound) {
            this.kickSound.play();
            // If recording, record the kick event
            if (this.isRecording) this.recordEventForSound(this.allSounds[this.selectedKickSoundIndex]);
          }
        }
      };
    },
    assignSelectedSounds() {
      if (this.allSounds[this.selectedSoundIndex]) {
        const mainSoundUrl = this.allSounds[this.selectedSoundIndex].sound;
        this.sound = new Howl({
          src: [mainSoundUrl],
          volume: 1.0,
          loop: false,
          html5: true,
          preload: true
        });
      }
      if (this.allSounds[this.selectedKickSoundIndex]) {
        const kickSoundUrl = this.allSounds[this.selectedKickSoundIndex].sound;
        this.kickSound = new Howl({
          src: [kickSoundUrl],
          volume: 1.0,
          loop: false,
          html5: true,
          preload: true
        });
      }
    },
    onSoundPlayed() {
      // If the Controls component emits when a sound is played
      // This can be a generic callback if needed
      if (this.isRecording) this.recordEventForSound(this.allSounds[this.selectedSoundIndex]);
    },
    onKickPlayed() {
      // If Controls emits when a kick sound is played
      if (this.isRecording) this.recordEventForSound(this.allSounds[this.selectedKickSoundIndex]);
    }
  },
};
</script>

