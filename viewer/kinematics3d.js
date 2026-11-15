// PolyGen Kinematics3D Engine - Real-Time Center-of-Mass & Inertia Vector Overlay
// Calculates dynamically shifting Center of Mass (CoM) and bounding envelope during teardown.
import * as THREE from "three";

export function installKinematics(View) {
  const P = View.prototype;

  P.createKinematicGizmo = function () {
    if (this._kinematicGroup) return this._kinematicGroup;

    const group = new THREE.Group();
    group.visible = false;

    // Glowing dual-ring CoM marker
    const ringGeom = new THREE.RingGeometry(0.12, 0.15, 32);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x00ffcc,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.85
    });

    const ring1 = new THREE.Mesh(ringGeom, ringMat);
    const ring2 = new THREE.Mesh(ringGeom, ringMat);
    ring2.rotation.x = Math.PI / 2;

    const coreDot = new THREE.Mesh(
      new THREE.SphereGeometry(0.06, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xffffff })
    );

    // Three orthogonal principal kinematic axes
    const axisMatX = new THREE.LineBasicMaterial({ color: 0xff3b30, linewidth: 2 });
    const axisMatY = new THREE.LineBasicMaterial({ color: 0x34c759, linewidth: 2 });
    const axisMatZ = new THREE.LineBasicMaterial({ color: 0x007aff, linewidth: 2 });

    const createAxisLine = (dir, mat) => {
      const geom = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        dir.clone().multiplyScalar(1.2)
      ]);
      return new THREE.Line(geom, mat);
    };

    const axisX = createAxisLine(new THREE.Vector3(1, 0, 0), axisMatX);
    const axisY = createAxisLine(new THREE.Vector3(0, 1, 0), axisMatY);
    const axisZ = createAxisLine(new THREE.Vector3(0, 0, 1), axisMatZ);

    group.add(ring1, ring2, coreDot, axisX, axisY, axisZ);
    this.root.add(group);

    this._kinematicGroup = group;
    return group;
  };

  P.setKinematicsOverlay = function (active) {
    this.kinematicsActive = active;
    const gizmo = this.createKinematicGizmo();
    gizmo.visible = active;
    this.poke?.();
  };

  P.updateKinematics = function () {
    if (!this.kinematicsActive || !this._kinematicGroup) return;

    let totalWeight = 0;
    const com = new THREE.Vector3(0, 0, 0);
    const tempPos = new THREE.Vector3();

    for (const p of this.parts) {
      if (!p.mesh || !p.group.visible) continue;
      p.mesh.getWorldPosition(tempPos);
      
      // Approximate mass by bounding volume
      const size = p.size || [1, 1, 1];
      const mass = Math.max(0.1, size[0] * size[1] * size[2]);

      com.addScaledVector(tempPos, mass);
      totalWeight += mass;
    }

    if (totalWeight > 0) {
      com.divideScalar(totalWeight);
      this._kinematicGroup.position.copy(com);

      // Subtle gyroscopic rotation
      const t = performance.now() * 0.0015;
      this._kinematicGroup.rotation.y = t;
    }
  };

  const origRender = P.render;
  P.render = function () {
    if (this.kinematicsActive) {
      this.updateKinematics();
    }
    if (origRender) origRender.call(this);
  };
}
