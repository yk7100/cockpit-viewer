import os
import json
import build123d as bd

# ========================================================
# 操縦席 (Cockpit) Version 7.0.0 (Major Release)
# ========================================================
# 【セマンティックバージョニング管理】
# v7.0.0: 【正方形・スマート導線・跳ね上げ操縦デスクモデル】
#         1. プロポーションを「正方形（幅900 x 全長1000mm）」に最適化（省スペース化）
#         2. 導線問題を完全解決する「跳ね上げ式（フリップアップ）操縦デスク」
#            - 乗降時は机天板が斜め上に跳ね上がり、正面から立ったままゆったり搭乗可能
#            - 着座後に机を手前に下ろしてコックピットが完成する戦闘機スタイル
#         3. パイロット正対操縦桿 ＋ 傾斜計器盤 ＋ スロットル
#         4. 木枠は縦の4本主角柱（90mm角 x 950mm）のみ堅持
#         5. 低床ドア（敷居50mm）＋足元完全フラット（躓きゼロ）
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

VERSION = "7.0.0"

POST_T = 90.0           # 柱太さ 90mm角材
POST_H = 950.0          # 柱高さ 950mm
BASE_SIZE = 300.0       # 足元ベース板 300mm角
BASE_THICK = 18.0       # ベース板厚 18mm

W_INNER = 720.0         # 内寸横幅 720mm (外幅 900mm)
DEPTH = 820.0           # 柱芯間隔 820mm (外全長 1000mmの正方形プロポーション！)

X_L = -(W_INNER + POST_T) / 2   # -405mm
X_R =  (W_INNER + POST_T) / 2   #  405mm
Y_F = -DEPTH / 2                # -410mm (機首・前方)
Y_R =  DEPTH / 2                #  410mm (シート・後方)

parts_posts = []
parts_door = []
parts_desk = []
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
    # 柱本体 (90mm角 x 950mm)
    col = bd.Location((px, py, POST_H / 2)) * bd.Box(POST_T, POST_T, POST_H)
    parts_posts.append(col)

    # 足元ベース板 (300mm角 x 18mm)
    base_plate = bd.Location((px, py, BASE_THICK / 2)) * bd.Box(BASE_SIZE, BASE_SIZE, BASE_THICK)
    parts_posts.append(base_plate)

    # 外側リブ (内側・通路・足元側にはリブを出さない完全フラット設計)
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

# 2. 低床大型乗降ドア (敷居高さ50mm、幅650×高800mm)
# 正方形モデルに合わせてドア幅を650mmに最適化、柱間をフルに活かした超広々乗降口
DOOR_W = 650.0
DOOR_H = 800.0
DOOR_T = 15.0
DOOR_Z = 50.0 + DOOR_H / 2
DOOR_Y_C = 0.0          # 中央乗降口

door_panel = bd.Location((X_L, DOOR_Y_C, DOOR_Z)) * bd.Box(DOOR_T, DOOR_W, DOOR_H)
handle_out = bd.Location((X_L - 30.0, DOOR_Y_C + DOOR_W/2 - 70.0, DOOR_Z)) * bd.Box(25.0, 30.0, 160.0)
handle_in  = bd.Location((X_L + 30.0, DOOR_Y_C + DOOR_W/2 - 70.0, DOOR_Z)) * bd.Box(25.0, 30.0, 160.0)
hinge_y = DOOR_Y_C - DOOR_W/2 + 35.0
hinge_t = bd.Location((X_L, hinge_y, DOOR_Z + DOOR_H/2 - 80.0)) * bd.Cylinder(radius=10, height=50)
hinge_b = bd.Location((X_L, hinge_y, DOOR_Z - DOOR_H/2 + 80.0)) * bd.Cylinder(radius=10, height=50)
parts_door.extend([door_panel, handle_out, handle_in, hinge_t, hinge_b])

# 3. 【新設計】導線を劇的に向上させる「跳ね上げ式操縦デスク（机）」
# 正方形空間の中で、乗降時には前上方へ跳ね上がり、着座時に手前に下ろすスマート構造
DESK_W = 690.0
DESK_D = 350.0
DESK_H = 700.0
DESK_TOP_T = 24.0
DESK_Y = -60.0          # シートの前方

# 机天板
desk_top = bd.Location((0, DESK_Y, DESK_H - DESK_TOP_T / 2)) * bd.Box(DESK_W, DESK_D, DESK_TOP_T)
# ヒンジ受けベースフレーム (前柱側で強固に支持)
desk_frame_l = bd.Location((-(DESK_W - 20)/2, Y_F + 80.0, DESK_H - 40.0)) * bd.Box(20.0, 160.0, 40.0)
desk_frame_r = bd.Location(( (DESK_W - 20)/2, Y_F + 80.0, DESK_H - 40.0)) * bd.Box(20.0, 160.0, 40.0)
# 跳ね上げヒンジ軸
desk_hinge = bd.Location((0, DESK_Y - DESK_D/2 + 15.0, DESK_H)) * bd.Cylinder(radius=12, height=DESK_W - 40.0)
parts_desk.extend([desk_top, desk_frame_l, desk_frame_r, desk_hinge])

# 4. 机上の操作コンソール & パイロット正対操縦桿
# (1) 傾斜計器ディスプレイパネル (机奥側)
inst_panel = bd.Location((0, DESK_Y - 80.0, DESK_H + 75.0), (30, 0, 0)) * bd.Box(500.0, 150.0, 20.0)
meter_l = bd.Location((-150.0, DESK_Y - 80.0, DESK_H + 85.0), (30, 0, 0)) * bd.Cylinder(radius=30, height=25)
meter_r = bd.Location(( 150.0, DESK_Y - 80.0, DESK_H + 85.0), (30, 0, 0)) * bd.Cylinder(radius=30, height=25)
display_center = bd.Location((0, DESK_Y - 80.0, DESK_H + 85.0), (30, 0, 0)) * bd.Box(190.0, 95.0, 25.0)

# (2) 操縦桿 (パイロット側 +Y に向けて正対配置！)
yoke_base = bd.Location((0, DESK_Y - 10.0, DESK_H + 15.0)) * bd.Box(140.0, 90.0, 30.0)
yoke_shaft = bd.Location((0, DESK_Y + 35.0, DESK_H + 50.0), (25, 0, 0)) * bd.Cylinder(radius=15, height=110)
yoke_center = bd.Location((0, DESK_Y + 75.0, DESK_H + 75.0), (20, 0, 0)) * bd.Box(160.0, 26.0, 28.0)
yoke_grip_l = bd.Location((-85.0, DESK_Y + 80.0, DESK_H + 105.0), (15, 0, 0)) * bd.Box(26.0, 26.0, 110.0)
yoke_grip_r = bd.Location(( 85.0, DESK_Y + 80.0, DESK_H + 105.0), (15, 0, 0)) * bd.Box(26.0, 26.0, 110.0)

# (3) スロットルレバー (机の左手側)
throt_base = bd.Location((-230.0, DESK_Y + 20.0, DESK_H + 15.0)) * bd.Box(70.0, 100.0, 30.0)
throt_lever = bd.Location((-230.0, DESK_Y + 20.0, DESK_H + 70.0), (-20, 0, 0)) * bd.Box(20.0, 35.0, 90.0)

parts_console.extend([inst_panel, meter_l, meter_r, display_center,
                      yoke_base, yoke_shaft, yoke_center, yoke_grip_l, yoke_grip_r,
                      throt_base, throt_lever])

# 5. ゆったりシート & ペダル
SEAT_Y = Y_R - 190.0    # 220mm (正方形にフィットするゆったりシート位置)
seat_base = bd.Location((0, SEAT_Y, 350.0)) * bd.Box(520.0, 420.0, 50.0)
seat_back = bd.Location((0, SEAT_Y + 190.0, 630.0), (14, 0, 0)) * bd.Box(500.0, 45.0, 520.0)
seat_head = bd.Location((0, SEAT_Y + 240.0, 930.0), (10, 0, 0)) * bd.Box(260.0, 55.0, 150.0)
# ペダル (机の下の足元前方)
pedal_l = bd.Location((-140.0, Y_F + 120.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
pedal_r = bd.Location(( 140.0, Y_F + 120.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
parts_seat.extend([seat_base, seat_back, seat_head, pedal_l, pedal_r])

# 6. 外装パネル
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
# 1. バージョン明記ファイル (v7.0.0)
v_frame_step = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_frame.step")
v_frame_stl  = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_frame.stl")
v_full_step  = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_assembly.step")
v_full_stl   = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_assembly.stl")

frame_compound = bd.Compound(parts_posts)
bd.export_step(frame_compound, v_frame_step)
bd.export_stl(frame_compound, v_frame_stl)

all_parts = parts_posts + parts_door + parts_desk + parts_console + parts_seat + parts_walls
full_assembly = bd.Compound(all_parts)
bd.export_step(full_assembly, v_full_step)
bd.export_stl(full_assembly, v_full_stl)

# 代表ファイルも最新版で上書き
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))

print(f"Exported v{VERSION} CAD files successfully!")
