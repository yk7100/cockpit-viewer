import math
import os
import json
import build123d as bd

# ========================================================
# コクピット新設計: 頑丈な4本角柱ベース・シミュレーター型
# (ユーザー手書きノートの数式・寸法を100%忠実にモデリング)
# ========================================================
# ノートの設計値:
# - 基準高さ h = 900 mm (87.5cm ≒ 90cm)
# - 横幅 = (4/5) h = 700〜720 mm (カフェ1人席基準)
# - 角柱の太さ = (1/9)h 〜 (1/12)h = 73〜97 mm (90mm角材を採用)
# - 柱の高さ = 約 900 mm (±20cm)
# - 柱の足元ベースプレート = (3/10)h ≒ (1/3)h = 270〜300 mm 角
# - 三角補強リブ: 柱の足元を「少し硬めの素材」で補強
# - 机 (操作卓) & モニターマウント (前方にモニター支持アームと斜めブレース)
# - 4本の柱で囲まれたコクピット着座スペース
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

# 基準寸法
H_REF = 900.0           # h = 900mm
W_INNER = 700.0         # (4/5)h = 700mm (内寸横幅)
POST_SIZE = 90.0        # 角柱太さ 90mm ((1/10)h = 90mm)
POST_HEIGHT = 900.0     # 柱高さ 900mm
BASE_SIZE = 300.0       # 足元ベース正方形 (1/3)h = 300mm
DEPTH_INNER = 750.0     # 前後柱間隔 750mm

# 中心座標計算
# 原点(0,0,0)は底面中央
X_HALF = (W_INNER + POST_SIZE) / 2      # 395mm
Y_FRONT = -DEPTH_INNER / 2              # -375mm (前柱Y)
Y_REAR  =  DEPTH_INNER / 2              #  375mm (後柱Y)

parts_posts = []
parts_bases = []
parts_desk = []
parts_monitor = []
parts_seat = []
parts_enclosure = []

print("Modeling 4 Heavy Posts and Base Flanges...")

# 1. 4本の角柱 (90x90x900mm)
post_coords = [
    ("前左柱", -X_HALF, Y_FRONT),
    ("前右柱",  X_HALF, Y_FRONT),
    ("後左柱", -X_HALF, Y_REAR),
    ("後右柱",  X_HALF, Y_REAR)
]

for name, px, py in post_coords:
    # 柱本体
    p = bd.Location((px, py, POST_HEIGHT/2)) * bd.Box(POST_SIZE, POST_SIZE, POST_HEIGHT)
    parts_posts.append(p)

    # 足元の正方形ベースプレート (300x300x18mm)
    b_plate = bd.Location((px, py, 9.0)) * bd.Box(BASE_SIZE, BASE_SIZE, 18.0)
    parts_bases.append(b_plate)

    # 足元三角リブ (ハカマ補強: ノート図の「少し硬めの素材」)
    # 4方向に直角三角リブを配置 (底辺90mm, 高さ150mm, 厚み15mm)
    rib_w = 90.0
    rib_h = 150.0
    rib_t = 15.0
    # X+ 方向
    rx_plus = bd.Location((px + POST_SIZE/2 + rib_w/2, py, 18.0 + rib_h/2), (-90, 0, 0)) * bd.Wedge(rib_w, rib_h, rib_t, 0, rib_h, 0, rib_h)
    # 簡易的に直角三角形リブを押し出しで作成
    with bd.BuildPart() as rib_builder:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px + POST_SIZE/2, 18.0), (px + POST_SIZE/2 + rib_w, 18.0))
                bd.Line((px + POST_SIZE/2 + rib_w, 18.0), (px + POST_SIZE/2, 18.0 + rib_h))
                bd.Line((px + POST_SIZE/2, 18.0 + rib_h), (px + POST_SIZE/2, 18.0))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_bases.append(rib_builder.part)

    with bd.BuildPart() as rib_builder_m:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px - POST_SIZE/2, 18.0), (px - POST_SIZE/2 - rib_w, 18.0))
                bd.Line((px - POST_SIZE/2 - rib_w, 18.0), (px - POST_SIZE/2, 18.0 + rib_h))
                bd.Line((px - POST_SIZE/2, 18.0 + rib_h), (px - POST_SIZE/2, 18.0))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_bases.append(rib_builder_m.part)

# 2. 机 (操作卓 / コントロールデスク)
# ノートの「1/2 h」(約450〜550mm) の高さに設置
H_DESK = 520.0
DESK_DEPTH = 350.0
DESK_THICK = 25.0
# 机天板
desk_top = bd.Location((0, Y_FRONT + DESK_DEPTH/2 - 50.0, H_DESK)) * bd.Box(W_INNER + POST_SIZE, DESK_DEPTH, DESK_THICK)
parts_desk.append(desk_top)

# 机を支える横木ビーム (左右前柱間)
desk_beam = bd.Location((0, Y_FRONT, H_DESK - DESK_THICK/2 - 20.0)) * bd.Box(W_INNER, 45.0, 45.0)
parts_desk.append(desk_beam)

# 操縦デバイス (ジョイスティック / キーボード台)
stick_base = bd.Location((180.0, Y_FRONT + 120.0, H_DESK + DESK_THICK/2 + 15.0)) * bd.Box(90, 90, 30)
stick_rod = bd.Location((180.0, Y_FRONT + 120.0, H_DESK + DESK_THICK/2 + 95.0)) * bd.Cylinder(radius=12, height=130)
parts_desk.extend([stick_base, stick_rod])

# 3. モニター支持フレーム & モニター (ノート左上・中央上の図)
# 前柱から斜め前上に伸びる支柱とブレース
H_MONITOR_CENTER = 980.0
Y_MONITOR = Y_FRONT - 80.0

# 左右モニター支柱 (45x45mm角材)
mon_post_l = bd.Location((-250.0, Y_MONITOR + 40.0, (H_DESK + 1150.0)/2)) * bd.Box(45.0, 45.0, 1150.0 - H_DESK)
mon_post_r = bd.Location(( 250.0, Y_MONITOR + 40.0, (H_DESK + 1150.0)/2)) * bd.Box(45.0, 45.0, 1150.0 - H_DESK)
# 斜めブレース (支柱と前柱を結ぶ補強筋交い)
mon_brace_l = bd.Location((-250.0, Y_FRONT - 20.0, 750.0), (25, 0, 0)) * bd.Box(30.0, 30.0, 320.0)
mon_brace_r = bd.Location(( 250.0, Y_FRONT - 20.0, 750.0), (25, 0, 0)) * bd.Box(30.0, 30.0, 320.0)
parts_monitor.extend([mon_post_l, mon_post_r, mon_brace_l, mon_brace_r])

# モニターマウント横板
mon_cross = bd.Location((0, Y_MONITOR + 20.0, H_MONITOR_CENTER)) * bd.Box(600.0, 30.0, 120.0)
parts_monitor.append(mon_cross)

# 液晶ディスプレイ本体 (27インチワイドモニター相当: 620 x 370 x 40 mm)
monitor_display = bd.Location((0, Y_MONITOR, H_MONITOR_CENTER), (-5, 0, 0)) * bd.Box(620.0, 40.0, 370.0)
monitor_screen  = bd.Location((0, Y_MONITOR - 21.0, H_MONITOR_CENTER), (-5, 0, 0)) * bd.Box(590.0, 2.0, 340.0)
parts_monitor.extend([monitor_display, monitor_screen])

# 4. 座席 (コクピットシート)
# 後柱の間に配置、座面高 400mm
H_SEAT = 400.0
W_SEAT = 500.0
L_SEAT = 450.0
Y_SEAT = Y_REAR - 150.0

seat_cushion = bd.Location((0, Y_SEAT, H_SEAT)) * bd.Box(W_SEAT, L_SEAT, 60.0)
seat_back    = bd.Location((0, Y_SEAT + L_SEAT/2 - 20.0, H_SEAT + 250.0), (12, 0, 0)) * bd.Box(W_SEAT, 50.0, 500.0)
seat_head    = bd.Location((0, Y_SEAT + L_SEAT/2 - 5.0, H_SEAT + 540.0), (10, 0, 0)) * bd.Box(260.0, 60.0, 160.0)
# シート支持ビーム (後柱間横木)
seat_beam = bd.Location((0, Y_REAR, H_SEAT - 40.0)) * bd.Box(W_INNER, 60.0, 60.0)
parts_seat.extend([seat_cushion, seat_back, seat_head, seat_beam])

# 5. サイドパネル & 囲いフレーム (ノート中央の囲いライン)
# 左右のサイドガードビーム (前柱と後柱を結ぶ腰高レール: Z=520mm)
side_rail_l = bd.Location((-X_HALF, 0, H_DESK)) * bd.Box(POST_SIZE, DEPTH_INNER - POST_SIZE, 45.0)
side_rail_r = bd.Location(( X_HALF, 0, H_DESK)) * bd.Box(POST_SIZE, DEPTH_INNER - POST_SIZE, 45.0)
# 上部トップサイドビーム (Z=900mm)
top_rail_l = bd.Location((-X_HALF, 0, POST_HEIGHT - 22.5)) * bd.Box(POST_SIZE, DEPTH_INNER - POST_SIZE, 45.0)
top_rail_r = bd.Location(( X_HALF, 0, POST_HEIGHT - 22.5)) * bd.Box(POST_SIZE, DEPTH_INNER - POST_SIZE, 45.0)
# サイド外壁パネル (段ボール/合板)
side_panel_l = bd.Location((-X_HALF - POST_SIZE/2 - 3.0, 0, POST_HEIGHT/2)) * bd.Box(6.0, DEPTH_INNER + POST_SIZE, POST_HEIGHT)
side_panel_r = bd.Location(( X_HALF + POST_SIZE/2 + 3.0, 0, POST_HEIGHT/2)) * bd.Box(6.0, DEPTH_INNER + POST_SIZE, POST_HEIGHT)
parts_enclosure.extend([side_rail_l, side_rail_r, top_rail_l, top_rail_r, side_panel_l, side_panel_r])

# --------------------------------------------------------
# アセンブリの結合 & エクスポート
# --------------------------------------------------------
print("Exporting CAD models...")

frame_components = parts_posts + parts_bases + parts_desk + parts_monitor + [seat_beam, side_rail_l, side_rail_r, top_rail_l, top_rail_r]
frame_compound = bd.Compound(frame_components)

bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_v3_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_v3_frame.stl"))

all_components = frame_components + parts_seat + [side_panel_l, side_panel_r, monitor_display, monitor_screen]
full_assembly = bd.Compound(all_components)

bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_v3_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_v3_full.stl"))

# Also overwrite primary files
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))

print("Export completed successfully!")

# カットリスト情報
summary = {
    "reference_height_h_mm": H_REF,
    "inner_width_mm": W_INNER,
    "outer_width_mm": W_INNER + 2 * POST_SIZE,
    "post_section_mm": f"{POST_SIZE}x{POST_SIZE}",
    "post_qty": 4,
    "post_length_mm": POST_HEIGHT,
    "base_plate_size_mm": f"{BASE_SIZE}x{BASE_SIZE}x18",
    "base_plate_qty": 4,
    "reinforcement_ribs_qty": 8,
    "desk_height_mm": H_DESK,
    "desk_size_mm": f"{W_INNER + POST_SIZE} x {DESK_DEPTH}",
    "monitor_size_approx": "27 inch (620x370 mm)"
}

with open(os.path.join(OUT_DIR, "v3_spec.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("v3_spec.json saved.")
