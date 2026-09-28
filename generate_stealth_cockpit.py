import math
import os
import json
import build123d as bd

# ========================================================
# 操縦席 (Cockpit) Mk-II: ステルス戦闘機 & SFメカスタイル
# ========================================================
# 特徴:
# - ステルス戦闘機（F-22/F-35風）多面体ウェッジシェイプ
# - 前方3面パノラマ・キャノピー（ラップで広い視野確保）
# - スタイリッシュ・ガルウィングドア（アクリル板×2枚）
# - 後部ツイン・アフターバーナーノズル（スタッフ外部効果投入口）
# - 内装: HUD (ヘッドアップディスプレイ), 3連MFD計器盤,
#        HOTAS (フライトスティック+ツインスロットル),
#        戦闘機バケットシート, ラダーペダル
# ========================================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

T = 30.0  # 角材 30mm x 30mm

frame_parts = []
cut_list = []

def add_beam_between(name, p1, p2):
    """Create a 30x30mm beam connecting p1 to p2."""
    v1 = bd.Vector(p1)
    v2 = bd.Vector(p2)
    diff = v2 - v1
    length = diff.length
    if length < 1.0:
        return None
    mid = (v1 + v2) / 2
    # Create Plane with z_dir aligned with diff
    plane = bd.Plane(origin=(mid.X, mid.Y, mid.Z), z_dir=diff)
    b = plane * bd.Box(T, T, length)
    frame_parts.append(b)
    cut_list.append({
        "name": name,
        "length_mm": round(length, 1),
        "qty": 1,
        "p1": [round(v1.X,1), round(v1.Y,1), round(v1.Z,1)],
        "p2": [round(v2.X,1), round(v2.Y,1), round(v2.Z,1)]
    })
    return b

# --------------------------------------------------------
# 骨組みノード座標定義 (X: 左右幅, Y: 前後奥行, Z: 上下高さ)
# 原点(0,0,0)は底面中央前端
# --------------------------------------------------------
# 前後ステーション
Y0 = 0.0      # ノーズ先端
Y1 = 400.0    # ノーズ後端 / キャノピー基部
Y2 = 950.0    # キャノピー頂点 / ルーフ前端
Y3 = 1600.0   # 後端

# 高さステーション
Z_BOT = T/2   # 15mm (底面)
Z_MID = 460.0 # ショルダーライン (ウェスト張り出し)
Z_TOP = 1250.0# ルーフ頂点

# 1. 底面フレームノード (Z = Z_BOT)
# 先端幅 500 (±250), ノーズ後端幅 640 (±320), キャノピー下幅 740 (±370), 後端幅 740 (±370)
B0_L = (-250, Y0, Z_BOT)
B0_R = ( 250, Y0, Z_BOT)
B1_L = (-320, Y1, Z_BOT)
B1_R = ( 320, Y1, Z_BOT)
B2_L = (-370, Y2, Z_BOT)
B2_R = ( 370, Y2, Z_BOT)
B3_L = (-370, Y3, Z_BOT)
B3_R = ( 370, Y3, Z_BOT)

# 2. ショルダーライン (ウェスト張り出しノード, Z = Z_MID)
# 先端幅 540 (±270), ノーズ後端幅 740 (±370), キャノピー頂点幅 960 (±480), 後端幅 880 (±440)
S0_L = (-270, Y0, Z_MID)
S0_R = ( 270, Y0, Z_MID)
S1_L = (-370, Y1, Z_MID)
S1_R = ( 370, Y1, Z_MID)
S2_L = (-480, Y2, Z_MID)
S2_R = ( 480, Y2, Z_MID)
S3_L = (-440, Y3, Z_MID)
S3_R = ( 440, Y3, Z_MID)

# 3. ルーフノード (Z = Z_TOP)
# キャノピー頂点幅 640 (±320), ルーフ後端幅 640 (±320)
R2_L = (-320, Y2, Z_TOP)
R2_R = ( 320, Y2, Z_TOP)
R3_L = (-320, Y3, Z_TOP)
R3_R = ( 320, Y3, Z_TOP)

# キャノピー中央頂点
R2_C = ( 0.0, Y2, Z_TOP + 30.0)
S1_C = ( 0.0, Y1, Z_MID + 30.0)

print("Assembling Stealth Airframe Beams...")

# --- A. 底面レール ---
add_beam_between("底面レール(左ノーズ)", B0_L, B1_L)
add_beam_between("底面レール(右ノーズ)", B0_R, B1_R)
add_beam_between("底面レール(左キャノピー)", B1_L, B2_L)
add_beam_between("底面レール(右キャノピー)", B1_R, B2_R)
add_beam_between("底面レール(左リア)", B2_L, B3_L)
add_beam_between("底面レール(右リア)", B2_R, B3_R)

# 底面横木
add_beam_between("底面横木(先端)", B0_L, B0_R)
add_beam_between("底面横木(ノーズ部)", B1_L, B1_R)
add_beam_between("底面横木(コクピット下)", B2_L, B2_R)
add_beam_between("底面横木(リア後端)", B3_L, B3_R)

# --- B. 下部支柱 & ショルダーライン (外側にハの字傾斜) ---
add_beam_between("ノーズ前支柱(左)", B0_L, S0_L)
add_beam_between("ノーズ前支柱(右)", B0_R, S0_R)
add_beam_between("ノーズ後支柱(左)", B1_L, S1_L)
add_beam_between("ノーズ後支柱(右)", B1_R, S1_R)
add_beam_between("センター支柱(左)", B2_L, S2_L)
add_beam_between("センター支柱(右)", B2_R, S2_R)
add_beam_between("リア支柱(左)", B3_L, S3_L)
add_beam_between("リア支柱(右)", B3_R, S3_R)

# ショルダーレール (前後)
add_beam_between("ショルダー桁(左ノーズ)", S0_L, S1_L)
add_beam_between("ショルダー桁(右ノーズ)", S0_R, S1_R)
add_beam_between("ショルダー桁(左キャノピー)", S1_L, S2_L)
add_beam_between("ショルダー桁(右キャノピー)", S1_R, S2_R)
add_beam_between("ショルダー桁(左リア)", S2_L, S3_L)
add_beam_between("ショルダー桁(右リア)", S2_R, S3_R)

# ショルダー横木
add_beam_between("ショルダー横木(先端)", S0_L, S0_R)
add_beam_between("ショルダー横木(ノーズ後)", S1_L, S1_R)

# --- C. キャノピー斜めピラー (Aピラー) & ルーフ ---
add_beam_between("Aピラー傾斜梁(左)", S1_L, R2_L)
add_beam_between("Aピラー傾斜梁(右)", S1_R, R2_R)
add_beam_between("キャノピー中央キール梁", S1_C, R2_C)

# ルーフ桁
add_beam_between("ルーフ前横木", R2_L, R2_R)
add_beam_between("ルーフ後横木", R3_L, R3_R)
add_beam_between("ルーフサイド桁(左)", R2_L, R3_L)
add_beam_between("ルーフサイド桁(右)", R2_R, R3_R)

# ルーフからリアへのCピラー
add_beam_between("Cピラー支柱(左)", R3_L, S3_L)
add_beam_between("Cピラー支柱(右)", R3_R, S3_R)

# --- D. コクピット内部構造 (座席・計器台) ---
# 計器台ビーム (Y=650, Z=580)
I_L = (-350, 650.0, 580.0)
I_R = ( 350, 650.0, 580.0)
add_beam_between("計器コンソール横木", I_L, I_R)

# シートサポートビーム (Y=1050, Z=350)
ST_L = (-250, 1050.0, 350.0)
ST_R = ( 250, 1050.0, 350.0)
add_beam_between("座席フロントサポート", ST_L, ST_R)
add_beam_between("座席フロント脚(左)", (-250, 1050.0, Z_BOT), ST_L)
add_beam_between("座席フロント脚(右)", ( 250, 1050.0, Z_BOT), ST_R)

STB_L = (-250, 1450.0, 350.0)
STB_R = ( 250, 1450.0, 350.0)
add_beam_between("座席リアサポート", STB_L, STB_R)
add_beam_between("座席リア脚(左)", (-250, 1450.0, Z_BOT), STB_L)
add_beam_between("座席リア脚(右)", ( 250, 1450.0, Z_BOT), STB_R)

print(f"Total frame beams: {len(frame_parts)}")

# --------------------------------------------------------
# 外装パネル・パーツ群 (段ボール, アクリル, ラップ, 内装)
# --------------------------------------------------------
panel_parts = []
cardboard_parts = []
acrylic_parts = []
wrap_parts = []

# 1. ノーズ・サイドポッド (段ボール)
# ノーズ上面
p_nose_deck = bd.Location((0, Y1/2, Z_MID + 2)) * bd.Box(540, Y1, 5)
cardboard_parts.append(p_nose_deck)

# ノーズ先端前パネル
p_nose_front = bd.Location((0, Y0, Z_MID/2)) * bd.Box(500, 5, Z_MID)
cardboard_parts.append(p_nose_front)

# カナード翼 (左右のエアロフィン: 段ボール)
canard_l = bd.Location((-380, 250, Z_MID + 10), (0, -5, -15)) * bd.Box(180, 220, 10)
canard_r = bd.Location(( 380, 250, Z_MID + 10), (0, -5,  15)) * bd.Box(180, 220, 10)
cardboard_parts.extend([canard_l, canard_r])

# 下部サイドパネル (左右外側)
side_l = bd.Location((-360, (Y1+Y3)/2, Z_MID/2)) * bd.Box(10, Y3-Y1, Z_MID)
side_r = bd.Location(( 360, (Y1+Y3)/2, Z_MID/2)) * bd.Box(10, Y3-Y1, Z_MID)
cardboard_parts.extend([side_l, side_r])

# 2. 前面3面キャノピー (ラップで視野確保)
# 正面傾斜窓
p_front_windshield = bd.Location((0, (Y1+Y2)/2, (Z_MID+Z_TOP)/2 + 10), (-52, 0, 0)) * bd.Box(640, 2, 850)
wrap_parts.append(p_front_windshield)

# 3. アクリル製ガルウィングドア (左右2枚)
# Y2..Y3 (950..1600 = 650mm), 高さ: Z_MID..Z_TOP (800mm)
# アクリル厚3mm
door_l = bd.Location((-400, (Y2+Y3)/2, (Z_MID+Z_TOP)/2)) * bd.Box(4, Y3-Y2, Z_TOP-Z_MID)
door_r = bd.Location(( 400, (Y2+Y3)/2, (Z_MID+Z_TOP)/2)) * bd.Box(4, Y3-Y2, Z_TOP-Z_MID)
acrylic_parts.extend([door_l, door_r])

# 4. 後部：ツイン・アフターバーナーノズル (スタッフ外部効果用ポート)
# 直径 280mm, 長さ 150mm の円筒ノズルが2基
nozzle_l_outer = bd.Location((-200, Y3 + 75, 450), (90, 0, 0)) * bd.Cylinder(radius=140, height=150)
nozzle_r_outer = bd.Location(( 200, Y3 + 75, 450), (90, 0, 0)) * bd.Cylinder(radius=140, height=150)
cardboard_parts.extend([nozzle_l_outer, nozzle_r_outer])

# 後部バックプレート (ノズル周囲を囲むリアバルクヘッド)
rear_plate = bd.Location((0, Y3 + 2, Z_TOP/2)) * bd.Box(740, 6, Z_TOP)
cardboard_parts.append(rear_plate)

# 5. 内装 (HUD, 3連MFD計器盤, HOTAS, バケットシート, ペダル)
# HUD (透明アクリルパネル)
hud_glass = bd.Location((0, 720.0, 780.0), (-35, 0, 0)) * bd.Box(260, 4, 180)
acrylic_parts.append(hud_glass)

# 3連MFD計器盤 (センター・左・右)
mfd_center = bd.Location((0, 660.0, 650.0), (-25, 0, 0)) * bd.Box(280, 20, 160)
mfd_left   = bd.Location((-240, 680.0, 640.0), (-25, -20, 0)) * bd.Box(180, 20, 140)
mfd_right  = bd.Location(( 240, 680.0, 640.0), (-25,  20, 0)) * bd.Box(180, 20, 140)
panel_parts.extend([mfd_center, mfd_left, mfd_right])

# HOTAS 操縦系
# 右手フライトスティック
stick_base = bd.Location((220, 850.0, 480.0)) * bd.Box(80, 80, 30)
stick_grip = bd.Location((220, 860.0, 580.0)) * bd.Box(35, 45, 160)
panel_parts.extend([stick_base, stick_grip])

# 左手ツインスロットル
throttle_base = bd.Location((-220, 850.0, 480.0)) * bd.Box(90, 120, 30)
throttle_lever1 = bd.Location((-235, 840.0, 550.0), (15, 0, 0)) * bd.Box(25, 50, 100)
throttle_lever2 = bd.Location((-205, 860.0, 550.0), (-10, 0, 0)) * bd.Box(25, 50, 100)
panel_parts.extend([throttle_base, throttle_lever1, throttle_lever2])

# フットペダル (ラダーペダル)
pedal_l = bd.Location((-140, 480.0, 120.0), (-30, 0, 0)) * bd.Box(90, 140, 20)
pedal_r = bd.Location(( 140, 480.0, 120.0), (-30, 0, 0)) * bd.Box(90, 140, 20)
panel_parts.extend([pedal_l, pedal_r])

# 戦闘機バケットシート
seat_cushion = bd.Location((0, 1220.0, 380.0)) * bd.Box(460, 440, 60)
seat_back    = bd.Location((0, 1420.0, 680.0), (15, 0, 0)) * bd.Box(460, 50, 580)
headrest     = bd.Location((0, 1480.0, 1010.0), (12, 0, 0)) * bd.Box(260, 60, 160)
# ショルダーサポート (左右バケットホールド)
side_support_l = bd.Location((-210, 1370.0, 680.0), (15, -20, 0)) * bd.Box(80, 120, 450)
side_support_r = bd.Location(( 210, 1370.0, 680.0), (15,  20, 0)) * bd.Box(80, 120, 450)
panel_parts.extend([seat_cushion, seat_back, headrest, side_support_l, side_support_r])

# --------------------------------------------------------
# エクスポート
# --------------------------------------------------------
print("Exporting CAD models...")

frame_compound = bd.Compound(frame_parts)
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_stealth_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_stealth_frame.stl"))

all_panels = panel_parts + cardboard_parts + acrylic_parts + wrap_parts
panels_compound = bd.Compound(all_panels)
bd.export_step(panels_compound, os.path.join(OUT_DIR, "cockpit_stealth_panels.step"))
bd.export_stl(panels_compound, os.path.join(OUT_DIR, "cockpit_stealth_panels.stl"))

full_stealth = bd.Compound(frame_parts + all_panels)
bd.export_step(full_stealth, os.path.join(OUT_DIR, "cockpit_stealth_full.step"))
bd.export_stl(full_stealth, os.path.join(OUT_DIR, "cockpit_stealth_full.stl"))

# Also update the primary files for convenience
bd.export_step(full_stealth, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_stealth, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))

print("Export completed successfully!")

# 木材カットリスト集計
total_wood = sum(c["length_mm"] for c in cut_list)
print(f"Total wooden beam length: {total_wood:.1f} mm ({total_wood/1000:.2f} m)")
print(f"Number of frame elements: {len(cut_list)}")
