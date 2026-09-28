import os
import json
import build123d as bd

# ========================================================
# 操縦席 (Cockpit) Version 5.0.0 (Major Release)
# ========================================================
# 【セマンティックバージョニング管理】
# v1.0.0: 黒板初期案 (30mm角材・キャノピー・ガルウィングドア)
# v2.0.0: ステルス戦闘機エディション (多面体ウェッジ・バーニア)
# v3.0.0: ノート第1案 (90mm角柱4本・机・モニターアーム)
# v4.0.0: ノート改訂案 (机・モニター撤去・操作コンソール)
# v5.0.0: 人間工学・長方形モデル
#         - 木の枠は縦の4本主角柱のみ (90mm角材 x 950mm)
#         - 全長1500mmの長方形プロポーション (幅880 x 全長1500mm)
#         - 敷居高さわずか50mmの低床大型スイングドア (幅750 x 高800mm)
#         - 内側リブ全廃・通路床面100%フラット化
#         - 操作コンソール (ハンドル・計器盤) 膝上クリアランス確保
#         - 足元広々700mmスペース
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

VERSION = "5.0.0"

POST_T = 90.0           # 柱太さ 90mm角材
POST_H = 950.0          # 柱高さ 950mm
BASE_SIZE = 300.0       # 足元ベース板 300mm角
BASE_THICK = 18.0       # ベース板厚 18mm

W_INNER = 700.0         # 内寸横幅 700mm
DEPTH = 1350.0          # 柱芯間隔 1350mm (全長 1500mmの長方形)

X_L = -(W_INNER + POST_T) / 2   # -395mm
X_R =  (W_INNER + POST_T) / 2   #  395mm
Y_F = -DEPTH / 2                # -675mm
Y_R =  DEPTH / 2                #  675mm

parts_posts = []
parts_door = []
parts_console = []
parts_seat = []
parts_walls = []

print(f"Generating Cockpit v{VERSION} CAD models...")

# 1. 縦の4本主角柱 ＋ 足元ベース板 ＋ 外側安全リブのみ
posts = [
    ("前左柱", X_L, Y_F, -1, -1),
    ("前右柱", X_R, Y_F,  1, -1),
    ("後左柱", X_L, Y_R, -1,  1),
    ("後右柱", X_R, Y_R,  1,  1)
]

for name, px, py, dirX, dirY in posts:
    # 柱本体
    col = bd.Location((px, py, POST_H / 2)) * bd.Box(POST_T, POST_T, POST_H)
    parts_posts.append(col)

    # 足元ベース板
    base_plate = bd.Location((px, py, BASE_THICK / 2)) * bd.Box(BASE_SIZE, BASE_SIZE, BASE_THICK)
    parts_posts.append(base_plate)

    # 外側リブ (通路・足元側にはリブを出さない完全フラット設計)
    rib_w, rib_h, rib_t = 90.0, 150.0, 15.0

    # X外側
    with bd.BuildPart() as rib_x:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px + dirX * POST_T/2, BASE_THICK),
                        (px + dirX * (POST_T/2 + rib_w), BASE_THICK))
                bd.Line((px + dirX * (POST_T/2 + rib_w), BASE_THICK),
                        (px + dirX * POST_T/2, BASE_THICK + rib_h))
                bd.Line((px + dirX * POST_T/2, BASE_THICK + rib_h),
                        (px + dirX * POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_posts.append(rib_x.part)

    # Y外側 (前後端壁側)
    with bd.BuildPart() as rib_y:
        with bd.BuildSketch(bd.Plane.YZ.offset(px)):
            with bd.BuildLine():
                bd.Line((py + dirY * POST_T/2, BASE_THICK),
                        (py + dirY * (POST_T/2 + rib_w), BASE_THICK))
                bd.Line((py + dirY * (POST_T/2 + rib_w), BASE_THICK),
                        (py + dirY * POST_T/2, BASE_THICK + rib_h))
                bd.Line((py + dirY * POST_T/2, BASE_THICK + rib_h),
                        (py + dirY * POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_posts.append(rib_y.part)

# 2. 低床大型乗降ドア (敷居高さわずか50mm、幅750×高800mm)
DOOR_W = 750.0
DOOR_H = 800.0
DOOR_T = 15.0
DOOR_Z = 50.0 + DOOR_H / 2
DOOR_Y_C = -50.0

door_panel = bd.Location((X_L, DOOR_Y_C, DOOR_Z)) * bd.Box(DOOR_T, DOOR_W, DOOR_H)
handle_out = bd.Location((X_L - 30.0, DOOR_Y_C + DOOR_W/2 - 80.0, DOOR_Z)) * bd.Box(25.0, 30.0, 160.0)
handle_in  = bd.Location((X_L + 30.0, DOOR_Y_C + DOOR_W/2 - 80.0, DOOR_Z)) * bd.Box(25.0, 30.0, 160.0)
hinge_y = DOOR_Y_C - DOOR_W/2 + 40.0
hinge_t = bd.Location((X_L, hinge_y, DOOR_Z + DOOR_H/2 - 80.0)) * bd.Cylinder(radius=10, height=50)
hinge_b = bd.Location((X_L, hinge_y, DOOR_Z - DOOR_H/2 + 80.0)) * bd.Cylinder(radius=10, height=50)
parts_door.extend([door_panel, handle_out, handle_in, hinge_t, hinge_b])

# 3. 操作コンソール (膝上クリアランス確保 Z=620mm)
CON_Y = Y_F + 160.0
CON_Z = 620.0
console_box = bd.Location((0, CON_Y, CON_Z), (-25, 0, 0)) * bd.Box(W_INNER - 10.0, 300.0, 130.0)
yoke_shaft = bd.Location((0, CON_Y - 45.0, CON_Z + 35.0), (-25, 0, 0)) * bd.Cylinder(radius=15, height=130)
yoke_center = bd.Location((0, CON_Y - 105.0, CON_Z + 65.0)) * bd.Box(150.0, 24.0, 28.0)
yoke_grip_l = bd.Location((-80.0, CON_Y - 115.0, CON_Z + 95.0)) * bd.Box(24.0, 24.0, 110.0)
yoke_grip_r = bd.Location(( 80.0, CON_Y - 115.0, CON_Z + 95.0)) * bd.Box(24.0, 24.0, 110.0)
meter_l = bd.Location((-180.0, CON_Y + 40.0, CON_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=36, height=15)
meter_r = bd.Location(( 180.0, CON_Y + 40.0, CON_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=36, height=15)
switch_plate = bd.Location((0, CON_Y + 60.0, CON_Z + 80.0), (-25, 0, 0)) * bd.Box(180.0, 85.0, 10.0)
throt_base = bd.Location((-260.0, Y_F + 250.0, 520.0)) * bd.Box(60.0, 100.0, 25.0)
throt_lever = bd.Location((-260.0, Y_F + 250.0, 575.0), (20, 0, 0)) * bd.Box(20.0, 35.0, 90.0)
parts_console.extend([console_box, yoke_shaft, yoke_center, yoke_grip_l, yoke_grip_r,
                      meter_l, meter_r, switch_plate, throt_base, throt_lever])

# 4. ゆったりシート & ペダル
SEAT_Y = Y_R - 240.0
seat_base = bd.Location((0, SEAT_Y, 350.0)) * bd.Box(520.0, 460.0, 50.0)
seat_back = bd.Location((0, SEAT_Y + 220.0, 630.0), (14, 0, 0)) * bd.Box(500.0, 45.0, 520.0)
seat_head = bd.Location((0, SEAT_Y + 270.0, 930.0), (10, 0, 0)) * bd.Box(260.0, 55.0, 150.0)
pedal_l = bd.Location((-140.0, Y_F + 120.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
pedal_r = bd.Location(( 140.0, Y_F + 120.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
parts_seat.extend([seat_base, seat_back, seat_head, pedal_l, pedal_r])

# 5. 外装パネル
wall_r = bd.Location((X_R + POST_T/2 + 6.0, 0, POST_H / 2)) * bd.Box(12.0, DEPTH + POST_T, POST_H)
wall_rear = bd.Location((0, Y_R + POST_T/2 + 6.0, POST_H / 2)) * bd.Box(W_INNER + POST_T*2, 12.0, POST_H)
wall_front = bd.Location((0, Y_F - POST_T/2 - 6.0, 250.0)) * bd.Box(W_INNER + POST_T*2, 12.0, 500.0)
len_fw = (DOOR_Y_C - DOOR_W/2) - (Y_F - POST_T/2)
wall_l_front = bd.Location((X_L, (Y_F - POST_T/2) + len_fw/2, POST_H / 2)) * bd.Box(12.0, len_fw, POST_H)
len_rw = (Y_R + POST_T/2) - (DOOR_Y_C + DOOR_W/2)
wall_l_rear = bd.Location((X_L, (DOOR_Y_C + DOOR_W/2) + len_rw/2, POST_H / 2)) * bd.Box(12.0, len_rw, POST_H)
parts_walls.extend([wall_r, wall_rear, wall_front, wall_l_front, wall_l_rear])

# --------------------------------------------------------
# バージョン名付きファイルのエクスポート
# --------------------------------------------------------
# 1. バージョン明記ファイル
v_frame_step = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_frame.step")
v_frame_stl  = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_frame.stl")
v_full_step  = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_assembly.step")
v_full_stl   = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_assembly.stl")

frame_compound = bd.Compound(parts_posts)
bd.export_step(frame_compound, v_frame_step)
bd.export_stl(frame_compound, v_frame_stl)

all_parts = parts_posts + parts_door + parts_console + parts_seat + parts_walls
full_assembly = bd.Compound(all_parts)
bd.export_step(full_assembly, v_full_step)
bd.export_stl(full_assembly, v_full_stl)

# 2. 代表ファイルも最新版で上書き
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))

print(f"Exported v{VERSION} CAD files successfully!")
