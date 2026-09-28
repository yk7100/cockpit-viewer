import math
import os
import json
import build123d as bd

# ========================================================
# 操縦席 (Cockpit) 最新確定版:
# 「木の枠は縦の4本だけ ＋ 人が入る十分なスペース ＋ 開閉扉」
# ========================================================
# ユーザー指示:
# 1. 木の枠は縦になってる4本だけ (90mm角柱 x 4本、余計な木枠梁は一切なし)
# 2. 人が入る十分なスペース (奥行きを1200mmに拡大、乗降しやすい空間)
# 3. 開閉扉 (側面に人が乗り降りできるドアを装備)
# 4. 手書きノートの数式 (柱太さ90mm, 足元30cm角ベース, 三角リブ)
# 5. 操作コンソール (ハンドル・スイッチ盤・メーター)
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------------
# 主要寸法 (mm)
# --------------------------------------------------------
POST_T = 90.0           # 柱の太さ (90mm角材)
POST_H = 950.0          # 柱の高さ (950mm)
BASE_SIZE = 300.0       # 足元ベース板 (300mm角)
BASE_THICK = 18.0       # ベース板厚 (18mm)

W_INNER = 750.0         # 内寸横幅 (人がゆったり座れる 750mm)
DEPTH = 1200.0          # 前後柱芯間隔 (ゆったり人が入れる 1200mm)

# 柱の中心座標
X_L = -(W_INNER + POST_T) / 2   # -420mm (左柱)
X_R =  (W_INNER + POST_T) / 2   #  420mm (右柱)
Y_F = -DEPTH / 2                # -600mm (前柱)
Y_R =  DEPTH / 2                #  600mm (後柱)

parts_posts_only = []   # 木の枠（縦の4本柱＋ベース＋リブ）
parts_door = []         # 開閉扉
parts_console = []      # 操作コンソール
parts_seat = []         # 座席・ペダル
parts_walls = []        # 外壁パネル

print("1. 木の枠（縦の4本角柱 ＋ 足元ベース板 ＋ 三角補強リブ）をモデリング中...")

posts = [
    ("前左柱", X_L, Y_F),
    ("前右柱", X_R, Y_F),
    ("後左柱", X_L, Y_R),
    ("後右柱", X_R, Y_R)
]

for name, px, py in posts:
    # 縦の角柱本体 (90x90x950mm) - 木の枠はこれだけ！
    col = bd.Location((px, py, POST_H / 2)) * bd.Box(POST_T, POST_T, POST_H)
    parts_posts_only.append(col)

    # 足元ベース板 (300x300x18mm)
    base_plate = bd.Location((px, py, BASE_THICK / 2)) * bd.Box(BASE_SIZE, BASE_SIZE, BASE_THICK)
    parts_posts_only.append(base_plate)

    # 足元直角三角リブ (底辺90mm, 高さ150mm, 厚み15mm: ハカマ補強)
    rib_w, rib_h, rib_t = 90.0, 150.0, 15.0

    # +X 方向
    with bd.BuildPart() as rib_xp:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px + POST_T/2, BASE_THICK), (px + POST_T/2 + rib_w, BASE_THICK))
                bd.Line((px + POST_T/2 + rib_w, BASE_THICK), (px + POST_T/2, BASE_THICK + rib_h))
                bd.Line((px + POST_T/2, BASE_THICK + rib_h), (px + POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_posts_only.append(rib_xp.part)

    # -X 方向
    with bd.BuildPart() as rib_xm:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px - POST_T/2, BASE_THICK), (px - POST_T/2 - rib_w, BASE_THICK))
                bd.Line((px - POST_T/2 - rib_w, BASE_THICK), (px - POST_T/2, BASE_THICK + rib_h))
                bd.Line((px - POST_T/2, BASE_THICK + rib_h), (px - POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_posts_only.append(rib_xm.part)

    # +Y 方向
    with bd.BuildPart() as rib_yp:
        with bd.BuildSketch(bd.Plane.YZ.offset(px)):
            with bd.BuildLine():
                bd.Line((py + POST_T/2, BASE_THICK), (py + POST_T/2 + rib_w, BASE_THICK))
                bd.Line((py + POST_T/2 + rib_w, BASE_THICK), (py + POST_T/2, BASE_THICK + rib_h))
                bd.Line((py + POST_T/2, BASE_THICK + rib_h), (py + POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_posts_only.append(rib_yp.part)

    # -Y 方向
    with bd.BuildPart() as rib_ym:
        with bd.BuildSketch(bd.Plane.YZ.offset(px)):
            with bd.BuildLine():
                bd.Line((py - POST_T/2, BASE_THICK), (py - POST_T/2 - rib_w, BASE_THICK))
                bd.Line((py - POST_T/2 - rib_w, BASE_THICK), (py - POST_T/2, BASE_THICK + rib_h))
                bd.Line((py - POST_T/2, BASE_THICK + rib_h), (py - POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_posts_only.append(rib_ym.part)

print("2. 開閉扉（ドア）をモデリング中...")
# 左側面に人が乗り降りできるドアを設置 (前柱と後柱の間: スパン1200mm中、ドア幅750mm, 高さ750mm)
# ヒンジ位置: 後柱側 (Y_R - POST_T/2)
DOOR_W = 750.0
DOOR_H = 750.0
DOOR_T = 15.0
DOOR_Z = 120.0 + DOOR_H / 2 # 地面から120mm浮かせて開閉しやすく

# ドアパネル本体
door_panel = bd.Location((X_L, 0.0, DOOR_Z)) * bd.Box(DOOR_T, DOOR_W, DOOR_H)
parts_door.append(door_panel)

# ドア取っ手 (ハンドル)
handle_rod = bd.Location((X_L - 30.0, -DOOR_W/2 + 80.0, DOOR_Z)) * bd.Box(20.0, 30.0, 160.0)
parts_door.append(handle_rod)

# ドアヒンジ金具 (2箇所)
hinge_top = bd.Location((X_L, DOOR_W/2 - 40.0, DOOR_Z + DOOR_H/2 - 60.0)) * bd.Cylinder(radius=10, height=50)
hinge_bot = bd.Location((X_L, DOOR_W/2 - 40.0, DOOR_Z - DOOR_H/2 + 60.0)) * bd.Cylinder(radius=10, height=50)
parts_door.extend([hinge_top, hinge_bot])

print("3. 操作コンソール（ハンドル・計器盤）をモデリング中...")
# 前柱の間にすっきりと収まる操作盤 (幅740mm, 奥行340mm, 高さ140mm, 傾斜25度)
CON_Y = Y_F + 160.0
CON_Z = 600.0
console_box = bd.Location((0, CON_Y, CON_Z), (-25, 0, 0)) * bd.Box(W_INNER - 10.0, 320.0, 140.0)
parts_console.append(console_box)

# 操縦ハンドル (フライトヨーク)
yoke_shaft = bd.Location((0, CON_Y - 45.0, CON_Z + 35.0), (-25, 0, 0)) * bd.Cylinder(radius=15, height=130)
yoke_center = bd.Location((0, CON_Y - 105.0, CON_Z + 65.0)) * bd.Box(150.0, 24.0, 28.0)
yoke_grip_l = bd.Location((-80.0, CON_Y - 115.0, CON_Z + 95.0)) * bd.Box(24.0, 24.0, 110.0)
yoke_grip_r = bd.Location(( 80.0, CON_Y - 115.0, CON_Z + 95.0)) * bd.Box(24.0, 24.0, 110.0)
parts_console.extend([yoke_shaft, yoke_center, yoke_grip_l, yoke_grip_r])

# 計器盤 (アナログメーター & スイッチプレート)
meter_l = bd.Location((-190.0, CON_Y + 40.0, CON_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=36, height=15)
meter_r = bd.Location(( 190.0, CON_Y + 40.0, CON_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=36, height=15)
switch_plate = bd.Location((0, CON_Y + 60.0, CON_Z + 80.0), (-25, 0, 0)) * bd.Box(180.0, 85.0, 10.0)
parts_console.extend([meter_l, meter_r, switch_plate])

# スロットルレバー
throt_base = bd.Location((-270.0, Y_F + 250.0, 510.0)) * bd.Box(60.0, 100.0, 25.0)
throt_lever = bd.Location((-270.0, Y_F + 250.0, 565.0), (20, 0, 0)) * bd.Box(20.0, 35.0, 90.0)
parts_console.extend([throt_base, throt_lever])

print("4. パイロットシート & ラダーペダルをモデリング中...")
# 人がゆったり座れるよう、後柱寄りにシートを配置 (足元スペース約700mm)
SEAT_Y = Y_R - 220.0
seat_base = bd.Location((0, SEAT_Y, 360.0)) * bd.Box(520.0, 460.0, 50.0)
seat_back = bd.Location((0, SEAT_Y + 220.0, 640.0), (12, 0, 0)) * bd.Box(500.0, 45.0, 520.0)
seat_head = bd.Location((0, SEAT_Y + 265.0, 940.0), (10, 0, 0)) * bd.Box(260.0, 55.0, 150.0)
parts_seat.extend([seat_base, seat_back, seat_head])

# ラダーペダル (フットレスト: 前柱寄り足元)
pedal_l = bd.Location((-140.0, Y_F + 100.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
pedal_r = bd.Location(( 140.0, Y_F + 100.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
parts_seat.extend([pedal_l, pedal_r])

print("5. 外壁パネル（右側面・背面・前下面）をモデリング中...")
# 右側面パネル (固定壁: 厚さ12mm 合板/段ボール)
wall_r = bd.Location((X_R + POST_T/2 + 6.0, 0, POST_H / 2)) * bd.Box(12.0, DEPTH + POST_T, POST_H)
# 背面パネル
wall_rear = bd.Location((0, Y_R + POST_T/2 + 6.0, POST_H / 2)) * bd.Box(W_INNER + POST_T*2, 12.0, POST_H)
# 前面下部パネル (コンソール下)
wall_front = bd.Location((0, Y_F - POST_T/2 - 6.0, 250.0)) * bd.Box(W_INNER + POST_T*2, 12.0, 500.0)
# 左側面固定部 (ドアの前後の小壁)
door_front_wall = bd.Location((X_L, Y_F + (DEPTH - DOOR_W)/4 + POST_T/2, POST_H / 2)) * bd.Box(12.0, (DEPTH - DOOR_W)/2, POST_H)
door_rear_wall = bd.Location((X_L, Y_R - (DEPTH - DOOR_W)/4 - POST_T/2, POST_H / 2)) * bd.Box(12.0, (DEPTH - DOOR_W)/2, POST_H)

parts_walls.extend([wall_r, wall_rear, wall_front, door_front_wall, door_rear_wall])

# --------------------------------------------------------
# CADデータのエクスポート
# --------------------------------------------------------
print("CADファイル（STEP / STL）をエクスポート中...")

# 木の枠単体 (縦の4本柱 + ベース板 + 三角リブ)
frame_compound = bd.Compound(parts_posts_only)
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))

# 全体アセンブリ (縦4本柱 + 扉 + コンソール + シート + パネル)
all_components = parts_posts_only + parts_door + parts_console + parts_seat + parts_walls
full_assembly = bd.Compound(all_components)
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))

print("STEP / STL エクスポート完了！")

summary = {
    "posts_qty": 4,
    "post_section_mm": "90x90",
    "post_height_mm": POST_H,
    "inner_width_mm": W_INNER,
    "depth_span_mm": DEPTH,
    "door_width_mm": DOOR_W,
    "door_height_mm": DOOR_H,
    "base_plate_size_mm": f"{BASE_SIZE}x{BASE_SIZE}x{BASE_THICK}",
    "note": "木の枠は縦の4本角柱のみ。人がゆったり入れる奥行き1200mmと乗降用開閉扉を装備。"
}

with open(os.path.join(OUT_DIR, "cockpit_v4_spec.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("スペックJSON保存完了。")
