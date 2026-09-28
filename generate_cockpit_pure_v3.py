import math
import os
import json
import build123d as bd

# ========================================================
# コクピット純粋新設計 (Pure V3 Simulator Cockpit)
# ========================================================
# 過去の板書（ガルウィングドア・ラップ窓・カーテン・ツインノズル）を完全に排し、
# 最新の手書き設計ノートの数式・スケッチ・ユーザー指示を100%純粋に具現化。
#
# 【ノートの確定設計仕様】
# 1. 基準高さ h = 900 mm (87.5 ≒ 90cm)
# 2. 内寸横幅 = (4/5) h = 700 mm (カフェ1人席の理想幅)
# 3. 4本の主角柱 = (1/9〜1/12) h ≒ 90mm角 (長さ900mm)
# 4. 足元ベース板 = (3/10) h ≒ (1/3) h = 300mm角
# 5. 足元三角補強リブ = 各柱の根元を「少し硬めの素材」でハカマ補強
# 6. 中間高さ (1/2) h = 450mm に連結梁・座面受木
# 7. 操作コンソール (ノート中央斜線ハッチング部):
#    前柱間にマウントされた本格操作盤（ハンドル、スイッチ群、メーター、スロットル）
# 8. パイロットシート & ペダル
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------------
# 基本寸法 (mm)
# --------------------------------------------------------
H = 900.0               # 基準高さ h
W_INNER = 700.0         # 内寸幅 (4/5)h
POST_T = 90.0           # 柱太さ 90mm
POST_H = 900.0          # 柱高さ 900mm
BASE_SIZE = 300.0       # 足元ベース板 300mm角
BASE_THICK = 18.0       # ベース板厚 18mm
DEPTH = 800.0           # 前後柱芯間隔 800mm
BEAM_T = 45.0           # 連結木材 45x45mm

# 柱の芯座標
X_L = -(W_INNER + POST_T) / 2   # -395mm (左柱)
X_R =  (W_INNER + POST_T) / 2   #  395mm (右柱)
Y_F = -DEPTH / 2                # -400mm (前柱)
Y_R =  DEPTH / 2                #  400mm (後柱)

parts_frame = []
parts_console = []
parts_seat = []

print("1. 4本の主角柱、ベース板、三角補強リブをモデリング中...")

posts = [
    ("前左柱", X_L, Y_F),
    ("前右柱", X_R, Y_F),
    ("後左柱", X_L, Y_R),
    ("後右柱", X_R, Y_R)
]

for name, px, py in posts:
    # 柱本体 (90x90x900mm)
    col = bd.Location((px, py, POST_H / 2)) * bd.Box(POST_T, POST_T, POST_H)
    parts_frame.append(col)

    # 足元正方形ベース板 (300x300x18mm)
    base_plate = bd.Location((px, py, BASE_THICK / 2)) * bd.Box(BASE_SIZE, BASE_SIZE, BASE_THICK)
    parts_frame.append(base_plate)

    # 足元直角三角補強リブ (底辺90mm, 高さ150mm, 厚み15mm: ハカマ補強)
    rib_w, rib_h, rib_t = 90.0, 150.0, 15.0

    # +X 方向リブ
    with bd.BuildPart() as rib_xp:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px + POST_T/2, BASE_THICK), (px + POST_T/2 + rib_w, BASE_THICK))
                bd.Line((px + POST_T/2 + rib_w, BASE_THICK), (px + POST_T/2, BASE_THICK + rib_h))
                bd.Line((px + POST_T/2, BASE_THICK + rib_h), (px + POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_frame.append(rib_xp.part)

    # -X 方向リブ
    with bd.BuildPart() as rib_xm:
        with bd.BuildSketch(bd.Plane.XZ.offset(py)):
            with bd.BuildLine():
                bd.Line((px - POST_T/2, BASE_THICK), (px - POST_T/2 - rib_w, BASE_THICK))
                bd.Line((px - POST_T/2 - rib_w, BASE_THICK), (px - POST_T/2, BASE_THICK + rib_h))
                bd.Line((px - POST_T/2, BASE_THICK + rib_h), (px - POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_frame.append(rib_xm.part)

    # +Y 方向リブ
    with bd.BuildPart() as rib_yp:
        with bd.BuildSketch(bd.Plane.YZ.offset(px)):
            with bd.BuildLine():
                bd.Line((py + POST_T/2, BASE_THICK), (py + POST_T/2 + rib_w, BASE_THICK))
                bd.Line((py + POST_T/2 + rib_w, BASE_THICK), (py + POST_T/2, BASE_THICK + rib_h))
                bd.Line((py + POST_T/2, BASE_THICK + rib_h), (py + POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_frame.append(rib_yp.part)

    # -Y 方向リブ
    with bd.BuildPart() as rib_ym:
        with bd.BuildSketch(bd.Plane.YZ.offset(px)):
            with bd.BuildLine():
                bd.Line((py - POST_T/2, BASE_THICK), (py - POST_T/2 - rib_w, BASE_THICK))
                bd.Line((py - POST_T/2 - rib_w, BASE_THICK), (py - POST_T/2, BASE_THICK + rib_h))
                bd.Line((py - POST_T/2, BASE_THICK + rib_h), (py - POST_T/2, BASE_THICK))
            bd.make_face()
        bd.extrude(amount=rib_t/2, both=True)
    parts_frame.append(rib_ym.part)

print("2. 柱間連結フレーム（梁・横木）をモデリング中...")
# 前横木 (Z = 450mm (1/2 h), Z = 900mm - BEAM_T/2)
f_beam_mid = bd.Location((0, Y_F, 450.0)) * bd.Box(W_INNER, BEAM_T, BEAM_T)
f_beam_top = bd.Location((0, Y_F, POST_H - BEAM_T/2)) * bd.Box(W_INNER, BEAM_T, BEAM_T)

# 後横木 (Z = 350mm (シート受), Z = 900mm - BEAM_T/2)
r_beam_seat = bd.Location((0, Y_R, 350.0)) * bd.Box(W_INNER, BEAM_T, BEAM_T)
r_beam_top  = bd.Location((0, Y_R, POST_H - BEAM_T/2)) * bd.Box(W_INNER, BEAM_T, BEAM_T)

# 左右サイドレール (Z = 450mm (1/2 h), Z = 900mm - BEAM_T/2)
s_beam_l_mid = bd.Location((X_L, 0, 450.0)) * bd.Box(BEAM_T, DEPTH - POST_T, BEAM_T)
s_beam_r_mid = bd.Location((X_R, 0, 450.0)) * bd.Box(BEAM_T, DEPTH - POST_T, BEAM_T)
s_beam_l_top = bd.Location((X_L, 0, POST_H - BEAM_T/2)) * bd.Box(BEAM_T, DEPTH - POST_T, BEAM_T)
s_beam_r_top = bd.Location((X_R, 0, POST_H - BEAM_T/2)) * bd.Box(BEAM_T, DEPTH - POST_T, BEAM_T)

parts_frame.extend([f_beam_mid, f_beam_top, r_beam_seat, r_beam_top,
                    s_beam_l_mid, s_beam_r_mid, s_beam_l_top, s_beam_r_top])

print("3. 操作コンソール（中央斜線ハッチング部: 計器盤・ハンドル・スイッチ）をモデリング中...")
# コンソール本体（前柱間にマウント、幅700mm, 奥行340mm, 傾斜約25度）
CON_Y = Y_F + 140.0
CON_Z = 580.0
console_box = bd.Location((0, CON_Y, CON_Z), (-25, 0, 0)) * bd.Box(W_INNER - 10.0, 320.0, 140.0)
parts_console.append(console_box)

# 操縦ハンドル (フライトヨーク)
# センターシャフト
yoke_shaft = bd.Location((0, CON_Y - 45.0, CON_Z + 35.0), (-25, 0, 0)) * bd.Cylinder(radius=15, height=130)
# ヨーク中央バー
yoke_center = bd.Location((0, CON_Y - 105.0, CON_Z + 65.0)) * bd.Box(150.0, 24.0, 28.0)
# ヨーク左右グリップ (W型ハンドル)
yoke_grip_l = bd.Location((-80.0, CON_Y - 115.0, CON_Z + 95.0)) * bd.Box(24.0, 24.0, 110.0)
yoke_grip_r = bd.Location(( 80.0, CON_Y - 115.0, CON_Z + 95.0)) * bd.Box(24.0, 24.0, 110.0)
parts_console.extend([yoke_shaft, yoke_center, yoke_grip_l, yoke_grip_r])

# 計器盤（アナログメーター2基 ＋ トグルスイッチ盤）
meter_l = bd.Location((-180.0, CON_Y + 40.0, CON_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=36, height=15)
meter_r = bd.Location(( 180.0, CON_Y + 40.0, CON_Z + 75.0), (-25, 0, 0)) * bd.Cylinder(radius=36, height=15)
switch_panel = bd.Location((0, CON_Y + 60.0, CON_Z + 80.0), (-25, 0, 0)) * bd.Box(180.0, 85.0, 10.0)
parts_console.extend([meter_l, meter_r, switch_panel])

# スロットルレバー (左手側)
throt_base = bd.Location((-260.0, Y_F + 220.0, 490.0)) * bd.Box(60.0, 100.0, 25.0)
throt_lever = bd.Location((-260.0, Y_F + 220.0, 545.0), (20, 0, 0)) * bd.Box(20.0, 35.0, 90.0)
parts_console.extend([throt_base, throt_lever])

print("4. パイロットシート & ラダーペダルをモデリング中...")
# シート座面・背もたれ
SEAT_Y = Y_R - 180.0
seat_cushion = bd.Location((0, SEAT_Y, 360.0)) * bd.Box(500.0, 440.0, 50.0)
seat_back    = bd.Location((0, SEAT_Y + 200.0, 620.0), (12, 0, 0)) * bd.Box(480.0, 45.0, 500.0)
seat_head    = bd.Location((0, SEAT_Y + 240.0, 910.0), (10, 0, 0)) * bd.Box(260.0, 55.0, 150.0)
parts_seat.extend([seat_cushion, seat_back, seat_head])

# ラダーペダル (フットレスト)
pedal_l = bd.Location((-130.0, Y_F + 60.0, 65.0), (-25, 0, 0)) * bd.Box(80.0, 130.0, 15.0)
pedal_r = bd.Location(( 130.0, Y_F + 60.0, 65.0), (-25, 0, 0)) * bd.Box(80.0, 130.0, 15.0)
parts_seat.extend([pedal_l, pedal_r])

# 左右サイドガードパネル (厚さ12mm 合板 / 段ボール)
panel_l = bd.Location((X_L - POST_T/2 - 6.0, 0, POST_H / 2)) * bd.Box(12.0, DEPTH + POST_T, POST_H)
panel_r = bd.Location((X_R + POST_T/2 + 6.0, 0, POST_H / 2)) * bd.Box(12.0, DEPTH + POST_T, POST_H)
parts_seat.extend([panel_l, panel_r])

# --------------------------------------------------------
# エクスポート
# --------------------------------------------------------
print("CADファイル（STEP / STL）をエクスポート中...")

# 骨組み単体
frame_compound = bd.Compound(parts_frame)
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))

# 全体アセンブリ
all_parts = parts_frame + parts_console + parts_seat
full_assembly = bd.Compound(all_parts)
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))

# 予備バックアップ
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_v3_pure_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_v3_pure_full.stl"))

print("エクスポート完了！")
