<!-- Controller.vue -->
<template>
  <div class="music-player">
    <h3 class="title">Music Player</h3>
    <div class="current-track">
      <p>{{ currentTrackName || 'No Track Selected' }}</p>
    </div>
    <div class="controls">
      <button class="icon-btn play" @click="playMusic(currentTrack)" :title="'Play'">
        <i class="fa fa-play"></i>
      </button>
      <button class="icon-btn pause" @click="pauseMusic" :title="'Pause'">
        <i class="fa fa-pause"></i>
      </button>
      <button class="icon-btn stop" @click="stopMusic" :title="'Stop'">
        <i class="fa fa-stop"></i>
      </button>
    </div>
    <div class="progress-bar">
      <input type="range" min="0" :max="duration" v-model="currentTime" @input="seekMusic">
    </div>
    <div class="volume-control">
      <label>Volume: {{ (volume * 100).toFixed(0) }}%</label>
      <input type="range" min="0" max="1" step="0.01" v-model="volume" @input="setVolume">
    </div>
    <ul class="track-list">
      <li v-for="(track, index) in tracks" :key="index">
        <button class="track-btn" @click="selectTrack(track)">
          <i class="fa fa-music"></i> {{ track.name }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import { Howl } from 'howler';

export default {
  name: 'Controller',
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
      if (!track) return;
      if (this.music) this.music.stop();
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
      if (this.music) this.music.pause();
    },
    stopMusic() {
      if (this.music) {
        this.music.stop();
        this.currentTime = 0;
      }
    },
    seekMusic(event) {
      if (this.music) this.music.seek(event.target.value);
    },
    setVolume(event) {
      if (this.music) this.music.volume(event.target.value);
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
  background: #2c2c2c;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  width: 100%;
  box-sizing: border-box;
  color: #eee;
  font-family: sans-serif;
}

.title {
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: normal;
  color: #fff;
}

.current-track {
  margin-bottom: 15px;
  font-size: 14px;
  font-style: italic;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 15px;
}

.icon-btn {
  border: none;
  background: #444;
  border-radius: 50%;
  width: 40px; height: 40px;
  color: #fff;
  font-size: 16px;
  display:flex;
  align-items:center;
  justify-content:center;
  cursor:pointer;
  transition: background 0.2s;
}
.icon-btn:hover {
  background:#555;
}

.progress-bar {
  margin-bottom: 15px;
}
.progress-bar input[type="range"] {
  width:100%;
}

.volume-control {
  margin-bottom: 15px;
  font-size:14px;
}
.volume-control label {
  display:block;
  margin-bottom:5px;
  color:#ccc;
}
.volume-control input[type="range"] {
  width:100%;
}

.track-list {
  list-style:none;
  padding:0;
  margin:0;
}

.track-list li {
  margin-bottom:10px;
}

.track-btn {
  background:#444;
  border:none;
  border-radius:4px;
  width:100%;
  text-align:left;
  padding:8px;
  color:#fff;
  cursor:pointer;
  display:flex;
  align-items:center;
  gap:8px;
  font-size:14px;
  transition: background 0.2s;
}

.track-btn:hover {
  background:#555;
}

.fa {
  width:16px;
  text-align:center;
}
</style>
