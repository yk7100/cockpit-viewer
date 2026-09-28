import json
import os

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"

with open(os.path.join(OUT_DIR, "cut_list.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# ------------------------------------------
# Generate Markdown Cut List
# ------------------------------------------
md_lines = [
    "# 操縦席 (Cockpit) 木取り表・工作ガイド\n",
    "## 1. 全体仕様",
    f"- **外形寸法**: 幅 {data['dimensions_mm']['width']} mm × 奥行 {data['dimensions_mm']['length']} mm × 高さ {data['dimensions_mm']['height']} mm",
    f"- **使用木材**: 角材（{data['dimensions_mm']['timber_cross_section']} mm）",
    f"- **角材総必要長**: **{data['total_wood_length_m']} m**",
    f"- **推奨仕入れ本数 (4m角材の場合)**: **{data['stock_4m_required']} 本**（※板書「角材×7」と完全一致）",
    f"- **推奨仕入れ本数 (3m角材の場合)**: **{data['stock_3m_required']} 本**\n",
    "## 2. 部材カットリスト (部品別)",
    "| 部品名 | 長さ (mm) | 数量 | 備考 |",
    "| :--- | :--- | :--- | :--- |"
]

for item in sorted(data["cut_list"], key=lambda x: x["length_mm"], reverse=True):
    md_lines.append(f"| {item['name']} | {item['length_mm']} | {item['qty']} | 角材 30×30 |")

md_lines.append("\n## 3. 木取り計画 (4m材 × 7本 からの切り出し計画)")
md_lines.append("> 鋸（ノコギリ）の刃幅（カーフ 3mm）を考慮した最適化切り出しプランです。\n")

for stock in data["cutting_plan_4m"]:
    cuts_str = " + ".join(stock["cuts"])
    md_lines.append(f"- **材 #{stock['stock_id']}** (使用: {stock['used_mm']} mm / 端材余り: {stock['remaining_mm']} mm)")
    md_lines.append(f"  - 内訳: {cuts_str}")

md_lines.append("\n## 4. その他必要資材")
md_lines.append("- **アクリル板**: 2枚（ガルウィングドア用：各 約 750mm × 800mm × 厚み 2〜3mm）")
md_lines.append("- **透明ラップ / 梱包用ストレッチフィルム**: 1〜2本（前方傾斜窓用：幅900mm × 傾斜長約895mm）")
md_lines.append("- **段ボール**: 大判複数枚（外壁・ノーズ部・座面用）")
md_lines.append("- **蝶番（ヒンジ）**: 4個（ガルウィングドア吊り下げ用、左右各2個）")
md_lines.append("- **木ネジ（スリムスレッド / コーススレッド 50〜65mm）**: 1箱（約100〜150本）")
md_lines.append("- **L字アングル金具**: 10〜16個（角部分の補強用）")
md_lines.append("- **遮光カーテン / 暗幕**: 1枚（後部開口部 幅600mm × 高さ1300mm 用）")

with open(os.path.join(OUT_DIR, "CUT_LIST.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print("CUT_LIST.md generated.")

# ------------------------------------------
# Generate Interactive 3D Viewer (Three.js Standalone HTML)
# ------------------------------------------
html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>操縦席 コクピット 3Dビューア (板書再現モデル)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      background: #121820;
      color: #e0e6ed;
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
      width: 340px;
      background: rgba(20, 26, 36, 0.95);
      border-left: 1px solid #2d3748;
      padding: 20px;
      overflow-y: auto;
      box-shadow: -4px 0 20px rgba(0,0,0,0.5);
      backdrop-filter: blur(10px);
      z-index: 10;
    }
    h1 {
      font-size: 18px;
      margin-bottom: 8px;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge {
      font-size: 11px;
      background: #0284c7;
      color: #fff;
      padding: 2px 6px;
      border-radius: 4px;
    }
    p.desc {
      font-size: 12px;
      color: #94a3b8;
      margin-bottom: 16px;
      line-height: 1.4;
    }
    .section-title {
      font-size: 13px;
      font-weight: bold;
      color: #cbd5e1;
      text-transform: uppercase;
      letter-spacing: 0.5px;
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
      font-size: 13px;
      color: #cbd5e1;
      margin-bottom: 6px;
      cursor: pointer;
    }
    input[type="range"] {
      width: 100%;
      accent-color: #38bdf8;
    }
    .btn-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 10px;
    }
    button {
      background: #1e293b;
      color: #e2e8f0;
      border: 1px solid #475569;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s;
    }
    button:hover {
      background: #334155;
      border-color: #64748b;
    }
    button.active {
      background: #0284c7;
      border-color: #38bdf8;
      color: #fff;
    }
    .spec-table {
      width: 100%;
      font-size: 12px;
      border-collapse: collapse;
      margin-top: 8px;
    }
    .spec-table td {
      padding: 6px 4px;
      border-bottom: 1px solid #1e293b;
    }
    .spec-table td:first-child {
      color: #94a3b8;
      width: 45%;
    }
    .spec-table td:last-child {
      color: #f1f5f9;
      font-weight: 500;
    }
    #legend {
      position: absolute;
      bottom: 20px;
      left: 20px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid #334155;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 12px;
      backdrop-filter: blur(8px);
      pointer-events: none;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
    }
    .legend-color {
      width: 14px;
      height: 14px;
      border-radius: 3px;
    }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
  <div id="canvas-container">
    <div id="legend">
      <div style="font-weight: bold; margin-bottom: 6px; color:#38bdf8;">素材凡例 (板書対応)</div>
      <div class="legend-item"><div class="legend-color" style="background: #c68a4c;"></div> 枠：角材 30×30mm</div>
      <div class="legend-item"><div class="legend-color" style="background: #966b44;"></div> 壁：段ボール (ダンボ)</div>
      <div class="legend-item"><div class="legend-color" style="background: #facc15; opacity: 0.8;"></div> 窓：ラップ (黄色斜線部分)</div>
      <div class="legend-item"><div class="legend-color" style="background: #38bdf8; opacity: 0.7;"></div> ドア：アクリル板 (ガルウィング)</div>
      <div class="legend-item"><div class="legend-color" style="background: #64748b;"></div> 後部：カーテン (外部効果用)</div>
    </div>
  </div>

  <div id="sidebar">
    <h1>操縦席 CAD プレビュー <span class="badge">板書忠実設計</span></h1>
    <p class="desc">文化祭等の体験型アトラクション向け操縦席（コクピット）。木枠フレーム、段ボール壁、ラップ視野窓、ガルウィング開閉アクリルドアを再現。</p>

    <div class="section-title">ギミック・開閉操作</div>
    <div class="control-group">
      <label for="door-angle">ガルウィングドア開閉: <span id="door-angle-val">0° (閉)</span></label>
      <input type="range" id="door-angle" min="0" max="85" value="0">
    </div>
    <div class="btn-row">
      <button onclick="setDoor(0)">ドア全閉</button>
      <button onclick="setDoor(75)">ドア跳ね上げ (開)</button>
    </div>

    <div class="section-title">表示パーツ切り替え</div>
    <div class="control-group">
      <label><input type="checkbox" id="toggle-frame" checked onchange="updateVisibility()"> 木製骨組み (角材)</label>
      <label><input type="checkbox" id="toggle-cardboard" checked onchange="updateVisibility()"> 段ボール壁 (ダンボ)</label>
      <label><input type="checkbox" id="toggle-wrap" checked onchange="updateVisibility()"> ラップ窓 (前方傾斜窓)</label>
      <label><input type="checkbox" id="toggle-door" checked onchange="updateVisibility()"> アクリル板ドア (ガルウィング)</label>
      <label><input type="checkbox" id="toggle-seat" checked onchange="updateVisibility()"> シート & 操縦桿</label>
      <label><input type="checkbox" id="toggle-pilot" checked onchange="updateVisibility()"> 搭乗者シルエット (165cm)</label>
    </div>

    <div class="section-title">外壁透過度</div>
    <div class="control-group">
      <label for="cardboard-opacity">段ボール壁の透明度: <span id="opacity-val">100%</span></label>
      <input type="range" id="cardboard-opacity" min="0" max="100" value="100" oninput="updateOpacity(this.value)">
    </div>

    <div class="section-title">設計寸法 & 仕様</div>
    <table class="spec-table">
      <tr><td>外寸 (幅×奥×高)</td><td>900 × 1500 × 1300 mm</td></tr>
      <tr><td>骨組み角材</td><td>30 × 30 mm</td></tr>
      <tr><td>角材必要総延長</td><td>約 23.3 m</td></tr>
      <tr><td>定尺木材 (4m)</td><td><strong>7本</strong> (板書「角材×7」)</td></tr>
      <tr><td>アクリル板</td><td>2枚 (ガルウィングドア用)</td></tr>
      <tr><td>正面窓</td><td>透明ラップ 900×895 mm</td></tr>
      <tr><td>後部開口</td><td>カーテン (外部効果スタッフ用)</td></tr>
    </table>

    <div class="section-title">CADファイル保存先</div>
    <p style="font-size: 11px; color:#94a3b8; word-break: break-all; line-height: 1.5;">
      /Users/y.jin/.gemini/antigravity/scratch/cockpit_cad/<br>
      • <code>cockpit_assembly_full.step</code><br>
      • <code>cockpit_assembly_full.stl</code><br>
      • <code>cockpit_frame.step</code> / <code>.stl</code><br>
      • <code>cockpit_panels.step</code> / <code>.stl</code><br>
      • <code>CUT_LIST.md</code> (木取り図面)
    </p>
  </div>

  <script>
    // ----------------------------------------------------
    // Three.js Scene Setup
    // ----------------------------------------------------
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x121820);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 10, 10000);
    camera.position.set(2200, 1800, 2400);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 650, 0);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.65);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight1.position.set(1500, 3000, 2000);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x90b0e0, 0.4);
    dirLight2.position.set(-1500, -500, -1000);
    scene.add(dirLight2);

    // Ground Grid
    const grid = new THREE.GridHelper(3000, 30, 0x334155, 0x1e293b);
    grid.position.y = 0;
    scene.add(grid);

    // ----------------------------------------------------
    // Materials
    // ----------------------------------------------------
    const woodMat = new THREE.MeshStandardMaterial({ color: 0xc68a4c, roughness: 0.6, metalness: 0.1 });
    const cardboardMat = new THREE.MeshStandardMaterial({ color: 0xa57548, roughness: 0.9, transparent: true, opacity: 1.0 });
    const wrapMat = new THREE.MeshPhysicalMaterial({ color: 0xfacc15, transparent: true, opacity: 0.35, roughness: 0.1, transmission: 0.8, thickness: 1.0 });
    const acrylicMat = new THREE.MeshPhysicalMaterial({ color: 0x67e8f9, transparent: true, opacity: 0.45, roughness: 0.1, transmission: 0.85, thickness: 3.0 });
    const curtainMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.9, side: THREE.DoubleSide });
    const seatMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.5 });
    const pilotMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });

    // Groups
    const groupFrame = new THREE.Group();
    const groupCardboard = new THREE.Group();
    const groupWrap = new THREE.Group();
    const groupDoors = new THREE.Group();
    const groupSeat = new THREE.Group();
    const groupPilot = new THREE.Group();

    scene.add(groupFrame);
    scene.add(groupCardboard);
    scene.add(groupWrap);
    scene.add(groupDoors);
    scene.add(groupSeat);
    scene.add(groupPilot);

    // Coordinate shift: Center cockpit at origin
    // Local coords: X: 0..900, Y: 0..1500 (in script,前後), Z: 0..1300 (in script,上下)
    // Three.js: X: -450..450, Y: 0..1300 (height), Z: -750..750 (depth, -Z is front, +Z is rear)
    function toWorld(lx, ly_depth, lz_height) {
      return new THREE.Vector3(lx - 450, lz_height, ly_depth - 750);
    }

    function addBox(group, w, h, d, px, py, pz, mat, rotX=0) {
      const geom = new THREE.BoxGeometry(w, h, d);
      const mesh = new THREE.Mesh(geom, mat);
      mesh.position.set(px, py, pz);
      if (rotX !== 0) mesh.rotation.x = rotX;
      group.add(mesh);
      return mesh;
    }

    // 1. Frame Beams (角材 30x30mm)
    const T = 30;
    // Bottom Skids
    addBox(groupFrame, T, T, 1500, -450+T/2, T/2, 0, woodMat);
    addBox(groupFrame, T, T, 1500, 450-T/2, T/2, 0, woodMat);
    addBox(groupFrame, 900-2*T, T, T, 0, T/2, -750+T/2, woodMat);
    addBox(groupFrame, 900-2*T, T, T, 0, T/2, 750-750, woodMat); // canopy mid
    addBox(groupFrame, 900-2*T, T, T, 0, T/2, 1500-750-T/2, woodMat);

    // Nose Uprights (Z=0..500, Y_depth=0)
    addBox(groupFrame, T, 500-2*T, T, -450+T/2, 250, -750+T/2, woodMat);
    addBox(groupFrame, T, 500-2*T, T, 450-T/2, 250, -750+T/2, woodMat);
    addBox(groupFrame, 900-2*T, T, T, 0, 500-T/2, -750+T/2, woodMat);

    // Nose horizontal side rails (Y_depth: 30..350)
    addBox(groupFrame, T, T, 350-2*T, -450+T/2, 500-T/2, -750+175, woodMat);
    addBox(groupFrame, T, T, 350-2*T, 450-T/2, 500-T/2, -750+175, woodMat);

    // Nose rear posts (Y_depth=350, Z=0..500)
    addBox(groupFrame, T, 500-2*T, T, -450+T/2, 250, -750+350-T/2, woodMat);
    addBox(groupFrame, T, 500-2*T, T, 450-T/2, 250, -750+350-T/2, woodMat);
    addBox(groupFrame, 900-2*T, T, T, 0, 500-T/2, -750+350-T/2, woodMat);

    // Main canopy rear pillars (Y_depth=750, Z=0..1300)
    addBox(groupFrame, T, 1300-2*T, T, -450+T/2, 650, 0, woodMat);
    addBox(groupFrame, T, 1300-2*T, T, 450-T/2, 650, 0, woodMat);
    addBox(groupFrame, 900-2*T, T, T, 0, 1300-T/2, 0, woodMat);

    // Rear pillars (Y_depth=1500, Z=0..1300)
    addBox(groupFrame, T, 1300-2*T, T, -450+T/2, 650, 750-T/2, woodMat);
    addBox(groupFrame, T, 1300-2*T, T, 450-T/2, 650, 750-T/2, woodMat);
    addBox(groupFrame, 900-2*T, T, T, 0, 1300-T/2, 750-T/2, woodMat);

    // Roof side rails (Y_depth: 750..1500, Z=1300)
    addBox(groupFrame, T, T, 750-T, -450+T/2, 1300-T/2, 375, woodMat);
    addBox(groupFrame, T, T, 750-T, 450-T/2, 1300-T/2, 375, woodMat);

    // Slanted Canopy Rafters (Y: 350->750, Z: 500->1300)
    const dZ = 800, dY = 400;
    const slantLen = Math.sqrt(dZ*dZ + dY*dY);
    const slantAngle = Math.atan2(dY, dZ); // rotation around X

    function addSlant(x) {
      const geom = new THREE.BoxGeometry(T, slantLen, T);
      const m = new THREE.Mesh(geom, woodMat);
      m.position.set(x, 900, -750 + 550);
      m.rotation.x = slantAngle;
      groupFrame.add(m);
    }
    addSlant(-450+T/2);
    addSlant(450-T/2);
    addSlant(0);

    // 2. Cardboard Enclosure (壁はダンボ)
    // Nose front
    addBox(groupCardboard, 900, 500, 6, 0, 250, -750, cardboardMat);
    // Nose top deck
    addBox(groupCardboard, 900, 6, 350, 0, 500, -750+175, cardboardMat);
    // Side bottom walls (left & right)
    addBox(groupCardboard, 6, 500, 1500, -450-3, 250, 0, cardboardMat);
    addBox(groupCardboard, 6, 500, 1500, 450+3, 250, 0, cardboardMat);
    // Rear walls (leaving center 600mm for curtain)
    addBox(groupCardboard, 150, 1300, 6, -375, 650, 750+3, cardboardMat);
    addBox(groupCardboard, 150, 1300, 6, 375, 650, 750+3, cardboardMat);
    // Rear curtain (うしろはカーテンかなんか)
    addBox(groupCardboard, 600, 1250, 2, 0, 625, 750+2, curtainMat);

    // 3. Front Clear Wrap Canopy (黄色斜線＝ラップで視野確保)
    const wrapGeom = new THREE.BoxGeometry(900, slantLen, 2);
    const wrapMesh = new THREE.Mesh(wrapGeom, wrapMat);
    wrapMesh.position.set(0, 900, -750 + 550);
    wrapMesh.rotation.x = slantAngle;
    groupWrap.add(wrapMesh);

    // 4. Gullwing Doors (アクリル板ドアをガルウィング形式で開閉)
    // Hinged at roof side rail: Z=1300, Y_depth: 750..1500, X= -450 or +450
    const doorPivotL = new THREE.Group();
    doorPivotL.position.set(-450, 1300, 375); // hinge axis
    groupDoors.add(doorPivotL);

    const doorPanelL = new THREE.Mesh(new THREE.BoxGeometry(4, 800, 750), acrylicMat);
    doorPanelL.position.set(0, -400, 0); // hang down 800mm
    doorPivotL.add(doorPanelL);

    // Add wooden door edge frame
    const doorFrameL = new THREE.LineSegments(
      new THREE.EdgesGeometry(new THREE.BoxGeometry(10, 800, 750)),
      new THREE.LineBasicMaterial({ color: 0x38bdf8, linewidth: 2 })
    );
    doorFrameL.position.set(0, -400, 0);
    doorPivotL.add(doorFrameL);

    const doorPivotR = new THREE.Group();
    doorPivotR.position.set(450, 1300, 375);
    groupDoors.add(doorPivotR);

    const doorPanelR = new THREE.Mesh(new THREE.BoxGeometry(4, 800, 750), acrylicMat);
    doorPanelR.position.set(0, -400, 0);
    doorPivotR.add(doorPanelR);

    const doorFrameR = new THREE.LineSegments(
      new THREE.EdgesGeometry(new THREE.BoxGeometry(10, 800, 750)),
      new THREE.LineBasicMaterial({ color: 0x38bdf8, linewidth: 2 })
    );
    doorFrameR.position.set(0, -400, 0);
    doorPivotR.add(doorFrameR);

    // 5. Seat & Flight Controls
    addBox(groupSeat, 450, 350, 450, 0, 175, 850-750+225, seatMat);
    const seatBack = addBox(groupSeat, 450, 500, 50, 0, 600, 850-750+430, seatMat);
    seatBack.rotation.x = -0.15;

    // Flight Joystick
    const stickBase = new THREE.Mesh(new THREE.CylinderGeometry(40, 50, 20, 16), seatMat);
    stickBase.position.set(0, 560, 600-750);
    groupSeat.add(stickBase);
    const stickRod = new THREE.Mesh(new THREE.CylinderGeometry(12, 12, 180, 16), seatMat);
    stickRod.position.set(0, 650, 600-750);
    groupSeat.add(stickRod);
    const stickGrip = new THREE.Mesh(new THREE.BoxGeometry(35, 60, 45), new THREE.MeshStandardMaterial({ color: 0xd97706 }));
    stickGrip.position.set(0, 740, 600-750);
    groupSeat.add(stickGrip);

    // 6. Pilot Silhouette (搭乗者ワイヤーフレーム)
    const head = new THREE.Mesh(new THREE.SphereGeometry(110, 16, 16), pilotMat);
    head.position.set(0, 980, 250);
    groupPilot.add(head);

    const torso = new THREE.Mesh(new THREE.CylinderGeometry(140, 120, 450, 8), pilotMat);
    torso.position.set(0, 680, 270);
    torso.rotation.x = -0.15;
    groupPilot.add(torso);

    const thighs = new THREE.Mesh(new THREE.BoxGeometry(260, 100, 380), pilotMat);
    thighs.position.set(0, 420, 80);
    groupPilot.add(thighs);

    const shins = new THREE.Mesh(new THREE.BoxGeometry(260, 360, 90), pilotMat);
    shins.position.set(0, 220, -130);
    shins.rotation.x = 0.35;
    groupPilot.add(shins);

    // ----------------------------------------------------
    // UI Interactions
    // ----------------------------------------------------
    const doorSlider = document.getElementById('door-angle');
    const doorVal = document.getElementById('door-angle-val');

    doorSlider.addEventListener('input', (e) => {
      setDoor(parseFloat(e.target.value));
    });

    function setDoor(deg) {
      doorSlider.value = deg;
      doorVal.innerText = deg.toFixed(0) + '° ' + (deg > 10 ? '(開)' : '(閉)');
      const rad = THREE.MathUtils.degToRad(deg);
      doorPivotL.rotation.z = rad;   // Left door swings UP outward
      doorPivotR.rotation.z = -rad;  // Right door swings UP outward
    }

    function updateVisibility() {
      groupFrame.visible = document.getElementById('toggle-frame').checked;
      groupCardboard.visible = document.getElementById('toggle-cardboard').checked;
      groupWrap.visible = document.getElementById('toggle-wrap').checked;
      groupDoors.visible = document.getElementById('toggle-door').checked;
      groupSeat.visible = document.getElementById('toggle-seat').checked;
      groupPilot.visible = document.getElementById('toggle-pilot').checked;
    }

    function updateOpacity(val) {
      document.getElementById('opacity-val').innerText = val + '%';
      cardboardMat.opacity = val / 100.0;
    }

    // Resize
    window.addEventListener('resize', () => {
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    });

    // Animation Loop
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }
    animate();
  </script>
</body>
</html>
"""

with open(os.path.join(OUT_DIR, "cockpit_viewer.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("cockpit_viewer.html generated.")
