import math
import os
import json
import build123d as bd

# ========================================================
# 操縦席 (Cockpit) 確定版設計スクリプト
# ユーザーの回答・ノートの数式を100%反映:
# 1. 4本の極太主角柱 (90x90x900mm)
#    - 内寸横幅: 700mm (ノート: 4/5 h)
#    - 足元ベース正方形: 300x300mm (ノート: 1/3 h)
#    - 足元三角補強リブ: 各柱の根元を「少し硬めの素材」でハカマ補強
# 2. 机・モニターは廃止 (ユーザー回答: 机・モニター不要)
# 3. 操作コンソール (ノート中央の斜線部):
#    - ハンドル、スイッチ類、メーター計器盤を配置した本格傾斜コンソール
# 4. パイロット着座シート & フットレスト
# 5. 板書のギミック統合:
#    - ガルウィング開閉アクリル板ドア
#    - 前方ラップ視野確保窓
#    - 段ボール外装
#    - 後部カーテン開口 (外部効果スタッフ用)
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------------
# 寸法パラメータ (mm)
# --------------------------------------------------------
H_REF = 900.0           # 基準高さ h = 900mm
W_INNER = 700.0         # 内寸横幅 (4/5)h = 700mm
POST_SIZE = 90.0        # 角柱太さ 90mm (1/10 h)
POST_HEIGHT = 900.0     # 柱高さ 900mm
BASE_SIZE = 300.0       # 足元ベース正方形 (1/3)h = 300mm
DEPTH_INNER = 800.0     # 前後柱スパン 800mm

# 座標オフセット
X_L = -(W_INNER + POST_SIZE) / 2    # -395mm (左柱芯)
X_R =  (W_INNER + POST_SIZE) / 2    #  395mm (右柱芯)
Y_F = -DEPTH_INNER / 2              # -400mm (前柱芯)
Y_R =  DEPTH_INNER / 2              #  400mm (後柱芯)

parts_frame = []
parts_console = []
parts_seat = []
parts_enclosure = []

print("1. 4本の主角柱および足元ベース・三角リブをモデリング中...")

# 柱座標リスト
posts = [
    ("前左柱", X_L, Y_F),
    ("前右柱", X_R, Y_F),
    ("後左柱", X_L, Y_R),
    ("後右柱", X_R, Y_R)
]

for name, px, py in posts:
    # 柱本体 (90x90x900mm)
    col = bd.Location((px, py, POST_HEIGHT / 2)) * bd.Box(POST_SIZE, POST_SIZE, POST_HEIGHT)
    parts_frame.append(col)

    # 足元ベース板 (300x300x18mm)
    base_plate = bd.Location((px, py, 9.0)) * bd.Box(BASE_SIZE, BASE_SIZE, 18.0)
    parts_frame.append(base_plate)

    # 足元直角三角リブ (底辺90mm, 高さ150mm, 厚み15mm)
    rib_w, rib_h, rib_t = 90.0, 150.0, 15.0
    
    # X軸方向の三角リブ (+X, -X)
    with bd.BuildPart() as rib_x_pos:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px + POST_SIZE/2, 18.0), (px + POST_SIZE/2 + rib_w, 18.0))
                bd.Line((px + POST_SIZE/2 + rib_w, 18.0), (px + POST_SIZE/2, 18.0 + rib_h))
                bd.Line((px + POST_SIZE/2, 18.0 + rib_h), (px + POST_SIZE/2, 18.0))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_frame.append(rib_x_pos.part)

    with bd.BuildPart() as rib_x_neg:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px - POST_SIZE/2, 18.0), (px - POST_SIZE/2 - rib_w, 18.0))
                bd.Line((px - POST_SIZE/2 - rib_w, 18.0), (px - POST_SIZE/2, 18.0 + rib_h))
                bd.Line((px - POST_SIZE/2, 18.0 + rib_h), (px - POST_SIZE/2, 18.0))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_frame.append(rib_x_neg.part)

    # Y軸方向の三角リブ (+Y, -Y)
    with bd.BuildPart() as rib_y_pos:
        with bd.BuildSketch(bd.Plane.YZ.offset(px)):
            with bd.BuildLine():
                bd.Line((py + POST_SIZE/2, 18.0), (py + POST_SIZE/2 + rib_w, 18.0))
                bd.Line((py + POST_SIZE/2 + rib_w, 18.0), (py + POST_SIZE/2, 18.0 + rib_h))
                bd.Line((py + POST_SIZE/2, 18.0 + rib_h), (py + POST_SIZE/2, 18.0))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_frame.append(rib_y_pos.part)

    with bd.BuildPart() as rib_y_neg:
        with bd.BuildSketch(bd.Plane.YZ.offset(px)):
            with bd.BuildLine():
                bd.Line((py - POST_SIZE/2, 18.0), (py - POST_SIZE/2 - rib_w, 18.0))
                bd.Line((py - POST_SIZE/2 - rib_w, 18.0), (py - POST_SIZE/2, 18.0 + rib_h))
                bd.Line((py - POST_SIZE/2, 18.0 + rib_h), (py - POST_SIZE/2, 18.0))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_frame.append(rib_y_neg.part)

# 2. 柱間の連結ビーム (フレーム補強)
print("2. 柱間フレームビームをモデリング中...")
BEAM_T = 45.0  # 45x45mm 角材
# 前横木 (前柱間: Z=500mm, Z=900mm)
f_beam_mid = bd.Location((0, Y_F, 500.0)) * bd.Box(W_INNER, BEAM_T, BEAM_T)
f_beam_top = bd.Location((0, Y_F, POST_HEIGHT - BEAM_T/2)) * bd.Box(W_INNER, BEAM_T, BEAM_T)
# 後横木 (後柱間: Z=350mm, Z=900mm)
r_beam_seat = bd.Location((0, Y_R, 350.0)) * bd.Box(W_INNER, BEAM_T, BEAM_T)
r_beam_top  = bd.Location((0, Y_R, POST_HEIGHT - BEAM_T/2)) * bd.Box(W_INNER, BEAM_T, BEAM_T)
# 左右サイドレール (前後柱間: Z=500mm, Z=900mm)
s_beam_l_mid = bd.Location((X_L, 0, 500.0)) * bd.Box(BEAM_T, DEPTH_INNER - POST_SIZE, BEAM_T)
s_beam_r_mid = bd.Location((X_R, 0, 500.0)) * bd.Box(BEAM_T, DEPTH_INNER - POST_SIZE, BEAM_T)
s_beam_l_top = bd.Location((X_L, 0, POST_HEIGHT - BEAM_T/2)) * bd.Box(BEAM_T, DEPTH_INNER - POST_SIZE, BEAM_T)
s_beam_r_top = bd.Location((X_R, 0, POST_HEIGHT - BEAM_T/2)) * bd.Box(BEAM_T, DEPTH_INNER - POST_SIZE, BEAM_T)

parts_frame.extend([f_beam_mid, f_beam_top, r_beam_seat, r_beam_top,
                    s_beam_l_mid, s_beam_r_mid, s_beam_l_top, s_beam_r_top])

# 3. 操作コンソール (ノート中央の斜線ハッチング部分: ハンドル・スイッチ盤)
print("3. 操作コンソール (ハンドル・計器盤) をモデリング中...")
# コンソール本体ボックス (前柱にマウント、幅700mm, 奥行360mm, 傾斜25度)
CONSOLE_Y = Y_F + 150.0
CONSOLE_Z = 580.0
console_body = bd.Location((0, CONSOLE_Y, CONSOLE_Z), (-25, 0, 0)) * bd.Box(W_INNER - 20.0, 320.0, 140.0)
parts_console.append(console_body)

# 操縦ハンドル (フライトヨーク / ステアリングホイール)
# センターシャフト
yoke_shaft = bd.Location((0, CONSOLE_Y - 40.0, CONSOLE_Z + 40.0), (-25, 0, 0)) * bd.Cylinder(radius=16, height=120)
# ヨークグリップ (W型操縦桿)
yoke_center = bd.Location((0, CONSOLE_Y - 100.0, CONSOLE_Z + 70.0)) * bd.Box(140.0, 25.0, 30.0)
yoke_handle_l = bd.Location((-90.0, CONSOLE_Y - 110.0, CONSOLE_Z + 100.0)) * bd.Box(25.0, 25.0, 110.0)
yoke_handle_r = bd.Location(( 90.0, CONSOLE_Y - 110.0, CONSOLE_Z + 100.0)) * bd.Box(25.0, 25.0, 110.0)
parts_console.extend([yoke_shaft, yoke_center, yoke_handle_l, yoke_handle_r])

# スイッチ・計器盤 (トグルスイッチパネル & アナログメーター)
meter_l = bd.Location((-180.0, CONSOLE_Y + 40.0, CONSOLE_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=35, height=15)
meter_r = bd.Location(( 180.0, CONSOLE_Y + 40.0, CONSOLE_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=35, height=15)
switch_plate = bd.Location((0, CONSOLE_Y + 60.0, CONSOLE_Z + 80.0), (-25, 0, 0)) * bd.Box(180.0, 90.0, 10.0)
parts_console.extend([meter_l, meter_r, switch_plate])

# スロットルレバー (左手側)
throttle_base = bd.Location((-260.0, Y_F + 220.0, 520.0)) * bd.Box(70.0, 100.0, 25.0)
throttle_lever = bd.Location((-260.0, Y_F + 220.0, 570.0), (20, 0, 0)) * bd.Box(20.0, 35.0, 90.0)
parts_console.extend([throttle_base, throttle_lever])

# 4. パイロットシート (座席)
print("4. パイロットシートをモデリング中...")
SEAT_Y = Y_R - 180.0
seat_base = bd.Location((0, SEAT_Y, 360.0)) * bd.Box(500.0, 440.0, 50.0)
seat_back = bd.Location((0, SEAT_Y + 200.0, 620.0), (12, 0, 0)) * bd.Box(480.0, 45.0, 500.0)
seat_head = bd.Location((0, SEAT_Y + 240.0, 910.0), (10, 0, 0)) * bd.Box(260.0, 55.0, 150.0)
parts_seat.extend([seat_base, seat_back, seat_head])

# フットレスト / ラダーペダル
pedal_l = bd.Location((-130.0, Y_F + 50.0, 70.0), (-25, 0, 0)) * bd.Box(80.0, 120.0, 15.0)
pedal_r = bd.Location(( 130.0, Y_F + 50.0, 70.0), (-25, 0, 0)) * bd.Box(80.0, 120.0, 15.0)
parts_seat.extend([pedal_l, pedal_r])

# 5. 外装・キャノピー (板書の要素: ガルウィングドア、ラップ窓、カーテン)
print("5. 外装パネル & ガルウィングドアをモデリング中...")
# 前方傾斜ラップ窓 (前柱〜コンソール上部)
windshield = bd.Location((0, Y_F - 50.0, 750.0), (-45, 0, 0)) * bd.Box(W_INNER, 4.0, 420.0)
parts_enclosure.append(windshield)

# ガルウィングアクリルドア (左右2枚: Z=500〜900mm)
door_l = bd.Location((X_L - 8.0, 0, 700.0)) * bd.Box(4.0, DEPTH_INNER, 380.0)
door_r = bd.Location((X_R + 8.0, 0, 700.0)) * bd.Box(4.0, DEPTH_INNER, 380.0)
parts_enclosure.extend([door_l, door_r])

# 段ボール外壁 (下部サイドパネル Z=0〜500mm)
side_wall_l = bd.Location((X_L - 8.0, 0, 250.0)) * bd.Box(5.0, DEPTH_INNER, 500.0)
side_wall_r = bd.Location((X_R + 8.0, 0, 250.0)) * bd.Box(5.0, DEPTH_INNER, 500.0)
parts_enclosure.extend([side_wall_l, side_wall_r])

# 後部カーテン開口 (外部効果スタッフ用: 幅600mm)
curtain = bd.Location((0, Y_R + 8.0, 450.0)) * bd.Box(600.0, 2.0, POST_HEIGHT - 60.0)
parts_enclosure.append(curtain)

# --------------------------------------------------------
# CADデータのエクスポート
# --------------------------------------------------------
print("エクスポート中...")

# 骨組み単体
frame_compound = bd.Compound(parts_frame)
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_v3_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_v3_frame.stl"))
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))

# 全体アセンブリ
all_parts = parts_frame + parts_console + parts_seat + parts_enclosure
full_assembly = bd.Compound(all_parts)
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_v3_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_v3_full.stl"))
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))

print("STEP / STL エクスポート完了！")
