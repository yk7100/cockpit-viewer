#!/usr/bin/env python3
"""
Generate Cockpit Web 3D Viewer for v10.0.0:
- Independent Grounded Desk Legs (reaching the floor Z=0 directly under pig's head)
- Complete self-supporting 4-legged heavy duty desk
- Pig's head cavity with control yoke and gauges
- Pilot seat moved closer (Y=+150mm)
- Multi-version switcher (v10.0.0, v9.0.0, v8.0.0, v7.0.0, v6.0.0)
- X-Ray transparency slider
"""

html_code = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>COCKPIT 3D Viewer - v10.0.0 自立接地机＆マイクラ豚モデル</title>
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
      background: linear-gradient(135deg, rgba(236, 72, 153, 0.35), rgba(16, 185, 129, 0.25));
      border: 1px solid #ec4899;
      border-radius: 10px;
      padding: 12px;
      margin-bottom: 12px;
    }
    .version-selector-card label {
      display: block;
      font-size: 11px;
      font-weight: 700;
      color: #f472b6;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }
    select.version-dropdown {
      width: 100%;
      background: #0f172a;
      color: #f472b6;
      border: 1px solid #f472b6;
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
      background: linear-gradient(135deg, #ec4899, #be185d);
      color: #fff;
      padding: 3px 9px;
      border-radius: 9999px;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
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
    .log-v10 {
      background: rgba(236, 72, 153, 0.2);
      border: 1px solid #ec4899;
      color: #fce7f3;
    }
    .log-v10 strong { color: #f472b6; }
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
      accent-color: #ec4899;
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
      background: #ec4899;
      border-color: #f472b6;
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
      border: 1px solid #ec4899;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 11px;
      backdrop-filter: blur(10px);
      pointer-events: none;
      box-shadow: 0 0 20px rgba(236, 72, 153, 0.35);
      z-index: 5;
    }
    .hud-title {
      font-weight: 800;
      color: #f472b6;
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
      color: #f472b6;
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
      border: 3px solid rgba(244, 114, 182, 0.2);
      border-top-color: #f472b6;
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
      <div class="hud-title" id="hud-title">◆ COCKPIT v10.0.0 (自立接地机＆マイクラ豚)</div>
      <div class="legend-item"><div class="legend-color" style="background: #f472b6;"></div> マイクラ豚 外装 (Head & Body)</div>
      <div class="legend-item"><div class="legend-color" style="background: #855627;"></div> 【新設】机の独立接地脚 (床面直立支持)</div>
      <div class="legend-item"><div class="legend-color" style="background: #c28b48;"></div> 操縦デスク天板 (頭部下支え)</div>
      <div class="legend-item"><div class="legend-color" style="background: #f59e0b;"></div> 【頭部内】操縦桿 (パイロット正対)</div>
      <div class="legend-item"><div class="legend-color" style="background: #e2b34a;"></div> 木枠主角柱 (90mm角: 4本足の芯)</div>
      <div class="legend-item"><div class="legend-color" style="background: #0284c7;"></div> 操縦席シート (机接近配置)</div>
    </div>
  </div>

  <div id="sidebar">
    <div class="version-selector-card">
      <label for="version-select">▼ バージョン切替（形状・装飾比較）:</label>
      <select id="version-select" class="version-dropdown" onchange="switchVersion(this.value)">
        <option value="v10.0.0" selected>v10.0.0 (自立接地机＆マイクラ豚) ★最新</option>
        <option value="v9.0.0">v9.0.0 (片持ち頭部支持机＆ヘッド操縦席)</option>
        <option value="v8.0.0">v8.0.0 (マイクラ豚装飾モデル・胴体机)</option>
        <option value="v7.0.0">v7.0.0 (正方形1000mm・跳ね上げ机・神導線)</option>
        <option value="v6.0.0">v6.0.0 (長方形1500mm・固定机・正対操縦桿)</option>
      </select>
    </div>

    <div class="version-header">
      <h1 id="view-title">操縦席ユニット</h1>
      <span id="view-badge" class="badge">v10.0.0 (最新)</span>
    </div>
    <p class="desc" id="view-desc">
      豚の頭部の下に机の脚を直接床まで立て、頭部の全重量を直受けする超高剛性・自立テーブルモデルです。
    </p>

    <div id="changelog-box" class="change-log log-v10">
      <!-- 動的更新 -->
    </div>

    <div id="pig-controls">
      <div class="section-title">🐷 マイクラ豚 外装透視 (X-Ray)</div>
      <div class="control-group">
        <label for="pig-opacity">外装の透明度: <span id="opacity-val">50% (透視モード)</span></label>
        <input type="range" id="pig-opacity" min="0" max="100" value="50">
      </div>
      <div class="btn-grid">
        <button onclick="setPigOpacity(0)">外装完全表示 (豚)</button>
        <button onclick="setPigOpacity(100)">外装非表示 (骨組み)</button>
      </div>
    </div>

    <div class="section-title">ドア開閉操作 (豚の左脇腹)</div>
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
      <button id="cam-pilot" onclick="setCameraMode('pilot')">操縦席カメラ (頭部コックピット)</button>
    </div>

    <div class="section-title">パーツ表示切り替え</div>
    <div class="control-group">
      <label><input type="checkbox" id="toggle-pig" checked onchange="updateVisibility()"> 🐷 マイクラ豚 外装 (頭・胴・足・鼻)</label>
      <label><input type="checkbox" id="toggle-posts" checked onchange="updateVisibility()"> 縦の4本角柱 (足の芯柱 90mm角)</label>
      <label><input type="checkbox" id="toggle-desk" checked onchange="updateVisibility()"> 【新設】自立操縦デスク (床接地4本脚)</label>
      <label><input type="checkbox" id="toggle-console" checked onchange="updateVisibility()"> 【頭部内】操縦桿 & 計器盤</label>
      <label><input type="checkbox" id="toggle-door" checked onchange="updateVisibility()"> 乗降ドア (胴体側面)</label>
      <label><input type="checkbox" id="toggle-seat" checked onchange="updateVisibility()"> シート & ペダル</label>
      <label><input type="checkbox" id="toggle-pilot" checked onchange="updateVisibility()"> パイロットシルエット</label>
    </div>

    <div class="section-title">機体スペック (v10.0.0)</div>
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
    let currentVersion = 'v10.0.0';
    let isPilotCam = false;

    let doorPivot = null;

    let groupPig, groupPosts, groupDesk, groupConsole, groupDoor, groupBase, groupSeat, groupWalls, groupPilot;

    let pigBodyMat, pigHeadMat, pigSnoutMat, pigEyeWhiteMat, pigEyeBlackMat, pigHoofMat,
        postMat, deskTopMat, deskLegMat, basePlateMat, doorMat, handleMat,
        consoleMat, yokeMat, screenMat, gaugeMat, seatMat, seatAccentMat, wallMat, pilotMat;

    function initMaterials() {
      pigBodyMat = new THREE.MeshStandardMaterial({
        color: 0xf49292,
        roughness: 0.8,
        transparent: true,
        opacity: 0.5
      });
      pigHeadMat = new THREE.MeshStandardMaterial({
        color: 0xf8a5a5,
        roughness: 0.8,
        transparent: true,
        opacity: 0.5
      });
      pigSnoutMat = new THREE.MeshStandardMaterial({
        color: 0xe06b6b,
        roughness: 0.8,
        transparent: true,
        opacity: 0.7
      });
      pigEyeWhiteMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      pigEyeBlackMat = new THREE.MeshBasicMaterial({ color: 0x111827 });
      pigHoofMat = new THREE.MeshStandardMaterial({
        color: 0x4a2e1b,
        roughness: 0.9,
        transparent: true,
        opacity: 0.7
      });

      postMat = new THREE.MeshStandardMaterial({ color: 0xd49b4b, roughness: 0.6 });
      deskTopMat = new THREE.MeshStandardMaterial({ color: 0xb58448, roughness: 0.5 });
      deskLegMat = new THREE.MeshStandardMaterial({ color: 0x855627, roughness: 0.7 }); // 机の脚
      basePlateMat = new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.7 });
      doorMat = new THREE.MeshStandardMaterial({ color: 0xf472b6, roughness: 0.5 });
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
      const groups = [groupPig, groupPosts, groupDesk, groupConsole, groupDoor, groupBase, groupSeat, groupWalls, groupPilot];
      groups.forEach(g => {
        if (g) {
          while (g.children.length > 0) {
            const obj = g.children[0];
            g.remove(obj);
          }
        }
      });
      doorPivot = null;
    }

    // ==========================================
    // モデル構築 (v10.0.0 最新自立接地脚)
    // ==========================================
    function buildModel(version) {
      clearModelGroups();

      if (version === 'v10.0.0') {
        // v10.0.0: 自立接地脚付きデスク ＆ マイクラ豚ヘッドキャビン
        const U = 87.5;
        const BODY_W = 10 * U;  // 875 mm
        const BODY_L = 16 * U;  // 1400 mm
        const BODY_H = 8 * U;   // 700 mm
        const LEG_S = 4 * U;    // 350 mm
        const LEG_H = 440;      // 440 mm
        const HEAD_W = 8 * U;   // 700 mm
        const HEAD_H = 8 * U;   // 700 mm
        const HEAD_D = 7 * U;   // 612 mm

        const POST_S = 90;
        const POST_H = 950;

        const X_L = -(BODY_W - LEG_S) / 2; // -262.5
        const X_R =  (BODY_W - LEG_S) / 2; //  262.5
        const Y_F = -(BODY_L - LEG_S) / 2; // -525.0
        const Y_R =  (BODY_L - LEG_S) / 2; //  525.0

        // 1. 縦の4本主角柱 (90mm角材)
        const postPositions = [
          [X_L, Y_F], [X_R, Y_F],
          [X_L, Y_R], [X_R, Y_R]
        ];
        postPositions.forEach(([px, pz]) => {
          addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);
          addBox(groupBase, 300, 18, 300, px, 9, pz, basePlateMat);
        });

        // 2. 🐷 マイクラ豚 外装
        postPositions.forEach(([px, pz]) => {
          addBox(groupPig, LEG_S, LEG_H - 80, LEG_S, px, (LEG_H - 80)/2 + 80, pz, pigBodyMat);
          addBox(groupPig, LEG_S, 80, LEG_S, px, 40, pz, pigHoofMat);
        });

        const BODY_Z_C = LEG_H + BODY_H / 2;
        addBox(groupPig, 15, BODY_H, BODY_L, BODY_W/2, BODY_Z_C, 0, pigBodyMat);
        addBox(groupPig, BODY_W, BODY_H, 15, 0, BODY_Z_C, BODY_L/2, pigBodyMat);
        addBox(groupPig, BODY_W, 15, BODY_L, 0, LEG_H + BODY_H, 0, pigBodyMat);
        addBox(groupPig, BODY_W, 15, BODY_L, 0, LEG_H, 0, pigBodyMat);
        addBox(groupPig, BODY_W, 200, 15, 0, LEG_H + 100, -BODY_L/2, pigBodyMat);

        // 頭部 (Head)
        const HEAD_Y_C = -(BODY_L / 2 + HEAD_D / 2) + 60;
        const HEAD_Z_C = LEG_H + HEAD_H / 2 - 20;
        addBox(groupPig, HEAD_W, HEAD_H, HEAD_D, 0, HEAD_Z_C, HEAD_Y_C, pigHeadMat);

        // 鼻 (Snout)
        const SNOUT_Y = HEAD_Y_C - HEAD_D/2 - 44;
        const SNOUT_Z = HEAD_Z_C - 70;
        addBox(groupPig, 350, 262, 88, 0, SNOUT_Z, SNOUT_Y, pigSnoutMat);
        addBox(groupPig, 50, 60, 4, -80, SNOUT_Z, SNOUT_Y - 45, pigEyeBlackMat);
        addBox(groupPig, 50, 60, 4,  80, SNOUT_Z, SNOUT_Y - 45, pigEyeBlackMat);

        // つぶらな目
        const EYE_Z = HEAD_Z_C + 40;
        const EYE_Y = HEAD_Y_C - HEAD_D/2 - 2;
        addBox(groupPig, 90, 90, 4, -HEAD_W/2 + 70, EYE_Z, EYE_Y, pigEyeWhiteMat);
        addBox(groupPig, 45, 90, 6, -HEAD_W/2 + 50, EYE_Z, EYE_Y, pigEyeBlackMat);
        addBox(groupPig, 90, 90, 4,  HEAD_W/2 - 70, EYE_Z, EYE_Y, pigEyeWhiteMat);
        addBox(groupPig, 45, 90, 6,  HEAD_W/2 - 50, EYE_Z, EYE_Y, pigEyeBlackMat);

        // 乗降ドア
        const DOOR_W = 700;
        const DOOR_H = BODY_H;
        const DOOR_Z = BODY_Z_C;
        doorPivot = new THREE.Group();
        doorPivot.position.set(-BODY_W/2, 0, -DOOR_W / 2);
        groupDoor.add(doorPivot);
        const doorMesh = new THREE.Mesh(new THREE.BoxGeometry(15, DOOR_H, DOOR_W), doorMat);
        doorMesh.position.set(0, DOOR_Z, DOOR_W / 2);
        doorPivot.add(doorMesh);
        const handleIn = new THREE.Mesh(new THREE.BoxGeometry(25, 160, 30), handleMat);
        handleIn.position.set(25, DOOR_Z, DOOR_W - 80);
        doorPivot.add(handleIn);

        const fixFrontLen = (BODY_L - DOOR_W) / 2;
        addBox(groupPig, 15, BODY_H, fixFrontLen, -BODY_W/2, BODY_Z_C, -BODY_L/2 + fixFrontLen/2, pigBodyMat);
        addBox(groupPig, 15, BODY_H, fixFrontLen, -BODY_W/2, BODY_Z_C,  BODY_L/2 - fixFrontLen/2, pigBodyMat);

        // 3. 【新設】床接地・自立操縦デスク (机の足が床面まで直立！)
        const DESK_W = 680;
        const DESK_H = 700;
        const DESK_L = 800;
        const DESK_Y_C = -650;
        const LEG_H_DESK = DESK_H - 24; // 676mm

        // 天板 (全長800mm)
        addBox(groupDesk, DESK_W, 24, DESK_L, 0, DESK_H - 12, DESK_Y_C, deskTopMat);

        // 【前脚 2本】豚の頭部の真下 (Y=-950mm) から床面Z=0まで直立接地！
        addBox(groupDesk, 60, LEG_H_DESK, 60, -300, LEG_H_DESK/2, -950, deskLegMat);
        addBox(groupDesk, 60, LEG_H_DESK, 60,  300, LEG_H_DESK/2, -950, deskLegMat);

        // 【後脚 2本】机の手前側 (Y=-350mm) から床面Z=0まで直立接地！
        addBox(groupDesk, 60, LEG_H_DESK, 60, -300, LEG_H_DESK/2, -350, deskLegMat);
        addBox(groupDesk, 60, LEG_H_DESK, 60,  300, LEG_H_DESK/2, -350, deskLegMat);

        // 天板下の補強梁フレーム (前後をつなぐ桟)
        addBox(groupDesk, 30, 45, DESK_L - 60, -300, DESK_H - 45, DESK_Y_C, deskLegMat);
        addBox(groupDesk, 30, 45, DESK_L - 60,  300, DESK_H - 45, DESK_Y_C, deskLegMat);

        // 4. 頭部内部の操縦桿 & 計器盤
        const YOKE_Y = -820;
        addBox(groupConsole, 140, 25, 90, 0, DESK_H + 12.5, YOKE_Y, consoleMat);
        const shaft = new THREE.Mesh(new THREE.CylinderGeometry(14, 14, 110, 16), gaugeMat);
        shaft.position.set(0, DESK_H + 50, YOKE_Y + 30);
        shaft.rotation.x = 0.45;
        groupConsole.add(shaft);

        addBox(groupConsole, 160, 24, 26, 0, DESK_H + 75, YOKE_Y + 70, yokeMat, 0.3);
        addBox(groupConsole, 26, 110, 26, -85, DESK_H + 105, YOKE_Y + 75, yokeMat, 0.2);
        addBox(groupConsole, 26, 110, 26,  85, DESK_H + 105, YOKE_Y + 75, yokeMat, 0.2);

        // 傾斜計器盤 & 液晶画面
        addBox(groupConsole, 500, 150, 20, 0, DESK_H + 80, -1080, consoleMat, -0.5);
        addBox(groupConsole, 220, 100, 15, 0, DESK_H + 90, -1075, screenMat, -0.5);
        const mL = new THREE.Mesh(new THREE.CylinderGeometry(28, 28, 15, 16), gaugeMat);
        mL.position.set(-160, DESK_H + 90, -1075);
        mL.rotation.x = -0.5;
        groupConsole.add(mL);
        const mR = new THREE.Mesh(new THREE.CylinderGeometry(28, 28, 15, 16), gaugeMat);
        mR.position.set(160, DESK_H + 90, -1075);
        mR.rotation.x = -0.5;
        groupConsole.add(mR);

        // 5. 机接近シート & ペダル
        const SEAT_Y = 150;
        addBox(groupSeat, 500, 50, 420, 0, 350, SEAT_Y, seatMat);
        const sBack = addBox(groupSeat, 480, 500, 45, 0, 620, SEAT_Y + 180, seatMat);
        sBack.rotation.x = -0.2;
        addBox(groupSeat, 240, 140, 50, 0, 900, SEAT_Y + 230, seatAccentMat);

        const pL = addBox(groupSeat, 85, 140, 18, -140, 70, -350, consoleMat);
        pL.rotation.x = -0.4;
        const pR = addBox(groupSeat, 85, 140, 18,  140, 70, -350, consoleMat);
        pR.rotation.x = -0.4;

        // パイロット
        const pHead = new THREE.Mesh(new THREE.SphereGeometry(100, 16, 16), pilotMat);
        pHead.position.set(0, 890, SEAT_Y + 150);
        groupPilot.add(pHead);
        const pTorso = new THREE.Mesh(new THREE.CylinderGeometry(120, 100, 400, 8), pilotMat);
        pTorso.position.set(0, 620, SEAT_Y + 90);
        pTorso.rotation.x = -0.2;
        groupPilot.add(pTorso);
        const pThighs = new THREE.Mesh(new THREE.BoxGeometry(250, 90, 340), pilotMat);
        pThighs.position.set(0, 370, SEAT_Y - 80);
        groupPilot.add(pThighs);
        const pShins = new THREE.Mesh(new THREE.BoxGeometry(250, 340, 90), pilotMat);
        pShins.position.set(0, 210, -280);
        pShins.rotation.x = 0.35;
        groupPilot.add(pShins);

        const armL = addBox(groupPilot, 40, 40, 480, -75, 750, -300, pilotMat, 0.2);
        const armR = addBox(groupPilot, 40, 40, 480,  75, 750, -300, pilotMat, 0.2);

      } else if (version === 'v9.0.0') {
        // v9.0.0 (片持ち頭部支持机)
        const U = 87.5;
        const BODY_W = 10 * U;
        const BODY_L = 16 * U;
        const BODY_H = 8 * U;
        const LEG_S = 4 * U;
        const LEG_H = 440;
        const HEAD_W = 8 * U;
        const HEAD_H = 8 * U;
        const HEAD_D = 7 * U;
        const POST_S = 90;
        const POST_H = 950;
        const X_L = -(BODY_W - LEG_S) / 2;
        const X_R =  (BODY_W - LEG_S) / 2;
        const Y_F = -(BODY_L - LEG_S) / 2;
        const Y_R =  (BODY_L - LEG_S) / 2;

        const postPositions = [[X_L, Y_F], [X_R, Y_F], [X_L, Y_R], [X_R, Y_R]];
        postPositions.forEach(([px, pz]) => {
          addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);
          addBox(groupBase, 300, 18, 300, px, 9, pz, basePlateMat);
          addBox(groupPig, LEG_S, LEG_H - 80, LEG_S, px, (LEG_H - 80)/2 + 80, pz, pigBodyMat);
          addBox(groupPig, LEG_S, 80, LEG_S, px, 40, pz, pigHoofMat);
        });

        const BODY_Z_C = LEG_H + BODY_H / 2;
        addBox(groupPig, 15, BODY_H, BODY_L, BODY_W/2, BODY_Z_C, 0, pigBodyMat);
        addBox(groupPig, BODY_W, BODY_H, 15, 0, BODY_Z_C, BODY_L/2, pigBodyMat);
        addBox(groupPig, BODY_W, 15, BODY_L, 0, LEG_H + BODY_H, 0, pigBodyMat);
        addBox(groupPig, BODY_W, 15, BODY_L, 0, LEG_H, 0, pigBodyMat);

        const HEAD_Y_C = -(BODY_L / 2 + HEAD_D / 2) + 60;
        const HEAD_Z_C = LEG_H + HEAD_H / 2 - 20;
        addBox(groupPig, HEAD_W, HEAD_H, HEAD_D, 0, HEAD_Z_C, HEAD_Y_C, pigHeadMat);
        addBox(groupPig, 350, 262, 88, 0, HEAD_Z_C - 70, HEAD_Y_C - HEAD_D/2 - 44, pigSnoutMat);

        // 片持ち机 (床脚なし)
        addBox(groupDesk, 680, 24, 800, 0, 688, -650, deskTopMat);
        addBox(groupDesk, 25, 50, 760, -320, 655, -650, deskLegMat);
        addBox(groupDesk, 25, 50, 760,  320, 655, -650, deskLegMat);

        addBox(groupConsole, 160, 24, 26, 0, 775, -750, yokeMat, 0.3);
        addBox(groupSeat, 500, 50, 420, 0, 350, 150, seatMat);

      } else if (version === 'v8.0.0') {
        // v8.0.0 (胴体机)
        const U = 87.5;
        const BODY_W = 10 * U;
        const BODY_L = 16 * U;
        const BODY_H = 8 * U;
        const LEG_S = 4 * U;
        const LEG_H = 440;
        const POST_S = 90;
        const POST_H = 950;
        const X_L = -(BODY_W - LEG_S) / 2;
        const X_R =  (BODY_W - LEG_S) / 2;
        const Y_F = -(BODY_L - LEG_S) / 2;
        const Y_R =  (BODY_L - LEG_S) / 2;

        const postPositions = [[X_L, Y_F], [X_R, Y_F], [X_L, Y_R], [X_R, Y_R]];
        postPositions.forEach(([px, pz]) => {
          addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);
          addBox(groupBase, 300, 18, 300, px, 9, pz, basePlateMat);
          addBox(groupPig, LEG_S, LEG_H - 80, LEG_S, px, (LEG_H - 80)/2 + 80, pz, pigBodyMat);
          addBox(groupPig, LEG_S, 80, LEG_S, px, 40, pz, pigHoofMat);
        });

        addBox(groupDesk, 680, 24, 360, 0, 688, -100, deskTopMat);
        addBox(groupConsole, 160, 24, 26, 0, 775, -30, yokeMat, 0.3);
        addBox(groupSeat, 500, 50, 420, 0, 350, Y_R - 120, seatMat);

      } else if (version === 'v7.0.0') {
        // v7.0.0 (正方形跳ね上げ机)
        const W_INNER = 720;
        const POST_S = 90;
        const POST_H = 950;
        const DEPTH = 820;
        const X_L = -(W_INNER + POST_S) / 2;
        const X_R =  (W_INNER + POST_S) / 2;
        const Y_F = -DEPTH / 2;
        const Y_R =  DEPTH / 2;

        const postPositions = [[X_L, Y_F], [X_R, Y_F], [X_L, Y_R], [X_R, Y_R]];
        postPositions.forEach(([px, pz]) => {
          addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);
          addBox(groupBase, 300, 18, 300, px, 9, pz, basePlateMat);
        });

        addBox(groupDesk, 690, 24, 350, 0, 688, -60, deskTopMat);
        addBox(groupConsole, 160, 24, 26, 0, 775, 10, yokeMat, 0.3);
        addBox(groupSeat, 520, 50, 420, 0, 350, Y_R - 190, seatMat);
        addBox(groupWalls, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, wallMat);

      } else if (version === 'v6.0.0') {
        // v6.0.0 (長方形1500mm・固定机)
        const W_INNER = 700;
        const POST_S = 90;
        const POST_H = 950;
        const DEPTH = 1350;
        const X_L = -(W_INNER + POST_S) / 2;
        const X_R =  (W_INNER + POST_S) / 2;
        const Y_F = -DEPTH / 2;
        const Y_R =  DEPTH / 2;

        const postPositions = [[X_L, Y_F], [X_R, Y_F], [X_L, Y_R], [X_R, Y_R]];
        postPositions.forEach(([px, pz]) => {
          addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);
          addBox(groupBase, 300, 18, 300, px, 9, pz, basePlateMat);
        });
        addBox(groupDesk, 680, 24, 380, 0, 688, 0, deskTopMat);
        addBox(groupConsole, 160, 24, 26, 0, 775, 70, yokeMat, 0.3);
        addBox(groupSeat, 520, 50, 460, 0, 350, Y_R - 240, seatMat);
        addBox(groupWalls, 12, POST_H, DEPTH + POST_S, X_R + POST_S/2 + 6, POST_H/2, 0, wallMat);
      }
    }

    // ==========================================
    // UI情報更新
    // ==========================================
    const versionData = {
      'v10.0.0': {
        title: '操縦席ユニット (自立接地机＆マイクラ豚)',
        badge: 'v10.0.0 (最新第10弾)',
        hudTitle: '◆ COCKPIT v10.0.0 (自立接地机＆マイクラ豚)',
        desc: '豚の頭部の下に机の脚（4本脚）を直接床面まで直立接地させ、頭部の重量を完全直受けする超高剛性モデル。',
        logClass: 'log-v10',
        logHTML: `
          <strong>【v10.0.0 アップデート内容】</strong>
          <ul>
            <li><strong>机の独立接地脚を新設</strong>: 豚の頭の下（Y=-950mm）に床まで届く頑丈な脚（60mm角）を配置！</li>
            <li><strong>頭部の荷重を床で直受け</strong>: 片持ち梁の不安定さが完全解消。頭部ボックスが一切沈まない！</li>
            <li><strong>完全自立テーブル構造</strong>: 木枠主角柱（90mm角×4本）とは独立して机単体で製作可能（工作が超ラク）</li>
            <li><strong>広大な足入れ空間</strong>: シートから前脚まで奥行900mmあり、大人の足先が前脚にすらぶつからない</li>
            <li><strong>頭の内部に操縦桿 ＆ 前寄りシート</strong>: 豚の頭の中で外を見ながら操縦する大迫力シム</li>
          </ul>
        `,
        specs: [
          ['モデル区分', '<strong>自立接地机 ＆ マイクラ豚モデル</strong>'],
          ['机の脚 (接地支持)', '<strong>60mm角材 x 4本 (床Z=0まで直立接地)</strong>'],
          ['頭部下支え', '<strong>前脚が頭の直下(Y=-950mm)で完全直受け</strong>'],
          ['操縦デスク寸法', '幅 680 × 全長 800 × 高 700 mm'],
          ['操縦桿の配置', '豚の「頭の内部」正対配置 (Y=-820mm)'],
          ['シート位置', '机接近前寄り配置 (Y=+150mm)'],
          ['木枠主角柱', '90mm角材 (長さ950mm) x 4本 (足の芯柱)']
        ],
        hasPigControls: true
      },
      'v9.0.0': {
        title: '操縦席ユニット (頭部支持机＆ヘッド操縦席)',
        badge: 'v9.0.0',
        hudTitle: '◆ COCKPIT v9.0.0 (片持ち頭部支持机)',
        desc: '机を前方に延長して豚の頭部を下支えしたモデル（床脚なし片持ち構造）。',
        logClass: 'log-v9',
        logHTML: `
          <strong>【v9.0.0 仕様】</strong>
          <ul>
            <li>机天板を前方に延長し頭部を片持ち支持</li>
            <li>頭部内部に操縦桿、シート前寄り配置</li>
          </ul>
        `,
        specs: [
          ['机の構造', '前柱からの片持ち梁支持 (床脚なし)'],
          ['操縦桿', '頭部内部配置']
        ],
        hasPigControls: true
      },
      'v8.0.0': {
        title: '操縦席ユニット (マイクラ豚装飾モデル)',
        badge: 'v8.0.0',
        hudTitle: '◆ COCKPIT v8.0.0 (マイクラ豚・胴体机)',
        desc: 'マイクラ豚の外装装飾に寸法を合わせた初期モデル。',
        logClass: 'log-v8',
        logHTML: `
          <strong>【v8.0.0 仕様】</strong>
          <ul>
            <li>マイクラ豚ボクセル公式比率準拠</li>
            <li>机と操縦桿は胴体内</li>
          </ul>
        `,
        specs: [
          ['外観スタイル', 'マインクラフト豚'],
          ['机', '胴体内配置']
        ],
        hasPigControls: true
      },
      'v7.0.0': {
        title: '操縦席ユニット (正方形・神導線)',
        badge: 'v7.0.0',
        hudTitle: '◆ COCKPIT v7.0.0 (正方形・神導線)',
        desc: '正方形プロポーション（幅900×長1000mm）と跳ね上げ机モデル。',
        logClass: 'log-v7',
        logHTML: `
          <strong>【v7.0.0 仕様】</strong>
          <ul>
            <li>正方形900×1000mm、跳ね上げ机</li>
          </ul>
        `,
        specs: [
          ['形状', '正方形 (900×1000mm)']
        ],
        hasPigControls: false
      }
    };

    function updateUIForVersion(ver) {
      const data = versionData[ver] || versionData['v10.0.0'];
      document.getElementById('view-title').innerText = data.title;
      document.getElementById('view-badge').innerText = data.badge;
      document.getElementById('hud-title').innerText = data.hudTitle;
      document.getElementById('view-desc').innerText = data.desc;

      const logBox = document.getElementById('changelog-box');
      logBox.className = 'change-log ' + data.logClass;
      logBox.innerHTML = data.logHTML;

      document.getElementById('pig-controls').style.display = data.hasPigControls ? 'block' : 'none';

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

      setDoor(0);
      if (ver === 'v10.0.0' || ver === 'v9.0.0' || ver === 'v8.0.0') {
        setPigOpacity(50);
        camera.position.set(2200, 1600, 2200);
        controls.target.set(0, 600, -250);
      } else if (ver === 'v7.0.0') {
        camera.position.set(1600, 1300, 1600);
        controls.target.set(0, 480, 0);
      } else {
        camera.position.set(1900, 1500, 2000);
        controls.target.set(0, 480, 0);
      }
    }

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

    function setPigOpacity(val) {
      const slider = document.getElementById('pig-opacity');
      const label = document.getElementById('opacity-val');
      if (slider) slider.value = val;
      if (label) {
        if (val === 0) label.innerText = '0% (外装完全表示)';
        else if (val === 100) label.innerText = '100% (外装非表示)';
        else label.innerText = val + '% (透視モード)';
      }
      const opacity = 1.0 - (val / 100.0);
      if (pigBodyMat) {
        pigBodyMat.opacity = opacity;
        pigBodyMat.visible = opacity > 0.02;
      }
      if (pigHeadMat) {
        pigHeadMat.opacity = opacity;
        pigHeadMat.visible = opacity > 0.02;
      }
      if (pigHoofMat) {
        pigHoofMat.opacity = Math.min(opacity * 1.4, 1.0);
        pigHoofMat.visible = opacity > 0.02;
      }
      if (pigSnoutMat) {
        pigSnoutMat.opacity = Math.min(opacity * 1.3, 1.0);
        pigSnoutMat.visible = opacity > 0.02;
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      const doorSlider = document.getElementById('door-slider');
      if (doorSlider) {
        doorSlider.addEventListener('input', (e) => setDoor(parseFloat(e.target.value)));
      }
      const pigSlider = document.getElementById('pig-opacity');
      if (pigSlider) {
        pigSlider.addEventListener('input', (e) => setPigOpacity(parseFloat(e.target.value)));
      }
    });

    function updateVisibility() {
      if (groupPig) groupPig.visible = document.getElementById('toggle-pig').checked;
      if (groupPosts) groupPosts.visible = document.getElementById('toggle-posts').checked;
      if (groupDesk) groupDesk.visible = document.getElementById('toggle-desk').checked;
      if (groupConsole) groupConsole.visible = document.getElementById('toggle-console').checked;
      if (groupDoor) groupDoor.visible = document.getElementById('toggle-door').checked;
      if (groupSeat) groupSeat.visible = document.getElementById('toggle-seat').checked;
      if (groupPilot) groupPilot.visible = document.getElementById('toggle-pilot').checked;
    }

    function setCameraMode(mode) {
      document.getElementById('cam-ext').classList.toggle('active', mode === 'ext');
      document.getElementById('cam-pilot').classList.toggle('active', mode === 'pilot');
      if (mode === 'pilot') {
        isPilotCam = true;
        if (controls) controls.enabled = false;
        if (currentVersion === 'v10.0.0' || currentVersion === 'v9.0.0') {
          camera.position.set(0, 890, 150);
          camera.lookAt(0, 750, -900);
        } else if (currentVersion === 'v8.0.0') {
          camera.position.set(0, 890, 380);
          camera.lookAt(0, 720, -500);
        } else {
          camera.position.set(0, 910, 220);
          camera.lookAt(0, 720, -60);
        }
      } else {
        isPilotCam = false;
        if (controls) controls.enabled = true;
        if (currentVersion === 'v10.0.0' || currentVersion === 'v9.0.0' || currentVersion === 'v8.0.0') {
          camera.position.set(2200, 1600, 2200);
          controls.target.set(0, 600, -250);
        } else {
          camera.position.set(1600, 1300, 1600);
          controls.target.set(0, 480, 0);
        }
      }
    }

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
        camera.position.set(2200, 1600, 2200);

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
          controls.target.set(0, 600, -250);
          controls.minDistance = 300;
          controls.maxDistance = 7000;
        }

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
        scene.add(ambientLight);

        const dirLight1 = new THREE.DirectionalLight(0xfff1f2, 0.9);
        dirLight1.position.set(1500, 2500, 1200);
        scene.add(dirLight1);

        const dirLight2 = new THREE.DirectionalLight(0x38bdf8, 0.6);
        dirLight2.position.set(-1500, 1200, -1500);
        scene.add(dirLight2);

        const grid = new THREE.GridHelper(5000, 50, 0xec4899, 0x1e293b);
        grid.position.y = 0;
        scene.add(grid);

        initMaterials();
        groupPig = new THREE.Group();
        groupPosts = new THREE.Group();
        groupDesk = new THREE.Group();
        groupConsole = new THREE.Group();
        groupDoor = new THREE.Group();
        groupBase = new THREE.Group();
        groupSeat = new THREE.Group();
        groupWalls = new THREE.Group();
        groupPilot = new THREE.Group();

        scene.add(groupPig);
        scene.add(groupPosts);
        scene.add(groupDesk);
        scene.add(groupConsole);
        scene.add(groupDoor);
        scene.add(groupBase);
        scene.add(groupSeat);
        scene.add(groupWalls);
        scene.add(groupPilot);

        switchVersion('v10.0.0');

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

with open('/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/cockpit_v10.0.0_viewer.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Generated Cockpit v10.0.0 Viewer successfully!")
