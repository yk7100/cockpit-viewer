import os
import json
import build123d as bd

# ========================================================
# 操縦席 (Cockpit) Version 8.0.0 (Minecraft Pig Edition)
# ========================================================
# 【マインクラフト豚（Minecraft Pig）完全準拠ボクセルモデル】
# ユーザー提供画像（Minecraft Pig）の外装装飾に100%合致するモジュール設計：
# - 基準モジュール (1 Pixel): U = 87.5 mm
# - 胴体 (Body): 10 U (幅875mm) x 16 U (全長1400mm) x 8 U (高700mm)
# - 頭部 (Head): 8 U (幅700mm) x 8 U (高700mm) x 8 U (奥行700mm)
# - 鼻 (Snout): 4 U (幅350mm) x 3 U (高262mm) x 1 U (出90mm)
# - 4本の足 (Legs): 4 U x 4 U (350mm角) x 5 U (高440mm)
# - 木枠主角柱: 90mm角材 x 4本が「豚の4本の足」の構造芯柱に完全合致！
# - 操縦席: 胴体内部にゆったり配置、頭部内側にモニター・計器盤、手前に操縦デスク＆正対操縦桿
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

VERSION = "8.0.0"

U = 87.5        # 1ボクセル単位 (mm)

# 胴体寸法
BODY_W = 10 * U # 875 mm
BODY_L = 16 * U # 1400 mm
BODY_H = 8 * U  # 700 mm (地上高 440 + 700 = 1140mm)

# 脚寸法
LEG_S = 4 * U   # 350 mm角
LEG_H = 440.0   # 440 mm (床〜胴体下端)
POST_T = 90.0   # 柱芯 90mm角材
POST_H = 950.0  # 角柱高さ 950mm (足底面から胴体上部まで貫通する強固な芯柱)

# 頭部寸法
HEAD_W = 8 * U  # 700 mm
HEAD_H = 8 * U  # 700 mm
HEAD_D = 7 * U  # 612.5 mm
SNOUT_W = 4 * U # 350 mm
SNOUT_H = 3 * U # 262.5 mm
SNOUT_D = 1 * U # 87.5 mm

# 柱の配置 (胴体の四隅、足の芯)
X_L = -(BODY_W - LEG_S) / 2     # -262.5 mm (足の芯)
X_R =  (BODY_W - LEG_S) / 2     #  262.5 mm
Y_F = -(BODY_L - LEG_S) / 2     # -525.0 mm
Y_R =  (BODY_L - LEG_S) / 2     #  525.0 mm

parts_posts = []
parts_legs = []
parts_body = []
parts_head = []
parts_interior = []

print(f"Generating Cockpit v{VERSION} (Minecraft Pig) CAD models...")

# 1. 縦の4本主角柱 (90mm角材) & 足元ベース板
posts_data = [
    ("前左足柱", X_L, Y_F),
    ("前右足柱", X_R, Y_F),
    ("後左足柱", X_L, Y_R),
    ("後右足柱", X_R, Y_R)
]

for name, px, py in posts_data:
    # 柱芯本体 (90mm角 x 950mm)
    col = bd.Location((px, py, POST_H / 2)) * bd.Box(POST_T, POST_T, POST_H)
    parts_posts.append(col)

    # 足元ベース板 (300mm角 x 18mm)
    base_plate = bd.Location((px, py, 9.0)) * bd.Box(300.0, 300.0, 18.0)
    parts_posts.append(base_plate)

    # 豚の足外殻 (350mm角のマイクラ足ブロック)
    leg_box = bd.Location((px, py, LEG_H / 2)) * bd.Box(LEG_S, LEG_S, LEG_H)
    parts_legs.append(leg_box)

# 2. 豚の胴体 (Body - コックピット本体外壁)
BODY_Z_C = LEG_H + BODY_H / 2 # 440 + 350 = 790 mm
# 胴体メインブロック
body_main = bd.Location((0, 0, BODY_Z_C)) * bd.Box(BODY_W, BODY_L, BODY_H)
parts_body.append(body_main)

# 3. 豚の頭部 (Head) & 鼻 (Snout)
HEAD_Y_C = -(BODY_L / 2 + HEAD_D / 2) + 80.0 # 胴体前端に少し食い込む
HEAD_Z_C = LEG_H + HEAD_H / 2 - 20.0
head_box = bd.Location((0, HEAD_Y_C, HEAD_Z_C)) * bd.Box(HEAD_W, HEAD_D, HEAD_H)

# 鼻ブロック (前方に突き出す)
SNOUT_Y_C = HEAD_Y_C - HEAD_D / 2 - SNOUT_D / 2
SNOUT_Z_C = HEAD_Z_C - 80.0
snout_box = bd.Location((0, SNOUT_Y_C, SNOUT_Z_C)) * bd.Box(SNOUT_W, SNOUT_D, SNOUT_H)
parts_head.extend([head_box, snout_box])

# 4. 内部操縦席 (シート、机、正対操縦桿、ペダル)
# シート
SEAT_Y = Y_R - 100.0
seat_base = bd.Location((0, SEAT_Y, 350.0)) * bd.Box(500.0, 420.0, 50.0)
seat_back = bd.Location((0, SEAT_Y + 180.0, 620.0), (12, 0, 0)) * bd.Box(480.0, 40.0, 500.0)

# 操縦デスク (机)
DESK_Y = -80.0
DESK_H = 700.0
desk_top = bd.Location((0, DESK_Y, DESK_H - 12.0)) * bd.Box(680.0, 360.0, 24.0)

# 操縦桿 (パイロット正対)
yoke_base = bd.Location((0, DESK_Y - 20.0, DESK_H + 15.0)) * bd.Box(140.0, 90.0, 30.0)
yoke_shaft = bd.Location((0, DESK_Y + 25.0, DESK_H + 50.0), (25, 0, 0)) * bd.Cylinder(radius=15, height=110)
yoke_center = bd.Location((0, DESK_Y + 65.0, DESK_H + 75.0), (20, 0, 0)) * bd.Box(160.0, 26.0, 28.0)
yoke_l = bd.Location((-85.0, DESK_Y + 70.0, DESK_H + 105.0), (15, 0, 0)) * bd.Box(26.0, 26.0, 110.0)
yoke_r = bd.Location(( 85.0, DESK_Y + 70.0, DESK_H + 105.0), (15, 0, 0)) * bd.Box(26.0, 26.0, 110.0)

# 計器盤 (頭部内側フード)
inst_panel = bd.Location((0, DESK_Y - 120.0, DESK_H + 80.0), (30, 0, 0)) * bd.Box(500.0, 160.0, 20.0)

# ペダル
pedal_l = bd.Location((-140.0, Y_F + 80.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)
pedal_r = bd.Location(( 140.0, Y_F + 80.0, 70.0), (-25, 0, 0)) * bd.Box(85.0, 140.0, 18.0)

parts_interior.extend([seat_base, seat_back, desk_top,
                      yoke_base, yoke_shaft, yoke_center, yoke_l, yoke_r,
                      inst_panel, pedal_l, pedal_r])

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

# 代表ファイル更新
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))

print(f"Exported v{VERSION} (Minecraft Pig) CAD models successfully!")
