import os
import json
import build123d as bd

# ========================================================
# 操縦席 (Cockpit) Version 9.0.0 (Minecraft Pig - Head Cabin & Desk Support)
# ========================================================
# 【ユーザー要望の完全反映】
# 1. 「頭の支えとして机を使いたい」
#    - 操縦デスク（天板＆フレーム）を前方（頭部側）へ延長
#    - 豚の頭部（Head）の底面・内部フレームを前柱と連結して強固に下支えする支持台として機能
# 2. 「頭の内部に操縦桿を置きたい」
#    - 操縦桿（ヨーク）と計器盤を、豚の頭部の内部空間（Head Cabin）に完全移設
#    - パイロットが頭部空間へ手を伸ばして操縦する本格コクピットノーズ
# 3. 「椅子をもっと机の方に近づけて大丈夫」
#    - シートを前方へ約250mm前進（Y=+150mm）
#    - 頭部内部の操縦桿に自然に手が届くジャストフィットな搭乗姿勢
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

VERSION = "9.0.0"

U = 87.5        # 1ボクセル単位 (mm)

BODY_W = 10 * U # 875 mm
BODY_L = 16 * U # 1400 mm
BODY_H = 8 * U  # 700 mm
LEG_S = 4 * U   # 350 mm
LEG_H = 440.0   # 440 mm
POST_T = 90.0   # 90mm主角柱
POST_H = 950.0  # 950mm

HEAD_W = 8 * U  # 700 mm
HEAD_H = 8 * U  # 700 mm
HEAD_D = 7 * U  # 612.5 mm
SNOUT_W = 4 * U # 350 mm
SNOUT_H = 3 * U # 262.5 mm
SNOUT_D = 1 * U # 87.5 mm

X_L = -(BODY_W - LEG_S) / 2     # -262.5 mm
X_R =  (BODY_W - LEG_S) / 2     #  262.5 mm
Y_F = -(BODY_L - LEG_S) / 2     # -525.0 mm (前柱芯)
Y_R =  (BODY_L - LEG_S) / 2     #  525.0 mm (後柱芯)

parts_posts = []
parts_legs = []
parts_body = []
parts_head = []
parts_interior = []

print(f"Generating Cockpit v{VERSION} CAD models...")

# 1. 縦の4本主角柱 (90mm角材) & ベース板
posts_data = [
    ("前左足柱", X_L, Y_F),
    ("前右足柱", X_R, Y_F),
    ("後左足柱", X_L, Y_R),
    ("後右足柱", X_R, Y_R)
]

for name, px, py in posts_data:
    col = bd.Location((px, py, POST_H / 2)) * bd.Box(POST_T, POST_T, POST_H)
    parts_posts.append(col)
    base_plate = bd.Location((px, py, 9.0)) * bd.Box(300.0, 300.0, 18.0)
    parts_posts.append(base_plate)
    leg_box = bd.Location((px, py, LEG_H / 2)) * bd.Box(LEG_S, LEG_S, LEG_H)
    parts_legs.append(leg_box)

# 2. 胴体外装
BODY_Z_C = LEG_H + BODY_H / 2
body_main = bd.Location((0, 0, BODY_Z_C)) * bd.Box(BODY_W, BODY_L, BODY_H)
parts_body.append(body_main)

# 3. 頭部外装 (Head & Snout)
HEAD_Y_C = -(BODY_L / 2 + HEAD_D / 2) + 60.0 # Y = -700 - 306 + 60 = -946 mm
HEAD_Z_C = LEG_H + HEAD_H / 2 - 20.0        # Z = 440 + 350 - 20 = 770 mm
head_box = bd.Location((0, HEAD_Y_C, HEAD_Z_C)) * bd.Box(HEAD_W, HEAD_D, HEAD_H)

SNOUT_Y_C = HEAD_Y_C - HEAD_D / 2 - SNOUT_D / 2
SNOUT_Z_C = HEAD_Z_C - 70.0
snout_box = bd.Location((0, SNOUT_Y_C, SNOUT_Z_C)) * bd.Box(SNOUT_W, SNOUT_D, SNOUT_H)
parts_head.extend([head_box, snout_box])

# 4. 【頭部支持デスク（机）】
# 前柱(Y=-525)から頭部前端(Y=-1200)まで前方に伸びて頭部をしっかり支える延長天板構造！
DESK_W = 680.0
DESK_H = 700.0
DESK_TOP_T = 24.0
# 天板: パイロット手元(Y=-250)から頭部内部(Y=-1050)まで全長800mmの超頑丈サポートデスク！
DESK_L = 800.0
DESK_Y_C = -650.0 # 胴体前端と頭部をつなぐ中心

desk_top = bd.Location((0, DESK_Y_C, DESK_H - DESK_TOP_T / 2)) * bd.Box(DESK_W, DESK_L, DESK_TOP_T)
# 前柱と連結する頭部受けフレーム (左右)
desk_sup_l = bd.Location((-320.0, DESK_Y_C, DESK_H - 50.0)) * bd.Box(25.0, DESK_L - 40.0, 60.0)
desk_sup_r = bd.Location(( 320.0, DESK_Y_C, DESK_H - 50.0)) * bd.Box(25.0, DESK_L - 40.0, 60.0)
parts_interior.extend([desk_top, desk_sup_l, desk_sup_r])

# 5. 【頭部内部に配置した操縦桿 & 計器盤】
# 操縦桿は頭部の内部空間 (Y = -800mm付近) に配置！
YOKE_Y = -820.0
yoke_base = bd.Location((0, YOKE_Y, DESK_H + 15.0)) * bd.Box(140.0, 90.0, 30.0)
yoke_shaft = bd.Location((0, YOKE_Y + 30.0, DESK_H + 50.0), (25, 0, 0)) * bd.Cylinder(radius=15, height=110)
yoke_center = bd.Location((0, YOKE_Y + 70.0, DESK_H + 75.0), (20, 0, 0)) * bd.Box(160.0, 26.0, 28.0)
yoke_l = bd.Location((-85.0, YOKE_Y + 75.0, DESK_H + 105.0), (15, 0, 0)) * bd.Box(26.0, 26.0, 110.0)
yoke_r = bd.Location(( 85.0, YOKE_Y + 75.0, DESK_H + 105.0), (15, 0, 0)) * bd.Box(26.0, 26.0, 110.0)

# 頭部正面内側の計器ディスプレイパネル
inst_panel = bd.Location((0, -1080.0, DESK_H + 80.0), (30, 0, 0)) * bd.Box(500.0, 160.0, 20.0)
parts_interior.extend([yoke_base, yoke_shaft, yoke_center, yoke_l, yoke_r, inst_panel])

# 6. 【机にグッと近づけたシート】
# シートを前進 (Y = +150mm)
SEAT_Y = 150.0
seat_base = bd.Location((0, SEAT_Y, 350.0)) * bd.Box(500.0, 420.0, 50.0)
seat_back = bd.Location((0, SEAT_Y + 180.0, 620.0), (12, 0, 0)) * bd.Box(480.0, 40.0, 500.0)
seat_head = bd.Location((0, SEAT_Y + 230.0, 900.0), (10, 0, 0)) * bd.Box(240.0, 50.0, 140.0)

# ペダル (机下足元)
pedal_l = bd.Location((-140.0, -350.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
pedal_r = bd.Location(( 140.0, -350.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)

parts_interior.extend([seat_base, seat_back, seat_head, pedal_l, pedal_r])

# --------------------------------------------------------
# エクスポート
# --------------------------------------------------------
v_frame_step = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_frame.step")
v_frame_stl  = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_frame.stl")
v_full_step  = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_assembly.step")
v_full_stl   = os.path.join(OUT_DIR, f"cockpit_v{VERSION}_assembly.stl")

frame_compound = bd.Compound(parts_posts)
bd.export_step(frame_compound, v_frame_step)
bd.export_stl(frame_compound, v_frame_stl)

all_parts = parts_posts + parts_legs + parts_body + parts_head + parts_interior
full_assembly = bd.Compound(all_parts)
bd.export_step(full_assembly, v_full_step)
bd.export_stl(full_assembly, v_full_stl)

bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))

print(f"Exported v{VERSION} CAD models successfully!")
