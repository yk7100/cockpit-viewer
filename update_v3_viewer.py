import os
import json

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"

# ------------------------------------------------------------------
# 1. Update CUT_LIST.md (ノートの数式に基づいた木材・資材リスト)
# ------------------------------------------------------------------
cut_list_md = """# コクピット新設計 (V3: 4本角柱シミュレーター型) 木取り表・工作ガイド

手書き設計図（ノート）に記載された寸法計算式と比率に基づき、高剛性なシミュレーター型コクピットの部材リストを作成しました。

---

## 1. ノートの基本計算式・基準寸法

* **基準高さ $h$**: **$90\\text{ cm}$**（$87.5\\text{ cm} \\fallingdotseq 90\\text{ cm}$）
  * 計算根拠: カフェ1人用席の理想横幅 **$70\\text{ cm}$** $\\rightarrow \\frac{4}{5}h = 70 \\implies h = 87.5 \\fallingdotseq 90\\text{ cm}$
* **機体内寸横幅**: **$70\\text{ cm}$**（$\\frac{4}{5}h$）
* **4本の主柱（角柱）の太さ**: **$9.0\\text{ cm}$角**（ノート: $\\frac{1}{9}h \\sim \\frac{1}{12}h = 7.3 \\sim 9.7\\text{ cm}$、ホームセンターで一般的な**90mm角材／3寸角**に該当）
* **主柱の高さ**: **$90\\text{ cm}$**（約 $90\\text{ cm} \\pm 20\\text{ cm}$）
* **足元ベース正方形**: **$30\\text{ cm} \\times 30\\text{ cm}$**（ノート: $\\frac{3}{10}h \\fallingdotseq \\frac{1}{3}h$）
* **足元三角補強リブ**: ノートの「少し硬めの素材」により、各柱の根元を直角三角リブ（底辺90mm×高150mm×厚15mm）でガチッと固定。

---

## 2. 部材カットリスト (木材・合板)

| 部品名 | 規格・断面 | 寸法 (mm) | 数量 | 用途・備考 |
| :--- | :--- | :--- | :--- | :--- |
| **主角柱 (脚)** | 90mm × 90mm 角材 | 長さ 900 | **4本** | メイン4本柱（前左右・後左右） |
| **足元ベース板** | 厚さ 15〜18mm 合板 | 300 × 300 | **4枚** | 転倒防止接地プレート |
| **足元三角補強リブ** | 厚さ 12〜15mm 合板/木片 | 90 × 150 (直角三角) | **8〜16個** | 柱根元のハカマ補強（少し硬めの素材） |
| **机天板 (操作卓)** | 厚さ 20〜25mm 集成材/合板 | 790 × 350 | **1枚** | コントロールデスク（高さ 約520mm） |
| **机受木 / 横木** | 45mm × 45mm または 30mm角 | 長さ 700 | **2本** | 机天板および前柱の連結補強 |
| **モニター支柱** | 45mm × 45mm 角材 | 長さ 650 | **2本** | 前柱から上方に伸びる画面支持柱 |
| **モニター斜めブレース** | 30mm × 30mm 角材 | 長さ 320 (斜めカット) | **2本** | モニター支柱の補強筋交い |
| **モニターマウント横板** | 厚さ 15mm 合板/板材 | 600 × 120 | **1枚** | VESAマウント/モニター固定背板 |
| **座面受木 (後柱間)** | 60mm × 60mm または 45mm角 | 長さ 700 | **1本** | シート座面を支える頑丈な横梁 |
| **サイドガード横木** | 45mm × 45mm 角材 | 長さ 660 | **4本** | 前後柱を繋ぐ腰高レール＆トップレール |
| **サイド外壁パネル** | 段ボール または 4mmベニヤ | 750 × 900 | **2枚** | 左右外装囲いパネル |

---

## 3. 推奨資材・ハードウェア

* **モニター**: 24インチ〜27インチ液晶ディスプレイ（HDMI入力、ゲーム機やPCを接続）
* **操縦系**: フライトシミュレーター用ジョイスティック または ハンドルコントローラー
* **木ネジ**: 
  * 90mm角柱接合用: 長さ 75〜90mm コーススレッド / スリムビス
  * ベース・リブ・合板固定用: 長さ 35〜45mm 木ネジ
* **L字アングル金具**: 8〜12個（机天板や柱の要所補強用）

---

## 4. 組み立て手順の目安

1. **足元ユニットの制作**: 4枚のベース板（300×300mm）に90mm角柱を立て、三角補強リブをビス止めして自立させる。
2. **フレーム連結**: 前柱2本、後柱2本の間を横木（700mm）で繋ぎ、左右の前後柱をサイドレールで連結して頑丈な直方体骨組みを構成。
3. **机・モニター台の設置**: 前柱の高さ約520mmに机天板を取り付け、上部へモニター支柱と斜めブレースを設置。
4. **座席＆外装**: コックピット内部にシートを据え付け、左右外側にサイドパネルを取り付けて完成。
"""

with open(os.path.join(OUT_DIR, "CUT_LIST.md"), "w", encoding="utf-8") as f:
    f.write(cut_list_md)

print("CUT_LIST.md updated for V3 simulator cockpit.")

# ------------------------------------------------------------------
# 2. Update cockpit_viewer.html (Three.js 3D Viewer for V3)
# ------------------------------------------------------------------
viewer_html = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>シミュレーターコクピット V3 (手書きノート忠実設計)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      background: #0b0f19;
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
      width: 370px;
      background: rgba(15, 23, 42, 0.95);
      border-left: 1px solid #334155;
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
    }
    .badge-v3 {
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
      margin-bottom: 16px;
      line-height: 1.5;
    }
    .math-box {
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid #0284c7;
      border-radius: 6px;
      padding: 10px 12px;
      font-size: 11.5px;
      margin-bottom: 14px;
      line-height: 1.6;
      color: #bae6fd;
    }
    .math-box strong { color: #38bdf8; }
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
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid #0284c7;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 12px;
      backdrop-filter: blur(8px);
      pointer-events: none;
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
      <div class="hud-title">◆ 新設計 V3: 4本角柱シミュレーター</div>
      <div class="legend-item"><div class="legend-color" style="background: #e2b34a;"></div> 4本主角柱 (90mm角×900mm)</div>
      <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> 足元ベース板 & 三角補強リブ (ハカマ)</div>
      <div class="legend-item"><div class="legend-color" style="background: #38bdf8;"></div> 机 (操作卓) & モニターマウント</div>
      <div class="legend-item"><div class="legend-color" style="background: #22c55e;"></div> 27インチ 液晶ディスプレイ</div>
      <div class="legend-item"><div class="legend-color" style="background: #64748b;"></div> サイド囲いパネル (段ボール)</div>
    </div>
  </div>

  <div id="sidebar">
    <h1>コクピット <span class="badge-v3">V3 ノート再現</span></h1>
    <p class="desc">手書きノートの数式・比率（横幅4/5h、柱太さ1/10h、足元1/3h）を100%正確に落とし込んだ高剛性シミュレーターモデル。</p>

    <div class="math-box">
      <strong>【ノートの設計数式】</strong><br>
      • 基準高さ: <code>h = 90cm</code> (87.5≒90cm)<br>
      • 横幅: <code>4/5 h = 70cm</code> (カフェ1人席の理想幅)<br>
      • 柱太さ: <code>1/9〜1/12 h ≒ 9.0cm角</code> (4本)<br>
      • 足元ベース: <code>1/3 h = 30cm角</code> ＋ 三角リブ
    </div>

    <div class="section-title">視点切り替え</div>
    <div class="btn-grid">
      <button id="cam-ext" class="active" onclick="setCameraMode('ext')">外観カメラ (全体)</button>
      <button id="cam-pilot" onclick="setCameraMode('pilot')">着座カメラ (プレイヤー視点)</button>
    </div>

    <div class="section-title">パーツ表示切り替え</div>
    <div class="control-group">
      <label><input type="checkbox" id="toggle-posts" checked onchange="updateVisibility()"> 4本主角柱 (90mm角)</label>
      <label><input type="checkbox" id="toggle-base" checked onchange="updateVisibility()"> 足元ベース板 & 三角リブ</label>
      <label><input type="checkbox" id="toggle-desk" checked onchange="updateVisibility()"> 机 (操作卓) & ジョイスティック</label>
      <label><input type="checkbox" id="toggle-monitor" checked onchange="updateVisibility()"> モニター & 支持アーム</label>
      <label><input type="checkbox" id="toggle-seat" checked onchange="updateVisibility()"> コクピットシート</label>
      <label><input type="checkbox" id="toggle-panels" checked onchange="updateVisibility()"> サイド外壁パネル</label>
      <label><input type="checkbox" id="toggle-pilot" checked onchange="updateVisibility()"> パイロットシルエット</label>
    </div>

    <div class="section-title">機体スペック (V3)</div>
    <table class="spec-table">
      <tr><td>内寸横幅</td><td>700 mm (ノート: 4/5h)</td></tr>
      <tr><td>外寸全幅</td><td>880 mm</td></tr>
      <tr><td>奥行き</td><td>900 mm</td></tr>
      <tr><td>柱の太さ</td><td>90 × 90 mm (4本)</td></tr>
      <tr><td>柱の長さ (高さ)</td><td>900 mm (ノート: h)</td></tr>
      <tr><td>足元ベース板</td><td>300 × 300 mm (4枚)</td></tr>
      <tr><td>足元補強</td><td>直角三角リブ (硬めの素材)</td></tr>
      <tr><td>机高さ</td><td>520 mm (ノート: 約1/2h)</td></tr>
      <tr><td>モニター</td><td>27インチ相当 (支持ブレース付)</td></tr>
    </table>

    <div class="section-title">CADデータ出力先</div>
    <p style="font-size: 11px; color:#94a3b8; word-break: break-all; line-height: 1.5;">
      /Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/<br>
      • <code>cockpit_v3_full.step</code> (全体CAD)<br>
      • <code>cockpit_v3_full.stl</code> (3Dメッシュ)<br>
      • <code>cockpit_v3_frame.step</code> / <code>.stl</code><br>
      • <code>CUT_LIST.md</code> (木取り・組み立て手順)
    </p>
  </div>

  <script>
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0b0f19);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 10, 15000);
    camera.position.set(1600, 1400, 1800);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 500, 0);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0x38bdf8, 0.8);
    dirLight1.position.set(1500, 2500, 1200);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.4);
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
    const deskMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.4 }); // 机天板
    const monitorFrameMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.3 });
    const screenMat = new THREE.MeshBasicMaterial({ color: 0x06b6d4 }); // モニター画面 (発光)
    const seatMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 });
    const seatAccentMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.6 });
    const panelMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.8, transparent: true, opacity: 0.6 });
    const pilotMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });

    // Groups
    const groupPosts = new THREE.Group();
    const groupBase = new THREE.Group();
    const groupDesk = new THREE.Group();
    const groupMonitor = new THREE.Group();
    const groupSeat = new THREE.Group();
    const groupPanels = new THREE.Group();
    const groupPilot = new THREE.Group();

    scene.add(groupPosts);
    scene.add(groupBase);
    scene.add(groupDesk);
    scene.add(groupMonitor);
    scene.add(groupSeat);
    scene.add(groupPanels);
    scene.add(groupPilot);

    // Dimensions
    const W_INNER = 700;
    const POST_S = 90;
    const POST_H = 900;
    const BASE_S = 300;
    const DEPTH = 750;
    const X_HALF = (W_INNER + POST_S) / 2; // 395
    const Y_F = -DEPTH / 2;                // -375 (Front)
    const Y_R =  DEPTH / 2;                //  375 (Rear)

    // Helper: Add box
    function addBox(group, w, h, d, px, py, pz, mat) {
      const geom = new THREE.BoxGeometry(w, h, d);
      const mesh = new THREE.Mesh(geom, mat);
      mesh.position.set(px, py, pz);
      group.add(mesh);
      return mesh;
    }

    // 1. 4 Heavy Posts and Flanges
    const postPositions = [
      [-X_HALF, Y_F], [X_HALF, Y_F],
      [-X_HALF, Y_R], [X_HALF, Y_R]
    ];

    postPositions.forEach(([px, pz]) => {
      // Post (90x90x900)
      addBox(groupPosts, POST_S, POST_H, POST_S, px, POST_H/2, pz, postMat);

      // Base Plate (300x300x18)
      addBox(groupBase, BASE_S, 18, BASE_S, px, 9, pz, basePlateMat);

      // 4 Triangular Ribs (ハカマ) around each post
      function addRib(rotY, offsetX, offsetZ) {
        const shape = new THREE.Shape();
        shape.moveTo(0, 0);
        shape.lineTo(95, 0);
        shape.lineTo(0, 160);
        shape.closePath();

        const extrudeSettings = { depth: 15, bevelEnabled: false };
        const ribGeom = new THREE.ExtrudeGeometry(shape, extrudeSettings);
        const ribMesh = new THREE.Mesh(ribGeom, ribMat);
        ribMesh.rotation.y = rotY;
        ribMesh.position.set(px + offsetX, 18, pz + offsetZ);
        groupBase.add(ribMesh);
      }
      addRib(0, POST_S/2, -7.5);           // +X
      addRib(Math.PI, -POST_S/2, 7.5);     // -X
      addRib(Math.PI/2, -7.5, POST_S/2);   // +Z
      addRib(-Math.PI/2, 7.5, -POST_S/2);  // -Z
    });

    // 2. Desk & Joystick (Height: 520)
    const H_DESK = 520;
    // Desk table top
    addBox(groupDesk, W_INNER + POST_S, 25, 360, 0, H_DESK, Y_F + 120, deskMat);
    // Desk support beam
    addBox(groupDesk, W_INNER, 45, 45, 0, H_DESK - 35, Y_F, postMat);

    // Flight Stick
    const stickBase = addBox(groupDesk, 90, 25, 90, 180, H_DESK + 25, Y_F + 120, deskMat);
    const stickRod = new THREE.Mesh(new THREE.CylinderGeometry(10, 10, 130, 16), seatAccentMat);
    stickRod.position.set(180, H_DESK + 90, Y_F + 120);
    groupDesk.add(stickRod);

    // 3. Monitor Mount & 27" Display
    const H_MON = 980;
    const Z_MON = Y_F - 80;

    // Upright struts (left & right)
    addBox(groupMonitor, 45, 650, 45, -250, H_DESK + 325, Z_MON + 30, postMat);
    addBox(groupMonitor, 45, 650, 45,  250, H_DESK + 325, Z_MON + 30, postMat);

    // Diagonal Braces (斜めブレース)
    const braceGeom = new THREE.BoxGeometry(30, 30, 320);
    const bL = new THREE.Mesh(braceGeom, postMat);
    bL.position.set(-250, 720, Y_F - 40);
    bL.rotation.x = 0.5;
    groupMonitor.add(bL);

    const bR = new THREE.Mesh(braceGeom, postMat);
    bR.position.set(250, 720, Y_F - 40);
    bR.rotation.x = 0.5;
    groupMonitor.add(bR);

    // Monitor Crossbar
    addBox(groupMonitor, 600, 120, 25, 0, H_MON, Z_MON + 15, postMat);

    // 27-inch Display (620 x 370 mm)
    const monBody = addBox(groupMonitor, 620, 370, 35, 0, H_MON, Z_MON, monitorFrameMat);
    monBody.rotation.x = -0.08;
    const monScreen = addBox(groupMonitor, 590, 340, 2, 0, H_MON, Z_MON - 19, screenMat);
    monScreen.rotation.x = -0.08;

    // 4. Cockpit Seat (Height: 400)
    const H_SEAT = 400;
    const Z_SEAT = Y_R - 150;
    // Seat base beam
    addBox(groupSeat, W_INNER, 60, 60, 0, H_SEAT - 40, Y_R, postMat);
    // Cushion
    addBox(groupSeat, 500, 60, 450, 0, H_SEAT, Z_SEAT, seatMat);
    // Backrest
    const seatBack = addBox(groupSeat, 480, 520, 50, 0, H_SEAT + 250, Z_SEAT + 200, seatMat);
    seatBack.rotation.x = -0.22;
    // Headrest
    const seatHead = addBox(groupSeat, 260, 150, 60, 0, H_SEAT + 540, Z_SEAT + 250, seatAccentMat);
    seatHead.rotation.x = -0.15;

    // 5. Side Rails & Cardboard Panels
    addBox(groupPanels, POST_S, 45, DEPTH - POST_S, -X_HALF, H_DESK, 0, postMat);
    addBox(groupPanels, POST_S, 45, DEPTH - POST_S,  X_HALF, H_DESK, 0, postMat);
    addBox(groupPanels, POST_S, 45, DEPTH - POST_S, -X_HALF, POST_H - 22, 0, postMat);
    addBox(groupPanels, POST_S, 45, DEPTH - POST_S,  X_HALF, POST_H - 22, 0, postMat);

    // Side outer cardboard walls
    addBox(groupPanels, 6, POST_H, DEPTH + POST_S, -X_HALF - POST_S/2 - 3, POST_H/2, 0, panelMat);
    addBox(groupPanels, 6, POST_H, DEPTH + POST_S,  X_HALF + POST_S/2 + 3, POST_H/2, 0, panelMat);

    // 6. Pilot Silhouette
    const pHead = new THREE.Mesh(new THREE.SphereGeometry(105, 16, 16), pilotMat);
    pHead.position.set(0, H_SEAT + 550, Z_SEAT + 180);
    groupPilot.add(pHead);

    const pTorso = new THREE.Mesh(new THREE.CylinderGeometry(130, 110, 420, 8), pilotMat);
    pTorso.position.set(0, H_SEAT + 280, Z_SEAT + 120);
    pTorso.rotation.x = -0.22;
    groupPilot.add(pTorso);

    const pThighs = new THREE.Mesh(new THREE.BoxGeometry(260, 90, 360), pilotMat);
    pThighs.position.set(0, H_SEAT + 40, Z_SEAT - 60);
    groupPilot.add(pThighs);

    const pShins = new THREE.Mesh(new THREE.BoxGeometry(260, 340, 90), pilotMat);
    pShins.position.set(0, H_SEAT - 150, Z_SEAT - 220);
    pShins.rotation.x = 0.4;
    groupPilot.add(pShins);

    // ----------------------------------------------------
    // Interactivity
    // ----------------------------------------------------
    function updateVisibility() {
      groupPosts.visible = document.getElementById('toggle-posts').checked;
      groupBase.visible = document.getElementById('toggle-base').checked;
      groupDesk.visible = document.getElementById('toggle-desk').checked;
      groupMonitor.visible = document.getElementById('toggle-monitor').checked;
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
        camera.position.set(0, H_SEAT + 550, Z_SEAT + 180); // Eye point
        camera.lookAt(0, H_MON, Z_MON);                    // Looking at 27" monitor
      } else {
        isPilotCam = false;
        controls.enabled = true;
        camera.position.set(1600, 1400, 1800);
        controls.target.set(0, 500, 0);
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
    f.write(viewer_html)

print("cockpit_viewer.html updated for V3 simulator cockpit.")
