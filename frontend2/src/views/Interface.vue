<script>
import * as THREE from 'three';
import DefaultNavbar from "../examples/navbars/NavbarDefault.vue";
import DefaultFooter from "../examples/footers/FooterDefault.vue";

export default {
  components: {
    DefaultNavbar,
    DefaultFooter,
  },
  mounted() {
    this.initialize3DScene();
  },
  methods: {
    initialize3DScene() {
      let homeButton = document.getElementById("home");
      
      let yaw = 0;
      let pitch = 0;
      let roll = 0;

      let yawZero = 0;
      let pitchZero = 0;
      let rollZero = 0;
      homeButton.addEventListener("click", e => {
        yawZero = yaw;
        pitchZero = pitch;
        rollZero = roll;
      });

      const scene = new THREE.Scene();

      // Cámara
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 15;

      const audioListener = new THREE.AudioListener();
      camera.add(audioListener);

      const kick_sound = new THREE.Audio(audioListener);
      const kick_loader = new THREE.AudioLoader();
      kick_loader.load('/static/airdrum/kick_sound.mp3', function (buffer) {
        kick_sound.setBuffer(buffer);
        kick_sound.setLoop(false);
        kick_sound.setVolume(1.0);
      });

      const BASE_URL = "{{base_url}}";
      let url = `ws://${BASE_URL}/ws/socket-server/`;
      console.log(url);
      const stream = new WebSocket(url);
      stream.binaryType = "arraybuffer";

      stream.onmessage = function (e) {
        if ((e.data instanceof ArrayBuffer)) {
          let buffer = e.data;
          let dataView = new DataView(buffer);

          roll = dataView.getFloat64(0, false);
          pitch = dataView.getFloat64(8, false);
          yaw = dataView.getFloat64(16, false);
          return;
        } else if (typeof e.data == "string") {
          let data = JSON.parse(e.data);
          if (data.command == "kick") {
            if (kick_sound && kick_sound.isPlaying) {
              kick_sound.stop();
            }
            if (kick_sound) {
              kick_sound.play();
            }
          }
        } else {
          console.log((e.data instanceof String));
          console.log(typeof e.data);
          console.log("Command");
        }
      };

      // Renderizador
      // Renderizador
      const renderer = new THREE.WebGLRenderer({ alpha: true }); // Configura alpha a true
      renderer.setSize(window.innerWidth, window.innerHeight);
      document.body.appendChild(renderer.domElement);

      // Material
      const baquetaMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 });

      // Crear baquetas
      function createBaqueta() {
        const bodyGeometry = new THREE.CylinderGeometry(0.1, 0.1, 8, 32);
        const body = new THREE.Mesh(bodyGeometry, baquetaMaterial);
        body.rotation.x = Math.PI / 2; // Inicialmente horizontal

        const tipGeometry = new THREE.SphereGeometry(0.2, 32, 32);
        const tip = new THREE.Mesh(tipGeometry, baquetaMaterial);
        tip.name = "tip";
        tip.position.set(0, 4, 0);
        body.add(tip);
        scene.add(body);
        return body;
      }

      const drumMaterial = new THREE.MeshStandardMaterial({ color: 0x808080 });
      const drumGeometry = new THREE.CylinderGeometry(5, 5, 2, 32);
      const drum = new THREE.Mesh(drumGeometry, drumMaterial);
      drum.position.y = -3;
      scene.add(drum);

      const baqueta1 = createBaqueta();
      const baqueta2 = createBaqueta();

      const sound = new THREE.Audio(audioListener);
      const audioLoader = new THREE.AudioLoader();
      audioLoader.load('/static/airdrum/mi-sonido2.mp3', function (buffer) {
        sound.setBuffer(buffer);
        sound.setLoop(false);
        sound.setVolume(1.0);
      });

      // Posiciones iniciales
      baqueta2.position.x = 5;

      // Luz
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
      directionalLight.position.set(10, 10, 10);
      scene.add(directionalLight);

      // Animaciones
      let active = true;
      let debounceTime = 100; // Milliseconds
      let lastPlayTime = 0;

      function animate() {
        requestAnimationFrame(animate);

        baqueta1.rotation.x = (pitch - pitchZero) + Math.PI / 2;
        baqueta1.rotation.y = (yaw - yawZero);
        baqueta1.rotation.z = -(roll - rollZero);

        let tip = baqueta1.getObjectByName("tip");
        const tipGlobalPosition = new THREE.Vector3();
        tip.getWorldPosition(tipGlobalPosition);

        if (active) {
          if (tipGlobalPosition.y + 3.5 <= 1) {
            const currentTime = Date.now();
            if (currentTime - lastPlayTime > debounceTime) {
              if (sound && sound.isPlaying) {
                sound.stop();
              }
              if (sound) {
                sound.play();
                lastPlayTime = currentTime;
                console.log("PUM");
              }
            }
            active = false;
          }
        } else {
          if (tipGlobalPosition.y + 3.5 > 1) {
            active = true;
          }
        }

        renderer.render(scene, camera);
      }
      animate();

      // Responsividad
      window.addEventListener('resize', () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
      });
    }
  }
};
</script>

<template>
 
    <DefaultNavbar
      :action="{
        route: 'javascript:;',
        color: 'btn-white',
      }"
      transparent
    />
    <div id="controls">
      <h3>Controles de Animación para Baqueta 1</h3>
      <button id="home">Home</button>
    </div>
    <DefaultFooter />
 
</template>

<style>
/* Mantener el navbar transparente */
.navbar {
  background: transparent;
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 1000;
}

/* Cambiar el fondo a una imagen */
body {
  background: url('https://images.unsplash.com/photo-1583944000409-00dd0ba1a873?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bXVzaWMlMjB3YWxscGFwZXJ8ZW58MHx8MHx8fDA%3D') no-repeat center center fixed;
  background-size: cover;
}

/* Ajustar los controles debajo del navbar */
#controls {
  position: absolute;
  margin-top: 100px;
  margin-left: 50px;
  background: rgba(255, 255, 255, 0.9);
  padding: 10px;
  border-radius: 8px;
  overflow-y: auto;
  max-height: 90vh;
}

/* Posicionar el footer en la parte final */
footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  background: rgba(255, 255, 255, 0.9); /* Ajusta el fondo del footer si es necesario */
  padding: 10px;
}

canvas {
  display: block;
}

label, input, button {
  display: block;
  margin-bottom: 5px;
}

button {
  cursor: pointer;
}
</style>