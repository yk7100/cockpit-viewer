#!/usr/bin/env python3
"""
Generate Cockpit v6.0.0 3D Web Viewer (index.html and cockpit_v6.0.0_viewer.html)
Features:
- Pilot-facing Flight Control Yoke (corrected from facing outwards)
- Newly added Flight Desk in front of seat (680mm W x 380mm D x 700mm H)
- Twin gauges, MFD screen, and throttle unit on desk
- Under-desk legroom 100% flat and unobstructed
- Pilot seat perspective camera showing the desk and yoke directly in front of hands
- Full mobile / tablet Safari compatibility with local Three.js & OrbitControls
"""

html_code = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>COCKPIT v6.0.0 (操縦デスク新設・パイロット正対操縦桿モデル)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      width: 100%;
      height: 100%;
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
      background: #060911;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    }
    body {
      display: flex;
      flex-direction: row;
    }
    #canvas-container {
      flex: 1;
      height: 100%;
      position: relative;
      background: #060911;
      overflow: hidden;
      touch-action: none;
    }
    #canvas-container canvas {
      display: block;
      width: 100% !important;
      height: 100% !important;
      touch-action: none;
    }
    #sidebar {
      width: 380px;
      flex-shrink: 0;
      background: rgba(13, 19, 33, 0.97);
      border-left: 1px solid #1e293b;
      padding: 18px;
      overflow-y: auto;
      box-shadow: -8px 0 30px rgba(0,0,0,0.85);
      backdrop-filter: blur(14px);
      z-index: 10;
      -webkit-overflow-scrolling: touch;
    }
    .version-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }
    h1 {
      font-size: 19px;
      color: #38bdf8;
      letter-spacing: 0.5px;
    }
    .badge-v6 {
      font-size: 11px;
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #fff;
      padding: 3px 9px;
      border-radius: 9999px;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(37, 99, 235, 0.5);
    }
    p.desc {
      font-size: 12px;
      color: #94a3b8;
      margin-bottom: 12px;
      line-height: 1.5;
    }
    .change-log {
      background: rgba(2, 132, 199, 0.15);
      border: 1px solid #0284c7;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 11px;
      margin-bottom: 14px;
      line-height: 1.5;
      color: #bae6fd;
    }
    .change-log strong { color: #38bdf8; font-size: 11.5px; }
    .change-log ul { margin-left: 14px; margin-top: 4px; }
    .section-title {
      font-size: 12px;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-top: 14px;
      margin-bottom: 8px;
      border-bottom: 1px solid #334155;
      padding-bottom: 4px;
    }
    .control-group {
      margin-bottom: 10px;
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
      height: 6px;
      accent-color: #38bdf8;
    }
    .btn-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 8px;
    }
    button {
      background: #1e293b;
      color: #f1f5f9;
      border: 1px solid #334155;
      padding: 9px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
    }
    button:hover, button:active {
      background: #0284c7;
      border-color: #38bdf8;
      color: #fff;
    }
    button.active {
      background: #0284c7;
      border-color: #38bdf8;
      color: #fff;
      font-weight: 700;
    }
    .spec-table {
      width: 100%;
      font-size: 11px;
      border-collapse: collapse;
      margin-top: 6px;
    }
    .spec-table td {
      padding: 5px 4px;
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
      top: 16px;
      left: 16px;
      background: rgba(13, 19, 33, 0.92);
      border: 1px solid #0284c7;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 11px;
      backdrop-filter: blur(10px);
      pointer-events: none;
      box-shadow: 0 0 20px rgba(2, 132, 199, 0.35);
      z-index: 5;
    }
    .hud-title {
      font-weight: 800;
      color: #38bdf8;
      font-size: 12px;
      margin-bottom: 6px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 3px;
      font-size: 10.5px;
    }
    .legend-color {
      width: 10px;
      height: 10px;
      border-radius: 2px;
    }
    #error-banner {
      display: none;
      position: absolute;
      top: 10px;
      left: 10px;
      right: 10px;
      z-index: 99999;
      background: rgba(220, 38, 38, 0.95);
      color: white;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 12px;
      line-height: 1.5;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    #loading-indicator {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: #38bdf8;
      font-size: 14px;
      pointer-events: none;
      z-index: 4;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }
    .spinner {
      width: 32px;
      height: 32px;
      border: 3px solid rgba(56, 189, 248, 0.2);
      border-top-color: #38bdf8;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* スマホ・タブレット用レスポンシブスタイル */
    @media (max-width: 768px) {
      body {
        flex-direction: column;
      }
      #canvas-container {
        height: 52vh;
        height: 52dvh;
        width: 100%;
        flex: none;
      }
      #sidebar {
        width: 100%;
        height: 48vh;
        height: 48dvh;
        border-left: none;
        border-top: 1px solid #334155;
        padding: 14px 16px;
        flex: 1;
      }
      #hud-overlay {
        top: 10px;
        left: 10px;
        padding: 6px 10px;
        font-size: 10px;
      }
      .hud-title { font-size: 11px; margin-bottom: 4px; }
      .legend-item { font-size: 9.5px; margin-bottom: 2px; }
      h1 { font-size: 17px; }
    }
  </style>

  <!-- ローカルライブラリ読み込み（CDN依存のブロック・タイムアウトを防止） -->
  <script src="three.min.js"></script>
  <script>
    if (typeof THREE === 'undefined') {
      document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"><\\/script>');
    }
  </script>
  <script src="OrbitControls.js"></script>
  <script>
    if (typeof THREE !== 'undefined' && !THREE.OrbitControls) {
      document.write('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"><\\/script>');
    }
  </script>
</head>
<body>
  <div id="error-banner">
    <strong style="display:block; font-size:13px; margin-bottom:4px;">⚠️ 3D描画エラー</strong>
    <span id="error-msg"></span>
  </div>

  <div id="canvas-container">
    <div id="loading-indicator">
      <div class="spinner"></div>
      <span>3Dコックピット読み込み中...</span>
    </div>

    <div id="hud-overlay">
      <div class="hud-title">◆ COCKPIT v6.0.0</div>
      <div class="legend-item"><div class="legend-color" style="background: #e2b34a;"></div> 木の枠：縦の4本角柱のみ (90mm角)</div>
      <div class="legend-item"><div class="legend-color" style="background: #c28b48;"></div> 【新設】操縦デスク (幅680×高700mm)</div>
      <div class="legend-item"><div class="legend-color" style="background: #f59e0b;"></div> パイロット正対操縦桿 (手前向き)</div>
      <div class="legend-item"><div class="legend-color" style="background: #10b981;"></div> 大型乗降ドア (敷居高さ50mm)</div>
      <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> 足元ベース＆外側リブ (床完全フラット)</div>
      <div class="legend-item"><div class="legend-color" style="background: #0284c7;"></div> 操縦席シート (座面高さ350mm)</div>
    </div>
  </div>

  <div id="sidebar">
    <div class="version-header">
      <h1>操縦席ユニット</h1>
      <span class="badge-v6">v6.0.0</span>
    </div>
    <p class="desc">スマホ・iPad対応3Dビューア。画面スワイプで360度回転、ピンチで拡大縮小できます。</p>

    <div class="change-log">
      <strong>【v6.0.0 アップデート内容】</strong>
      <ul>
        <li><strong>操縦桿の向き修正</strong>: 外向きからパイロット（手前）正対向きへ完全修正</li>
        <li><strong>操縦デスク（机）新設</strong>: 椅子の前に幅680×奥380×高700mmの机を配置</li>
        <li><strong>机上本格コックピット</strong>: 傾斜計器盤、液晶画面、スロットルレバーを配置</li>
        <li><strong>足元空間の維持</strong>: 机下は両側板脚構造で中央足元は完全オープン・躓きゼロ</li>
        <li><strong>木枠の原則堅持</strong>: 骨組みは縦の4本主角柱（90mm角）のみ</li>
      </ul>
    </div>

    <div class="section-title">ドア開閉操作</div>
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
      <button id="cam-ext" class="active" onclick="setCameraMode('ext')">外観カメラ</button>
      <button id="cam-pilot" onclick="setCameraMode('pilot')">操縦席カメラ (机・操縦桿)</button>
    </div>

    <div class="section-title">パーツ表示切り替え</div>
    <div class="control-group">
      <label><input type="checkbox" id="toggle-posts" checked onchange="updateVisibility()"> 縦の4本角柱 (木の枠はこれだけ)</label>
      <label><input type="checkbox" id="toggle-desk" checked onchange="updateVisibility()"> 【新設】操縦デスク (机天板&側板)</label>
      <label><input type="checkbox" id="toggle-console" checked onchange="updateVisibility()"> 操縦桿 & 計器盤 (パイロット正対)</label>
      <label><input type="checkbox" id="toggle-door" checked onchange="updateVisibility()"> 大型乗降ドア (幅750×高800mm)</label>
      <label><input type="checkbox" id="toggle-base" checked onchange="updateVisibility()"> 足元ベース板 & 外側安全リブ</label>
      <label><input type="checkbox" id="toggle-seat" checked onchange="updateVisibility()"> シート & ペダル (机下足元広々)</label>
      <label><input type="checkbox" id="toggle-walls" checked onchange="updateVisibility()"> 外壁パネル</label>
      <label><input type="checkbox" id="toggle-pilot" checked onchange="updateVisibility()"> パイロットシルエット</label>
    </div>

    <div class="section-title">機体スペック (v6.0.0)</div>
    <table class="spec-table">
      <tr><td>形状・比率</td><td><strong>長方形 (幅880 × 全長1500mm)</strong></td></tr>
      <tr><td>操縦デスク (机)</td><td><strong>幅 680 × 奥行 380 × 高 700 mm</strong></td></tr>
      <tr><td>操縦桿の向き</td><td><strong>パイロット正面 (手前) 正対</strong></td></tr>
      <tr><td>机下クリアランス</td><td><strong>幅 640 × 高 676 mm (広々足入れ)</strong></td></tr>
      <tr><td>木枠フレーム</td><td><strong>縦の4本角柱のみ</strong> (90mm角材)</td></tr>
      <tr><td>ドア寸法</td><td>幅 750 × 高さ 800 mm</td></tr>
      <tr><td>ドア敷居高さ</td><td><strong>わずか 50 mm</strong> (躓きなし)</td></tr>
      <tr><td>通路床面</td><td><strong>100% フラット (リブ外側のみ)</strong></td></tr>
    </table>
  </div>

  <script>
    function showError(msg) {
      console.error(msg);
      const banner = document.getElementById('error-banner');
      const text = document.getElementById('error-msg');
      if (banner && text) {
        banner.style.display = 'block';
        text.innerText = msg;
      }
    }

    window.addEventListener('error', function(e) {
      showError((e.message || 'JavaScript Error') + (e.filename ? ' (' + e.filename + ':' + e.lineno + ')' : ''));
    });

    let scene, camera, renderer, controls;
    let container;
    let doorPivot;
    let isPilotCam = false;
    let groupPosts, groupDesk, groupConsole, groupDoor, groupBase, groupSeat, groupWalls, groupPilot;

    const W_INNER = 700;
    const POST_S = 90;
    const POST_H = 950;
    const BASE_S = 300;
    const DEPTH = 1350;
    const X_L = -(W_INNER + POST_S) / 2;
    const X_R =  (W_INNER + POST_S) / 2;
    const Y_F = -DEPTH / 2;
    const Y_R =  DEPTH / 2;

    const SEAT_Y = Y_R - 240;   // 435mm
    const DESK_Y = 0;           // 机の中心 Y=0mm (椅子の直前)
    const DESK_H = 700;         // 机天板高さ 700mm

    function getCanvasSize() {
      if (!container) return { w: window.innerWidth, h: window.innerHeight };
      let w = container.clientWidth;
      let h = container.clientHeight;
      if (!w || w <= 0) {
        w = window.innerWidth > 768 ? Math.max(window.innerWidth - 380, 300) : window.innerWidth;
      }
      if (!h || h <= 0) {
        h = window.innerWidth > 768 ? window.innerHeight : Math.round(window.innerHeight * 0.52);
      }
      return { w: Math.max(w, 200), h: Math.max(h, 200) };
    }

    // 三角柱 (直角三角リブ) を安全なBufferGeometryで構築
    function createTriangularPrismGeometry(width, height, depth) {
      const geom = new THREE.BufferGeometry();
      const positions = new Float32Array([
        // 底面 (Z=0): (0,0,0)-(width,0,0)-(0,height,0)
        0, 0, 0,     0, height, 0,    width, 0, 0,
        // 上面 (Z=depth): (0,0,depth)-(width,0,depth)-(0,height,depth)
        0, 0, depth, width, 0, depth, 0, height, depth,
        // 垂直面 (X=0) 2枚
        0, 0, 0,     0, 0, depth,     0, height, depth,
        0, 0, 0,     0, height, depth, 0, height, 0,
        // 水平面 (Y=0) 2枚
        0, 0, 0,     width, 0, 0,     width, 0, depth,
        0, 0, 0,     width, 0, depth, 0, 0, depth,
        // 斜面 2枚
        width, 0, 0,  0, height, depth,  0, height, 0,
        width, 0, 0,  width, 0, depth,   0, height, depth
      ]);
      geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geom.computeVertexNormals();
      return geom;
    }

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

    function init3D() {
      try {
        if (typeof THREE === 'undefined') {
          showError('Three.js ライブラリが読み込めませんでした。ブラウザの再読み込みをお試しください。');
          return;
        }

        container = document.getElementById('canvas-container');
        const size = getCanvasSize();

        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x060911);

        camera = new THREE.PerspectiveCamera(45, size.w / size.h, 10, 15000);
        camera.position.set(1900, 1500, 2000);

        // WebGLレンダラー
        try {
          renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'default' });
        } catch (e) {
          renderer = new THREE.WebGLRenderer({ antialias: false });
        }
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.setSize(size.w, size.h);
        renderer.domElement.style.touchAction = 'none';
        container.appendChild(renderer.domElement);

        // OrbitControls
        if (typeof THREE.OrbitControls !== 'undefined') {
          controls = new THREE.OrbitControls(camera, renderer.domElement);
          controls.enableDamping = true;
          controls.dampingFactor = 0.08;
          controls.target.set(0, 520, 0);
          controls.minDistance = 300;
          controls.maxDistance = 6000;
        }

        // 照明
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const dirLight1 = new THREE.DirectionalLight(0x38bdf8, 0.85);
        dirLight1.position.set(1500, 2500, 1200);
        scene.add(dirLight1);

        const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.55);
        dirLight2.position.set(-1500, 1200, -1500);
        scene.add(dirLight2);

        // 地面グリッド
        const grid = new THREE.GridHelper(4000, 40, 0x0284c7, 0x1e293b);
        grid.position.y = 0;
        scene.add(grid);

        // マテリアル
        const postMat = new THREE.MeshStandardMaterial({ color: 0xd49b4b, roughness: 0.6 });
        const deskTopMat = new THREE.MeshStandardMaterial({ color: 0xb58448, roughness: 0.5 });
        const deskLegMat = new THREE.MeshStandardMaterial({ color: 0x855627, roughness: 0.7 });
        const basePlateMat = new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.7 });
        const ribMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.5 });
        const doorMat = new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.4 });
        const handleMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, metalness: 0.8, roughness: 0.2 });
        const consoleMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4 });
        const yokeMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.4, metalness: 0.2 });
        const screenMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.2, emissive: 0x075985, emissiveIntensity: 0.4 });
        const gaugeMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, metalness: 0.6 });
        const seatMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });
        const seatAccentMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.6 });
        const wallMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.8, transparent: true, opacity: 0.65 });
        const pilotMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });

        // グループ作成
        groupPosts = new THREE.Group();
        groupDesk = new THREE.Group();
        groupConsole = new THREE.Group();
        groupDoor = new THREE.Group();
        groupBase = new THREE.Group();
        groupSeat = new THREE.Group();
        groupWalls = new THREE.Group();
        groupPilot = new THREE.Group();

        scene.add(groupPosts);
        scene.add(groupDesk);
        scene.add(groupConsole);
        scene.add(groupDoor);
        scene.add(groupBase);
        scene.add(groupSeat);
        scene.add(groupWalls);
        scene.add(groupPilot);

        // 1. 縦の4本主角柱 & 外側補強リブ（内側完全フラット）
        const ribGeom = createTriangularPrismGeometry(90, 150, 15);
        const postPositions = [
          [X_L, Y_F, -1, -1],
          [X_R, Y_F,  1, -1],
          [X_L, Y_R, -1,  1],
          [X_R, Y_R,  1,  1]
        ];

        postPositions.forEach(([px, pz, dirX, dirZ]) => {
          addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);
          addBox(groupBase, BASE_S, 18, BASE_S, px, 9, pz, basePlateMat);

          function placeRib(rotY, offsetX, offsetZ) {
            const ribMesh = new THREE.Mesh(ribGeom, ribMat);
            ribMesh.rotation.y = rotY;
            ribMesh.position.set(px + offsetX, 18, pz + offsetZ);
            groupBase.add(ribMesh);
          }

          if (dirX === 1) placeRib(0, POST_S/2, -7.5);
          else placeRib(Math.PI, -POST_S/2, 7.5);

          if (dirZ === 1) placeRib(Math.PI/2, -7.5, POST_S/2);
          else placeRib(-Math.PI/2, 7.5, -POST_S/2);
        });

        // 2. 【新設】椅子の前の「操縦デスク（机）」
        // 天板 (幅680 x 奥行380 x 厚24mm, 上面高さ700mm)
        addBox(groupDesk, 680, 24, 380, 0, DESK_H - 12, DESK_Y, deskTopMat);
        // 側板脚 (左右2枚: 壁際に寄せて中央足元幅640mmフルオープン)
        addBox(groupDesk, 20, DESK_H - 24, 340, -330, (DESK_H - 24)/2, DESK_Y, deskLegMat);
        addBox(groupDesk, 20, DESK_H - 24, 340,  330, (DESK_H - 24)/2, DESK_Y, deskLegMat);
        // 幕板 (天板下奥の横揺れ防止板)
        addBox(groupDesk, 640, 120, 18, 0, DESK_H - 84, DESK_Y - 160, deskLegMat);

        // 3. 【向き完全修正】机上の操作コンソール ＆ パイロット正対操縦桿
        // (1) 傾斜計器盤 (机の奥側)
        addBox(groupConsole, 520, 160, 20, 0, DESK_H + 80, DESK_Y - 90, consoleMat, -0.5);
        // 液晶モニター (中央)
        addBox(groupConsole, 200, 100, 15, 0, DESK_H + 90, DESK_Y - 85, screenMat, -0.5);
        // 円形メーター (左右)
        const meterL = new THREE.Mesh(new THREE.CylinderGeometry(30, 30, 15, 16), gaugeMat);
        meterL.position.set(-160, DESK_H + 90, DESK_Y - 85);
        meterL.rotation.x = -0.5;
        groupConsole.add(meterL);
        const meterR = new THREE.Mesh(new THREE.CylinderGeometry(30, 30, 15, 16), gaugeMat);
        meterR.position.set(160, DESK_H + 90, DESK_Y - 85);
        meterR.rotation.x = -0.5;
        groupConsole.add(meterR);

        // (2) 操縦桿 (手前・パイロット正対向き！)
        // マウントベース
        addBox(groupConsole, 140, 25, 90, 0, DESK_H + 12.5, DESK_Y - 20, consoleMat);
        // シャフト (パイロット側手前に向かって伸びる！)
        const shaft = new THREE.Mesh(new THREE.CylinderGeometry(14, 14, 110, 16), gaugeMat);
        shaft.position.set(0, DESK_H + 50, DESK_Y + 25);
        shaft.rotation.x = 0.45; // 手前（+Z）に傾斜
        groupConsole.add(shaft);

        // U字ヨークハンドル (パイロットに正対！)
        // 中央水平バー
        addBox(groupConsole, 160, 24, 26, 0, DESK_H + 75, DESK_Y + 70, yokeMat, 0.3);
        // 左右グリップ (手前向き)
        addBox(groupConsole, 26, 110, 26, -85, DESK_H + 105, DESK_Y + 75, yokeMat, 0.2);
        addBox(groupConsole, 26, 110, 26,  85, DESK_H + 105, DESK_Y + 75, yokeMat, 0.2);

        // (3) スロットルレバー (机の左手側)
        addBox(groupConsole, 70, 25, 110, -230, DESK_H + 12.5, DESK_Y + 20, consoleMat);
        const throt = addBox(groupConsole, 20, 85, 30, -230, DESK_H + 65, DESK_Y + 20, yokeMat);
        throt.rotation.x = -0.3;

        // 4. 大型乗降ドア (敷居高さ50mm)
        const DOOR_W = 750;
        const DOOR_H = 800;
        const DOOR_Z = 50 + DOOR_H / 2;
        const DOOR_Y_C = -50;
        const HINGE_Z = DOOR_Y_C - DOOR_W / 2;

        doorPivot = new THREE.Group();
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
        hinge2.position.set(0, DOOR_Z - DOOR_H/2 + 80, 0);
        doorPivot.add(hinge2);

        // 5. シート & 机下ペダル
        addBox(groupSeat, 520, 50, 460, 0, 350, SEAT_Y, seatMat);
        const sBack = addBox(groupSeat, 500, 520, 45, 0, 630, SEAT_Y + 220, seatMat);
        sBack.rotation.x = -0.24;
        const sHead = addBox(groupSeat, 260, 150, 55, 0, 930, SEAT_Y + 270, seatAccentMat);
        sHead.rotation.x = -0.16;

        // 机下のペダル (前壁寄り足元)
        const pL = addBox(groupSeat, 85, 140, 18, -140, 70, Y_F + 150, consoleMat);
        pL.rotation.x = -0.4;
        const pR = addBox(groupSeat, 85, 140, 18,  140, 70, Y_F + 150, consoleMat);
        pR.rotation.x = -0.4;

        // 6. 外壁パネル
        addBox(groupWalls, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, wallMat);
        addBox(groupWalls, W_INNER + POST_S*2, POST_H, 12, 0, POST_H/2, Y_R + POST_S/2 + 6, wallMat);
        addBox(groupWalls, W_INNER + POST_S*2, 500, 12, 0, 250, Y_F - POST_S/2 - 6, wallMat);

        const lenFw = (DOOR_Y_C - DOOR_W/2) - (Y_F - POST_S/2);
        addBox(groupWalls, 12, POST_H, lenFw, X_L, POST_H/2, (Y_F - POST_S/2) + lenFw/2, wallMat);
        const lenRw = (Y_R + POST_S/2) - (DOOR_Y_C + DOOR_W/2);
        addBox(groupWalls, 12, POST_H, lenRw, X_L, POST_H/2, (DOOR_Y_C + DOOR_W/2) + lenRw/2, wallMat);

        // 7. パイロットシルエット
        const pHead = new THREE.Mesh(new THREE.SphereGeometry(105, 16, 16), pilotMat);
        pHead.position.set(0, 910, SEAT_Y + 180);
        groupPilot.add(pHead);

        const pTorso = new THREE.Mesh(new THREE.CylinderGeometry(130, 110, 420, 8), pilotMat);
        pTorso.position.set(0, 630, SEAT_Y + 120);
        pTorso.rotation.x = -0.24;
        groupPilot.add(pTorso);

        const pThighs = new THREE.Mesh(new THREE.BoxGeometry(260, 90, 360), pilotMat);
        pThighs.position.set(0, 370, SEAT_Y - 80);
        groupPilot.add(pThighs);

        // 足は机の下にすっぽり入る
        const pShins = new THREE.Mesh(new THREE.BoxGeometry(260, 340, 90), pilotMat);
        pShins.position.set(0, 210, DESK_Y - 120);
        pShins.rotation.x = 0.35;
        groupPilot.add(pShins);

        // パイロットの腕（操縦桿へ伸ばす）
        const armL = addBox(groupPilot, 45, 45, 220, -75, 750, SEAT_Y - 40, pilotMat, 0.45);
        const armR = addBox(groupPilot, 45, 45, 220,  75, 750, SEAT_Y - 40, pilotMat, 0.45);

        // ローディング表示を非表示に
        const loader = document.getElementById('loading-indicator');
        if (loader) loader.style.display = 'none';

        // 初回サイズ補正
        onResize();

        // アニメーションループ開始
        animate();

      } catch (err) {
        showError('初期化エラー: ' + err.message);
      }
    }

    function onResize() {
      if (!camera || !renderer || !container) return;
      const size = getCanvasSize();
      camera.aspect = size.w / size.h;
      camera.updateProjectionMatrix();
      renderer.setSize(size.w, size.h, false);
    }

    window.addEventListener('resize', onResize);
    window.addEventListener('orientationchange', () => {
      setTimeout(onResize, 100);
      setTimeout(onResize, 400);
    });

    let renderLoopError = false;
    function animate() {
      requestAnimationFrame(animate);
      if (renderLoopError) return;
      try {
        if (!isPilotCam && controls) controls.update();
        if (renderer && scene && camera) {
          renderer.render(scene, camera);
        }
      } catch (e) {
        renderLoopError = true;
        showError('描画ループエラー: ' + e.message);
      }
    }

    function setDoor(deg) {
      const doorSlider = document.getElementById('door-slider');
      const doorVal = document.getElementById('door-val');
      if (doorSlider) doorSlider.value = deg;
      if (doorVal) doorVal.innerText = deg.toFixed(0) + '° ' + (deg > 5 ? '(開)' : '(全閉)');
      if (doorPivot) {
        const rad = (deg * Math.PI) / 180;
        doorPivot.rotation.y = -rad;
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      const doorSlider = document.getElementById('door-slider');
      if (doorSlider) {
        doorSlider.addEventListener('input', (e) => setDoor(parseFloat(e.target.value)));
      }
    });

    function updateVisibility() {
      if (!groupPosts) return;
      groupPosts.visible = document.getElementById('toggle-posts').checked;
      groupDesk.visible = document.getElementById('toggle-desk').checked;
      groupConsole.visible = document.getElementById('toggle-console').checked;
      groupDoor.visible = document.getElementById('toggle-door').checked;
      groupBase.visible = document.getElementById('toggle-base').checked;
      groupSeat.visible = document.getElementById('toggle-seat').checked;
      groupWalls.visible = document.getElementById('toggle-walls').checked;
      groupPilot.visible = document.getElementById('toggle-pilot').checked;
    }

    function setCameraMode(mode) {
      document.getElementById('cam-ext').classList.toggle('active', mode === 'ext');
      document.getElementById('cam-pilot').classList.toggle('active', mode === 'pilot');
      if (mode === 'pilot') {
        isPilotCam = true;
        if (controls) controls.enabled = false;
        // パイロットの目線から目の前の机と操縦桿を見下ろす
        camera.position.set(0, 930, SEAT_Y + 120);
        camera.lookAt(0, DESK_H + 40, DESK_Y + 40);
      } else {
        isPilotCam = false;
        if (controls) {
          controls.enabled = true;
          controls.target.set(0, 520, 0);
        }
        camera.position.set(1900, 1500, 2000);
      }
    }

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
      init3D();
    } else {
      window.addEventListener('DOMContentLoaded', init3D);
    }

    window.addEventListener('load', () => {
      setTimeout(onResize, 50);
      setTimeout(onResize, 200);
      setTimeout(onResize, 600);
    });
  </script>
</body>
</html>
'''

with open('/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

with open('/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/cockpit_v6.0.0_viewer.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Generated Cockpit v6.0.0 viewers successfully!")
