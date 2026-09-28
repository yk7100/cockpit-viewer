import os

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"

html_code = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>コクピット 3Dビューア (縦4本柱・広々空間・開閉扉モデル)</title>
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
      background: linear-gradient(135deg, #10b981, #059669);
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
    .card-info {
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid #0284c7;
      border-radius: 6px;
      padding: 10px 12px;
      font-size: 11.5px;
      margin-bottom: 16px;
      line-height: 1.6;
      color: #bae6fd;
    }
    .card-info strong { color: #38bdf8; }
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
      <div class="hud-title">◆ コクピット最新仕様</div>
      <div class="legend-item"><div class="legend-color" style="background: #e2b34a;"></div> 木の枠：縦の4本角柱のみ (90mm角)</div>
      <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> 足元ベース板 (30cm角) ＋ 三角リブ</div>
      <div class="legend-item"><div class="legend-color" style="background: #10b981;"></div> 乗降用 開閉扉 (ドア)</div>
      <div class="legend-item"><div class="legend-color" style="background: #38bdf8;"></div> 操作コンソール (ハンドル・スイッチ盤)</div>
      <div class="legend-item"><div class="legend-color" style="background: #0284c7;"></div> 操縦席シート (ゆったり空間)</div>
    </div>
  </div>

  <div id="sidebar">
    <h1>操縦席ユニット <span class="badge-fixed">最新仕様</span></h1>
    <p class="desc">「木の枠は縦の4本だけ」「もっと人が入るスペース」「乗降扉をつける」というご指示を忠実に反映したモデルです。</p>

    <div class="card-info">
      <strong>【最新の確定仕様】</strong><br>
      • 木の枠: <strong>縦の4本角柱（90mm角×950mm）のみ</strong><br>
      • 広々空間: <strong>奥行き1200mm</strong>（足元ゆったり約70cm）<br>
      • 乗降扉: <strong>左側面に開閉スイングドア</strong>を新設<br>
      • 足元補強: 300mm角ベース板 ＋ 三角補強リブ<br>
      • 操作コンソール: ハンドル・スイッチ盤・メーター
    </div>

    <div class="section-title">扉（ドア）の開閉操作</div>
    <div class="control-group">
      <label for="door-slider">ドア開閉角度: <span id="door-val">0° (全閉)</span></label>
      <input type="range" id="door-slider" min="0" max="85" value="0">
    </div>
    <div class="btn-grid">
      <button onclick="setDoor(0)">ドア全閉</button>
      <button onclick="setDoor(80)">ドアを開ける</button>
    </div>

    <div class="section-title">視点切り替え</div>
    <div class="btn-grid">
      <button id="cam-ext" class="active" onclick="setCameraMode('ext')">外観カメラ (全体)</button>
      <button id="cam-pilot" onclick="setCameraMode('pilot')">操縦席カメラ (パイロット目線)</button>
    </div>

    <div class="section-title">パーツ表示切り替え</div>
    <div class="control-group">
      <label><input type="checkbox" id="toggle-posts" checked onchange="updateVisibility()"> 縦の4本角柱 (木の枠はこれだけ)</label>
      <label><input type="checkbox" id="toggle-base" checked onchange="updateVisibility()"> 足元ベース板 & 三角補強リブ</label>
      <label><input type="checkbox" id="toggle-door" checked onchange="updateVisibility()"> 開閉扉 (ドア)</label>
      <label><input type="checkbox" id="toggle-console" checked onchange="updateVisibility()"> 操作コンソール (ハンドル・スイッチ)</label>
      <label><input type="checkbox" id="toggle-seat" checked onchange="updateVisibility()"> シート & ラダーペダル</label>
      <label><input type="checkbox" id="toggle-walls" checked onchange="updateVisibility()"> 外壁パネル</label>
      <label><input type="checkbox" id="toggle-pilot" checked onchange="updateVisibility()"> パイロットシルエット</label>
    </div>

    <div class="section-title">機体確定スペック</div>
    <table class="spec-table">
      <tr><td>木枠フレーム</td><td><strong>縦の4本角柱のみ</strong> (90mm角)</td></tr>
      <tr><td>内寸横幅</td><td>750 mm (ゆったり幅)</td></tr>
      <tr><td>奥行き (スパン)</td><td><strong>1200 mm</strong> (人が余裕で乗降可能)</td></tr>
      <tr><td>柱の高さ</td><td>950 mm</td></tr>
      <tr><td>乗降扉 (ドア)</td><td>幅750 × 高750 mm (取っ手付)</td></tr>
      <tr><td>足元ベース板</td><td>300 × 300 mm (4枚)</td></tr>
      <tr><td>足元補強</td><td>直角三角リブ (硬めの素材)</td></tr>
      <tr><td>操作コンソール</td><td>ハンドル, スイッチ, メーター</td></tr>
    </table>

    <div class="section-title">CADデータ保存先</div>
    <p style="font-size: 11px; color:#94a3b8; word-break: break-all; line-height: 1.5;">
      /Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/<br>
      • <code>cockpit_assembly_full.step</code> (全体CAD)<br>
      • <code>cockpit_assembly_full.stl</code> (3Dメッシュ)<br>
      • <code>cockpit_frame.step</code> / <code>.stl</code> (縦4本柱)<br>
      • <code>CUT_LIST.md</code> (木取り・組み立て手順)
    </p>
  </div>

  <script>
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x090d16);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 10, 15000);
    camera.position.set(1900, 1500, 2100);

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
    const grid = new THREE.GridHelper(3500, 35, 0x0284c7, 0x1e293b);
    grid.position.y = 0;
    scene.add(grid);

    // ----------------------------------------------------
    // Materials
    // ----------------------------------------------------
    const postMat = new THREE.MeshStandardMaterial({ color: 0xd49b4b, roughness: 0.6 }); // 90mm角柱
    const basePlateMat = new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.7 }); // ベース板
    const ribMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.5 }); // 三角リブ
    const doorMat = new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.4 }); // ドア
    const handleMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, metalness: 0.8, roughness: 0.2 });
    const consoleMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4 });
    const yokeMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.5 }); // ハンドル
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

    // Dimensions
    const W_INNER = 750;
    const POST_S = 90;
    const POST_H = 950;
    const BASE_S = 300;
    const DEPTH = 1200;
    const X_L = -(W_INNER + POST_S) / 2; // -420
    const X_R =  (W_INNER + POST_S) / 2; //  420
    const Y_F = -DEPTH / 2;              // -600 (Front)
    const Y_R =  DEPTH / 2;              //  600 (Rear)

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

    // 1. 4 Heavy Posts and Flanges ONLY (木の枠は縦の4本だけ！)
    const postPositions = [
      [X_L, Y_F], [X_R, Y_F],
      [X_L, Y_R], [X_R, Y_R]
    ];

    postPositions.forEach(([px, pz]) => {
      // 90mm主角柱 (高さ950mm)
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

    // 2. 開閉扉 (ドア: 左側面)
    // ヒンジ軸を後柱側のドア端 (Z: Y_R - 150) に配置
    const DOOR_W = 750;
    const DOOR_H = 750;
    const DOOR_Z = 120 + DOOR_H / 2;
    const HINGE_Z = 350; // ヒンジ位置

    const doorPivot = new THREE.Group();
    doorPivot.position.set(X_L, 0, HINGE_Z); // ヒンジの回転中心
    groupDoor.add(doorPivot);

    // ドアパネル本体 (ヒンジから前方へ伸びる)
    const doorMesh = new THREE.Mesh(new THREE.BoxGeometry(15, DOOR_H, DOOR_W), doorMat);
    doorMesh.position.set(0, DOOR_Z, -DOOR_W / 2);
    doorPivot.add(doorMesh);

    // ドア取っ手 (ハンドル: ドア先端外側)
    const dHandle = new THREE.Mesh(new THREE.BoxGeometry(25, 160, 30), handleMat);
    dHandle.position.set(-25, DOOR_Z, -DOOR_W + 80);
    doorPivot.add(dHandle);

    // ヒンジ金具 (2箇所)
    const hinge1 = new THREE.Mesh(new THREE.CylinderGeometry(10, 10, 50, 16), handleMat);
    hinge1.position.set(0, DOOR_Z + DOOR_H/2 - 60, 0);
    doorPivot.add(hinge1);
    const hinge2 = new THREE.Mesh(new THREE.CylinderGeometry(10, 10, 50, 16), handleMat);
    hing2.position.set(0, DOOR_Z - DOOR_H/2 + 60, 0);
    doorPivot.add(hinge2);

    // 3. Control Console (操作コンソール: 前柱間にマウント)
    const CON_Y = 600;
    const CON_Z = Y_F + 160;
    // Console Body
    addBox(groupConsole, W_INNER - 10, 140, 320, 0, CON_Y, CON_Z, consoleMat, -0.4);

    // Flight Yoke (操縦ハンドル)
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(15, 15, 130, 16), switchMat);
    shaft.position.set(0, CON_Y + 35, CON_Z - 45);
    shaft.rotation.x = -0.4;
    groupConsole.add(shaft);

    addBox(groupConsole, 150, 24, 28, 0, CON_Y + 65, CON_Z - 105, yokeMat, -0.4);
    addBox(groupConsole, 24, 110, 24, -80, CON_Y + 95, CON_Z - 115, yokeMat);
    addBox(groupConsole, 24, 110, 24,  80, CON_Y + 95, CON_Z - 115, yokeMat);

    // Gauges & Switches
    const gaugeL = new THREE.Mesh(new THREE.CylinderGeometry(36, 36, 12, 16), switchMat);
    gaugeL.position.set(-190, CON_Y + 60, CON_Z + 40);
    gaugeL.rotation.x = -0.4;
    groupConsole.add(gaugeL);

    const gaugeR = new THREE.Mesh(new THREE.CylinderGeometry(36, 36, 12, 16), switchMat);
    gaugeR.position.set(190, CON_Y + 60, CON_Z + 40);
    gaugeR.rotation.x = -0.4;
    groupConsole.add(gaugeR);

    addBox(groupConsole, 180, 8, 85, 0, CON_Y + 65, CON_Z + 50, switchMat, -0.4);

    // Throttle Lever
    addBox(groupConsole, 60, 25, 100, -270, 510, Y_F + 250, consoleMat);
    const throt = addBox(groupConsole, 20, 90, 35, -270, 565, Y_F + 250, yokeMat);
    throt.rotation.x = 0.35;

    // 4. Seat & Pedals (奥行き1200mmを活かしたゆったり配置)
    const SEAT_Z = Y_R - 220;
    addBox(groupSeat, 520, 50, 460, 0, 360, SEAT_Z, seatMat);
    const sBack = addBox(groupSeat, 500, 520, 45, 0, 640, SEAT_Z + 220, seatMat);
    sBack.rotation.x = -0.22;
    const sHead = addBox(groupSeat, 260, 150, 55, 0, 940, SEAT_Z + 265, seatAccentMat);
    sHead.rotation.x = -0.15;

    // Rudder Pedals (前柱足元)
    const pL = addBox(groupSeat, 85, 140, 18, -140, 70, Y_F + 100, consoleMat);
    pL.rotation.x = -0.4;
    const pR = addBox(groupSeat, 85, 140, 18,  140, 70, Y_F + 100, consoleMat);
    pR.rotation.x = -0.4;

    // 5. Walls (外壁パネル: 右側面・背面・前下面・ドア前後)
    addBox(groupWalls, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, wallMat);
    addBox(groupWalls, W_INNER + POST_S*2, POST_H, 12, 0, POST_H/2, Y_R + POST_S/2 + 6, wallMat);
    addBox(groupWalls, W_INNER + POST_S*2, 500, 12, 0, 250, Y_F - POST_S/2 - 6, wallMat);
    // 左側面の固定部 (ドアの前後の小壁)
    const fixedWallLen = (DEPTH - DOOR_W) / 2;
    addBox(groupWalls, 12, POST_H, fixedWallLen, X_L, POST_H/2, Y_F + fixedWallLen/2 + POST_S/2, wallMat);
    addBox(groupWalls, 12, POST_H, fixedWallLen, X_L, POST_H/2, Y_R - fixedWallLen/2 - POST_S/2, wallMat);

    // 6. Pilot Silhouette
    const pHead = new THREE.Mesh(new THREE.SphereGeometry(105, 16, 16), pilotMat);
    pHead.position.set(0, 920, SEAT_Z + 180);
    groupPilot.add(pHead);

    const pTorso = new THREE.Mesh(new THREE.CylinderGeometry(130, 110, 420, 8), pilotMat);
    pTorso.position.set(0, 640, SEAT_Z + 120);
    pTorso.rotation.x = -0.22;
    groupPilot.add(pTorso);

    const pThighs = new THREE.Mesh(new THREE.BoxGeometry(260, 90, 360), pilotMat);
    pThighs.position.set(0, 380, SEAT_Z - 80);
    groupPilot.add(pThighs);

    const pShins = new THREE.Mesh(new THREE.BoxGeometry(260, 340, 90), pilotMat);
    pShins.position.set(0, 220, Y_F + 220);
    pShins.rotation.x = 0.35;
    groupPilot.add(pShins);

    // ----------------------------------------------------
    // Interactivity
    // ----------------------------------------------------
    const doorSlider = document.getElementById('door-slider');
    const doorVal = document.getElementById('door-val');

    doorSlider.addEventListener('input', (e) => setDoor(parseFloat(e.target.value)));

    function setDoor(deg) {
      doorSlider.value = deg;
      doorVal.innerText = deg.toFixed(0) + '° ' + (deg > 5 ? '(開)' : '(全閉)');
      const rad = THREE.MathUtils.degToRad(deg);
      doorPivot.rotation.y = rad; // 外側へスイングオープン
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
        camera.position.set(0, 920, SEAT_Z + 180); // Eye point
        camera.lookAt(0, CON_Y + 40, CON_Z - 50);   // Looking at Yoke & Console
      } else {
        isPilotCam = false;
        controls.enabled = true;
        camera.position.set(1900, 1500, 2100);
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

print("Updated cockpit_viewer.html with 4 posts and door!")
