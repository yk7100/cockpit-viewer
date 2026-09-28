import os

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"

html_code = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>戦闘機コクピット Mk-II (Stealth Fighter Edition) 3D Viewer</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      background: #080c14;
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
      width: 360px;
      background: rgba(13, 19, 33, 0.95);
      border-left: 1px solid #1e293b;
      padding: 20px;
      overflow-y: auto;
      box-shadow: -8px 0 30px rgba(0,0,0,0.7);
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
      letter-spacing: 0.5px;
    }
    .badge-stealth {
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
      margin-bottom: 16px;
      line-height: 1.5;
    }
    .section-title {
      font-size: 12px;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-top: 20px;
      margin-bottom: 10px;
      border-bottom: 1px solid #334155;
      padding-bottom: 4px;
      display: flex;
      justify-content: space-between;
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
      accent-color: #38bdf8;
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
      background: #2563eb;
      border-color: #38bdf8;
      color: #fff;
      transform: translateY(-1px);
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
      width: 48%;
    }
    .spec-table td:last-child {
      color: #f8fafc;
      font-weight: 600;
    }
    #hud-overlay {
      position: absolute;
      top: 20px;
      left: 20px;
      background: rgba(10, 15, 26, 0.8);
      border: 1px solid #0284c7;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 12px;
      backdrop-filter: blur(8px);
      pointer-events: none;
      box-shadow: 0 0 15px rgba(2, 132, 199, 0.3);
    }
    .hud-title {
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 6px;
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
      <div class="hud-title">◆ STEALTH COCKPIT Mk-II</div>
      <div class="legend-item"><div class="legend-color" style="background: #38bdf8;"></div> ステルス多面体ウェッジ (段ボール)</div>
      <div class="legend-item"><div class="legend-color" style="background: #e2b34a;"></div> 骨組みトラス (30mm角材×7本ジャスト)</div>
      <div class="legend-item"><div class="legend-color" style="background: #facc15;"></div> 3面パノラマキャノピー (透明ラップ)</div>
      <div class="legend-item"><div class="legend-color" style="background: #06b6d4;"></div> ガルウィングドア (アクリル板×2)</div>
      <div class="legend-item"><div class="legend-color" style="background: #f97316;"></div> ツイン・バーニアノズル (外部効果用)</div>
    </div>
  </div>

  <div id="sidebar">
    <h1>戦闘機コクピット <span class="badge-stealth">Mk-II</span></h1>
    <p class="desc">四角い箱型から、ステルス戦闘機（F-22/F-35風）のエッジの効いたクサビ型多面体フォルムへ完全進化！材料（角材×7、段ボール、アクリル×2、ラップ）はそのまま踏襲。</p>

    <div class="section-title">視点切り替え</div>
    <div class="btn-grid">
      <button id="cam-ext" class="active" onclick="setCameraMode('ext')">外観カメラ (全体)</button>
      <button id="cam-pilot" onclick="setCameraMode('pilot')">操縦席カメラ (パイロット視点)</button>
    </div>

    <div class="section-title">ガルウィングドア開閉</div>
    <div class="control-group">
      <label for="door-angle">ドア角度: <span id="door-angle-val">0° (全閉)</span></label>
      <input type="range" id="door-angle" min="0" max="85" value="0">
    </div>
    <div class="btn-grid">
      <button onclick="setDoor(0)">ドア全閉</button>
      <button onclick="setDoor(80)">ドア跳ね上げ (開)</button>
    </div>

    <div class="section-title">パーツ表示切り替え</div>
    <div class="control-group">
      <label><input type="checkbox" id="toggle-frame" checked onchange="updateVisibility()"> 木工トラス骨組み (角材 30mm)</label>
      <label><input type="checkbox" id="toggle-cardboard" checked onchange="updateVisibility()"> ステルス外装パネル (段ボール)</label>
      <label><input type="checkbox" id="toggle-wrap" checked onchange="updateVisibility()"> 3面パノラマキャノピー (ラップ)</label>
      <label><input type="checkbox" id="toggle-door" checked onchange="updateVisibility()"> ガルウィングドア (アクリル板)</label>
      <label><input type="checkbox" id="toggle-interior" checked onchange="updateVisibility()"> HUD・計器盤・HOTAS操縦系</label>
      <label><input type="checkbox" id="toggle-seat" checked onchange="updateVisibility()"> バケットシート & ペダル</label>
      <label><input type="checkbox" id="toggle-pilot" checked onchange="updateVisibility()"> 搭乗パイロットシルエット</label>
    </div>

    <div class="section-title">外壁シースルー (透過)</div>
    <div class="control-group">
      <label for="cardboard-opacity">段ボール外壁透過度: <span id="opacity-val">100%</span></label>
      <input type="range" id="cardboard-opacity" min="0" max="100" value="100" oninput="updateOpacity(this.value)">
    </div>

    <div class="section-title">機体スペック (Mk-II)</div>
    <table class="spec-table">
      <tr><td>デザイン</td><td>F-22/F-35風ステルス多面体</td></tr>
      <tr><td>外寸 (幅×奥×高)</td><td>960 × 1600 × 1250 mm</td></tr>
      <tr><td>ノーズ形状</td><td>鋭角ウェッジ (先端幅500mm)</td></tr>
      <tr><td>断面形状</td><td>ハの字六角形ファセット</td></tr>
      <tr><td>骨組み角材</td><td>30×30mm (総延長 24.1m)</td></tr>
      <tr><td>必要定尺角材(4m)</td><td><strong>7本</strong> (板書と合致)</td></tr>
      <tr><td>ドア機構</td><td>左右アクリル跳ね上げ式</td></tr>
      <tr><td>外部効果投入口</td><td>ツイン・ジェットノズル (後部)</td></tr>
    </table>

    <div class="section-title">CADデータ出力先</div>
    <p style="font-size: 11px; color:#94a3b8; word-break: break-all; line-height: 1.5;">
      /Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/<br>
      • <code>cockpit_stealth_full.step</code> (全体CAD)<br>
      • <code>cockpit_stealth_full.stl</code> (3Dメッシュ)<br>
      • <code>cockpit_stealth_frame.step</code> / <code>.stl</code><br>
      • <code>cockpit_stealth_panels.step</code> / <code>.stl</code>
    </p>
  </div>

  <script>
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x080c14);
    scene.fog = new THREE.FogExp2(0x080c14, 0.0003);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 10, 15000);
    camera.position.set(2200, 1600, 2400);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 550, 0);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0x38bdf8, 0.8);
    dirLight1.position.set(2000, 3000, 1500);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0xf97316, 0.6);
    dirLight2.position.set(-2000, 1500, -2000);
    scene.add(dirLight2);

    // Grid Floor
    const grid = new THREE.GridHelper(4000, 40, 0x0284c7, 0x1e293b);
    grid.position.y = 0;
    scene.add(grid);

    // ----------------------------------------------------
    // Materials
    // ----------------------------------------------------
    const woodMat = new THREE.MeshStandardMaterial({ color: 0xd49b4b, roughness: 0.6 });
    const stealthCardboardMat = new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      roughness: 0.4,
      metalness: 0.3,
      transparent: true,
      opacity: 1.0
    });
    const canardMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.3, metalness: 0.4 });
    const wrapMat = new THREE.MeshPhysicalMaterial({
      color: 0xfacc15,
      transparent: true,
      opacity: 0.35,
      roughness: 0.1,
      transmission: 0.85,
      thickness: 1.0
    });
    const acrylicDoorMat = new THREE.MeshPhysicalMaterial({
      color: 0x38bdf8,
      transparent: true,
      opacity: 0.5,
      roughness: 0.1,
      transmission: 0.9,
      thickness: 3.0
    });
    const seatMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });
    const seatAccentMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.6 });
    const hudMat = new THREE.MeshBasicMaterial({ color: 0x22c55e, transparent: true, opacity: 0.75, wireframe: true });
    const mfdScreenMat = new THREE.MeshBasicMaterial({ color: 0x06b6d4 });
    const mfdConsoleMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.5 });
    const nozzleGlowMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
    const pilotMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });

    // Groups
    const groupFrame = new THREE.Group();
    const groupCardboard = new THREE.Group();
    const groupWrap = new THREE.Group();
    const groupDoors = new THREE.Group();
    const groupInterior = new THREE.Group();
    const groupSeat = new THREE.Group();
    const groupPilot = new THREE.Group();

    scene.add(groupFrame);
    scene.add(groupCardboard);
    scene.add(groupWrap);
    scene.add(groupDoors);
    scene.add(groupInterior);
    scene.add(groupSeat);
    scene.add(groupPilot);

    // Helpers
    // In our coordinate system:
    // X: Width (-480..480), Y: Height (0..1250), Z: Depth (-800..800, -800=nose front, +800=rear)
    function addBeam(p1, p2) {
      const v1 = new THREE.Vector3(p1[0], p1[2], p1[1] - 800);
      const v2 = new THREE.Vector3(p2[0], p2[2], p2[1] - 800);
      const dist = v1.distanceTo(v2);
      const geom = new THREE.BoxGeometry(30, 30, dist);
      const mesh = new THREE.Mesh(geom, woodMat);
      
      const mid = new THREE.Vector3().addVectors(v1, v2).multiplyScalar(0.5);
      mesh.position.copy(mid);
      mesh.lookAt(v2);
      groupFrame.add(mesh);
    }

    // Node definitions (Matching Python script)
    const B0_L = [-250, 0, 15], B0_R = [250, 0, 15];
    const B1_L = [-320, 400, 15], B1_R = [320, 400, 15];
    const B2_L = [-370, 950, 15], B2_R = [370, 950, 15];
    const B3_L = [-370, 1600, 15], B3_R = [370, 1600, 15];

    const S0_L = [-270, 0, 460], S0_R = [270, 0, 460];
    const S1_L = [-370, 400, 460], S1_R = [370, 400, 460];
    const S2_L = [-480, 950, 460], S2_R = [480, 950, 460];
    const S3_L = [-440, 1600, 460], S3_R = [440, 1600, 460];

    const R2_L = [-320, 950, 1250], R2_R = [320, 950, 1250];
    const R3_L = [-320, 1600, 1250], R3_R = [320, 1600, 1250];

    // Frame Beams
    // Bottom
    addBeam(B0_L, B1_L); addBeam(B0_R, B1_R);
    addBeam(B1_L, B2_L); addBeam(B1_R, B2_R);
    addBeam(B2_L, B3_L); addBeam(B2_R, B3_R);
    addBeam(B0_L, B0_R); addBeam(B1_L, B1_R); addBeam(B2_L, B2_R); addBeam(B3_L, B3_R);

    // Lower Uprights
    addBeam(B0_L, S0_L); addBeam(B0_R, S0_R);
    addBeam(B1_L, S1_L); addBeam(B1_R, S1_R);
    addBeam(B2_L, S2_L); addBeam(B2_R, S2_R);
    addBeam(B3_L, S3_L); addBeam(B3_R, S3_R);

    // Shoulder Rails
    addBeam(S0_L, S1_L); addBeam(S0_R, S1_R);
    addBeam(S1_L, S2_L); addBeam(S1_R, S2_R);
    addBeam(S2_L, S3_L); addBeam(S2_R, S3_R);
    addBeam(S0_L, S0_R); addBeam(S1_L, S1_R);

    // A-Pillars & Roof
    addBeam(S1_L, R2_L); addBeam(S1_R, R2_R);
    addBeam([0, 400, 490], [0, 950, 1280]); // Center Keel
    addBeam(R2_L, R2_R); addBeam(R3_L, R3_R);
    addBeam(R2_L, R3_L); addBeam(R2_R, R3_R);
    addBeam(R3_L, S3_L); addBeam(R3_R, S3_R);

    // Seat frame
    addBeam([-250, 1050, 350], [250, 1050, 350]);
    addBeam([-250, 1450, 350], [250, 1450, 350]);

    // ----------------------------------------------------
    // Stealth Panels & Airframe
    // ----------------------------------------------------
    // Nose Top Deck (Wedge)
    const noseGeom = new THREE.BufferGeometry();
    const noseVertices = new Float32Array([
      -270, 460, -800,   270, 460, -800,  -370, 460, -400,
       270, 460, -800,   370, 460, -400,  -370, 460, -400,
      // Front flat
      -270, 460, -800,  -250,  15, -800,   270, 460, -800,
       270, 460, -800,  -250,  15, -800,   250,  15, -800,
    ]);
    noseGeom.setAttribute('position', new THREE.BufferAttribute(noseVertices, 3));
    noseGeom.computeVertexNormals();
    groupCardboard.add(new THREE.Mesh(noseGeom, stealthCardboardMat));

    // Side Facet Lower Panels
    function addSideFacet(p1, p2, p3, p4) {
      const g = new THREE.BufferGeometry();
      const v = new Float32Array([
        p1[0], p1[2], p1[1]-800,  p2[0], p2[2], p2[1]-800,  p3[0], p3[2], p3[1]-800,
        p2[0], p2[2], p2[1]-800,  p4[0], p4[2], p4[1]-800,  p3[0], p3[2], p3[1]-800,
      ]);
      g.setAttribute('position', new THREE.BufferAttribute(v, 3));
      g.computeVertexNormals();
      groupCardboard.add(new THREE.Mesh(g, stealthCardboardMat));
    }
    // Left Lower side
    addSideFacet(B0_L, S0_L, B1_L, S1_L);
    addSideFacet(B1_L, S1_L, B2_L, S2_L);
    addSideFacet(B2_L, S2_L, B3_L, S3_L);
    // Right Lower side
    addSideFacet(S0_R, B0_R, S1_R, B1_R);
    addSideFacet(S1_R, B1_R, S2_R, B2_R);
    addSideFacet(S2_R, B2_R, S3_R, B3_R);

    // Canards (エアロフィン: 左右)
    const canardL = new THREE.Mesh(new THREE.BoxGeometry(180, 10, 240), canardMat);
    canardL.position.set(-390, 470, -550);
    canardL.rotation.y = -0.3;
    canardL.rotation.z = -0.15;
    groupCardboard.add(canardL);

    const canardR = new THREE.Mesh(new THREE.BoxGeometry(180, 10, 240), canardMat);
    canardR.position.set(390, 470, -550);
    canardR.rotation.y = 0.3;
    canardR.rotation.z = 0.15;
    groupCardboard.add(canardR);

    // Rear Jet Nozzles (ツイン・アフターバーナー: 外部効果用)
    const nozzleL = new THREE.Mesh(new THREE.CylinderGeometry(140, 160, 180, 24, 1, true), canardMat);
    nozzleL.position.set(-200, 450, 890);
    nozzleL.rotation.x = Math.PI / 2;
    groupCardboard.add(nozzleL);

    const nozzleGlowL = new THREE.Mesh(new THREE.CircleGeometry(130, 24), nozzleGlowMat);
    nozzleGlowL.position.set(-200, 450, 880);
    groupCardboard.add(nozzleGlowL);

    const nozzleR = new THREE.Mesh(new THREE.CylinderGeometry(140, 160, 180, 24, 1, true), canardMat);
    nozzleR.position.set(200, 450, 890);
    nozzleR.rotation.x = Math.PI / 2;
    groupCardboard.add(nozzleR);

    const nozzleGlowR = new THREE.Mesh(new THREE.CircleGeometry(130, 24), nozzleGlowMat);
    nozzleGlowR.position.set(200, 450, 880);
    groupCardboard.add(nozzleGlowR);

    // ----------------------------------------------------
    // Panoramic 3-Piece Canopy (ラップ窓)
    // ----------------------------------------------------
    // Center Slanted Windshield
    const cWindGeom = new THREE.BufferGeometry();
    const cWindV = new Float32Array([
      -370, 460, -400,   370, 460, -400,   -320, 1250, 150,
       370, 460, -400,   320, 1250, 150,   -320, 1250, 150,
    ]);
    cWindGeom.setAttribute('position', new THREE.BufferAttribute(cWindV, 3));
    cWindGeom.computeVertexNormals();
    groupWrap.add(new THREE.Mesh(cWindGeom, wrapMat));

    // Left/Right Quarter Windows
    const qWinL = new THREE.BufferGeometry();
    qWinL.setAttribute('position', new THREE.BufferAttribute(new Float32Array([
      -370, 460, -400,  -320, 1250, 150,  -480, 460, 150
    ]), 3));
    qWinL.computeVertexNormals();
    groupWrap.add(new THREE.Mesh(qWinL, wrapMat));

    const qWinR = new THREE.BufferGeometry();
    qWinR.setAttribute('position', new THREE.BufferAttribute(new Float32Array([
       370, 460, -400,   480,  460, 150,   320, 1250, 150
    ]), 3));
    qWinR.computeVertexNormals();
    groupWrap.add(new THREE.Mesh(qWinR, wrapMat));

    // ----------------------------------------------------
    // Gullwing Acrylic Doors (跳ね上げドア)
    // ----------------------------------------------------
    const doorPivotL = new THREE.Group();
    doorPivotL.position.set(-320, 1250, 150 + 325); // hinge along roof edge
    groupDoors.add(doorPivotL);

    const doorPanelL = new THREE.Mesh(new THREE.BoxGeometry(6, 790, 650), acrylicDoorMat);
    doorPanelL.position.set(-60, -395, 0);
    doorPanelL.rotation.z = -0.15; // slightly flared
    doorPivotL.add(doorPanelL);

    const doorPivotR = new THREE.Group();
    doorPivotR.position.set(320, 1250, 150 + 325);
    groupDoors.add(doorPivotR);

    const doorPanelR = new THREE.Mesh(new THREE.BoxGeometry(6, 790, 650), acrylicDoorMat);
    doorPanelR.position.set(60, -395, 0);
    doorPanelR.rotation.z = 0.15;
    doorPivotR.add(doorPanelR);

    // ----------------------------------------------------
    // Cockpit Interior (HUD, MFDs, HOTAS, Seat)
    // ----------------------------------------------------
    // HUD Glass
    const hud = new THREE.Mesh(new THREE.BoxGeometry(260, 180, 4), hudMat);
    hud.position.set(0, 780, -80);
    hud.rotation.x = 0.6;
    groupInterior.add(hud);

    // MFD Panels (3 Screens)
    const mfdC = new THREE.Mesh(new THREE.BoxGeometry(260, 150, 20), mfdConsoleMat);
    mfdC.position.set(0, 640, -140);
    mfdC.rotation.x = -0.4;
    groupInterior.add(mfdC);

    const mfdScreenC = new THREE.Mesh(new THREE.PlaneGeometry(240, 130), mfdScreenMat);
    mfdScreenC.position.set(0, 640, -128);
    mfdScreenC.rotation.x = -0.4;
    groupInterior.add(mfdScreenC);

    const mfdL = new THREE.Mesh(new THREE.BoxGeometry(160, 130, 20), mfdConsoleMat);
    mfdL.position.set(-230, 630, -120);
    mfdL.rotation.set(-0.4, 0.35, 0);
    groupInterior.add(mfdL);

    const mfdR = new THREE.Mesh(new THREE.BoxGeometry(160, 130, 20), mfdConsoleMat);
    mfdR.position.set(230, 630, -120);
    mfdR.rotation.set(-0.4, -0.35, 0);
    groupInterior.add(mfdR);

    // HOTAS: Flight Stick (Right)
    const stickBase = new THREE.Mesh(new THREE.CylinderGeometry(40, 50, 20, 16), mfdConsoleMat);
    stickBase.position.set(220, 480, 50);
    groupInterior.add(stickBase);
    const stickGrip = new THREE.Mesh(new THREE.BoxGeometry(35, 140, 45), seatAccentMat);
    stickGrip.position.set(220, 550, 50);
    stickGrip.rotation.x = -0.15;
    groupInterior.add(stickGrip);

    // HOTAS: Twin Throttle (Left)
    const throtBase = new THREE.Mesh(new THREE.BoxGeometry(80, 20, 120), mfdConsoleMat);
    throtBase.position.set(-220, 480, 50);
    groupInterior.add(throtBase);
    const throtLev1 = new THREE.Mesh(new THREE.BoxGeometry(25, 80, 45), seatAccentMat);
    throtLev1.position.set(-235, 530, 40);
    groupInterior.add(throtLev1);
    const throtLev2 = new THREE.Mesh(new THREE.BoxGeometry(25, 80, 45), seatAccentMat);
    throtLev2.position.set(-205, 530, 60);
    groupInterior.add(throtLev2);

    // Rudder Pedals
    const pedL = new THREE.Mesh(new THREE.BoxGeometry(80, 120, 20), mfdConsoleMat);
    pedL.position.set(-140, 120, -320);
    pedL.rotation.x = -0.5;
    groupInterior.add(pedL);
    const pedR = new THREE.Mesh(new THREE.BoxGeometry(80, 120, 20), mfdConsoleMat);
    pedR.position.set(140, 120, -320);
    pedR.rotation.x = -0.5;
    groupInterior.add(pedR);

    // Bucket Seat
    const sCush = new THREE.Mesh(new THREE.BoxGeometry(460, 60, 440), seatMat);
    sCush.position.set(0, 380, 420);
    groupSeat.add(sCush);

    const sBack = new THREE.Mesh(new THREE.BoxGeometry(440, 560, 50), seatMat);
    sBack.position.set(0, 660, 620);
    sBack.rotation.x = -0.22;
    groupSeat.add(sBack);

    const sHead = new THREE.Mesh(new THREE.BoxGeometry(240, 160, 60), seatAccentMat);
    sHead.position.set(0, 970, 690);
    groupSeat.add(sHead);

    // Shoulder Supports
    const supL = new THREE.Mesh(new THREE.BoxGeometry(60, 380, 100), seatAccentMat);
    supL.position.set(-210, 680, 570);
    supL.rotation.set(-0.22, 0.25, 0);
    groupSeat.add(supL);
    const supR = new THREE.Mesh(new THREE.BoxGeometry(60, 380, 100), seatAccentMat);
    supR.position.set(210, 680, 570);
    supR.rotation.set(-0.22, -0.25, 0);
    groupSeat.add(supR);

    // Pilot Silhouette
    const pHead = new THREE.Mesh(new THREE.SphereGeometry(105, 16, 16), pilotMat);
    pHead.position.set(0, 960, 460);
    groupPilot.add(pHead);

    const pTorso = new THREE.Mesh(new THREE.CylinderGeometry(130, 110, 420, 8), pilotMat);
    pTorso.position.set(0, 670, 480);
    pTorso.rotation.x = -0.22;
    groupPilot.add(pTorso);

    const pThighs = new THREE.Mesh(new THREE.BoxGeometry(260, 90, 360), pilotMat);
    pThighs.position.set(0, 420, 300);
    groupPilot.add(pThighs);

    const pShins = new THREE.Mesh(new THREE.BoxGeometry(260, 340, 90), pilotMat);
    pShins.position.set(0, 240, -10);
    pShins.rotation.x = 0.45;
    groupPilot.add(pShins);

    // ----------------------------------------------------
    // UI Handlers & Interactivity
    // ----------------------------------------------------
    const doorSlider = document.getElementById('door-angle');
    const doorVal = document.getElementById('door-angle-val');

    doorSlider.addEventListener('input', (e) => setDoor(parseFloat(e.target.value)));

    function setDoor(deg) {
      doorSlider.value = deg;
      doorVal.innerText = deg.toFixed(0) + '° ' + (deg > 10 ? '(跳ね上げ開)' : '(全閉)');
      const rad = THREE.MathUtils.degToRad(deg);
      doorPivotL.rotation.z = rad;
      doorPivotR.rotation.z = -rad;
    }

    function updateVisibility() {
      groupFrame.visible = document.getElementById('toggle-frame').checked;
      groupCardboard.visible = document.getElementById('toggle-cardboard').checked;
      groupWrap.visible = document.getElementById('toggle-wrap').checked;
      groupDoors.visible = document.getElementById('toggle-door').checked;
      groupInterior.visible = document.getElementById('toggle-interior').checked;
      groupSeat.visible = document.getElementById('toggle-seat').checked;
      groupPilot.visible = document.getElementById('toggle-pilot').checked;
    }

    function updateOpacity(val) {
      document.getElementById('opacity-val').innerText = val + '%';
      stealthCardboardMat.opacity = val / 100.0;
    }

    let isPilotCam = false;
    function setCameraMode(mode) {
      document.getElementById('cam-ext').classList.toggle('active', mode === 'ext');
      document.getElementById('cam-pilot').classList.toggle('active', mode === 'pilot');
      if (mode === 'pilot') {
        isPilotCam = true;
        controls.enabled = false;
        camera.position.set(0, 960, 460); // Eye point
        camera.lookAt(0, 780, -800);      // Looking through HUD forward
      } else {
        isPilotCam = false;
        controls.enabled = true;
        camera.position.set(2200, 1600, 2400);
        controls.target.set(0, 550, 0);
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

print("Updated cockpit_viewer.html with Stealth Fighter Mk-II design!")
