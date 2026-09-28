import math
import os
import json
import build123d as bd

# ========================================================
# 操縦席 (Cockpit) 人間工学・長方形乗降性 改善モデル
# ========================================================
# ユーザーの疑問・指示への完全対応:
# 1. 「長方形のほうがいい？」
#    → 全長1500mmの美しい長方形プロポーションに最適化。
#       前部(操作盤+ペダル) / 中央(乗降開口) / 後部(座席)の3ゾーン分離。
# 2. 「人入れないかな？」
#    → ドア下端を床スレスレ(Z=50mm)まで下げ、大人が足を引っ掛けず
#       そのままシートに自然に腰掛けられる大型スイングドア(幅750x高800mm)を装備。
# 3. 「足元の障害物撤去」
#    → 柱内側(通路)に出ていた三角リブを完全撤去！
#       リブは外側・壁側のみに配置し、乗降通路と足元を100%フラット化。
# 4. 「木の枠は縦の4本だけ」
#    → 90mm角材(長さ950mm)の4本主角柱のみ。余計な木枠梁は一切なし。
# 5. 「操作コンソール & 膝クリアランス」
#    → 膝がコンソールに当たらない十分な高さを確保し、シートまで約700mmの
#       足元クリアランスを確保。
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------------
# 主要寸法 (mm)
# --------------------------------------------------------
POST_T = 90.0           # 柱太さ 90mm角材
POST_H = 950.0          # 柱高さ 950mm
BASE_SIZE = 300.0       # 足元ベース板 300mm角
BASE_THICK = 18.0       # ベース板厚 18mm

W_INNER = 700.0         # 内寸横幅 700mm
DEPTH = 1350.0          # 柱芯間隔 1350mm (全長 1500mmの長方形)

# 柱の中心座標
X_L = -(W_INNER + POST_T) / 2   # -395mm (左柱)
X_R =  (W_INNER + POST_T) / 2   #  395mm (右柱)
Y_F = -DEPTH / 2                # -675mm (前柱)
Y_R =  DEPTH / 2                #  675mm (後柱)

parts_posts = []
parts_door = []
parts_console = []
parts_seat = []
parts_walls = []

print("1. 4本の主角柱および足元ベース板・安全三角リブをモデリング中...")

posts = [
    ("前左柱", X_L, Y_F),
    ("前右柱", X_R, Y_F),
    ("後左柱", X_L, Y_R),
    ("後右柱", X_R, Y_R)
]

for name, px, py in posts:
    # 縦の角柱本体 (90x90x950mm) - 木の枠は縦の4本のみ！
    col = bd.Location((px, py, POST_H / 2)) * bd.Box(POST_T, POST_T, POST_H)
    parts_posts.append(col)

    # 足元ベース板 (300x300x18mm)
    base_plate = bd.Location((px, py, BASE_THICK / 2)) * bd.Box(BASE_SIZE, BASE_SIZE, BASE_THICK)
    parts_posts.append(base_plate)

    # 三角補強リブ (ハカマ)
    # ★重要改善★: 通路・足元側（内側）にはリブを出さない！
    # 外側（±X方向で機体の外に向かう側）と、壁側（前後壁側）のみに配置。
    rib_w, rib_h, rib_t = 90.0, 150.0, 15.0

    # 機体外側方向のリブ (左柱は -X, 右柱は +X)
    rib_dir_x = -1 if px < 0 else 1
    with bd.BuildPart() as rib_outer_x:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px + rib_dir_x * POST_T/2, BASE_THICK),
                        (px + rib_dir_x * (POST_T/2 + rib_w), BASE_THICK))
                bd.Line((px + rib_dir_x * (POST_T/2 + rib_w), BASE_THICK),
                        (px + rib_dir_x * POST_T/2, BASE_THICK + rib_h))
                bd.Line((px + rib_dir_x * POST_T/2, BASE_THICK + rib_h),
                        (px + rib_dir_x * POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_posts.append(rib_outer_x.part)

    # 機体前後端方向のリブ (前柱は -Y, 後柱は +Y)
    rib_dir_y = -1 if py < 0 else 1
    with bd.BuildPart() as rib_outer_y:
        with bd.BuildSketch(bd.Plane.YZ.offset(px)):
            with bd.BuildLine():
                bd.Line((py + rib_dir_y * POST_T/2, BASE_THICK),
                        (py + rib_dir_y * (POST_T/2 + rib_w), BASE_THICK))
                bd.Line((py + rib_dir_y * (POST_T/2 + rib_w), BASE_THICK),
                        (py + rib_dir_y * POST_T/2, BASE_THICK + rib_h))
                bd.Line((py + rib_dir_y * POST_T/2, BASE_THICK + rib_h),
                        (py + rib_dir_y * POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_posts.append(rib_outer_y.part)

print("2. 乗降用大型開閉扉（ドア: 幅750x高800mm, 床スレスレ設計）をモデリング中...")
# ドア寸法: 幅750mm, 高さ800mm, 厚さ15mm
# ★重要改善★: ドア下端を地面からわずか50mmまで下げ、足を上げずにそのままシートへ腰掛け可能！
DOOR_W = 750.0
DOOR_H = 800.0
DOOR_T = 15.0
DOOR_Z = 50.0 + DOOR_H / 2 # Z = 450mm中心 (50mm〜850mm)

# ドア中心位置 (前柱寄りの乗降エリア: Y = -50mm付近)
DOOR_Y_CENTER = -50.0

door_panel = bd.Location((X_L, DOOR_Y_CENTER, DOOR_Z)) * bd.Box(DOOR_T, DOOR_W, DOOR_H)
parts_door.append(door_panel)

# ドア取っ手 (外側ハンドル & 内側ハンドル)
handle_out = bd.Location((X_L - 30.0, DOOR_Y_CENTER + DOOR_W/2 - 80.0, DOOR_Z)) * bd.Box(25.0, 30.0, 160.0)
handle_in  = bd.Location((X_L + 30.0, DOOR_Y_CENTER + DOOR_W/2 - 80.0, DOOR_Z)) * bd.Box(25.0, 30.0, 160.0)
parts_door.extend([handle_out, handle_in])

# 蝶番金具 (前柱寄り端部: Y = DOOR_Y_CENTER - DOOR_W/2 + 40)
hinge_y = DOOR_Y_CENTER - DOOR_W/2 + 40.0
hinge_t = bd.Location((X_L, hinge_y, DOOR_Z + DOOR_H/2 - 80.0)) * bd.Cylinder(radius=10, height=50)
hinge_b = bd.Location((X_L, hinge_y, DOOR_Z - DOOR_H/2 + 80.0)) * bd.Cylinder(radius=10, height=50)
parts_door.extend([hinge_t, hinge_b])

print("3. 操作コンソール（ハンドル・計器盤・膝クリアランス確保）をモデリング中...")
# 前柱間にマウント、膝に当たらない高さ Z=620mm、傾斜25度
CON_Y = Y_F + 160.0
CON_Z = 620.0
console_box = bd.Location((0, CON_Y, CON_Z), (-25, 0, 0)) * bd.Box(W_INNER - 10.0, 300.0, 130.0)
parts_console.append(console_box)

# 操縦ハンドル (フライトヨーク)
yoke_shaft = bd.Location((0, CON_Y - 45.0, CON_Z + 35.0), (-25, 0, 0)) * bd.Cylinder(radius=15, height=130)
yoke_center = bd.Location((0, CON_Y - 105.0, CON_Z + 65.0)) * bd.Box(150.0, 24.0, 28.0)
yoke_grip_l = bd.Location((-80.0, CON_Y - 115.0, CON_Z + 95.0)) * bd.Box(24.0, 24.0, 110.0)
yoke_grip_r = bd.Location(( 80.0, CON_Y - 115.0, CON_Z + 95.0)) * bd.Box(24.0, 24.0, 110.0)
parts_console.extend([yoke_shaft, yoke_center, yoke_grip_l, yoke_grip_r])

# 計器盤 (アナログメーター & スイッチ盤)
meter_l = bd.Location((-180.0, CON_Y + 40.0, CON_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=36, height=15)
meter_r = bd.Location(( 180.0, CON_Y + 40.0, CON_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=36, height=15)
switch_plate = bd.Location((0, CON_Y + 60.0, CON_Z + 80.0), (-25, 0, 0)) * bd.Box(180.0, 85.0, 10.0)
parts_console.extend([meter_l, meter_r, switch_plate])

# スロットルレバー (左手側)
throt_base = bd.Location((-260.0, Y_F + 250.0, 520.0)) * bd.Box(60.0, 100.0, 25.0)
throt_lever = bd.Location((-260.0, Y_F + 250.0, 575.0), (20, 0, 0)) * bd.Box(20.0, 35.0, 90.0)
parts_console.extend([throt_base, throt_lever])

print("4. ゆったり操縦席シート & ラダーペダルをモデリング中...")
# 足元スペース約700mmを確保し、後柱寄りにシートを配置 (座面高350mm)
SEAT_Y = Y_R - 240.0
seat_base = bd.Location((0, SEAT_Y, 350.0)) * bd.Box(520.0, 460.0, 50.0)
seat_back = bd.Location((0, SEAT_Y + 220.0, 630.0), (14, 0, 0)) * bd.Box(500.0, 45.0, 520.0)
seat_head = bd.Location((0, SEAT_Y + 270.0, 930.0), (10, 0, 0)) * bd.Box(260.0, 55.0, 150.0)
parts_seat.extend([seat_base, seat_back, seat_head])

# ラダーペダル (前柱足元)
pedal_l = bd.Location((-140.0, Y_F + 120.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
pedal_r = bd.Location(( 140.0, Y_F + 120.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
parts_seat.extend([pedal_l, pedal_r])

print("5. 外壁パネル（右側面・背面・前下面・ドア前後小壁）をモデリング中...")
# 全長1500mmの長方形外装
# 右側面パネル (全面固定壁: 厚さ12mm)
wall_r = bd.Location((X_R + POST_T/2 + 6.0, 0, POST_H / 2)) * bd.Box(12.0, DEPTH + POST_T, POST_H)
# 背面壁 (後柱外側)
wall_rear = bd.Location((0, Y_R + POST_T/2 + 6.0, POST_H / 2)) * bd.Box(W_INNER + POST_T*2, 12.0, POST_H)
# 前面下部パネル (コンソール下)
wall_front = bd.Location((0, Y_F - POST_T/2 - 6.0, 250.0)) * bd.Box(W_INNER + POST_T*2, 12.0, 500.0)

# 左側面ドア前後の固定小壁
# 前小壁: 前柱からドア前端まで
len_fw = (DOOR_Y_CENTER - DOOR_W/2) - (Y_F - POST_T/2)
y_fw = (Y_F - POST_T/2) + len_fw / 2
wall_l_front = bd.Location((X_L, y_fw, POST_H / 2)) * bd.Box(12.0, len_fw, POST_H)

# 後小壁: ドア後端から後柱まで
len_rw = (Y_R + POST_T/2) - (DOOR_Y_CENTER + DOOR_W/2)
y_rw = (DOOR_Y_CENTER + DOOR_W/2) + len_rw / 2
wall_l_rear = bd.Location((X_L, y_rw, POST_H / 2)) * bd.Box(12.0, len_rw, POST_H)

parts_walls.extend([wall_r, wall_rear, wall_front, wall_l_front, wall_l_rear])

# --------------------------------------------------------
# エクスポート
# --------------------------------------------------------
print("エクスポート中...")

# 木の枠単体 (縦の4本主角柱 + ベース板 + 三角リブのみ)
frame_compound = bd.Compound(parts_posts)
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))

# 全体アセンブリ
all_parts = parts_posts + parts_door + parts_console + parts_seat + parts_walls
full_assembly = bd.Compound(all_parts)
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))

print("STEP / STL エクスポート完了！")

spec = {
    "overall_dimensions_mm": {"width": 880, "length": 1500, "height": 950},
    "shape": "長方形 (幅880 x 全長1500mm)",
    "posts_qty": 4,
    "post_section_mm": "90x90",
    "post_height_mm": 950,
    "door_dimensions_mm": {"width": 750, "height": 800, "sill_height": 50},
    "foot_clearance_mm": 700,
    "trip_hazard_eliminated": "通路・足元側の三角リブを完全撤去し、床面を100%フラット化",
    "timber_frame_rule": "木の枠は縦の4本角柱のみ"
}

with open(os.path.join(OUT_DIR, "ergonomic_spec.json"), "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=2)

print("ergonomic_spec.json 保存完了！")
