/**
 * PolyGen Week 4 - Game Engine Export Lab & Studio Staging Client
 * Manages Unreal Engine 5 / Unity ZIP bundle export, Multi-LOD preview switching,
 * PBR material preset application, and photometric HDRI studio lighting rigs.
 */

window.PolyGenExportLab = (function () {
    let currentModelId = "sword-01";
    let activePreset = "cyberpunk_neon";
    let activeHDRI = "clean_industrial";
    let activeLOD = "LOD0";

    const PBR_PRESETS = [
        { id: "cyberpunk_neon", name: "Cyberpunk Neon", color: "#00E5FF", rough: 0.18, metal: 0.85, emissive: "#00E5FF", emissiveInt: 2.2 },
        { id: "weathered_rust", name: "Weathered Rust", color: "#8B3A1C", rough: 0.88, metal: 0.10, emissive: "#000000", emissiveInt: 0.0 },
        { id: "scifi_matte", name: "Sci-Fi Matte", color: "#2D3136", rough: 0.45, metal: 0.30, emissive: "#FFA01A", emissiveInt: 0.3 },
        { id: "anodized_titanium", name: "Anodized Titanium", color: "#6A0DAD", rough: 0.22, metal: 0.94, emissive: "#000000", emissiveInt: 0.0 },
        { id: "obsidian_glass", name: "Obsidian Glass", color: "#0C0D0E", rough: 0.08, metal: 0.05, emissive: "#000000", emissiveInt: 0.0 },
        { id: "gold_leaf", name: "24k Gold Leaf", color: "#FFD700", rough: 0.12, metal: 0.98, emissive: "#000000", emissiveInt: 0.0 }
    ];

    const HDRI_PRESETS = [
        { id: "clean_industrial", name: "Neutral Studio (5600K)", bg: "#121519", exp: 1.0, keyColor: 0xF4F8FF, keyInt: 1.8 },
        { id: "cyberpunk_studio", name: "Cyberpunk Rig (8500K)", bg: "#080811", exp: 1.25, keyColor: 0x00E5FF, keyInt: 2.2 },
        { id: "sunset_desert", name: "Golden Sunset (3200K)", bg: "#181315", exp: 1.1, keyColor: 0xFFA858, keyInt: 2.8 },
        { id: "deep_space", name: "Void Deep Space", bg: "#030407", exp: 1.35, keyColor: 0xFFFFFF, keyInt: 3.4 }
    ];

    function init(modelId) {
        if (modelId) currentModelId = modelId;
        injectUI();
        console.log("[PolyGenExportLab] Initialized for model:", currentModelId);
    }

    function injectUI() {
        if (document.getElementById("polygen-export-lab-container")) return;

        const container = document.createElement("div");
        container.id = "polygen-export-lab-container";
        container.innerHTML = `
            <style>
                .export-lab-pillbox {
                    position: fixed;
                    bottom: 24px;
                    right: 24px;
                    z-index: 9999;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                }
                .export-lab-btn {
                    background: linear-gradient(135deg, #00f0ff 0%, #7000ff 100%);
                    color: #fff;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 30px;
                    font-weight: 700;
                    font-size: 13px;
                    letter-spacing: 0.5px;
                    cursor: pointer;
                    box-shadow: 0 8px 24px rgba(0, 240, 255, 0.35);
                    transition: transform 0.2s, box-shadow 0.2s;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .export-lab-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 12px 30px rgba(112, 0, 255, 0.5);
                }
                .export-lab-modal {
                    display: none;
                    position: fixed;
                    top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(4, 7, 14, 0.85);
                    backdrop-filter: blur(12px);
                    z-index: 10000;
                    align-items: center;
                    justify-content: center;
                }
                .export-lab-modal.active { display: flex; }
                .export-modal-card {
                    background: #0d111a;
                    border: 1px solid rgba(0, 240, 255, 0.3);
                    border-radius: 16px;
                    width: 580px;
                    max-width: 90vw;
                    padding: 28px;
                    color: #e2e8f0;
                    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 40px rgba(0, 240, 255, 0.15);
                }
                .export-modal-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                    padding-bottom: 14px;
                }
                .export-modal-title { font-size: 18px; font-weight: 700; color: #00f0ff; }
                .export-modal-close {
                    background: transparent; border: none; color: #94a3b8; font-size: 22px; cursor: pointer;
                }
                .export-section { margin-bottom: 18px; }
                .export-section-title {
                    font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #64748b; margin-bottom: 10px; font-weight: 700;
                }
                .engine-toggle-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
                .engine-card {
                    background: #161d2d;
                    border: 2px solid transparent;
                    border-radius: 10px;
                    padding: 14px;
                    cursor: pointer;
                    transition: border-color 0.2s, background 0.2s;
                }
                .engine-card.selected {
                    border-color: #00f0ff;
                    background: #1a253c;
                }
                .engine-name { font-weight: 700; font-size: 15px; margin-bottom: 4px; }
                .engine-desc { font-size: 11px; color: #94a3b8; line-height: 1.4; }
                .preset-pills-row { display: flex; flex-wrap: wrap; gap: 8px; }
                .preset-pill {
                    background: #161d2d;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 20px;
                    padding: 6px 14px;
                    font-size: 12px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    transition: all 0.2s;
                }
                .preset-pill:hover, .preset-pill.active {
                    border-color: #00f0ff;
                    background: rgba(0, 240, 255, 0.15);
                    color: #fff;
                }
                .pill-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
                .download-cta-btn {
                    width: 100%;
                    background: #00f0ff;
                    color: #04070e;
                    border: none;
                    border-radius: 8px;
                    padding: 14px;
                    font-size: 14px;
                    font-weight: 800;
                    letter-spacing: 0.5px;
                    cursor: pointer;
                    margin-top: 10px;
                    transition: background 0.2s, transform 0.1s;
                }
                .download-cta-btn:hover { background: #38f4ff; transform: scale(1.01); }
            </style>

            <div class="export-lab-pillbox">
                <button class="export-lab-btn" id="open-export-modal-btn">
                    <span>⚡</span> Game Engine Export & PBR Studio
                </button>
            </div>

            <div class="export-lab-modal" id="export-lab-modal">
                <div class="export-modal-card">
                    <div class="export-modal-header">
                        <div class="export-modal-title">🎮 Game Engine Packaging Pipeline</div>
                        <button class="export-modal-close" id="close-export-modal-btn">&times;</button>
                    </div>

                    <div class="export-section">
                        <div class="export-section-title">1. Target Game Engine</div>
                        <div class="engine-toggle-grid">
                            <div class="engine-card selected" id="opt-unreal" onclick="PolyGenExportLab.selectEngine('unreal')">
                                <div class="engine-name" style="color: #00f0ff;">Unreal Engine 5</div>
                                <div class="engine-desc">Nanite LODs, UCX_* Collision Hulls, discrete T_*_D/N/R/M textures & uasset manifest.</div>
                            </div>
                            <div class="engine-card" id="opt-unity" onclick="PolyGenExportLab.selectEngine('unity')">
                                <div class="engine-name" style="color: #ff007f;">Unity URP / HDRP</div>
                                <div class="engine-desc">Channel-packed Metallic-Smoothness map (R/A), LODGroup thresholds & .prefab spec.</div>
                            </div>
                        </div>
                    </div>

                    <div class="export-section">
                        <div class="export-section-title">2. PBR Material Presets</div>
                        <div class="preset-pills-row" id="pbr-pills-container"></div>
                    </div>

                    <div class="export-section">
                        <div class="export-section-title">3. Studio Environment Lighting (HDRI)</div>
                        <div class="preset-pills-row" id="hdri-pills-container"></div>
                    </div>

                    <div class="export-section">
                        <div class="export-section-title">4. Multi-LOD & Collision Inclusions</div>
                        <label style="display: flex; align-items: center; gap: 8px; font-size: 13px; margin-bottom: 6px; cursor: pointer;">
                            <input type="checkbox" id="chk-include-lods" checked> Include Multi-LOD Hierarchy (LOD0, LOD1, LOD2, LOD3)
                        </label>
                        <label style="display: flex; align-items: center; gap: 8px; font-size: 13px; cursor: pointer;">
                            <input type="checkbox" id="chk-include-collision" checked> Include Physics Collision Hulls (Convex / OBB)
                        </label>
                    </div>

                    <button class="download-cta-btn" id="export-package-download-btn" onclick="PolyGenExportLab.triggerExport()">
                        Package & Download Production ZIP Bundle
                    </button>
                    <div id="export-status-indicator" style="font-size: 12px; margin-top: 8px; text-align: center; color: #94a3b8;"></div>
                </div>
            </div>
        `;
        document.body.appendChild(container);

        // Populate Pills
        const pbrContainer = document.getElementById("pbr-pills-container");
        PBR_PRESETS.forEach(p => {
            const pill = document.createElement("div");
            pill.className = `preset-pill ${p.id === activePreset ? "active" : ""}`;
            pill.id = `pill-pbr-${p.id}`;
            pill.innerHTML = `<span class="pill-dot" style="background: ${p.color};"></span> ${p.name}`;
            pill.onclick = () => selectPreset(p.id);
            pbrContainer.appendChild(pill);
        });

        const hdriContainer = document.getElementById("hdri-pills-container");
        HDRI_PRESETS.forEach(h => {
            const pill = document.createElement("div");
            pill.className = `preset-pill ${h.id === activeHDRI ? "active" : ""}`;
            pill.id = `pill-hdri-${h.id}`;
            pill.innerHTML = `☀️ ${h.name}`;
            pill.onclick = () => selectHDRI(h.id);
            hdriContainer.appendChild(pill);
        });

        // Event listeners
        document.getElementById("open-export-modal-btn").onclick = () => {
            document.getElementById("export-lab-modal").classList.add("active");
        };
        document.getElementById("close-export-modal-btn").onclick = () => {
            document.getElementById("export-lab-modal").classList.remove("active");
        };
    }

    let selectedEngineType = "unreal";

    function selectEngine(type) {
        selectedEngineType = type;
        document.getElementById("opt-unreal").classList.toggle("selected", type === "unreal");
        document.getElementById("opt-unity").classList.toggle("selected", type === "unity");
    }

    function selectPreset(presetId) {
        activePreset = presetId;
        document.querySelectorAll("[id^='pill-pbr-']").forEach(el => el.classList.remove("active"));
        const target = document.getElementById(`pill-pbr-${presetId}`);
        if (target) target.classList.add("active");

        // Apply on live 3D scene if scene is available
        const p = PBR_PRESETS.find(x => x.id === presetId);
        if (p && window.viewerScene) {
            window.viewerScene.traverse(child => {
                if (child.isMesh && child.material) {
                    child.material.roughness = p.rough;
                    child.material.metalness = p.metal;
                    if (child.material.color) child.material.color.set(p.color);
                    if (child.material.emissive && p.emissiveInt > 0) {
                        child.material.emissive.set(p.emissive);
                        child.material.emissiveIntensity = p.emissiveInt;
                    }
                }
            });
        }
    }

    function selectHDRI(hdriId) {
        activeHDRI = hdriId;
        document.querySelectorAll("[id^='pill-hdri-']").forEach(el => el.classList.remove("active"));
        const target = document.getElementById(`pill-hdri-${hdriId}`);
        if (target) target.classList.add("active");

        const h = HDRI_PRESETS.find(x => x.id === hdriId);
        if (h && window.viewerRenderer) {
            if (window.viewerScene) window.viewerScene.background = new THREE.Color(h.bg);
            window.viewerRenderer.toneMappingExposure = h.exp;
        }
    }

    async function triggerExport() {
        const statusEl = document.getElementById("export-status-indicator");
        const btn = document.getElementById("export-package-download-btn");
        const incLods = document.getElementById("chk-include-lods").checked;
        const incColl = document.getElementById("chk-include-collision").checked;

        statusEl.innerHTML = "⏳ Bundling assets, LODs, collision hulls, and manifests...";
        btn.disabled = true;

        try {
            const resp = await fetch(`/api/export/game-engine/${currentModelId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    engine: selectedEngineType,
                    include_lods: incLods,
                    include_collision: incColl
                })
            });

            if (!resp.ok) throw new Error("Export pipeline failed");
            const data = await resp.json();

            statusEl.innerHTML = `✅ Successfully created ${data.package_filename} (${data.file_count} files)! Downloading...`;

            // Trigger download
            const a = document.createElement("a");
            a.href = data.download_url;
            a.download = data.package_filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        } catch (e) {
            statusEl.innerHTML = `<span style="color: #ff5555;">Export error: ${e.message}</span>`;
        } finally {
            btn.disabled = false;
        }
    }

    return {
        init: init,
        selectEngine: selectEngine,
        selectPreset: selectPreset,
        selectHDRI: selectHDRI,
        triggerExport: triggerExport
    };
})();

// Auto-boot if window loaded
if (document.readyState === "complete" || document.readyState === "interactive") {
    setTimeout(window.PolyGenExportLab.init, 500);
} else {
    window.addEventListener("DOMContentLoaded", () => setTimeout(window.PolyGenExportLab.init, 500));
}
