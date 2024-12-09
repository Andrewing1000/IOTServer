<template>
  <div class="visualizer">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import { Howl, Howler } from 'howler';

export default {
  data() {
    return {
      analyser: null,
      dataArray: null,
      bufferLength: null,
      canvasCtx: null,
      animationId: null,
    };
  },
  mounted() {
    this.setupVisualizer();
  },
  beforeDestroy() {
    cancelAnimationFrame(this.animationId);
  },
  methods: {
    setupVisualizer() {
      const canvas = this.$refs.canvas;
      this.canvasCtx = canvas.getContext('2d');
      canvas.width = window.innerWidth;
      canvas.height = 200;

      const audioCtx = Howler.ctx;
      if (!audioCtx) {
        console.error('Audio context is not available.');
        return;
      }

      this.analyser = audioCtx.createAnalyser();
      Howler.masterGain.connect(this.analyser);
      this.analyser.connect(audioCtx.destination);

      this.analyser.fftSize = 256;
      this.bufferLength = this.analyser.frequencyBinCount;
      this.dataArray = new Uint8Array(this.bufferLength);

      this.draw();
    },
    draw() {
      this.animationId = requestAnimationFrame(this.draw);

      this.analyser.getByteFrequencyData(this.dataArray);

      this.canvasCtx.fillStyle = 'rgb(0, 0, 0)';
      this.canvasCtx.fillRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height);

      const barWidth = (this.$refs.canvas.width / this.bufferLength) * 2.5;
      let barHeight;
      let x = 0;

      for (let i = 0; i < this.bufferLength; i++) {
        barHeight = this.dataArray[i];

        this.canvasCtx.fillStyle = 'rgb(' + (barHeight + 100) + ',50,50)';
        this.canvasCtx.fillRect(x, this.$refs.canvas.height - barHeight / 2, barWidth, barHeight / 2);

        x += barWidth + 1;
      }
    }
  }
};
</script>

<style scoped>
.visualizer {
  width: 100%;
  height: 200px;
  background-color: #000;
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
}
</style>