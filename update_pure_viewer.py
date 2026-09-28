import os

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"

html_code = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>操縦席コンソールユニット 3D Viewer (手書きノート完全再現版)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      background: #090d16;
      color: #e2e8f0;
      overflow: hidden;
      height: 100vh;
      display: flex;
    }
    #canvas-container {
      flex: 1;
      height: 100%;
      position: relative;
    }
    #sidebar {
      width: 380px;
      background: rgba(15, 23, 42, 0.96);
      border-left: 1px solid #334155;
      padding: 20px;
      overflow-y: auto;
      box-shadow: -8px 0 30px rgba(0,0,0,0.8);
      backdrop-filter: blur(12px);
      z-index: 10;
    }
    h1 {
      font-size: 19px;
      margin-bottom: 6px;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge-fixed {
      font-size: 11px;
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #fff;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 600;
    }
    p.desc {
      font-size: 12px;
      color: #94a3b8;
      margin-bottom: 14px;
      line-height: 1.5;
    }
    .formula-card {
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid #0284c7;
      border-radius: 6px;
      padding: 10px 12px;
      font-size: 11.5px;
      margin-bottom: 16px;
      line-height: 1.6;
      color: #bae6fd;
    }
    .formula-card strong { color: #38bdf8; }
    .section-title {
      font-size: 12px;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-top: 18px;
      margin-bottom: 10px;
      border-bottom: 1px solid #334155;
      padding-bottom: 4px;
    }
    .control-group {
      margin-bottom: 12px;
    }
    .control-group label {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: #cbd5e1;
      margin-bottom: 6px;
      cursor: pointer;
    }
    .btn-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 10px;
    }
    button {
      background: #1e293b;
      color: #f1f5f9;
      border: 1px solid #334155;
      padding: 9px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
    }
    button:hover {
      background: #0284c7;
      border-color: #38bdf8;
      color: #fff;
    }
    button.active {
      background: #0284c7;
      border-color: #38bdf8;
      color: #fff;
    }
    .spec-table {
      width: 100%;
      font-size: 11.5px;
      border-collapse: collapse;
      margin-top: 8px;
    }
    .spec-table td {
      padding: 6px 4px;
      border-bottom: 1px solid #1e293b;
    }
    .spec-table td:first-child {
      color: #94a3b8;
      width: 50%;
    }
    .spec-table td:last-child {
      color: #f8fafc;
      font-weight: 600;
    }
    #hud-overlay {
      position: absolute;
      top: 20px;
      left: 20px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid #0284c7;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 12px;
      backdrop-filter: blur(8px);
      pointer-events: none;
      box-shadow: 0 0 15px rgba(2, 132, 199, 0.25);
    }
    .hud-title {
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 6px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
      font-size: 11px;
    }
    .legend-color {
      width: 12px;
      height: 12px;
      border-radius: 3px;
    }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
  <div id="canvas-container">
    <div id="hud-overlay">
      <div class="hud-title">◆ 操縦席コンソールユニット (確定版)</div>
      <div class="legend-item"><div class="legend-color" style="background: #e2b34a;"></div> 4本主角柱 (90mm角材 × 長さ900mm)</div>
      <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> 足元ベース板 (30cm角) ＋ 三角補強リブ</div>
      <div class="legend-item"><div class="legend-color" style="background: #38bdf8;"></div> 操作コンソール (ハンドル・スイッチ・メーター)</div>
      <div class="legend-item"><div class="legend-color" style="background: #0284c7;"></div> 操縦席シート & ラダーペダル</div>
      <div class="legend-item"><div class="legend-color" style="background: #64748b;"></div> サイドガードパネル (肘掛け・防護板)</div>
    </div>
  </div>

  <div id="sidebar">
    <h1>操縦席ユニット <span class="badge-fixed">確定モデル</span></h1>
    <p class="desc">前の板書（ガルウィングドア・ラップ窓等）の混入を完全排除。手書きノートの数式・スケッチ（4本角柱・足元ハカマ・操作コンソール）を100%純粋に再現した確定設計です。</p>

    <div class="formula-card">
      <strong>【ノート記載の確定数式】</strong><br>
      • 基準高さ: <code>h = 90cm</code> (87.5 ≒ 90cm)<br>
      • 内寸横幅: <code>4/5 h = 70cm</code> (カフェ1人席の理想幅)<br>
      • 柱の太さ: <code>1/9〜1/12 h ≒ 9.0cm角</code> (4本)<br>
      • 足元ベース: <code>1/3 h = 30cm角</code> ＋ 三角リブ (ハカマ)<br>
      • 中央斜線部: <strong>操作コンソール（ハンドル・スイッチ類）</strong>
    </div>

    <div class="section-title">視点切り替え</div>
    <div class="btn-grid">
      <button id="cam-ext" class="active" onclick="setCameraMode('ext')">外観カメラ (全体)</button>
      <button id="cam-pilot" onclick="setCameraMode('pilot')">操縦席カメラ (パイロット目線)</button>
    </div>

    <div class="section-title">パーツ表示切り替え</div>
    <div class="control-group">
      <label><input type="checkbox" id="toggle-posts" checked onchange="updateVisibility()"> 4本主角柱 (90mm角)</label>
      <label><input type="checkbox" id="toggle-base" checked onchange="updateVisibility()"> 足元ベース板 & 三角補強リブ</label>
      <label><input type="checkbox" id="toggle-frame" checked onchange="updateVisibility()"> 連結梁フレーム (45mm角)</label>
      <label><input type="checkbox" id="toggle-console" checked onchange="updateVisibility()"> 操作コンソール (ハンドル・スイッチ盤)</label>
      <label><input type="checkbox" id="toggle-seat" checked onchange="updateVisibility()"> パイロットシート & ペダル</label>
      <label><input type="checkbox" id="toggle-panels" checked onchange="updateVisibility()"> サイドガードパネル</label>
      <label><input type="checkbox" id="toggle-pilot" checked onchange="updateVisibility()"> パイロットシルエット</label>
    </div>

    <div class="section-title">機体確定スペック</div>
    <table class="spec-table">
      <tr><td>内寸横幅</td><td>700 mm (ノート: 4/5h)</td></tr>
      <tr><td>外寸全幅</td><td>880 mm</td></tr>
      <tr><td>奥行き (スパン)</td><td>800 mm</td></tr>
      <tr><td>主角柱太さ</td><td>90 × 90 mm (4本)</td></tr>
      <tr><td>主角柱長さ</td><td>900 mm (ノート: h)</td></tr>
      <tr><td>足元ベース板</td><td>300 × 300 mm (4枚)</td></tr>
      <tr><td>足元補強</td><td>直角三角リブ (硬めの素材)</td></tr>
      <tr><td>中間梁高さ</td><td>450 mm (ノート: 1/2h)</td></tr>
      <tr><td>操作コンソール</td><td>ハンドル, スイッチ, メーター</td></tr>
    </table>

    <div class="section-title">CADデータ保存先</div>
    <p style="font-size: 11px; color:#94a3b8; word-break: break-all; line-height: 1.5;">
      /Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/<br>
      • <code>cockpit_assembly_full.step</code> (全体CAD)<br>
      • <code>cockpit_assembly_full.stl</code> (3Dメッシュ)<br>
      • <code>cockpit_frame.step</code> / <code>.stl</code> (骨組み)<br>
      • <code>CUT_LIST.md</code> (木取り・組み立て手順)
    </p>
  </div>

  <script>
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x090d16);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 10, 15000);
    camera.position.set(1600, 1300, 1800);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 480, 0);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0x38bdf8, 0.85);
    dirLight1.position.set(1500, 2500, 1200);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.45);
    dirLight2.position.set(-1500, 1000, -1500);
    scene.add(dirLight2);

    // Ground Grid
    const grid = new THREE.GridHelper(3000, 30, 0x0284c7, 0x1e293b);
    grid.position.y = 0;
    scene.add(grid);

    // ----------------------------------------------------
    // Materials
    // ----------------------------------------------------
    const postMat = new THREE.MeshStandardMaterial({ color: 0xd49b4b, roughness: 0.6 }); // 90mm角材
    const basePlateMat = new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.7 }); // ベース板
    const ribMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.5 }); // 三角リブ
    const consoleMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4 });
    const yokeMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.5 }); // ハンドル
    const switchMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, metalness: 0.5 });
    const seatMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });
    const seatAccentMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.6 });
    const panelMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.8, transparent: true, opacity: 0.75 });
    const pilotMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });

    // Groups
    const groupPosts = new THREE.Group();
    const groupBase = new THREE.Group();
    const groupFrame = new THREE.Group();
    const groupConsole = new THREE.Group();
    const groupSeat = new THREE.Group();
    const groupPanels = new THREE.Group();
    const groupPilot = new THREE.Group();

    scene.add(groupPosts);
    scene.add(groupBase);
    scene.add(groupFrame);
    scene.add(groupConsole);
    scene.add(groupSeat);
    scene.add(groupPanels);
    scene.add(groupPilot);

    // Dimensions
    const W_INNER = 700;
    const POST_S = 90;
    const POST_H = 900;
    const BASE_S = 300;
    const DEPTH = 800;
    const X_L = -(W_INNER + POST_S) / 2; // -395
    const X_R =  (W_INNER + POST_S) / 2; //  395
    const Y_F = -DEPTH / 2;              // -400 (Front)
    const Y_R =  DEPTH / 2;              //  400 (Rear)

    function addBox(group, w, h, d, px, py, pz, mat, rotX=0, rotY=0, rotZ=0) {
      const geom = new THREE.BoxGeometry(w, h, d);
      const mesh = new THREE.Mesh(geom, mat);
      mesh.position.set(px, py, pz);
      if (rotX !== 0) mesh.rotation.x = rotX;
      if (rotY !== 0) mesh.rotation.y = rotY;
      if (rotZ !== 0) mesh.rotation.z = rotZ;
      group.add(mesh);
      return mesh;
    }

    // 1. 4 Heavy Posts and Flanges
    const postPositions = [
      [X_L, Y_F], [X_R, Y_F],
      [X_L, Y_R], [X_R, Y_R]
    ];

    postPositions.forEach(([px, pz]) => {
      // 90mm角柱
      addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);

      // 300mm角ベース板
      addBox(groupBase, BASE_S, 18, BASE_S, px, 9, pz, basePlateMat);

      // 三角補強リブ (ハカマ)
      function addRib(rotY, offsetX, offsetZ) {
        const shape = new THREE.Shape();
        shape.moveTo(0, 0);
        shape.lineTo(90, 0);
        shape.lineTo(0, 150);
        shape.closePath();

        const extrudeSettings = { depth: 15, bevelEnabled: false };
        const ribGeom = new THREE.ExtrudeGeometry(shape, extrudeSettings);
        const ribMesh = new THREE.Mesh(ribGeom, ribMat);
        ribMesh.rotation.y = rotY;
        ribMesh.position.set(px + offsetX, 18, pz + offsetZ);
        groupBase.add(ribMesh);
      }
      addRib(0, POST_S/2, -7.5);
      addRib(Math.PI, -POST_S/2, 7.5);
      addRib(Math.PI/2, -7.5, POST_S/2);
      addRib(-Math.PI/2, 7.5, -POST_S/2);
    });

    // 2. Connecting Horizontal Beams (梁フレーム: 45x45mm)
    addBox(groupFrame, W_INNER, 45, 45, 0, 450, Y_F, postMat);
    addBox(groupFrame, W_INNER, 45, 45, 0, POST_H - 22, Y_F, postMat);
    addBox(groupFrame, W_INNER, 45, 45, 0, 350, Y_R, postMat);
    addBox(groupFrame, W_INNER, 45, 45, 0, POST_H - 22, Y_R, postMat);
    addBox(groupFrame, 45, 45, DEPTH - POST_S, X_L, 450, 0, postMat);
    addBox(groupFrame, 45, 45, DEPTH - POST_S, X_R, 450, 0, postMat);
    addBox(groupFrame, 45, 45, DEPTH - POST_S, X_L, POST_H - 22, 0, postMat);
    addBox(groupFrame, 45, 45, DEPTH - POST_S, X_R, POST_H - 22, 0, postMat);

    // 3. Control Console (中央斜線ハッチング部: ハンドル・スイッチ盤)
    const CON_Y = 580;
    const CON_Z = Y_F + 140;
    // Console Main Slanted Body
    addBox(groupConsole, W_INNER - 10, 140, 320, 0, CON_Y, CON_Z, consoleMat, -0.4);

    // Flight Yoke (操縦ハンドル)
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(15, 15, 130, 16), switchMat);
    shaft.position.set(0, CON_Y + 35, CON_Z - 45);
    shaft.rotation.x = -0.4;
    groupConsole.add(shaft);

    // Yoke Grips (W型ハンドル)
    addBox(groupConsole, 150, 24, 28, 0, CON_Y + 65, CON_Z - 105, yokeMat, -0.4);
    addBox(groupConsole, 24, 110, 24, -80, CON_Y + 95, CON_Z - 115, yokeMat);
    addBox(groupConsole, 24, 110, 24,  80, CON_Y + 95, CON_Z - 115, yokeMat);

    // Gauges & Switches
    const gaugeL = new THREE.Mesh(new THREE.CylinderGeometry(36, 36, 12, 16), switchMat);
    gaugeL.position.set(-180, CON_Y + 60, CON_Z + 40);
    gaugeL.rotation.x = -0.4;
    groupConsole.add(gaugeL);

    const gaugeR = new THREE.Mesh(new THREE.CylinderGeometry(36, 36, 12, 16), switchMat);
    gaugeR.position.set(180, CON_Y + 60, CON_Z + 40);
    gaugeR.rotation.x = -0.4;
    groupConsole.add(gaugeR);

    // Switch Panel
    addBox(groupConsole, 180, 8, 85, 0, CON_Y + 65, CON_Z + 50, switchMat, -0.4);

    // Throttle Lever (Left hand)
    addBox(groupConsole, 60, 25, 100, -260, 490, Y_F + 220, consoleMat);
    const throt = addBox(groupConsole, 20, 90, 35, -260, 545, Y_F + 220, yokeMat);
    throt.rotation.x = 0.35;

    // 4. Seat & Pedals
    const SEAT_Z = Y_R - 180;
    addBox(groupSeat, 500, 50, 440, 0, 360, SEAT_Z, seatMat);
    const sBack = addBox(groupSeat, 480, 500, 45, 0, 620, SEAT_Z + 200, seatMat);
    sBack.rotation.x = -0.22;
    const sHead = addBox(groupSeat, 260, 150, 55, 0, 910, SEAT_Z + 240, seatAccentMat);
    sHead.rotation.x = -0.15;

    // Rudder Pedals
    const pL = addBox(groupSeat, 80, 130, 15, -130, 65, Y_F + 60, consoleMat);
    pL.rotation.x = -0.4;
    const pR = addBox(groupSeat, 80, 130, 15,  130, 65, Y_F + 60, consoleMat);
    pR.rotation.x = -0.4;

    // 5. Side Guard Panels (左右アームレスト・防護パネル)
    addBox(groupPanels, 12, POST_H, DEPTH + POST_S, X_L - POST_S/2 - 6, POST_H/2, 0, panelMat);
    addBox(groupPanels, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, panelMat);

    // 6. Pilot Silhouette
    const pHead = new THREE.Mesh(new THREE.SphereGeometry(105, 16, 16), pilotMat);
    pHead.position.set(0, 900, SEAT_Z + 160);
    groupPilot.add(pHead);

    const pTorso = new THREE.Mesh(new THREE.CylinderGeometry(130, 110, 420, 8), pilotMat);
    pTorso.position.set(0, 620, SEAT_Z + 100);
    pTorso.rotation.x = -0.22;
    groupPilot.add(pTorso);

    const pThighs = new THREE.Mesh(new THREE.BoxGeometry(260, 90, 360), pilotMat);
    pThighs.position.set(0, 380, SEAT_Z - 80);
    groupPilot.add(pThighs);

    const pShins = new THREE.Mesh(new THREE.BoxGeometry(260, 340, 90), pilotMat);
    pShins.position.set(0, 200, Y_F + 120);
    pShins.rotation.x = 0.4;
    groupPilot.add(pShins);

    // ----------------------------------------------------
    // Interactivity
    // ----------------------------------------------------
    function updateVisibility() {
      groupPosts.visible = document.getElementById('toggle-posts').checked;
      groupBase.visible = document.getElementById('toggle-base').checked;
      groupFrame.visible = document.getElementById('toggle-frame').checked;
      groupConsole.visible = document.getElementById('toggle-console').checked;
      groupSeat.visible = document.getElementById('toggle-seat').checked;
      groupPanels.visible = document.getElementById('toggle-panels').checked;
      groupPilot.visible = document.getElementById('toggle-pilot').checked;
    }

    let isPilotCam = false;
    function setCameraMode(mode) {
      document.getElementById('cam-ext').classList.toggle('active', mode === 'ext');
      document.getElementById('cam-pilot').classList.toggle('active', mode === 'pilot');
      if (mode === 'pilot') {
        isPilotCam = true;
        controls.enabled = false;
        camera.position.set(0, 900, SEAT_Z + 160);  // Eye point
        camera.lookAt(0, CON_Y + 40, CON_Z - 50);    // Looking at Flight Yoke / Console
      } else {
        isPilotCam = false;
        controls.enabled = true;
        camera.position.set(1600, 1300, 1800);
        controls.target.set(0, 480, 0);
      }
    }

    window.addEventListener('resize', () => {
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    });

    function animate() {
      requestAnimationFrame(animate);
      if (!isPilotCam) controls.update();
      renderer.render(scene, camera);
    }
    animate();
  </script>
</body>
</html>
"""

with open(os.path.join(OUT_DIR, "cockpit_viewer.html"), "w", encoding="utf-8") as f:
    f.write(html_code)

print("Updated cockpit_viewer.html for pure V3 simulator cockpit.")
