/**
 * PolyGen 3D Authentication & Security Terminal Client
 * Manages Admin Login (username: admin, password: admin), Register,
 * and 3D 7-slab portal warp transitions between the Security Terminal and Studios.
 */

window.PolyGenAuth = (function () {
  const N = 7; // 7 slabs matching lab-transit.js
  let activeTab = "login";

  function getStoredUser() {
    try {
      const u = sessionStorage.getItem("polygen_auth");
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  }

  function setStoredUser(user) {
    try {
      if (user) {
        sessionStorage.setItem("polygen_auth", JSON.stringify(user));
      } else {
        sessionStorage.removeItem("polygen_auth");
      }
    } catch {}
  }

  // Exact 7-slab 3D transit animation builder (same as lab-transit.js)
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
      // 2. Slabs fly apart toward you in 3D perspective
      setTimeout(() => {
        o.classList.remove("closing");
        o.classList.add("opening");
        setTimeout(() => o.remove(), 1200);
      }, 350);
    }, 700);
  }

  function injectNavbarButton() {
    const actions = document.querySelector("header.vre-nav .actions");
    if (!actions || document.getElementById("navLoginBtn")) return;

    const btn = document.createElement("button");
    btn.id = "navLoginBtn";
    btn.className = "auth-pill-btn";
    btn.type = "button";

    const user = getStoredUser();
    if (user) {
      btn.classList.add("logged-in");
      btn.innerHTML = `<span class="auth-dot"></span> <span>${user.username} (Admin)</span>`;
    } else {
      btn.innerHTML = `<span class="auth-dot"></span> <span>Sign In</span>`;
    }

    btn.onclick = () => {
      const currentUser = getStoredUser();
      if (currentUser) {
        if (confirm(`Currently signed in as ${currentUser.display_name || currentUser.username} (SuperAdmin).\n\nWould you like to log out?`)) {
          setStoredUser(null);
          updateNavState();
          runSlabTransition("Signed Out", "Session Terminated", () => {});
        }
      } else {
        // Run slab transition into the login terminal
        runSlabTransition("Security Gateway", "Administrator Authentication", () => {
          openAuthOverlay();
        });
      }
    };

    // Prepend or append to actions
    actions.appendChild(btn);
  }

  function updateNavState() {
    const btn = document.getElementById("navLoginBtn");
    if (!btn) return;
    const user = getStoredUser();
    if (user) {
      btn.classList.add("logged-in");
      btn.innerHTML = `<span class="auth-dot"></span> <span>${user.username} (Admin)</span>`;
    } else {
      btn.classList.remove("logged-in");
      btn.innerHTML = `<span class="auth-dot"></span> <span>Sign In</span>`;
    }
  }

  function injectAuthOverlay() {
    if (document.getElementById("authOverlay")) return;

    const overlay = document.createElement("div");
    overlay.id = "authOverlay";
    overlay.className = "auth-overlay";
    overlay.innerHTML = `
      <div class="auth-card">
        <button class="auth-close-btn" id="authCloseBtn" title="Close">&times;</button>
        <div class="auth-header">
          <div class="auth-badge">PolyGen Core Security</div>
          <h2 class="auth-title" id="authTitle">Admin Portal</h2>
          <p class="auth-subtitle">Sign in to access advanced 3D engineering & full studio models</p>
        </div>

        <div class="auth-tabs">
          <button class="auth-tab-btn active" id="tabBtnLogin" type="button">Sign In</button>
          <button class="auth-tab-btn" id="tabBtnRegister" type="button">Register</button>
        </div>

        <form id="authForm">
          <div class="auth-form-group">
            <label class="auth-label" for="authUsernameInput">Username</label>
            <input class="auth-input" id="authUsernameInput" type="text" value="admin" autocomplete="username" required />
          </div>

          <div class="auth-form-group">
            <label class="auth-label" for="authPasswordInput">Password</label>
            <input class="auth-input" id="authPasswordInput" type="password" value="admin" autocomplete="current-password" required />
          </div>

          <div class="auth-helper-chip" id="autoFillAdminChip" title="Click to fill default admin credentials">
            <span>⚡</span> Default credentials: <b>admin / admin</b>
          </div>

          <button class="auth-submit-btn" id="authSubmitBtn" type="submit">
            Enter PolyGen Studio
          </button>
          <div class="auth-msg" id="authMsg"></div>
        </form>
      </div>
    `;

    document.body.appendChild(overlay);

    // Event handlers
    document.getElementById("authCloseBtn").onclick = closeAuthOverlay;
    document.getElementById("autoFillAdminChip").onclick = () => {
      document.getElementById("authUsernameInput").value = "admin";
      document.getElementById("authPasswordInput").value = "admin";
    };

    document.getElementById("tabBtnLogin").onclick = () => switchTab("login");
    document.getElementById("tabBtnRegister").onclick = () => switchTab("register");

    document.getElementById("authForm").onsubmit = handleAuthSubmit;
  }

  function switchTab(tab) {
    activeTab = tab;
    document.getElementById("tabBtnLogin").classList.toggle("active", tab === "login");
    document.getElementById("tabBtnRegister").classList.toggle("active", tab === "register");
    document.getElementById("authTitle").textContent = tab === "login" ? "Admin Portal" : "New Account";
    document.getElementById("authSubmitBtn").textContent = tab === "login" ? "Enter PolyGen Studio" : "Create Developer Account";
    document.getElementById("authMsg").textContent = "";
  }

  function openAuthOverlay() {
    const o = document.getElementById("authOverlay");
    if (o) {
      o.classList.add("active");
      document.getElementById("authUsernameInput").focus();
    }
  }

  function closeAuthOverlay() {
    const o = document.getElementById("authOverlay");
    if (o) o.classList.remove("active");
  }

  async function handleAuthSubmit(e) {
    e.preventDefault();
    const username = document.getElementById("authUsernameInput").value.trim();
    const password = document.getElementById("authPasswordInput").value.trim();
    const submitBtn = document.getElementById("authSubmitBtn");
    const msg = document.getElementById("authMsg");

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
      updateNavState();

      // Close login card
      closeAuthOverlay();

      // Trigger the 7-slab transit animation arriving into the full studio
      runSlabTransition("Access Granted", "Welcome Administrator", () => {
        // Trigger sample load or ensure iPhone/laptop 3D models load
        console.log("[PolyGenAuth] Authenticated as Admin successfully.");
      });

    } catch (err) {
      msg.className = "auth-msg error";
      msg.textContent = err.message;
    } finally {
      submitBtn.disabled = false;
    }
  }

  function init() {
    injectNavbarButton();
    injectAuthOverlay();
    updateNavState();
  }

  return {
    init: init,
    openAuthOverlay: openAuthOverlay,
    closeAuthOverlay: closeAuthOverlay,
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
