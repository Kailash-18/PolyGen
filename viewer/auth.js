/**
 * PolyGen 3D Gated Authentication & Interactive 3D Portal Gateway
 *
 * Infotact Solutions · Project 3 (Backend & 3D Models)
 *
 * GATING SPECIFICATIONS:
 * 1. On initial load, strictly gates the site (hides Physical/Digital switcher, 3D phone model, laptops, and gallery).
 * 2. Renders an interactive 3D WebGL portal background (Three.js gimbal rings, rotating holographic core, particle dust motes, mouse parallax).
 * 3. Shows Project Name "PolyGen 3D" and topbar with only [Login] / [Register] actions.
 * 4. Empty inputs (no default pre-filled credentials; user types manually).
 * 5. Single Sign-On (SSO): Entering credentials once unlocks both Physical and Digital studios.
 * 6. Submitting credentials triggers the exact 7-slab 3D transit animation ("Access Granted — Welcome Administrator").
 * 7. Logging out plays the 7-slab 3D transit and returns cleanly to the 3D portal.
 */

window.PolyGenAuth = (function () {
  const N = 7; // 7 slabs matching lab-transit.js
  let activeTab = "login";
  let threeScene = null;
  let animFrameId = null;

  function getStoredUser() {
    try {
      const u = localStorage.getItem("polygen_auth") || sessionStorage.getItem("polygen_auth");
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  }

  function setStoredUser(user) {
    try {
      if (user) {
        const str = JSON.stringify(user);
        localStorage.setItem("polygen_auth", str);
        sessionStorage.setItem("polygen_auth", str);
      } else {
        localStorage.removeItem("polygen_auth");
        sessionStorage.removeItem("polygen_auth");
      }
    } catch { }
  }

  // Exact 7-slab 3D transit animation builder (same cinematic perspective as lab-transit.js)
  function runSlabTransition(mainTitle, subTitle, callback) {
    const o = document.createElement("div");
    o.className = "lab-transit lt-physical";
    o.setAttribute("aria-hidden", "true");
    o.style.zIndex = "10005";

    for (let i = 0; i < N; i++) {
      const s = document.createElement("i");
      const c = i - (N - 1) / 2;
      s.style.setProperty("--i", i);
      s.style.setProperty("--c", c);
      s.style.setProperty("--y0", (i % 2 ? 104 : -104) + "%");
      s.style.setProperty("--rx0", (i % 2 ? -1 : 1) * 24 + "deg");
      s.style.setProperty("--d1", i * 0.045 + "s");
      s.style.setProperty("--d2", Math.abs(c) * 0.05 + "s");
      o.append(s);
    }

    const t = document.createElement("div");
    t.className = "lt-title";
    t.style.opacity = "1";
    t.style.transform = "scale(1)";
    t.style.transition = "transform 0.4s ease, opacity 0.4s ease";

    const b = document.createElement("b");
    const sp = document.createElement("span");
    b.textContent = mainTitle;
    sp.textContent = subTitle;
    t.append(b, sp);
    o.append(t);
    document.body.append(o);

    // 1. Slabs close over the screen
    void o.offsetWidth;
    o.classList.add("closing");

    setTimeout(() => {
      if (typeof callback === "function") callback();
      // 2. Slabs fly apart toward camera in 3D perspective
      setTimeout(() => {
        o.classList.remove("closing");
        o.classList.add("opening");
        setTimeout(() => o.remove(), 1200);
      }, 380);
    }, 720);
  }

  // -------------------------------------------------------------
  // Interactive Three.js 3D WebGL Portal Background
  // -------------------------------------------------------------
  function init3DPortal(canvas) {
    if (!canvas || !window.THREE) return;

    try {
      const THREE = window.THREE;
      const width = canvas.parentElement.clientWidth || window.innerWidth;
      const height = canvas.parentElement.clientHeight || window.innerHeight;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(48, width / height, 0.1, 1000);
      camera.position.z = 28;

      const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        powerPreference: "high-performance"
      });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setSize(width, height);

      // Root interactive group
      const rootGroup = new THREE.Group();
      scene.add(rootGroup);

      // 1. Outer Icosahedron Wireframe
      const outerGeo = new THREE.IcosahedronGeometry(7.2, 1);
      const outerMat = new THREE.MeshBasicMaterial({
        color: 0x00f0ff,
        wireframe: true,
        transparent: true,
        opacity: 0.32
      });
      const outerMesh = new THREE.Mesh(outerGeo, outerMat);
      rootGroup.add(outerMesh);

      // 2. Inner Faceted Hologram Core
      const innerGeo = new THREE.OctahedronGeometry(4.5, 0);
      const innerMat = new THREE.MeshStandardMaterial({
        color: 0x8b7bff,
        emissive: 0x1f1144,
        roughness: 0.25,
        metalness: 0.85,
        wireframe: true
      });
      const innerMesh = new THREE.Mesh(innerGeo, innerMat);
      rootGroup.add(innerMesh);

      // 3. Central Glowing Energy Node
      const coreGeo = new THREE.DodecahedronGeometry(2.3, 0);
      const coreMat = new THREE.MeshStandardMaterial({
        color: 0x5ee6ff,
        emissive: 0x00d4ff,
        emissiveIntensity: 0.75,
        roughness: 0.1,
        metalness: 0.95
      });
      const coreMesh = new THREE.Mesh(coreGeo, coreMat);
      rootGroup.add(coreMesh);

      // 4. Gimbal Orbital Torus Rings
      const ringGroup = new THREE.Group();
      rootGroup.add(ringGroup);

      const ring1Geo = new THREE.TorusGeometry(10.2, 0.06, 16, 100);
      const ring1Mat = new THREE.MeshBasicMaterial({ color: 0x5ee6ff, transparent: true, opacity: 0.55 });
      const ring1 = new THREE.Mesh(ring1Geo, ring1Mat);
      ring1.rotation.x = Math.PI / 4;
      ringGroup.add(ring1);

      const ring2Geo = new THREE.TorusGeometry(12.6, 0.05, 16, 100);
      const ring2Mat = new THREE.MeshBasicMaterial({ color: 0x8b7bff, transparent: true, opacity: 0.45 });
      const ring2 = new THREE.Mesh(ring2Geo, ring2Mat);
      ring2.rotation.y = Math.PI / 3;
      ring2.rotation.z = Math.PI / 6;
      ringGroup.add(ring2);

      const ring3Geo = new THREE.TorusGeometry(15.0, 0.05, 16, 100);
      const ring3Mat = new THREE.MeshBasicMaterial({ color: 0xff007f, transparent: true, opacity: 0.4 });
      const ring3 = new THREE.Mesh(ring3Geo, ring3Mat);
      ring3.rotation.x = -Math.PI / 5;
      ring3.rotation.z = Math.PI / 2.5;
      ringGroup.add(ring3);

      // Satellite beacons on rings
      const beaconGeo = new THREE.SphereGeometry(0.22, 12, 12);
      const beaconMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff });
      for (let b = 0; b < 6; b++) {
        const beacon = new THREE.Mesh(beaconGeo, beaconMat);
        const ang = (b / 6) * Math.PI * 2;
        beacon.position.set(Math.cos(ang) * 10.2, Math.sin(ang) * 10.2, 0);
        ring1.add(beacon);
      }

      // 5. Floating Cosmic Dust Particles
      const particleCount = 1200;
      const particlePos = new Float32Array(particleCount * 3);
      for (let p = 0; p < particleCount * 3; p += 3) {
        const r = 16 + Math.random() * 32;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(Math.random() * 2 - 1);
        particlePos[p] = r * Math.sin(phi) * Math.cos(theta);
        particlePos[p + 1] = r * Math.sin(phi) * Math.sin(theta);
        particlePos[p + 2] = r * Math.cos(phi);
      }
      const particleGeo = new THREE.BufferGeometry();
      particleGeo.setAttribute("position", new THREE.BufferAttribute(particlePos, 3));
      const particleMat = new THREE.PointsMaterial({
        color: 0x5ee6ff,
        size: 0.55,
        transparent: true,
        opacity: 0.65,
        blending: THREE.AdditiveBlending
      });
      const particles = new THREE.Points(particleGeo, particleMat);
      scene.add(particles);

      // 6. Lighting
      const ambLight = new THREE.AmbientLight(0x0a1224, 2.0);
      scene.add(ambLight);

      const ptLight1 = new THREE.PointLight(0x00f0ff, 3.0, 50);
      ptLight1.position.set(16, 16, 14);
      scene.add(ptLight1);

      const ptLight2 = new THREE.PointLight(0xff007f, 2.5, 50);
      ptLight2.position.set(-16, -16, 12);
      scene.add(ptLight2);

      // 7. Interactive Parallax & Focus Reactivity
      let targetRotX = 0;
      let targetRotY = 0;
      let targetSpeed = 1.0;
      let currentSpeed = 1.0;

      const onPointerMove = (e) => {
        const nx = (e.clientX / window.innerWidth) * 2 - 1;
        const ny = (e.clientY / window.innerHeight) * 2 - 1;
        targetRotY = nx * 0.5;
        targetRotX = -ny * 0.4;
      };
      window.addEventListener("pointermove", onPointerMove);

      const onResize = () => {
        const w = window.innerWidth;
        const h = window.innerHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      };
      window.addEventListener("resize", onResize);

      // Input focus acceleration
      const setExcitedSpeed = (active) => {
        targetSpeed = active ? 3.0 : 1.0;
      };

      const inputs = [document.getElementById("authUsernameInput"), document.getElementById("authPasswordInput")];
      inputs.forEach((inp) => {
        if (inp) {
          inp.addEventListener("focus", () => setExcitedSpeed(true));
          inp.addEventListener("blur", () => setExcitedSpeed(false));
          inp.addEventListener("input", () => {
            targetSpeed = 4.2;
            setTimeout(() => { if (document.activeElement === inp) targetSpeed = 3.0; }, 300);
          });
        }
      });

      // Render Loop
      let clock = new THREE.Clock();

      function animate() {
        animFrameId = requestAnimationFrame(animate);

        // Sleep when unlocked to save GPU
        if (!document.documentElement.classList.contains("auth-gated")) {
          return;
        }

        const delta = clock.getDelta();
        currentSpeed += (targetSpeed - currentSpeed) * 0.08;

        // Mouse Parallax Lerp
        rootGroup.rotation.y += (targetRotY - rootGroup.rotation.y) * 0.05;
        rootGroup.rotation.x += (targetRotX - rootGroup.rotation.x) * 0.05;

        // Autonomous Rotations
        outerMesh.rotation.y += 0.25 * delta * currentSpeed;
        outerMesh.rotation.z += 0.15 * delta * currentSpeed;

        innerMesh.rotation.y -= 0.45 * delta * currentSpeed;
        innerMesh.rotation.x += 0.3 * delta * currentSpeed;

        coreMesh.rotation.x += 0.6 * delta * currentSpeed;
        coreMesh.rotation.y += 0.6 * delta * currentSpeed;

        ring1.rotation.z += 0.35 * delta * currentSpeed;
        ring2.rotation.x += 0.28 * delta * currentSpeed;
        ring3.rotation.y += 0.22 * delta * currentSpeed;

        particles.rotation.y += 0.04 * delta;

        renderer.render(scene, camera);
      }

      animate();

      threeScene = {
        renderer,
        destroy: () => {
          if (animFrameId) cancelAnimationFrame(animFrameId);
          window.removeEventListener("pointermove", onPointerMove);
          window.removeEventListener("resize", onResize);
          renderer.dispose();
        }
      };
    } catch (err) {
      console.warn("[PolyGenAuth] Three.js portal initialization skipped:", err);
    }
  }

  // -------------------------------------------------------------
  // Gateway UI Injection
  // -------------------------------------------------------------
  function injectGatewayScreen() {
    if (document.getElementById("polygenAuthGateway")) return;

    const screen = document.createElement("div");
    screen.id = "polygenAuthGateway";
    screen.className = "auth-gateway-screen";
    screen.innerHTML = `
      <canvas id="auth3DCanvas"></canvas>

      <div class="auth-gateway-content">
        <!-- Left Showcase Column: Capabilities & Pipeline -->
        <div class="auth-showcase">
          <div class="auth-showcase-badge">
            <span class="pulse-dot"></span>
            <span>PolyGen 3D Engine · Generative Pipeline</span>
          </div>
          <h1 class="auth-showcase-title">
            Unified 3D Studio & <span class="grad">Asset Engine</span>
          </h1>
          <p class="auth-showcase-desc">
            High-fidelity generative text-to-3D asset synthesis, multi-LOD decimation, real-time kinematics, and automated Unreal Engine 5 & Unity pipeline exports.
          </p>

          <div class="auth-features-grid">
            <div class="auth-feat-card">
              <div class="auth-feat-head">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                <span>TripoSR Fast Meshing</span>
              </div>
              <p class="auth-feat-desc">Sub-second neural geometry extraction with watertight manifold verification and instant GLB synthesis.</p>
            </div>

            <div class="auth-feat-card">
              <div class="auth-feat-head">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 22 22 22"/></svg>
                <span>QEM Multi-LOD Engine</span>
              </div>
              <p class="auth-feat-desc">Quadric error decimation with automated LOD0–LOD3 hierarchy generation and Hausdorff error bounds.</p>
            </div>

            <div class="auth-feat-card">
              <div class="auth-feat-head">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/></svg>
                <span>PBR Texture Presets</span>
              </div>
              <p class="auth-feat-desc">Albedo, roughness, metallic, normal, and emissive baking with 5600K studio HDRI lighting rigs.</p>
            </div>

            <div class="auth-feat-card">
              <div class="auth-feat-head">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
                <span>Game Engine Exporter</span>
              </div>
              <p class="auth-feat-desc">Automated export to Unreal Engine 5 Nanite ZIP packages & Unity URP Prefabs with UCX collision hulls.</p>
            </div>
          </div>

          <div class="auth-telemetry-bar">
            <span>⚡ Latency: 12ms</span>
            <span>🛡️ SSO: AES-256 JWT</span>
            <span>🎮 Nanite: Verified</span>
            <span>📦 API: v1.2.0 Active</span>
          </div>
        </div>

        <!-- Right Column: Glassmorphic Security Terminal Card -->
        <div class="auth-gateway-card">
          <div class="auth-card-header">
            <h2 class="auth-card-title" id="authCardTitle">Security Terminal</h2>
            <p class="auth-card-subtitle" id="authCardSub">Sign in with administrator credentials to enter the studio</p>
          </div>

          <div class="auth-tabs">
            <button class="auth-tab-btn active" id="tabBtnLogin" type="button">Sign In</button>
            <button class="auth-tab-btn" id="tabBtnRegister" type="button">Register</button>
          </div>

          <form id="authForm" autocomplete="off">
            <div class="auth-form-group">
              <label class="auth-label" for="authUsernameInput">Username</label>
              <input class="auth-input" id="authUsernameInput" type="text" placeholder="Enter username" autocomplete="off" required />
            </div>

            <div class="auth-form-group">
              <label class="auth-label" for="authPasswordInput">Password</label>
              <input class="auth-input" id="authPasswordInput" type="password" placeholder="Enter password" autocomplete="off" required />
            </div>

            <button class="auth-submit-btn" id="authSubmitBtn" type="submit">
              Enter PolyGen Studio
            </button>
            <div class="auth-msg" id="authMsg"></div>
          </form>

          <div class="auth-role-hint">
            Infotact Solutions · Project 3 (Backend & 3D Models)<br/>
            PolyGen Security Gateway · Authorized Personnel Only
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(screen);

    document.getElementById("tabBtnLogin").onclick = () => switchTab("login");
    document.getElementById("tabBtnRegister").onclick = () => switchTab("register");
    document.getElementById("authForm").onsubmit = handleAuthSubmit;

    // Initialize 3D canvas
    const canvas = document.getElementById("auth3DCanvas");
    if (canvas) {
      if (window.THREE) {
        init3DPortal(canvas);
      } else {
        window.addEventListener("load", () => {
          if (window.THREE) init3DPortal(canvas);
        });
      }
    }
  }

  // -------------------------------------------------------------
  // Top Navbar Cluster Injection
  // -------------------------------------------------------------
  function injectNavbarButtons() {
    const actions = document.querySelector("header.vre-nav .actions");
    if (!actions || document.getElementById("authNavCluster")) return;

    const cluster = document.createElement("div");
    cluster.id = "authNavCluster";
    cluster.style.display = "inline-flex";
    cluster.style.alignItems = "center";
    cluster.style.gap = "8px";

    actions.appendChild(cluster);
    updateNavState();
  }

  function updateNavState() {
    const cluster = document.getElementById("authNavCluster");
    const user = getStoredUser();

    if (!user) {
      // User is NOT logged in: Lock the app to Login Gateway
      document.documentElement.classList.add("auth-gated");

      if (cluster) {
        cluster.innerHTML = `
          <button type="button" class="auth-pill-btn" onclick="PolyGenAuth.switchTab('login')">
            <span class="auth-dot"></span> <span>Login</span>
          </button>
          <button type="button" class="auth-pill-btn" onclick="PolyGenAuth.switchTab('register')" style="background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.2);">
            <span>Register</span>
          </button>
        `;
      }
    } else {
      // User IS logged in: Unlock studio
      document.documentElement.classList.remove("auth-gated");

      if (cluster) {
        cluster.innerHTML = `
          <div class="auth-pill-btn logged-in" style="cursor: default;">
            <span class="auth-dot"></span> <span>${user.username} (Admin)</span>
          </div>
          <button type="button" class="auth-pill-btn" onclick="PolyGenAuth.logout()" style="background: rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.4); color: #fca5a5;">
            <span>Log Out</span>
          </button>
        `;
      }
    }
  }

  function switchTab(tab) {
    activeTab = tab;
    const btnL = document.getElementById("tabBtnLogin");
    const btnR = document.getElementById("tabBtnRegister");
    const submitBtn = document.getElementById("authSubmitBtn");
    const cardTitle = document.getElementById("authCardTitle");
    const cardSub = document.getElementById("authCardSub");
    const msg = document.getElementById("authMsg");

    if (btnL) btnL.classList.toggle("active", tab === "login");
    if (btnR) btnR.classList.toggle("active", tab === "register");
    if (cardTitle) cardTitle.textContent = tab === "login" ? "Security Terminal" : "Developer Registration";
    if (cardSub) cardSub.textContent = tab === "login" ? "Sign in with administrator credentials to enter the studio" : "Create a developer profile for pipeline access";
    if (submitBtn) submitBtn.textContent = tab === "login" ? "Enter PolyGen Studio" : "Create Developer Account";
    if (msg) msg.textContent = "";

    const uInput = document.getElementById("authUsernameInput");
    if (uInput) {
      uInput.value = "";
      uInput.focus();
    }
    const pInput = document.getElementById("authPasswordInput");
    if (pInput) pInput.value = "";
  }

  async function handleAuthSubmit(e) {
    e.preventDefault();
    const username = document.getElementById("authUsernameInput").value.trim();
    const password = document.getElementById("authPasswordInput").value.trim();
    const submitBtn = document.getElementById("authSubmitBtn");
    const msg = document.getElementById("authMsg");

    if (!username || !password) {
      msg.className = "auth-msg error";
      msg.textContent = "Please enter both username and password.";
      return;
    }

    msg.className = "auth-msg";
    msg.textContent = "Verifying security credentials...";
    submitBtn.disabled = true;

    const endpoint = activeTab === "login" ? "/api/auth/login" : "/api/auth/register";

    try {
      const resp = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      const data = await resp.json();

      if (!resp.ok) {
        throw new Error(data.detail || "Authentication rejected");
      }

      msg.className = "auth-msg success";
      msg.textContent = `Access granted! Welcome, ${data.user.display_name || data.user.username}.`;

      setStoredUser(data.user);

      // Trigger the exact 7-slab 3D transit animation arriving into the studio
      runSlabTransition("Access Granted", "Welcome Administrator", () => {
        updateNavState();
        console.log("[PolyGenAuth] Studio unlocked for user:", data.user.username);
      });

    } catch (err) {
      msg.className = "auth-msg error";
      msg.textContent = err.message;
    } finally {
      submitBtn.disabled = false;
    }
  }

  function logout() {
    if (confirm("Sign out of PolyGen 3D Studio?")) {
      runSlabTransition("Signed Out", "Session Terminated", () => {
        setStoredUser(null);
        updateNavState();
        switchTab("login");
      });
    }
  }

  function init() {
    injectNavbarButtons();
    injectGatewayScreen();
    updateNavState();

    window.addEventListener("storage", (e) => {
      if (e.key === "polygen_auth") updateNavState();
    });
  }

  return {
    init: init,
    switchTab: switchTab,
    logout: logout,
    getStoredUser: getStoredUser,
    runSlabTransition: runSlabTransition
  };
})();

// Auto-boot
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", window.PolyGenAuth.init);
} else {
  window.PolyGenAuth.init();
}
