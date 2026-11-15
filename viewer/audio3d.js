// PolyGen Audio3D Engine - Procedural Web Audio API Sound Synthesizer
// Generates dynamic mechanical audio feedback for 3D exploded views and kinematics in real time.
// Zero external audio files or dependencies; 100% procedurally synthesized in the browser.

class ProceduralSynthesizer {
  constructor() {
    this.ctx = null;
    this.enabled = true;
    this.lastExplode = 0;
    this.lastTickTime = 0;
  }

  ensureContext() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === "suspended") {
      this.ctx.resume().catch(() => {});
    }
  }

  // Metallic snap when assembly snaps completely shut
  playSnapLock() {
    if (!this.enabled) return;
    this.ensureContext();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;
    
    // Crisp primary impulse
    const osc1 = this.ctx.createOscillator();
    const gain1 = this.ctx.createGain();
    osc1.type = "triangle";
    osc1.frequency.setValueAtTime(320, t);
    osc1.frequency.exponentialRampToValueAtTime(70, t + 0.08);

    gain1.gain.setValueAtTime(0.35, t);
    gain1.gain.exponentialRampToValueAtTime(0.001, t + 0.12);

    osc1.connect(gain1);
    gain1.connect(this.ctx.destination);
    osc1.start(t);
    osc1.stop(t + 0.13);

    // High metallic resonant ping
    const osc2 = this.ctx.createOscillator();
    const gain2 = this.ctx.createGain();
    osc2.type = "sine";
    osc2.frequency.setValueAtTime(1480, t + 0.01);
    osc2.frequency.exponentialRampToValueAtTime(800, t + 0.22);

    gain2.gain.setValueAtTime(0.18, t + 0.01);
    gain2.gain.exponentialRampToValueAtTime(0.0001, t + 0.24);

    osc2.connect(gain2);
    gain2.connect(this.ctx.destination);
    osc2.start(t + 0.01);
    osc2.stop(t + 0.25);
  }

  // Soft pneumatic hiss when parts separate
  playPneumaticRelease() {
    if (!this.enabled) return;
    this.ensureContext();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;
    const dur = 0.28;
    const bufferSize = this.ctx.sampleRate * dur;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);

    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1;
    }

    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;

    const filter = this.ctx.createBiquadFilter();
    filter.type = "bandpass";
    filter.frequency.setValueAtTime(1800, t);
    filter.frequency.exponentialRampToValueAtTime(600, t + dur);
    filter.Q.value = 3.5;

    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.12, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + dur);

    noise.connect(filter);
    filter.connect(gain);
    gain.connect(this.ctx.destination);

    noise.start(t);
  }

  // High-tech UI click for hover & selection
  playPartSelect(freq = 640) {
    if (!this.enabled) return;
    this.ensureContext();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = "sine";
    osc.frequency.setValueAtTime(freq, t);
    osc.frequency.exponentialRampToValueAtTime(freq * 1.5, t + 0.06);

    gain.gain.setValueAtTime(0.15, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.08);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(t);
    osc.stop(t + 0.09);
  }

  // Dynamic mechanical servo clicks during continuous explosion scrubbing
  updateExplodeAudio(explodeValue) {
    if (!this.enabled) return;
    const now = performance.now();
    const delta = Math.abs(explodeValue - this.lastExplode);

    if (delta > 0.03 && now - this.lastTickTime > 75) {
      this.ensureContext();
      if (!this.ctx) return;

      const t = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      const pitch = 220 + explodeValue * 450;
      osc.type = "sawtooth";
      osc.frequency.setValueAtTime(pitch, t);
      osc.frequency.exponentialRampToValueAtTime(pitch * 0.7, t + 0.04);

      gain.gain.setValueAtTime(0.04, t);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.045);

      const filter = this.ctx.createBiquadFilter();
      filter.type = "lowpass";
      filter.frequency.value = 1400;

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(t);
      osc.stop(t + 0.05);

      this.lastTickTime = now;
    }

    if (this.lastExplode > 0.05 && explodeValue <= 0.001) {
      this.playSnapLock();
    } else if (this.lastExplode <= 0.01 && explodeValue > 0.05) {
      this.playPneumaticRelease();
    }

    this.lastExplode = explodeValue;
  }
}

export const soundFx = new ProceduralSynthesizer();
if (typeof window !== "undefined") {
  window.__soundFx = soundFx;
}

export function installAudio(View) {
  const P = View.prototype;
  const originalSetExploded = P.setExploded;

  P.setExploded = function (t) {
    if (originalSetExploded) originalSetExploded.call(this, t);
    soundFx.updateExplodeAudio(t);
  };
}
