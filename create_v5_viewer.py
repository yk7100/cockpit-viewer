import os

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"

html_code = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>COCKPIT v5.0.0 (長方形・低床ドア・縦4本柱モデル)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      background: #060911;
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
      width: 390px;
      background: rgba(13, 19, 33, 0.97);
      border-left: 1px solid #1e293b;
      padding: 20px;
      overflow-y: auto;
      box-shadow: -8px 0 30px rgba(0,0,0,0.85);
      backdrop-filter: blur(14px);
      z-index: 10;
    }
    .version-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }
    h1 {
      font-size: 20px;
      color: #38bdf8;
      letter-spacing: 0.5px;
    }
    .badge-v5 {
      font-size: 12px;
      background: linear-gradient(135deg, #10b981, #059669);
      color: #fff;
      padding: 3px 10px;
      border-radius: 9999px;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
    }
    p.desc {
      font-size: 12px;
      color: #94a3b8;
      margin-bottom: 14px;
      line-height: 1.5;
    }
    .change-log {
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid #10b981;
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 11.5px;
      margin-bottom: 16px;
      line-height: 1.6;
      color: #a7f3d0;
    }
    .change-log strong { color: #34d399; font-size: 12px; }
    .change-log ul { margin-left: 16px; margin-top: 4px; }
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
    input[type="range"] {
      width: 100%;
      accent-color: #10b981;
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
      background: #10b981;
      border-color: #34d399;
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
      background: rgba(13, 19, 33, 0.92);
      border: 1px solid #10b981;
      padding: 14px 18px;
      border-radius: 8px;
      font-size: 12px;
      backdrop-filter: blur(10px);
      pointer-events: none;
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
    }
    .hud-title {
      font-weight: 800;
      color: #34d399;
      font-size: 13px;
      margin-bottom: 8px;
      letter-spacing: 0.5px;
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
      <div class="hud-title">◆ COCKPIT RELEASE v5.0.0</div>
      <div class="legend-item"><div class="legend-color" style="background: #e2b34a;"></div> 木の枠：縦の4本角柱のみ (90mm角材)</div>
      <div class="legend-item"><div class="legend-color" style="background: #10b981;"></div> 大型乗降ドア (敷居高さ50mm・足元フラット)</div>
      <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> 足元ベース＆外側リブ (通路側リブ全廃)</div>
      <div class="legend-item"><div class="legend-color" style="background: #38bdf8;"></div> 操作コンソール (膝上クリアランス確保)</div>
      <div class="legend-item"><div class="legend-color" style="background: #0284c7;"></div> 操縦席シート (足元広々70cmクリアランス)</div>
    </div>
  </div>

  <div id="sidebar">
    <div class="version-header">
      <h1>操縦席ユニット</h1>
      <span class="badge-v5">v5.0.0</span>
    </div>
    <p class="desc">「長方形のほうがいい？」「人入れないかな？」の疑問を完全解決したメジャーバージョンです。</p>

    <div class="change-log">
      <strong>【v5.0.0 メジャーアップデート内容】</strong>
      <ul>
        <li><strong>長方形プロポーション</strong>: 全長1500mmに拡大（座席・通路・操作盤が綺麗に独立）</li>
        <li><strong>床スレスレ大型ドア</strong>: 敷居高さをわずか50mmに引き下げ、車のようにスッと腰掛け可能</li>
        <li><strong>足元完全フラット化</strong>: 通路側・内側の三角リブを全廃し、躓きリスクをゼロに</li>
        <li><strong>木枠の原則</strong>: 縦の4本主角柱（90mm角×950mm）のみで構成</li>
        <li><strong>膝・足元クリアランス</strong>: コンソール高620mm、足元70cm確保</li>
      </ul>
    </div>

    <div class="section-title">ドア開閉アニメーション</div>
    <div class="control-group">
      <label for="door-slider">ドア角度: <span id="door-val">0° (全閉)</span></label>
      <input type="range" id="door-slider" min="0" max="85" value="0">
    </div>
    <div class="btn-grid">
      <button onclick="setDoor(0)">ドア全閉</button>
      <button onclick="setDoor(80)">ドアを開ける</button>
    </div>

    <div class="section-title">カメラ視点切り替え</div>
    <div class="btn-grid">
      <button id="cam-ext" class="active" onclick="setCameraMode('ext')">外観カメラ (全体)</button>
      <button id="cam-pilot" onclick="setCameraMode('pilot')">操縦席カメラ (パイロット目線)</button>
    </div>

    <div class="section-title">パーツ表示切り替え</div>
    <div class="control-group">
      <label><input type="checkbox" id="toggle-posts" checked onchange="updateVisibility()"> 縦の4本角柱 (木の枠はこれだけ)</label>
      <label><input type="checkbox" id="toggle-base" checked onchange="updateVisibility()"> 足元ベース板 & 外側安全リブ</label>
      <label><input type="checkbox" id="toggle-door" checked onchange="updateVisibility()"> 大型乗降ドア (幅750×高800mm)</label>
      <label><input type="checkbox" id="toggle-console" checked onchange="updateVisibility()"> 操作コンソール (ハンドル・スイッチ)</label>
      <label><input type="checkbox" id="toggle-seat" checked onchange="updateVisibility()"> シート & ペダル (足元70cm)</label>
      <label><input type="checkbox" id="toggle-walls" checked onchange="updateVisibility()"> 外壁パネル</label>
      <label><input type="checkbox" id="toggle-pilot" checked onchange="updateVisibility()"> パイロットシルエット</label>
    </div>

    <div class="section-title">機体スペック (v5.0.0)</div>
    <table class="spec-table">
      <tr><td>形状・比率</td><td><strong>長方形 (幅880 × 全長1500mm)</strong></td></tr>
      <tr><td>内寸横幅</td><td>700 mm (ノート: 4/5h)</td></tr>
      <tr><td>足元クリアランス</td><td><strong>約 700 mm</strong> (足を自然に伸ばせる)</td></tr>
      <tr><td>木枠フレーム</td><td><strong>縦の4本角柱のみ</strong> (90mm角×950mm)</td></tr>
      <tr><td>ドア寸法</td><td>幅 750 × 高さ 800 mm</td></tr>
      <tr><td>ドア敷居高さ</td><td><strong>わずか 50 mm</strong> (躓きなし)</td></tr>
      <tr><td>通路床面</td><td><strong>100% フラット</strong> (内側リブ全廃)</td></tr>
      <tr><td>操作コンソール</td><td>ハンドル, スイッチ, メーター</td></tr>
    </table>

    <div class="section-title">CADデータ保存先</div>
    <p style="font-size: 11px; color:#94a3b8; word-break: break-all; line-height: 1.5;">
      /Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/<br>
      • <code>cockpit_v5.0.0_assembly.step</code><br>
      • <code>cockpit_v5.0.0_assembly.stl</code><br>
      • <code>cockpit_v5.0.0_frame.step</code> / <code>.stl</code><br>
      • <code>CUT_LIST_v5.0.0.md</code>
    </p>
  </div>

  <script>
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x060911);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 10, 15000);
    camera.position.set(2100, 1600, 2200);

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
    const grid = new THREE.GridHelper(4000, 40, 0x0284c7, 0x1e293b);
    grid.position.y = 0;
    scene.add(grid);

    // Materials
    const postMat = new THREE.MeshStandardMaterial({ color: 0xd49b4b, roughness: 0.6 });
    const basePlateMat = new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.7 });
    const ribMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.5 });
    const doorMat = new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.4 });
    const handleMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, metalness: 0.8, roughness: 0.2 });
    const consoleMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4 });
    const yokeMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.5 });
    const switchMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, metalness: 0.5 });
    const seatMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });
    const seatAccentMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.6 });
    const wallMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.8, transparent: true, opacity: 0.65 });
    const pilotMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });

    // Groups
    const groupPosts = new THREE.Group();
    const groupBase = new THREE.Group();
    const groupDoor = new THREE.Group();
    const groupConsole = new THREE.Group();
    const groupSeat = new THREE.Group();
    const groupWalls = new THREE.Group();
    const groupPilot = new THREE.Group();

    scene.add(groupPosts);
    scene.add(groupBase);
    scene.add(groupDoor);
    scene.add(groupConsole);
    scene.add(groupSeat);
    scene.add(groupWalls);
    scene.add(groupPilot);

    // Dimensions: 長方形 (幅880 x 全長1500mm)
    const W_INNER = 700;
    const POST_S = 90;
    const POST_H = 950;
    const BASE_S = 300;
    const DEPTH = 1350;
    const X_L = -(W_INNER + POST_S) / 2; // -395
    const X_R =  (W_INNER + POST_S) / 2; //  395
    const Y_F = -DEPTH / 2;              // -675 (Front)
    const Y_R =  DEPTH / 2;              //  675 (Rear)

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

    // 1. 4 Heavy Posts and Flanges (木の枠は縦の4本のみ！)
    // 内側リブ全廃、外側・壁側のみに配置
    const postPositions = [
      [X_L, Y_F, -1, -1],
      [X_R, Y_F,  1, -1],
      [X_L, Y_R, -1,  1],
      [X_R, Y_R,  1,  1]
    ];

    postPositions.forEach(([px, pz, dirX, dirZ]) => {
      // 90mm主角柱
      addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);

      // 300mm角ベース板
      addBox(groupBase, BASE_S, 18, BASE_S, px, 9, pz, basePlateMat);

      // 安全三角リブ (外側のみ)
      function addRib(rotY, offsetX, offsetZ) {
        const shape = new THREE.Shape();
        shape.moveTo(0, 0);
        shape.lineTo(90, 0);
        shape.lineTo(0, 150);
        shape.closePath();

        const ribGeom = new THREE.ExtrudeGeometry(shape, { depth: 15, bevelEnabled: false });
        const ribMesh = new THREE.Mesh(ribGeom, ribMat);
        ribMesh.rotation.y = rotY;
        ribMesh.position.set(px + offsetX, 18, pz + offsetZ);
        groupBase.add(ribMesh);
      }

      if (dirX === 1) addRib(0, POST_S/2, -7.5);
      else addRib(Math.PI, -POST_S/2, 7.5);

      if (dirZ === 1) addRib(Math.PI/2, -7.5, POST_S/2);
      else addRib(-Math.PI/2, 7.5, -POST_S/2);
    });

    // 2. 乗降用大型ドア (幅750×高800mm, 敷居高さ50mm)
    const DOOR_W = 750;
    const DOOR_H = 800;
    const DOOR_Z = 50 + DOOR_H / 2;
    const DOOR_Y_C = -50;
    const HINGE_Z = DOOR_Y_C - DOOR_W / 2; // 前柱寄りがヒンジ

    const doorPivot = new THREE.Group();
    doorPivot.position.set(X_L, 0, HINGE_Z);
    groupDoor.add(doorPivot);

    const doorMesh = new THREE.Mesh(new THREE.BoxGeometry(15, DOOR_H, DOOR_W), doorMat);
    doorMesh.position.set(0, DOOR_Z, DOOR_W / 2);
    doorPivot.add(doorMesh);

    const handleOut = new THREE.Mesh(new THREE.BoxGeometry(25, 160, 30), handleMat);
    handleOut.position.set(-25, DOOR_Z, DOOR_W - 80);
    doorPivot.add(handleOut);

    const handleIn = new THREE.Mesh(new THREE.BoxGeometry(25, 160, 30), handleMat);
    handleIn.position.set(25, DOOR_Z, DOOR_W - 80);
    doorPivot.add(handleIn);

    const hinge1 = new THREE.Mesh(new THREE.CylinderGeometry(10, 10, 50, 16), handleMat);
    hinge1.position.set(0, DOOR_Z + DOOR_H/2 - 80, 0);
    doorPivot.add(hinge1);
    const hinge2 = new THREE.Mesh(new THREE.CylinderGeometry(10, 10, 50, 16), handleMat);
    hing2.position.set(0, DOOR_Z - DOOR_H/2 + 80, 0);
    doorPivot.add(hinge2);

    // 3. Control Console
    const CON_Y = 620;
    const CON_Z = Y_F + 160;
    addBox(groupConsole, W_INNER - 10, 130, 300, 0, CON_Y, CON_Z, consoleMat, -0.4);

    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(15, 15, 130, 16), switchMat);
    shaft.position.set(0, CON_Y + 35, CON_Z - 45);
    shaft.rotation.x = -0.4;
    groupConsole.add(shaft);

    addBox(groupConsole, 150, 24, 28, 0, CON_Y + 65, CON_Z - 105, yokeMat, -0.4);
    addBox(groupConsole, 24, 110, 24, -80, CON_Y + 95, CON_Z - 115, yokeMat);
    addBox(groupConsole, 24, 110, 24,  80, CON_Y + 95, CON_Z - 115, yokeMat);

    const gaugeL = new THREE.Mesh(new THREE.CylinderGeometry(36, 36, 12, 16), switchMat);
    gaugeL.position.set(-180, CON_Y + 60, CON_Z + 40);
    gaugeL.rotation.x = -0.4;
    groupConsole.add(gaugeL);

    const gaugeR = new THREE.Mesh(new THREE.CylinderGeometry(36, 36, 12, 16), switchMat);
    gaugeR.position.set(180, CON_Y + 60, CON_Z + 40);
    gaugeR.rotation.x = -0.4;
    groupConsole.add(gaugeR);

    addBox(groupConsole, 180, 8, 85, 0, CON_Y + 65, CON_Z + 50, switchMat, -0.4);

    addBox(groupConsole, 60, 25, 100, -260, 520, Y_F + 250, consoleMat);
    const throt = addBox(groupConsole, 20, 90, 35, -260, 575, Y_F + 250, yokeMat);
    throt.rotation.x = 0.35;

    // 4. Seat & Pedals (足元スペース約700mm)
    const SEAT_Z = Y_R - 240;
    addBox(groupSeat, 520, 50, 460, 0, 350, SEAT_Z, seatMat);
    const sBack = addBox(groupSeat, 500, 520, 45, 0, 630, SEAT_Z + 220, seatMat);
    sBack.rotation.x = -0.24;
    const sHead = addBox(groupSeat, 260, 150, 55, 0, 930, SEAT_Z + 270, seatAccentMat);
    sHead.rotation.x = -0.16;

    const pL = addBox(groupSeat, 85, 140, 18, -140, 70, Y_F + 120, consoleMat);
    pL.rotation.x = -0.4;
    const pR = addBox(groupSeat, 85, 140, 18,  140, 70, Y_F + 120, consoleMat);
    pR.rotation.x = -0.4;

    // 5. Walls
    addBox(groupWalls, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, wallMat);
    addBox(groupWalls, W_INNER + POST_S*2, POST_H, 12, 0, POST_H/2, Y_R + POST_S/2 + 6, wallMat);
    addBox(groupWalls, W_INNER + POST_S*2, 500, 12, 0, 250, Y_F - POST_S/2 - 6, wallMat);

    const lenFw = (DOOR_Y_C - DOOR_W/2) - (Y_F - POST_S/2);
    addBox(groupWalls, 12, POST_H, lenFw, X_L, POST_H/2, (Y_F - POST_S/2) + lenFw/2, wallMat);
    const lenRw = (Y_R + POST_S/2) - (DOOR_Y_C + DOOR_W/2);
    addBox(groupWalls, 12, POST_H, lenRw, X_L, POST_H/2, (DOOR_Y_C + DOOR_W/2) + lenRw/2, wallMat);

    // 6. Pilot Silhouette
    const pHead = new THREE.Mesh(new THREE.SphereGeometry(105, 16, 16), pilotMat);
    pHead.position.set(0, 910, SEAT_Z + 180);
    groupPilot.add(pHead);

    const pTorso = new THREE.Mesh(new THREE.CylinderGeometry(130, 110, 420, 8), pilotMat);
    pTorso.position.set(0, 630, SEAT_Z + 120);
    pTorso.rotation.x = -0.24;
    groupPilot.add(pTorso);

    const pThighs = new THREE.Mesh(new THREE.BoxGeometry(260, 90, 360), pilotMat);
    pThighs.position.set(0, 370, SEAT_Z - 80);
    groupPilot.add(pThighs);

    const pShins = new THREE.Mesh(new THREE.BoxGeometry(260, 340, 90), pilotMat);
    pShins.position.set(0, 210, Y_F + 250);
    pShins.rotation.x = 0.35;
    groupPilot.add(pShins);

    // Interactivity
    const doorSlider = document.getElementById('door-slider');
    const doorVal = document.getElementById('door-val');

    doorSlider.addEventListener('input', (e) => setDoor(parseFloat(e.target.value)));

    function setDoor(deg) {
      doorSlider.value = deg;
      doorVal.innerText = deg.toFixed(0) + '° ' + (deg > 5 ? '(開)' : '(全閉)');
      const rad = THREE.MathUtils.degToRad(deg);
      doorPivot.rotation.y = -rad;
    }

    function updateVisibility() {
      groupPosts.visible = document.getElementById('toggle-posts').checked;
      groupBase.visible = document.getElementById('toggle-base').checked;
      groupDoor.visible = document.getElementById('toggle-door').checked;
      groupConsole.visible = document.getElementById('toggle-console').checked;
      groupSeat.visible = document.getElementById('toggle-seat').checked;
      groupWalls.visible = document.getElementById('toggle-walls').checked;
      groupPilot.visible = document.getElementById('toggle-pilot').checked;
    }

    let isPilotCam = false;
    function setCameraMode(mode) {
      document.getElementById('cam-ext').classList.toggle('active', mode === 'ext');
      document.getElementById('cam-pilot').classList.toggle('active', mode === 'pilot');
      if (mode === 'pilot') {
        isPilotCam = true;
        controls.enabled = false;
        camera.position.set(0, 910, SEAT_Z + 180);
        camera.lookAt(0, CON_Y + 40, CON_Z - 50);
      } else {
        isPilotCam = false;
        controls.enabled = true;
        camera.position.set(2100, 1600, 2200);
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

# Save as versioned file AND primary file
with open(os.path.join(OUT_DIR, "cockpit_v5.0.0_viewer.html"), "w", encoding="utf-8") as f:
    f.write(html_code)

with open(os.path.join(OUT_DIR, "cockpit_viewer.html"), "w", encoding="utf-8") as f:
    f.write(html_code)

print("Saved cockpit_v5.0.0_viewer.html and updated cockpit_viewer.html!")
