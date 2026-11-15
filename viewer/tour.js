// Full-site guided tour: open /?tour. Title card -> Physical Lab (8 steps, iPhone 17 sample) -> transition ->
// Digital Lab (10 steps, played by build-fx.js) -> closing card. Every step uses saved sample results, so it needs no live AI call.
// It drives the real controls (samples menu, explode slider, spin, X-ray, parts list, what-if), like a user would.
(() => {
  if (!new URLSearchParams(location.search).has("tour")) return;
  document.documentElement.classList.add("touring");  // tour.css hides UI that should not appear in the video
  const TOTAL = 18, PHYS = 8;
  const q = (s) => document.querySelector(s);
  const sleep = (ms) => new Promise((ok) => setTimeout(ok, ms));
  const waitFor = async (ok, ms = 60000) => { const t = Date.now(); while (!ok() && Date.now() - t < ms) await sleep(150); return ok(); };
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const words = (t) => esc(t).split(" ").map((w, i) => `<span class="w" style="--i:${i}">${w}</span>`).join(" ");

  // ---- voice-over (/?tour&voice): each step plays its clip from /viewer/voice and the next step waits for it to finish ----
  const VOICE = new URLSearchParams(location.search).has("voice");
  const clips = {};
  const clip = (k) => clips[k] || (clips[k] = Object.assign(new Audio(`/viewer/voice/${k}.mp3`), { preload: "auto" }));
  if (VOICE) ["intro", "bridge", "outro", ...Array.from({ length: PHYS }, (_, i) => `p${i + 1}`), ...Array.from({ length: TOTAL - PHYS }, (_, i) => `d${i + 1}`)].forEach(clip);
  let vEnd = Promise.resolve();
  function speak(k) {
    if (!VOICE) return;
    const a = clip(k);
    vEnd = new Promise((ok) => {
      a.onended = ok; a.onerror = ok;
      a.play().catch(() => {  // browser blocked autoplay: one click resumes (cut it from the recording)
        const b = document.createElement("button");
        b.textContent = "▶ Click to continue with voice";
        b.style.cssText = "position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);z-index:99999;padding:16px 26px;font:600 16px system-ui;border-radius:12px;border:0;background:#ffd84d;color:#111;cursor:pointer";
        b.onclick = () => { b.remove(); a.play().catch(ok); };
        document.body.appendChild(b);
      });
    });
  }
  async function say(n, text) { await vEnd; cap(n, text); speak(n <= PHYS ? `p${n}` : `d${n - PHYS}`); }
  function gate() {  // gives the page a user click so the browser allows audio for the rest of the tour
    if (!VOICE) return Promise.resolve();
    return new Promise((ok) => {
      const g = document.createElement("div");
      g.style.cssText = "position:fixed;inset:0;z-index:99999;display:grid;place-items:center;background:#000c;color:#fff;font:600 20px system-ui;cursor:pointer";
      g.textContent = "Click anywhere to start the tour (with voice)";
      g.onclick = () => { g.remove(); ok(); };
      document.body.appendChild(g);
    });
  }

  function cap(n, text, lab = n <= PHYS ? "PHYSICAL" : "DIGITAL") {
    let c = q("#tourCap");
    if (!c) { c = document.createElement("div"); c.id = "tourCap"; c.className = "tour-cap"; document.body.appendChild(c); }
    c.innerHTML = n ? `<span class="lab">${lab}</span><span class="n">${n} / ${TOTAL}</span><span class="txt">${esc(text)}</span>` : `<span class="txt">${esc(text)}</span>`;
    c.classList.remove("in"); void c.offsetWidth; c.classList.add("in");
    let b = q("#tourBar");
    if (!b) { b = document.createElement("div"); b.id = "tourBar"; b.className = "tour-bar"; document.body.appendChild(b); }
    b.style.width = `${(Math.max(0, n) / TOTAL) * 100}%`;
  }
  function hideCap() { q("#tourCap")?.classList.remove("in"); }

  async function card(html, ms) {
    const el = document.createElement("div");
    el.className = "tour-card";
    el.innerHTML = `<div class="beam"></div><div class="tour-inner">${html}</div>`;
    document.body.appendChild(el);
    requestAnimationFrame(() => el.classList.add("in"));
    if (ms === Infinity) return el;
    await sleep(ms);
    el.classList.remove("in");
    await sleep(700);
    el.remove();
  }
  const INTRO = `<div class="tour-kicker">PolyGen · Generative 3D Asset Studio</div>
    <h1 class="tour-title">${words("PolyGen 3D")}</h1>
    <p class="tour-sub">AI-Powered 3D Generation & Multi-Part Kinematics Studio by Kailash-18.</p>
    <div class="tour-pair">
      <div class="tour-lab"><b>3D ASSET STUDIO</b><h3>3D Generative Mesh</h3><p>Watertight geometry, QEM decimation, PBR texture synthesis, and GLB/OBJ packaging.</p></div>
      <div class="tour-mid"><span>one<br>engine</span></div>
      <div class="tour-lab"><b>KINEMATICS LAB</b><h3>Exploded-View Decomposition</h3><p>Kinematic trajectories, wiring flow, collision-free separation, and interactive teardown.</p></div>
    </div>`;
  const BRIDGE = `<div class="tour-kicker">PolyGen Core</div><h1 class="tour-title">${words("Spatial 3D AI")}</h1>
    <p class="tour-sub">High-precision procedural solids, parametric shapes, and realistic physical dressing.</p>`;
  const OUTRO = `<div class="tour-kicker">PolyGen Architecture</div>
    <h1 class="tour-title">${words("Text In · Full 3D Asset Out.")}</h1>
    <p class="tour-sub">Components · relationships · behaviours · dependencies, for 3D game and metaverse assets.</p>
    <div class="tour-pair">
      <div class="tour-lab"><b>ASSET GENERATOR</b><h3>Procedural & Neural</h3><p>Fast AI generation, trimesh topology optimization, UV conformal unwrapping.</p></div>
      <div class="tour-mid"><span>PolyGen</span></div>
      <div class="tour-lab"><b>3D VIEWER</b><h3>Kinematics & Shaders</h3><p>Exploded model, X-ray wiring, thermal FLIR, procedural audio, grounded inspection.</p></div>
    </div>
    <div class="tour-team">PolyGen · Created by Kailash-18</div>`;

  // smooth slider motion that the viewer sees as real input
  function slide(input, from, to, ms) {
    return new Promise((ok) => {
      const t1 = performance.now();
      const st = (now) => {
        const t = Math.min(1, (now - t1) / ms), e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
        input.value = String(from + (to - from) * e);
        input.dispatchEvent(new Event("input", { bubbles: true }));
        t < 1 ? requestAnimationFrame(st) : ok();
      };
      requestAnimationFrame(st);
    });
  }
  function setCheck(sel, on) { const c = q(sel); if (c && c.checked !== on) { c.checked = on; c.dispatchEvent(new Event("change", { bubbles: true })); } }

  async function hi(el, ms) { if (!el) return; el.classList.add("tour-hi"); await sleep(ms); el.classList.remove("tour-hi"); }
  const partLi = (re) => [...document.querySelectorAll("#parts li")].find((l) => re.test(l.textContent));
  const partId = (re) => window.__vre.asm.parts.find((p) => re.test(p.label?.element?.textContent || "") || re.test(p.id))?.id;

  async function physical() {
    await waitFor(() => window.__vre && q("#samples")?.options.length > 1, 20000);
    await gate();
    speak("intro");
    await card(INTRO, VOICE ? 7900 : 6200);
    const V = window.__vre, A = V.asm;
    await say(1, "Photograph any object. Here: a brand-new iPhone 17, named down to the exact model");
    const sel = q("#samples"), id = [...sel.options].find((o) => /iphone/i.test(o.value))?.value || sel.options[1].value;
    sel.value = id; sel.dispatchEvent(new Event("change"));
    await waitFor(() => V.state.parts > 0 && q("#loading").hidden, 40000);
    await sleep(600);
    q('#ptabs [data-tab="overview"]')?.click();  // the exact-model card lives on the Overview tab
    hi(q("#product"), 4400);
    await waitFor(() => !A.intro, 8000);
    await waitFor(() => q("#spin").checked, 3500);  // the viewer starts spinning once its intro is over
    await sleep(500);
    await say(2, "It rebuilds it in 3D: every part it can see, and the ones hidden inside");
    setCheck("#spin", false);
    await sleep(300);
    // the back of the phone faces -z: come round from its right, behind it, so the camera island and the layers show
    await A.orbitTo({ theta: 2.35, el: 0.3, zoom: 0.85, ms: 3200 });
    await say(3, "Explode it: watch every part come apart, layer by layer");
    const ex = q("#explode"), v0 = parseFloat(ex.value) || 0.65;
    await slide(ex, v0, 0, 1100);
    A.orbitTo({ theta: 2.05, el: 0.34, zoom: 1.05, ms: 3600 });  // more from the side: the gaps between layers open up
    await slide(ex, 0, 1, 2600);
    await A.ripple({ ms: 3800, amp: 1 });
    await say(4, "Grab any part and pull it out by hand");
    for (const re of [/battery/i, /logic|board/i, /display|screen/i]) {
      const pid = partId(re); if (!pid) continue;
      for (let k = 0; k < 3; k++) { A.nudge(pid, 1, 220); await sleep(240); }
      await sleep(350);
    }
    await sleep(600);
    A.resetParts(700); q("#resetParts") && (q("#resetParts").hidden = true);
    await sleep(900);
    await slide(ex, 1, 0.7, 900);
    await say(5, "X-ray the wiring: how power and signals flow between the parts");
    setCheck("#xray", true);   // glides to the full view while the scan reveals the wiring
    await sleep(4000);
    setCheck("#xray", false);
    await say(6, "Click any part: what it does, what it is made of, what it connects to");
    q('#ptabs [data-tab="parts"]')?.click();
    const board = partLi(/logic|board|pcb|circuit/i) || q("#parts li");
    board?.click();
    await sleep(700);
    q("#detail")?.scrollIntoView({ behavior: "smooth", block: "center" });
    await sleep(3800);
    await say(7, "What if the battery fails? The cascade shows everything that stops working");
    (partLi(/battery/i) || board)?.click();
    await sleep(700);
    q("#whatif")?.click();
    await sleep(6400);
    if (q("#whatif")?.textContent.match(/put it back/i)) q("#whatif").click();
    await sleep(700);
    await say(8, "And the connections: every part and what it depends on, ready to explore or ask about");
    q('#ptabs [data-tab="links"]')?.click();  // Connections: every part and what it depends on
    hi(q("#links"), 4600);
    await sleep(4800);
    await vEnd;
    hideCap();
    speak("bridge");
    await card(BRIDGE, Infinity);
    await sleep(2600);
    await vEnd;
    location.href = "/digital" + location.search;  // keeps ?tour (and &voice) for the Digital Lab half
  }

  // the Digital Lab part is played by build-fx.js (demo mode); it calls these to keep one look and one numbering
  window.tour = {
    total: TOTAL, offset: PHYS,
    cap: (n, text) => say(PHYS + n, text),  // waits for the previous clip, then speaks this step
    async bridgeOut() { const el = await card(BRIDGE, Infinity); el.style.transition = "none"; el.classList.add("in"); await sleep(900); el.style.transition = ""; el.classList.remove("in"); await sleep(700); el.remove(); },
    async outro() { await vEnd; hideCap(); q("#tourBar")?.remove(); speak("outro"); await card(OUTRO, Infinity); },
  };
  if (location.pathname === "/" || location.pathname === "/index.html") {
    const run = () => physical().catch((e) => cap(0, `Tour stopped: ${e.message}`));
    document.readyState === "complete" ? setTimeout(run, 300) : addEventListener("load", () => setTimeout(run, 300));
  }
})();
