<template>
  <div class="music-player">
    <h3>Music Player</h3>
    <div class="current-track">
      <p>{{ currentTrackName }}</p>
    </div>
    <div class="controls">
      <button class="btn btn-primary" @click="playMusic(currentTrack)">Play</button>
      <button class="btn btn-warning" @click="pauseMusic">Pause</button>
      <button class="btn btn-danger" @click="stopMusic">Stop</button>
    </div>
    <div class="progress-bar">
      <input type="range" min="0" :max="duration" v-model="currentTime" @input="seekMusic">
    </div>
    <div class="volume-control">
      <label for="volume">Volume: {{ volume * 100}}</label>
      <input type="range" id="volume" min="0" max="1" step="0.01" v-model="volume" @input="setVolume">
    </div>
    <ul class="track-list">
      <li v-for="(track, index) in tracks" :key="index">
        <button class="btn btn-secondary" @click="selectTrack(track)">{{ track.name }}</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { Howl } from 'howler';
import Swal from 'sweetalert2';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  data() {
    return {
      music: null,
      currentTrack: null,
      currentTrackName: '',
      currentTime: 0,
      duration: 0,
      volume: 1.0,
      tracks: [
        { name: 'Ambient_Rock', src: () => import('@/assets/music/Ambient_Rock.mp3') },
        { name: 'Energetic_Rock_Track', src: () => import('@/assets/music/Energetic_Rock_Track.mp3') },
        { name: 'Funky_Soul_Disco_Track', src: () => import('@/assets/music/Funky_Soul_Disco_Track.mp3') },
        { name: 'Hip_Hop_Neo_Soul', src: () => import('@/assets/music/Hip_Hop_Neo_Soul.mp3') },
        { name: 'Soulful_Funk_Fusion_Drumless', src: () => import('@/assets/music/Soulful_Funk_Fusion_Drumless.mp3') }
      ]
    };
  },
  methods: {
    selectTrack(track) {
      this.currentTrack = track;
      this.currentTrackName = track.name;
      this.playMusic(track);
    },
    playMusic(track) {
      if (!track) {
        Swal.fire('Error', 'No track selected.', 'error');
        return;
      }

      if (this.music) {
        this.music.stop();
      }
      track.src().then((module) => {
        this.music = new Howl({
          src: [module.default],
          volume: this.volume,
          loop: true,
          onplay: () => {
            this.duration = this.music.duration();
            requestAnimationFrame(this.updateProgress);
          }
        });
        this.music.play();
      });
    },
    pauseMusic() {
      if (this.music) {
        this.music.pause();
      }
    },
    stopMusic() {
      if (this.music) {
        this.music.stop();
        this.currentTime = 0;
      }
    },
    seekMusic(event) {
      if (this.music) {
        this.music.seek(event.target.value);
      }
    },
    setVolume(event) {
      if (this.music) {
        this.music.volume(event.target.value);
      }
    },
    updateProgress() {
      if (this.music && this.music.playing()) {
        this.currentTime = this.music.seek();
        requestAnimationFrame(this.updateProgress);
      }
    }
  }
};
</script>

<style scoped>
.music-player {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 100%;
  margin: 0 auto;
}

.current-track {
  margin-bottom: 10px;
}

.controls {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.controls button {
  margin: 0 5px;
}

.progress-bar {
  margin-bottom: 10px;
}

.volume-control {
  margin-bottom: 10px;
}

.track-list {
  list-style: none;
  padding: 0;
}

.track-list li {
  margin-bottom: 5px;
  
}

.track-list button {
  width: 100%;
  text-align: left;
  padding: 5px;
  border: none;
  background: none;
  cursor: pointer;
  
  color: black;
}

.track-list button:hover {
  background: rgba(91, 231, 10, 0.918);
}
</style>