#!/usr/bin/env python3
"""
Generate Cockpit Web 3D Viewer with Interactive Multi-Version Switcher:
- v7.0.0: Square 1000mm, Flip-Up Desk (Smart Flow / 100% smooth entry), Pilot-facing Yoke, 4 Heavy Posts
- v6.0.0: Rectangular 1500mm, Fixed Desk, Pilot-facing Yoke
- v5.0.0: Rectangular 1500mm, Low-floor Door, Integrated Console
- v3.0.0: Square 900mm, Initial Notebook Desk Proposal
"""

html_code = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>COCKPIT 3D Viewer - バージョン切替対応</title>
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
      width: 390px;
      flex-shrink: 0;
      background: rgba(13, 19, 33, 0.97);
      border-left: 1px solid #1e293b;
      padding: 16px 18px;
      overflow-y: auto;
      box-shadow: -8px 0 30px rgba(0,0,0,0.85);
      backdrop-filter: blur(14px);
      z-index: 10;
      -webkit-overflow-scrolling: touch;
    }
    .version-selector-card {
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.2), rgba(16, 185, 129, 0.2));
      border: 1px solid #0284c7;
      border-radius: 10px;
      padding: 12px;
      margin-bottom: 12px;
    }
    .version-selector-card label {
      display: block;
      font-size: 11px;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }
    select.version-dropdown {
      width: 100%;
      background: #0f172a;
      color: #38bdf8;
      border: 1px solid #38bdf8;
      padding: 8px 10px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 700;
      outline: none;
      cursor: pointer;
    }
    select.version-dropdown option {
      background: #0f172a;
      color: #e2e8f0;
    }
    .version-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }
    h1 {
      font-size: 18px;
      color: #f1f5f9;
      letter-spacing: 0.5px;
    }
    .badge {
      font-size: 11px;
      background: linear-gradient(135deg, #10b981, #059669);
      color: #fff;
      padding: 3px 9px;
      border-radius: 9999px;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
    }
    p.desc {
      font-size: 11.5px;
      color: #94a3b8;
      margin-bottom: 10px;
      line-height: 1.5;
    }
    .change-log {
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 11px;
      margin-bottom: 12px;
      line-height: 1.5;
    }
    .change-log strong { font-size: 11.5px; }
    .change-log ul { margin-left: 14px; margin-top: 4px; }
    .log-v7 {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid #10b981;
      color: #a7f3d0;
    }
    .log-v7 strong { color: #34d399; }
    .section-title {
      font-size: 11.5px;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-top: 12px;
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
      font-size: 11.5px;
      color: #cbd5e1;
      margin-bottom: 5px;
      cursor: pointer;
    }
    input[type="range"] {
      width: 100%;
      height: 6px;
      accent-color: #10b981;
    }
    .btn-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 8px;
    }
    .btn-grid-3 {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 6px;
      margin-bottom: 8px;
    }
    button {
      background: #1e293b;
      color: #f1f5f9;
      border: 1px solid #334155;
      padding: 8px 6px;
      border-radius: 6px;
      font-size: 11.5px;
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
      background: #10b981;
      border-color: #34d399;
      color: #fff;
      font-weight: 700;
    }
    button.highlight {
      background: linear-gradient(135deg, #0284c7, #2563eb);
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
      width: 48%;
    }
    .spec-table td:last-child {
      color: #f8fafc;
      font-weight: 600;
    }
    #hud-overlay {
      position: absolute;
      top: 14px;
      left: 14px;
      background: rgba(13, 19, 33, 0.92);
      border: 1px solid #10b981;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 11px;
      backdrop-filter: blur(10px);
      pointer-events: none;
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
      z-index: 5;
    }
    .hud-title {
      font-weight: 800;
      color: #34d399;
      font-size: 12px;
      margin-bottom: 5px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 3px;
      font-size: 10px;
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
      font-size: 13px;
      pointer-events: none;
      z-index: 4;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }
    .spinner {
      width: 30px;
      height: 30px;
      border: 3px solid rgba(56, 189, 248, 0.2);
      border-top-color: #38bdf8;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    @media (max-width: 768px) {
      body {
        flex-direction: column;
      }
      #canvas-container {
        height: 50vh;
        height: 50dvh;
        width: 100%;
        flex: none;
      }
      #sidebar {
        width: 100%;
        height: 50vh;
        height: 50dvh;
        border-left: none;
        border-top: 1px solid #334155;
        padding: 12px 14px;
        flex: 1;
      }
      #hud-overlay {
        top: 8px;
        left: 8px;
        padding: 6px 8px;
        font-size: 9.5px;
      }
      .hud-title { font-size: 10.5px; margin-bottom: 3px; }
      .legend-item { font-size: 9px; margin-bottom: 1.5px; }
      h1 { font-size: 16px; }
    }
  </style>

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
      <div class="hud-title" id="hud-title">◆ COCKPIT v7.0.0 (正方形・神導線)</div>
      <div class="legend-item"><div class="legend-color" style="background: #e2b34a;"></div> 木の枠：縦の4本角柱のみ (90mm角)</div>
      <div class="legend-item"><div class="legend-color" style="background: #c28b48;"></div> 【神導線】跳ね上げ操縦デスク (机)</div>
      <div class="legend-item"><div class="legend-color" style="background: #f59e0b;"></div> パイロット正対操縦桿 (手前向き)</div>
      <div class="legend-item"><div class="legend-color" style="background: #10b981;"></div> 大型乗降ドア (敷居わずか50mm)</div>
      <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> 足元ベース＆外側リブ (床完全フラット)</div>
      <div class="legend-item"><div class="legend-color" style="background: #0284c7;"></div> 操縦席シート (ゆったり着座)</div>
    </div>
  </div>

  <div id="sidebar">
    <!-- バージョン選択プルダウン -->
    <div class="version-selector-card">
      <label for="version-select">▼ バージョン切替（形状・導線比較）:</label>
      <select id="version-select" class="version-dropdown" onchange="switchVersion(this.value)">
        <option value="v7.0.0" selected>v7.0.0 (正方形1000mm・跳ね上げ机・神導線) ★推奨</option>
        <option value="v6.0.0">v6.0.0 (長方形1500mm・固定机・正対操縦桿)</option>
        <option value="v5.0.0">v5.0.0 (長方形1500mm・低床ドア・コンソール)</option>
        <option value="v3.0.0">v3.0.0 (正方形900mm・ノート初期案)</option>
      </select>
    </div>

    <div class="version-header">
      <h1 id="view-title">操縦席ユニット</h1>
      <span id="view-badge" class="badge">v7.0.0</span>
    </div>
    <p class="desc" id="view-desc">
      画面スワイプで360度回転、ピンチで拡大縮小できます。
    </p>

    <div id="changelog-box" class="change-log log-v7">
      <!-- 動的更新 -->
    </div>

    <!-- v7.0.0専用 導線ギミック操作 -->
    <div id="v7-flow-controls">
      <div class="section-title">🚀 導線アクション (神ギミック)</div>
      <div class="btn-grid">
        <button class="highlight" onclick="setBoardingSequence(true)">乗降モード (ドア開+机UP)</button>
        <button class="active" onclick="setBoardingSequence(false)">操縦モード (全閉・セット)</button>
      </div>

      <div class="control-group">
        <label for="desk-slider">机の跳ね上げ角度: <span id="desk-val">0° (操縦状態)</span></label>
        <input type="range" id="desk-slider" min="0" max="55" value="0">
      </div>
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
      <button id="cam-pilot" onclick="setCameraMode('pilot')">操縦席カメラ (パイロット目線)</button>
    </div>

    <div class="section-title">パーツ表示切り替え</div>
    <div class="control-group">
      <label><input type="checkbox" id="toggle-posts" checked onchange="updateVisibility()"> 縦の4本角柱 (木の枠はこれだけ)</label>
      <label><input type="checkbox" id="toggle-desk" checked onchange="updateVisibility()"> 操縦デスク (机天板)</label>
      <label><input type="checkbox" id="toggle-console" checked onchange="updateVisibility()"> 操縦桿 & 計器盤</label>
      <label><input type="checkbox" id="toggle-door" checked onchange="updateVisibility()"> 大型乗降ドア (敷居50mm)</label>
      <label><input type="checkbox" id="toggle-base" checked onchange="updateVisibility()"> 足元ベース板 & 外側安全リブ</label>
      <label><input type="checkbox" id="toggle-seat" checked onchange="updateVisibility()"> シート & ペダル</label>
      <label><input type="checkbox" id="toggle-walls" checked onchange="updateVisibility()"> 外壁パネル</label>
      <label><input type="checkbox" id="toggle-pilot" checked onchange="updateVisibility()"> パイロットシルエット</label>
    </div>

    <div class="section-title">機体スペック</div>
    <div id="spec-table-container">
      <!-- 動的更新 -->
    </div>
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
    let currentVersion = 'v7.0.0';
    let isPilotCam = false;

    // アニメーション用Pivot
    let doorPivot = null;
    let deskPivot = null;

    // グループ
    let groupPosts, groupDesk, groupConsole, groupDoor, groupBase, groupSeat, groupWalls, groupPilot;

    // マテリアル定義
    let postMat, deskTopMat, deskLegMat, basePlateMat, ribMat, doorMat, handleMat,
        consoleMat, yokeMat, screenMat, gaugeMat, seatMat, seatAccentMat, wallMat, pilotMat;

    function initMaterials() {
      postMat = new THREE.MeshStandardMaterial({ color: 0xd49b4b, roughness: 0.6 });
      deskTopMat = new THREE.MeshStandardMaterial({ color: 0xb58448, roughness: 0.5 });
      deskLegMat = new THREE.MeshStandardMaterial({ color: 0x855627, roughness: 0.7 });
      basePlateMat = new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.7 });
      ribMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.5 });
      doorMat = new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.4 });
      handleMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, metalness: 0.8, roughness: 0.2 });
      consoleMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4 });
      yokeMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.4, metalness: 0.2 });
      screenMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.2, emissive: 0x075985, emissiveIntensity: 0.4 });
      gaugeMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, metalness: 0.6 });
      seatMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });
      seatAccentMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.6 });
      wallMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.8, transparent: true, opacity: 0.65 });
      pilotMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });
    }

    function createTriangularPrismGeometry(width, height, depth) {
      const geom = new THREE.BufferGeometry();
      const positions = new Float32Array([
        0, 0, 0,     0, height, 0,    width, 0, 0,
        0, 0, depth, width, 0, depth, 0, height, depth,
        0, 0, 0,     0, 0, depth,     0, height, depth,
        0, 0, 0,     0, height, depth, 0, height, 0,
        0, 0, 0,     width, 0, 0,     width, 0, depth,
        0, 0, 0,     width, 0, depth, 0, 0, depth,
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

    function clearModelGroups() {
      const groups = [groupPosts, groupDesk, groupConsole, groupDoor, groupBase, groupSeat, groupWalls, groupPilot];
      groups.forEach(g => {
        if (g) {
          while (g.children.length > 0) {
            const obj = g.children[0];
            g.remove(obj);
          }
        }
      });
      doorPivot = null;
      deskPivot = null;
    }

    // ==========================================
    // モデル構築ロジック (v7, v6, v5, v3)
    // ==========================================
    function buildModel(version) {
      clearModelGroups();
      const ribGeom = createTriangularPrismGeometry(90, 150, 15);

      if (version === 'v7.0.0') {
        // v7.0.0: 正方形1000mm、跳ね上げ机、パイロット正対操縦桿、神導線
        const W_INNER = 720;
        const POST_S = 90;
        const POST_H = 950;
        const BASE_S = 300;
        const DEPTH = 820; // 正方形プロポーション！
        const X_L = -(W_INNER + POST_S) / 2;
        const X_R =  (W_INNER + POST_S) / 2;
        const Y_F = -DEPTH / 2;
        const Y_R =  DEPTH / 2;
        const SEAT_Y = Y_R - 190;
        const DESK_Y = -60;
        const DESK_H = 700;

        // 1. 縦の4本主角柱 & 外側リブ
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

        // 2. 跳ね上げ式操縦デスク (天板＋操縦桿＋計器盤をPivot内に格納！)
        deskPivot = new THREE.Group();
        // ヒンジ軸: 机の前端奥 (Z=700, Y = DESK_Y - 175)
        const HINGE_DESK_Y = DESK_Y - 175;
        const HINGE_DESK_Z = DESK_H;
        deskPivot.position.set(0, HINGE_DESK_Z, HINGE_DESK_Y);
        groupDesk.add(deskPivot);

        // 天板 (Pivot原点を基準にローカル配置)
        // ローカル中心: Y = +175, Z = -12
        const localTop = new THREE.Mesh(new THREE.BoxGeometry(690, 24, 350), deskTopMat);
        localTop.position.set(0, -12, 175);
        deskPivot.add(localTop);

        // ヒンジ軸バー (金属)
        const hingeBar = new THREE.Mesh(new THREE.CylinderGeometry(10, 10, 680, 16), handleMat);
        hingeBar.rotation.z = Math.PI/2;
        hingeBar.position.set(0, 0, 0);
        deskPivot.add(hingeBar);

        // 傾斜計器盤 (ローカル配置)
        const localInst = new THREE.Mesh(new THREE.BoxGeometry(500, 150, 20), consoleMat);
        localInst.position.set(0, 80, 95);
        localInst.rotation.x = -0.5;
        deskPivot.add(localInst);
        // 液晶モニター
        const localScreen = new THREE.Mesh(new THREE.BoxGeometry(190, 95, 15), screenMat);
        localScreen.position.set(0, 90, 100);
        localScreen.rotation.x = -0.5;
        deskPivot.add(localScreen);
        // メーター
        const meterL = new THREE.Mesh(new THREE.CylinderGeometry(28, 28, 15, 16), gaugeMat);
        meterL.position.set(-150, 90, 100);
        meterL.rotation.x = -0.5;
        deskPivot.add(meterL);
        const meterR = new THREE.Mesh(new THREE.CylinderGeometry(28, 28, 15, 16), gaugeMat);
        meterR.position.set(150, 90, 100);
        meterR.rotation.x = -0.5;
        deskPivot.add(meterR);

        // 操縦桿 (手前パイロット正対)
        const yokeMount = new THREE.Mesh(new THREE.BoxGeometry(140, 25, 90), consoleMat);
        yokeMount.position.set(0, 12.5, 165);
        deskPivot.add(yokeMount);

        const yokeShaft = new THREE.Mesh(new THREE.CylinderGeometry(14, 14, 110, 16), gaugeMat);
        yokeShaft.position.set(0, 50, 210);
        yokeShaft.rotation.x = 0.45;
        deskPivot.add(yokeShaft);

        const yokeCenter = new THREE.Mesh(new THREE.BoxGeometry(160, 24, 26), yokeMat);
        yokeCenter.position.set(0, 75, 250);
        yokeCenter.rotation.x = 0.3;
        deskPivot.add(yokeCenter);
        const yokeL = new THREE.Mesh(new THREE.BoxGeometry(26, 110, 26), yokeMat);
        yokeL.position.set(-85, 105, 255);
        yokeL.rotation.x = 0.2;
        deskPivot.add(yokeL);
        const yokeR = new THREE.Mesh(new THREE.BoxGeometry(26, 110, 26), yokeMat);
        yokeR.position.set(85, 105, 255);
        yokeR.rotation.x = 0.2;
        deskPivot.add(yokeR);

        // スロットルレバー
        const throtBase = new THREE.Mesh(new THREE.BoxGeometry(70, 25, 100), consoleMat);
        throtBase.position.set(-230, 12.5, 195);
        deskPivot.add(throtBase);
        const throtLev = new THREE.Mesh(new THREE.BoxGeometry(20, 85, 30), yokeMat);
        throtLev.position.set(-230, 65, 195);
        throtLev.rotation.x = -0.3;
        deskPivot.add(throtLev);

        // 固定側ヒンジ受けフレーム
        addBox(groupDesk, 20, 40, 160, -345, DESK_H - 20, Y_F + 80, deskLegMat);
        addBox(groupDesk, 20, 40, 160,  345, DESK_H - 20, Y_F + 80, deskLegMat);

        // 3. 大型乗降ドア (敷居わずか50mm、幅650mm)
        const DOOR_W = 650;
        const DOOR_H = 800;
        const DOOR_Z = 50 + DOOR_H / 2;
        const DOOR_Y_C = 0;
        const HINGE_Z = DOOR_Y_C - DOOR_W / 2;

        doorPivot = new THREE.Group();
        doorPivot.position.set(X_L, 0, HINGE_Z);
        groupDoor.add(doorPivot);

        const doorMesh = new THREE.Mesh(new THREE.BoxGeometry(15, DOOR_H, DOOR_W), doorMat);
        doorMesh.position.set(0, DOOR_Z, DOOR_W / 2);
        doorPivot.add(doorMesh);

        const handleOut = new THREE.Mesh(new THREE.BoxGeometry(25, 160, 30), handleMat);
        handleOut.position.set(-25, DOOR_Z, DOOR_W - 70);
        doorPivot.add(handleOut);
        const handleIn = new THREE.Mesh(new THREE.BoxGeometry(25, 160, 30), handleMat);
        handleIn.position.set(25, DOOR_Z, DOOR_W - 70);
        doorPivot.add(handleIn);

        // 4. シート & ペダル
        addBox(groupSeat, 520, 50, 420, 0, 350, SEAT_Y, seatMat);
        const sBack = addBox(groupSeat, 500, 520, 45, 0, 630, SEAT_Y + 190, seatMat);
        sBack.rotation.x = -0.24;
        const sHead = addBox(groupSeat, 260, 150, 55, 0, 930, SEAT_Y + 240, seatAccentMat);
        sHead.rotation.x = -0.16;

        const pL = addBox(groupSeat, 85, 140, 18, -140, 70, Y_F + 120, consoleMat);
        pL.rotation.x = -0.4;
        const pR = addBox(groupSeat, 85, 140, 18,  140, 70, Y_F + 120, consoleMat);
        pR.rotation.x = -0.4;

        // 5. 外壁
        addBox(groupWalls, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, wallMat);
        addBox(groupWalls, W_INNER + POST_S*2, POST_H, 12, 0, POST_H/2, Y_R + POST_S/2 + 6, wallMat);
        addBox(groupWalls, W_INNER + POST_S*2, 500, 12, 0, 250, Y_F - POST_S/2 - 6, wallMat);
        const lenFw = (DOOR_Y_C - DOOR_W/2) - (Y_F - POST_S/2);
        addBox(groupWalls, 12, POST_H, lenFw, X_L, POST_H/2, (Y_F - POST_S/2) + lenFw/2, wallMat);
        const lenRw = (Y_R + POST_S/2) - (DOOR_Y_C + DOOR_W/2);
        addBox(groupWalls, 12, POST_H, lenRw, X_L, POST_H/2, (DOOR_Y_C + DOOR_W/2) + lenRw/2, wallMat);

        // 6. パイロット
        const pHead = new THREE.Mesh(new THREE.SphereGeometry(105, 16, 16), pilotMat);
        pHead.position.set(0, 910, SEAT_Y + 160);
        groupPilot.add(pHead);
        const pTorso = new THREE.Mesh(new THREE.CylinderGeometry(130, 110, 420, 8), pilotMat);
        pTorso.position.set(0, 630, SEAT_Y + 100);
        pTorso.rotation.x = -0.24;
        groupPilot.add(pTorso);
        const pThighs = new THREE.Mesh(new THREE.BoxGeometry(260, 90, 360), pilotMat);
        pThighs.position.set(0, 370, SEAT_Y - 80);
        groupPilot.add(pThighs);
        const pShins = new THREE.Mesh(new THREE.BoxGeometry(260, 340, 90), pilotMat);
        pShins.position.set(0, 210, DESK_Y - 80);
        pShins.rotation.x = 0.35;
        groupPilot.add(pShins);

      } else if (version === 'v6.0.0') {
        // v6.0.0: 長方形1500mm、固定机、正対操縦桿
        const W_INNER = 700;
        const POST_S = 90;
        const POST_H = 950;
        const BASE_S = 300;
        const DEPTH = 1350;
        const X_L = -(W_INNER + POST_S) / 2;
        const X_R =  (W_INNER + POST_S) / 2;
        const Y_F = -DEPTH / 2;
        const Y_R =  DEPTH / 2;
        const SEAT_Y = Y_R - 240;
        const DESK_Y = 0;
        const DESK_H = 700;

        const postPositions = [
          [X_L, Y_F, -1, -1], [X_R, Y_F,  1, -1],
          [X_L, Y_R, -1,  1], [X_R, Y_R,  1,  1]
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

        // 固定机
        addBox(groupDesk, 680, 24, 380, 0, DESK_H - 12, DESK_Y, deskTopMat);
        addBox(groupDesk, 20, DESK_H - 24, 340, -330, (DESK_H - 24)/2, DESK_Y, deskLegMat);
        addBox(groupDesk, 20, DESK_H - 24, 340,  330, (DESK_H - 24)/2, DESK_Y, deskLegMat);
        addBox(groupDesk, 640, 120, 18, 0, DESK_H - 84, DESK_Y - 160, deskLegMat);

        // 操縦桿 ＆ 計器
        addBox(groupConsole, 520, 160, 20, 0, DESK_H + 80, DESK_Y - 90, consoleMat, -0.5);
        addBox(groupConsole, 200, 100, 15, 0, DESK_H + 90, DESK_Y - 85, screenMat, -0.5);
        const mL = new THREE.Mesh(new THREE.CylinderGeometry(30, 30, 15, 16), gaugeMat);
        mL.position.set(-160, DESK_H + 90, DESK_Y - 85);
        mL.rotation.x = -0.5;
        groupConsole.add(mL);
        const mR = new THREE.Mesh(new THREE.CylinderGeometry(30, 30, 15, 16), gaugeMat);
        mR.position.set(160, DESK_H + 90, DESK_Y - 85);
        mR.rotation.x = -0.5;
        groupConsole.add(mR);

        addBox(groupConsole, 140, 25, 90, 0, DESK_H + 12.5, DESK_Y - 20, consoleMat);
        const sh = new THREE.Mesh(new THREE.CylinderGeometry(14, 14, 110, 16), gaugeMat);
        sh.position.set(0, DESK_H + 50, DESK_Y + 25);
        sh.rotation.x = 0.45;
        groupConsole.add(sh);

        addBox(groupConsole, 160, 24, 26, 0, DESK_H + 75, DESK_Y + 70, yokeMat, 0.3);
        addBox(groupConsole, 26, 110, 26, -85, DESK_H + 105, DESK_Y + 75, yokeMat, 0.2);
        addBox(groupConsole, 26, 110, 26,  85, DESK_H + 105, DESK_Y + 75, yokeMat, 0.2);

        // ドア
        const DOOR_W = 750;
        const DOOR_H = 800;
        const DOOR_Z = 50 + DOOR_H / 2;
        const DOOR_Y_C = -50;
        const HINGE_Z = DOOR_Y_C - DOOR_W / 2;
        doorPivot = new THREE.Group();
        doorPivot.position.set(X_L, 0, HINGE_Z);
        groupDoor.add(doorPivot);
        const dMesh = new THREE.Mesh(new THREE.BoxGeometry(15, DOOR_H, DOOR_W), doorMat);
        dMesh.position.set(0, DOOR_Z, DOOR_W / 2);
        doorPivot.add(dMesh);

        // シート
        addBox(groupSeat, 520, 50, 460, 0, 350, SEAT_Y, seatMat);
        const sBack = addBox(groupSeat, 500, 520, 45, 0, 630, SEAT_Y + 220, seatMat);
        sBack.rotation.x = -0.24;
        const sHead = addBox(groupSeat, 260, 150, 55, 0, 930, SEAT_Y + 270, seatAccentMat);
        sHead.rotation.x = -0.16;

        // 壁
        addBox(groupWalls, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, wallMat);
        addBox(groupWalls, W_INNER + POST_S*2, POST_H, 12, 0, POST_H/2, Y_R + POST_S/2 + 6, wallMat);
        addBox(groupWalls, W_INNER + POST_S*2, 500, 12, 0, 250, Y_F - POST_S/2 - 6, wallMat);

      } else if (version === 'v5.0.0') {
        // v5.0.0: 長方形1500mm、コンソール埋込、机なし
        const W_INNER = 700;
        const POST_S = 90;
        const POST_H = 950;
        const BASE_S = 300;
        const DEPTH = 1350;
        const X_L = -(W_INNER + POST_S) / 2;
        const X_R =  (W_INNER + POST_S) / 2;
        const Y_F = -DEPTH / 2;
        const Y_R =  DEPTH / 2;
        const SEAT_Z = Y_R - 240;

        const postPositions = [
          [X_L, Y_F, -1, -1], [X_R, Y_F,  1, -1],
          [X_L, Y_R, -1,  1], [X_R, Y_R,  1,  1]
        ];
        postPositions.forEach(([px, pz, dirX, dirZ]) => {
          addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);
          addBox(groupBase, BASE_S, 18, BASE_S, px, 9, pz, basePlateMat);
        });

        // コンソール (前壁側)
        const CON_Y = 620;
        const CON_Z = Y_F + 160;
        addBox(groupConsole, W_INNER - 10, 130, 300, 0, CON_Y, CON_Z, consoleMat, -0.4);

        // ドア
        const DOOR_W = 750;
        const DOOR_H = 800;
        const DOOR_Z = 50 + DOOR_H / 2;
        const DOOR_Y_C = -50;
        doorPivot = new THREE.Group();
        doorPivot.position.set(X_L, 0, DOOR_Y_C - DOOR_W / 2);
        groupDoor.add(doorPivot);
        const dMesh = new THREE.Mesh(new THREE.BoxGeometry(15, DOOR_H, DOOR_W), doorMat);
        dMesh.position.set(0, DOOR_Z, DOOR_W / 2);
        doorPivot.add(dMesh);

        // シート
        addBox(groupSeat, 520, 50, 460, 0, 350, SEAT_Z, seatMat);
        const sBack = addBox(groupSeat, 500, 520, 45, 0, 630, SEAT_Z + 220, seatMat);
        sBack.rotation.x = -0.24;

        // 壁
        addBox(groupWalls, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, wallMat);
        addBox(groupWalls, W_INNER + POST_S*2, POST_H, 12, 0, POST_H/2, Y_R + POST_S/2 + 6, wallMat);

      } else if (version === 'v3.0.0') {
        // v3.0.0: 正方形900mm、ノート初期案（机＋モニターアーム）
        const W_INNER = 720;
        const POST_S = 90;
        const POST_H = 950;
        const DEPTH = 720; // 900mm角
        const X_L = -(W_INNER + POST_S) / 2;
        const X_R =  (W_INNER + POST_S) / 2;
        const Y_F = -DEPTH / 2;
        const Y_R =  DEPTH / 2;

        const postPositions = [
          [X_L, Y_F, -1, -1], [X_R, Y_F,  1, -1],
          [X_L, Y_R, -1,  1], [X_R, Y_R,  1,  1]
        ];
        postPositions.forEach(([px, pz]) => {
          addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);
          addBox(groupBase, 300, 18, 300, px, 9, pz, basePlateMat);
        });

        // 初期の固定机
        addBox(groupDesk, 700, 24, 400, 0, 688, -100, deskTopMat);
        addBox(groupDesk, 20, 676, 360, -340, 338, -100, deskLegMat);
        addBox(groupDesk, 20, 676, 360,  340, 338, -100, deskLegMat);

        // モニターアーム
        const arm = new THREE.Mesh(new THREE.CylinderGeometry(15, 15, 300, 16), handleMat);
        arm.position.set(0, 850, -250);
        groupConsole.add(arm);
        addBox(groupConsole, 380, 240, 20, 0, 950, -230, screenMat, 0.15);

        // シート
        addBox(groupSeat, 500, 50, 400, 0, 350, 180, seatMat);
        addBox(groupSeat, 480, 500, 40, 0, 620, 360, seatMat, -0.2);

        // 壁
        addBox(groupWalls, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, wallMat);
        addBox(groupWalls, W_INNER + POST_S*2, POST_H, 12, 0, POST_H/2, Y_R + POST_S/2 + 6, wallMat);
      }
    }

    // ==========================================
    // UI情報更新 (タイトル、Changelog、スペック)
    // ==========================================
    const versionData = {
      'v7.0.0': {
        title: '操縦席ユニット (最新案)',
        badge: 'v7.0.0',
        hudTitle: '◆ COCKPIT v7.0.0 (正方形・神導線)',
        desc: '正方形プロポーション（幅900×長1000mm）に最適化し、乗降導線問題を「跳ね上げ式操縦デスク」で完全解決した決定版。',
        logClass: 'log-v7',
        logHTML: `
          <strong>【v7.0.0 アップデート内容】</strong>
          <ul>
            <li><strong>正方形プロポーション</strong>: 幅900×長1000mm（設置面積33%省スペース）</li>
            <li><strong>【神導線】跳ね上げ机</strong>: 乗降時に机天板が斜め上にパカッと跳ね上がり、身体をねじ込まず正面からゆったり着座可能！</li>
            <li><strong>戦闘機スタイル搭乗</strong>: 座った後に机を手前に引き下ろしてロック！</li>
            <li><strong>パイロット正対操縦桿</strong>: 手前に伸びるU字ヨーク＆傾斜計器盤</li>
            <li><strong>木枠の原則堅持</strong>: 縦の4本主角柱（90mm角×950mm）のみ</li>
            <li><strong>床面完全フラット</strong>: 内側リブ全廃・躓きゼロ</li>
          </ul>
        `,
        specs: [
          ['形状・プロポーション', '<strong>正方形 (幅900 × 全長1000mm)</strong>'],
          ['乗降導線ギミック', '<strong>跳ね上げ式操縦デスク (フリップアップ)</strong>'],
          ['操縦デスク寸法', '幅 690 × 奥行 350 × 高 700 mm'],
          ['操縦桿の向き', '<strong>パイロット正面 (手前) 正対</strong>'],
          ['木枠フレーム', '<strong>縦の4本角柱のみ</strong> (90mm角材)'],
          ['ドア寸法・敷居', '幅 650 × 高 800 mm / <strong>敷居わずか50mm</strong>'],
          ['通路床面', '<strong>100% フラット (躓きゼロ)</strong>']
        ],
        hasDeskFlip: true
      },
      'v6.0.0': {
        title: '操縦席ユニット (長方形・固定机)',
        badge: 'v6.0.0',
        hudTitle: '◆ COCKPIT v6.0.0 (長方形・固定机)',
        desc: '全長1500mmの長方形モデルに机を新設し、操縦桿をパイロットに向けたバージョン。',
        logClass: 'log-v6',
        logHTML: `
          <strong>【v6.0.0 仕様】</strong>
          <ul>
            <li><strong>長方形プロポーション</strong>: 幅880×全長1500mm</li>
            <li><strong>操縦デスク設置</strong>: 幅680×奥380×高700mm（固定式）</li>
            <li><strong>パイロット正対操縦桿</strong>: 手前向きU字ハンドル</li>
            <li><strong>課題</strong>: 机が固定のため横ドアからの乗り降りに身体をねじ込む必要あり（導線がやや窮屈）</li>
          </ul>
        `,
        specs: [
          ['形状・プロポーション', '長方形 (幅880 × 全長1500mm)'],
          ['操縦デスク', '幅 680 × 奥行 380 × 高 700 mm (固定)'],
          ['操縦桿', 'パイロット正対U字ヨーク'],
          ['ドア寸法・敷居', '幅 750 × 高 800 mm / 敷居50mm'],
          ['乗降性', '机と椅子の間を横から滑り込む']
        ],
        hasDeskFlip: false
      },
      'v5.0.0': {
        title: '操縦席ユニット (長方形・コンソール)',
        badge: 'v5.0.0',
        hudTitle: '◆ COCKPIT v5.0.0 (長方形・低床ドア)',
        desc: '長方形1500mm、敷居50mmの低床ドア、前壁埋込コンソールモデル。机なし。',
        logClass: 'log-v5',
        logHTML: `
          <strong>【v5.0.0 仕様】</strong>
          <ul>
            <li><strong>長方形プロポーション</strong>: 幅880×全長1500mm</li>
            <li><strong>低床大型ドア</strong>: 敷居高さ50mm</li>
            <li><strong>足元完全フラット</strong>: 内側リブ全廃</li>
            <li><strong>机なし</strong>: 前壁埋込操作コンソール</li>
          </ul>
        `,
        specs: [
          ['形状・プロポーション', '長方形 (幅880 × 全長1500mm)'],
          ['操縦系', '前壁埋込コンソール (机なし)'],
          ['ドア寸法・敷居', '幅 750 × 高 800 mm / 敷居50mm'],
          ['足元クリアランス', '約 700 mm']
        ],
        hasDeskFlip: false
      },
      'v3.0.0': {
        title: '操縦席ユニット (正方形・初期案)',
        badge: 'v3.0.0',
        hudTitle: '◆ COCKPIT v3.0.0 (正方形・初期案)',
        desc: '手書きノートに基づく初期の900mm正方形モデル（固定机＋モニターアーム）。',
        logClass: 'log-v3',
        logHTML: `
          <strong>【v3.0.0 仕様】</strong>
          <ul>
            <li><strong>正方形</strong>: 900×900mm</li>
            <li><strong>初期机</strong>: 固定机＋モニターアーム</li>
            <li><strong>課題</strong>: 正方形で固定机があるとドアがなく乗り降りが困難</li>
          </ul>
        `,
        specs: [
          ['形状・プロポーション', '正方形 (900 × 900mm)'],
          ['机・設備', '固定机 (700×400mm) ＋ モニターアーム'],
          ['乗降性', '乗り降りが極めて困難']
        ],
        hasDeskFlip: false
      }
    };

    function updateUIForVersion(ver) {
      const data = versionData[ver] || versionData['v7.0.0'];
      document.getElementById('view-title').innerText = data.title;
      document.getElementById('view-badge').innerText = data.badge;
      document.getElementById('hud-title').innerText = data.hudTitle;
      document.getElementById('view-desc').innerText = data.desc;

      const logBox = document.getElementById('changelog-box');
      logBox.className = 'change-log ' + data.logClass;
      logBox.innerHTML = data.logHTML;

      // v7専用フリップ机コントローラーの表示・非表示
      const flowCtrl = document.getElementById('v7-flow-controls');
      flowCtrl.style.display = data.hasDeskFlip ? 'block' : 'none';

      // スペック表
      let tableHtml = '<table class="spec-table">';
      data.specs.forEach(([k, v]) => {
        tableHtml += `<tr><td>${k}</td><td>${v}</td></tr>`;
      });
      tableHtml += '</table>';
      document.getElementById('spec-table-container').innerHTML = tableHtml;
    }

    function switchVersion(ver) {
      currentVersion = ver;
      updateUIForVersion(ver);
      buildModel(ver);

      // スライダー初期化
      setDoor(0);
      setDeskAngle(0);

      // カメラ位置の最適化
      if (controls) {
        if (ver === 'v7.0.0' || ver === 'v3.0.0') {
          controls.target.set(0, 480, 0);
          camera.position.set(1600, 1300, 1600);
        } else {
          controls.target.set(0, 480, 0);
          camera.position.set(1900, 1500, 2000);
        }
      }
    }

    // ==========================================
    // インタラクション操作
    // ==========================================
    function setDoor(deg) {
      const slider = document.getElementById('door-slider');
      const val = document.getElementById('door-val');
      if (slider) slider.value = deg;
      if (val) val.innerText = deg.toFixed(0) + '° ' + (deg > 5 ? '(開)' : '(全閉)');
      if (doorPivot) {
        const rad = (deg * Math.PI) / 180;
        doorPivot.rotation.y = -rad;
      }
    }

    function setDeskAngle(deg) {
      const slider = document.getElementById('desk-slider');
      const val = document.getElementById('desk-val');
      if (slider) slider.value = deg;
      if (val) val.innerText = deg.toFixed(0) + '° ' + (deg > 5 ? '(跳ね上げ・乗降状態)' : '(操縦状態)');
      if (deskPivot) {
        const rad = (deg * Math.PI) / 180;
        deskPivot.rotation.x = -rad;
      }
    }

    // 神導線シーケンス: 乗降モード / 操縦モード
    function setBoardingSequence(isBoarding) {
      if (isBoarding) {
        // ドアを開け、机を跳ね上げる！
        animateValue(0, 80, 400, setDoor);
        animateValue(0, 50, 400, setDeskAngle);
      } else {
        // 机を下ろし、ドアを閉める！
        animateValue(50, 0, 350, setDeskAngle);
        animateValue(80, 0, 350, setDoor);
      }
    }

    function animateValue(from, to, duration, callback) {
      const start = performance.now();
      function step(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 0.5 - Math.cos(progress * Math.PI) / 2; // easeInOut
        const current = from + (to - from) * ease;
        callback(current);
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    document.addEventListener('DOMContentLoaded', () => {
      const doorSlider = document.getElementById('door-slider');
      if (doorSlider) {
        doorSlider.addEventListener('input', (e) => setDoor(parseFloat(e.target.value)));
      }
      const deskSlider = document.getElementById('desk-slider');
      if (deskSlider) {
        deskSlider.addEventListener('input', (e) => setDeskAngle(parseFloat(e.target.value)));
      }
    });

    function updateVisibility() {
      if (groupPosts) groupPosts.visible = document.getElementById('toggle-posts').checked;
      if (groupDesk) groupDesk.visible = document.getElementById('toggle-desk').checked;
      if (groupConsole) groupConsole.visible = document.getElementById('toggle-console').checked;
      if (groupDoor) groupDoor.visible = document.getElementById('toggle-door').checked;
      if (groupBase) groupBase.visible = document.getElementById('toggle-base').checked;
      if (groupSeat) groupSeat.visible = document.getElementById('toggle-seat').checked;
      if (groupWalls) groupWalls.visible = document.getElementById('toggle-walls').checked;
      if (groupPilot) groupPilot.visible = document.getElementById('toggle-pilot').checked;
    }

    function setCameraMode(mode) {
      document.getElementById('cam-ext').classList.toggle('active', mode === 'ext');
      document.getElementById('cam-pilot').classList.toggle('active', mode === 'pilot');
      if (mode === 'pilot') {
        isPilotCam = true;
        if (controls) controls.enabled = false;
        if (currentVersion === 'v7.0.0') {
          camera.position.set(0, 910, 220);
          camera.lookAt(0, 720, -60);
        } else if (currentVersion === 'v6.0.0') {
          camera.position.set(0, 930, 550);
          camera.lookAt(0, 740, 40);
        } else {
          camera.position.set(0, 910, 400);
          camera.lookAt(0, 650, -400);
        }
      } else {
        isPilotCam = false;
        if (controls) {
          controls.enabled = true;
          controls.target.set(0, 480, 0);
        }
        if (currentVersion === 'v7.0.0' || currentVersion === 'v3.0.0') {
          camera.position.set(1600, 1300, 1600);
        } else {
          camera.position.set(1900, 1500, 2000);
        }
      }
    }

    // ==========================================
    // 初期化とレンダリング
    // ==========================================
    function getCanvasSize() {
      if (!container) return { w: window.innerWidth, h: window.innerHeight };
      let w = container.clientWidth;
      let h = container.clientHeight;
      if (!w || w <= 0) {
        w = window.innerWidth > 768 ? Math.max(window.innerWidth - 390, 300) : window.innerWidth;
      }
      if (!h || h <= 0) {
        h = window.innerWidth > 768 ? window.innerHeight : Math.round(window.innerHeight * 0.50);
      }
      return { w: Math.max(w, 200), h: Math.max(h, 200) };
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
        camera.position.set(1600, 1300, 1600);

        try {
          renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'default' });
        } catch (e) {
          renderer = new THREE.WebGLRenderer({ antialias: false });
        }
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.setSize(size.w, size.h);
        renderer.domElement.style.touchAction = 'none';
        container.appendChild(renderer.domElement);

        if (typeof THREE.OrbitControls !== 'undefined') {
          controls = new THREE.OrbitControls(camera, renderer.domElement);
          controls.enableDamping = true;
          controls.dampingFactor = 0.08;
          controls.target.set(0, 480, 0);
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

        // マテリアル & グループ
        initMaterials();
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

        // 初期バージョン (v7.0.0) を構築
        switchVersion('v7.0.0');

        // ローダー非表示
        const loader = document.getElementById('loading-indicator');
        if (loader) loader.style.display = 'none';

        onResize();
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

with open('/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/cockpit_v7.0.0_viewer.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Generated Multi-version Viewer (v7.0.0) successfully!")
