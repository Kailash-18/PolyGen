/**
 * PolyGen 3D Authentication & Gated Security Terminal
 *
 * Infotact Solutions · Project 3 (Backend & 3D Models)
 *
 * SPECIFICATIONS:
 * 1. Initial entrance is strictly the Login Page (Physical/Digital switcher & 3D models hidden).
 * 2. Clean login card (no 3D background canvas clutter).
 * 3. On invalid login attempt, displays strictly: "Wrong credentials".
 * 4. Zero password or credential disclosure anywhere on the screen.
 * 5. On successful login, triggers the 7-slab 3D transit animation and reveals the iPhone 3D model and studio.
 * 6. Single Sign-On (SSO) persists across Physical and Digital studios.
 */

window.PolyGenAuth = (function () {
  const N = 7; // 7 slabs matching lab-transit.js
  let activeTab = "login";

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
    } catch {}
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
  // Clean Login Screen Injection
  // -------------------------------------------------------------
  function injectLoginScreen() {
    if (document.getElementById("polygenLoginScreen")) return;

    const screen = document.createElement("div");
    screen.id = "polygenLoginScreen";
    screen.className = "auth-login-screen";
    screen.innerHTML = `
      <div class="auth-login-card">
        <div class="auth-card-header">
          <div class="auth-badge">PolyGen Security</div>
          <h2 class="auth-card-title" id="authCardTitle">PolyGen 3D Login</h2>
          <p class="auth-card-subtitle" id="authCardSub">Sign in to access 3D studio and engineering models</p>
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
      </div>
    `;

    document.body.appendChild(screen);

    document.getElementById("tabBtnLogin").onclick = () => switchTab("login");
    document.getElementById("tabBtnRegister").onclick = () => switchTab("register");
    document.getElementById("authForm").onsubmit = handleAuthSubmit;
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
    if (cardTitle) cardTitle.textContent = tab === "login" ? "PolyGen 3D Login" : "Create Account";
    if (cardSub) cardSub.textContent = tab === "login" ? "Sign in to access 3D studio and engineering models" : "Create a developer profile for pipeline access";
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
      msg.textContent = "Wrong credentials";
      return;
    }

    msg.className = "auth-msg";
    msg.textContent = "Verifying...";
    submitBtn.disabled = true;

    const endpoint = activeTab === "login" ? "/api/auth/login" : "/api/auth/register";

    try {
      const resp = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      if (!resp.ok) {
        throw new Error("Wrong credentials");
      }

      const data = await resp.json();
      msg.className = "auth-msg success";
      msg.textContent = `Access granted! Welcome, ${data.user.display_name || data.user.username}.`;

      setStoredUser(data.user);

      // Trigger the 7-slab 3D transit animation arriving into the studio
      runSlabTransition("Access Granted", "Welcome Administrator", () => {
        updateNavState();
        console.log("[PolyGenAuth] Studio unlocked for user:", data.user.username);
      });

    } catch (err) {
      msg.className = "auth-msg error";
      msg.textContent = "Wrong credentials";
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
    injectLoginScreen();
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
