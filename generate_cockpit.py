import math
import os
import json
import build123d as bd

# ==========================================
# 操縦席 (Cockpit) CAD Generation Script
# Based on blackboard concept sketches:
# - Wooden frame (角材 30x30mm)
# - Cardboard walls (段ボール)
# - Clear wrap front canopy (ラップで視野確保)
# - Gullwing acrylic doors (アクリル板ドア ガルウィング)
# - Rear open/curtain for crew/external effects (外部効果・スタッフ)
# ==========================================

OUT_DIR = "/Users/y.jin/.gemini/antigravity/scratch/cockpit_cad"
os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------
# Main Dimensions (mm)
# ------------------------------------------
W = 900.0       # Overall Width (外幅)
L = 1500.0      # Overall Depth/Length (外奥行)
H = 1300.0      # Overall Height (全高)
T = 30.0        # Timber section (角材 30mm x 30mm)

# Functional Zones
Y_NOSE_END = 350.0      # Nose horizontal section end (ノーズ部後端)
Z_NOSE = 500.0          # Nose height (ノーズ上面高さ)
Y_CANOPY_END = 750.0    # Canopy slope end / Roof start (キャノピー傾斜終了・ルーフ開始)
Z_ROOF = 1300.0         # Roof height (ルーフ上面高さ)
Y_REAR = 1500.0         # Rear end (後端)

print("Building wooden frame parts...")

frame_parts = []
cut_list = []

def add_beam(name, dx, dy, dz, cx, cy, cz, rx=0.0, ry=0.0, rz=0.0):
    """Create a rectangular beam and place it using Location."""
    box = bd.Box(dx, dy, dz)
    loc = bd.Location((cx, cy, cz), (rx, ry, rz))
    b = loc * box
    frame_parts.append(b)
    # Record cut list length (maximum dimension)
    length = round(max(dx, dy, dz), 1)
    cut_list.append({"name": name, "length_mm": length, "qty": 1, "dx": dx, "dy": dy, "dz": dz})
    return b

# 1. Base Frame (底面枠)
# Left & Right Long Skids (左右土台桁: L=1500)
add_beam("底面縦桁(左)", T, L, T, T/2, L/2, T/2)
add_beam("底面縦桁(右)", T, L, T, W - T/2, L/2, T/2)
# Front, Mid, Rear Bottom Crossbars (横木: 長さ 840)
W_CROSS = W - 2*T
add_beam("底面横木(前)", W_CROSS, T, T, W/2, T/2, T/2)
add_beam("底面横木(キャノピー下)", W_CROSS, T, T, W/2, Y_CANOPY_END, T/2)
add_beam("底面横木(後)", W_CROSS, T, T, W/2, L - T/2, T/2)

# 2. Nose Uprights & Top Frame (ノーズ部: 高さ500, 奥行350)
H_NOSE_POST = Z_NOSE - 2*T
add_beam("ノーズ前柱(左)", T, T, H_NOSE_POST, T/2, T/2, T + H_NOSE_POST/2)
add_beam("ノーズ前柱(右)", T, T, H_NOSE_POST, W - T/2, T/2, T + H_NOSE_POST/2)
add_beam("ノーズ前上横木", W_CROSS, T, T, W/2, T/2, Z_NOSE - T/2)

# Nose Side Rails (ノーズ左右上面桁)
L_NOSE_SIDE = Y_NOSE_END - 2*T
add_beam("ノーズ上面桁(左)", T, L_NOSE_SIDE, T, T/2, T + L_NOSE_SIDE/2, Z_NOSE - T/2)
add_beam("ノーズ上面桁(右)", T, L_NOSE_SIDE, T, W - T/2, T + L_NOSE_SIDE/2, Z_NOSE - T/2)

# Nose Rear Post & Crossbar (ノーズ後部柱・横木)
add_beam("ノーズ後柱(左)", T, T, H_NOSE_POST, T/2, Y_NOSE_END - T/2, T + H_NOSE_POST/2)
add_beam("ノーズ後柱(右)", T, T, H_NOSE_POST, W - T/2, Y_NOSE_END - T/2, T + H_NOSE_POST/2)
add_beam("ノーズ後上横木", W_CROSS, T, T, W/2, Y_NOSE_END - T/2, Z_NOSE - T/2)

# 3. Main Pillars (キャノピー後端・ルーフ前端柱 Y=Y_CANOPY_END & 後端柱 Y=Y_REAR)
H_ROOF_POST = Z_ROOF - 2*T
add_beam("キャノピー後柱(左)", T, T, H_ROOF_POST, T/2, Y_CANOPY_END, T + H_ROOF_POST/2)
add_beam("キャノピー後柱(右)", T, T, H_ROOF_POST, W - T/2, Y_CANOPY_END, T + H_ROOF_POST/2)

add_beam("後部メイン柱(左)", T, T, H_ROOF_POST, T/2, L - T/2, T + H_ROOF_POST/2)
add_beam("後部メイン柱(右)", T, T, H_ROOF_POST, W - T/2, L - T/2, T + H_ROOF_POST/2)

# 4. Roof Frame (ルーフ枠)
add_beam("ルーフ前横木", W_CROSS, T, T, W/2, Y_CANOPY_END, Z_ROOF - T/2)
add_beam("ルーフ後横木", W_CROSS, T, T, W/2, L - T/2, Z_ROOF - T/2)
L_ROOF_SIDE = L - Y_CANOPY_END - T
add_beam("ルーフ上桁(左)", T, L_ROOF_SIDE, T, T/2, Y_CANOPY_END + T/2 + L_ROOF_SIDE/2, Z_ROOF - T/2)
add_beam("ルーフ上桁(右)", T, L_ROOF_SIDE, T, W - T/2, Y_CANOPY_END + T/2 + L_ROOF_SIDE/2, Z_ROOF - T/2)

# 5. Slanted Canopy Rafters (斜めキャノピー梁: Y_NOSE_END, Z_NOSE -> Y_CANOPY_END, Z_ROOF)
dY_canopy = Y_CANOPY_END - Y_NOSE_END  # 750 - 350 = 400
dZ_canopy = Z_ROOF - Z_NOSE            # 1300 - 500 = 800
L_rafter = math.sqrt(dY_canopy**2 + dZ_canopy**2)
pitch_angle = math.degrees(math.atan2(dZ_canopy, dY_canopy)) # ~63.4 degrees
rot_angle_x = -(90.0 - pitch_angle)

def add_slanted_rafter(name, x_pos):
    cy = (Y_NOSE_END + Y_CANOPY_END) / 2
    cz = (Z_NOSE + Z_ROOF) / 2
    b = bd.Location((x_pos, cy, cz), (rot_angle_x, 0, 0)) * bd.Box(T, T, L_rafter)
    frame_parts.append(b)
    cut_list.append({"name": name, "length_mm": round(L_rafter, 1), "qty": 1, "dx": T, "dy": T, "dz": round(L_rafter, 1)})
    return b

add_slanted_rafter("キャノピー斜め梁(左)", T/2)
add_slanted_rafter("キャノピー斜め梁(右)", W - T/2)
add_slanted_rafter("キャノピー中央補強梁", W/2)

# 6. Cockpit Seat and Console Substructure (内部シート・操縦桿台)
H_SEAT = 350.0
W_SEAT = 450.0
L_SEAT = 450.0
Y_SEAT = 850.0
X_SEAT_CENTER = W / 2

add_beam("座席台脚(左前)", T, T, H_SEAT - T, X_SEAT_CENTER - W_SEAT/2 + T/2, Y_SEAT + T/2, (H_SEAT - T)/2 + T)
add_beam("座席台脚(右前)", T, T, H_SEAT - T, X_SEAT_CENTER + W_SEAT/2 - T/2, Y_SEAT + T/2, (H_SEAT - T)/2 + T)
add_beam("座席台脚(左後)", T, T, H_SEAT - T, X_SEAT_CENTER - W_SEAT/2 + T/2, Y_SEAT + L_SEAT - T/2, (H_SEAT - T)/2 + T)
add_beam("座席台脚(右後)", T, T, H_SEAT - T, X_SEAT_CENTER + W_SEAT/2 - T/2, Y_SEAT + L_SEAT - T/2, (H_SEAT - T)/2 + T)
add_beam("座席座面受木(前)", W_SEAT, T, T, X_SEAT_CENTER, Y_SEAT + T/2, H_SEAT - T/2)
add_beam("座席座面受木(後)", W_SEAT, T, T, X_SEAT_CENTER, Y_SEAT + L_SEAT - T/2, H_SEAT - T/2)

# Control Console Desk (計器盤・操縦桿テーブル)
add_beam("計器台横木", W_CROSS, T, T, W/2, 550.0, 550.0)

print(f"Wooden frame beams generated: {len(frame_parts)} parts.")

# ------------------------------------------
# Panels & Functional Enclosure (外装・内装パネル)
# ------------------------------------------
panel_parts = []
cardboard_parts = []
acrylic_parts = []
wrap_parts = []

T_CARD = 5.0
T_ACRYL = 3.0

# 1. Front Nose Bottom Panel (段ボール: 正面前下面)
p_front_nose = bd.Location((W/2, -T_CARD/2, Z_NOSE/2)) * bd.Box(W, T_CARD, Z_NOSE)
cardboard_parts.append(p_front_nose)

# 2. Nose Top Deck Panel (段ボール: ノーズ上面カバー)
p_nose_top = bd.Location((W/2, Y_NOSE_END/2, Z_NOSE + T_CARD/2)) * bd.Box(W, Y_NOSE_END, T_CARD)
cardboard_parts.append(p_nose_top)

# 3. Lower Side Panels (段ボール: 左右下部壁 Z=0..500, Y=0..1500)
p_side_l = bd.Location((-T_CARD/2, L/2, Z_NOSE/2)) * bd.Box(T_CARD, L, Z_NOSE)
cardboard_parts.append(p_side_l)

p_side_r = bd.Location((W + T_CARD/2, L/2, Z_NOSE/2)) * bd.Box(T_CARD, L, Z_NOSE)
cardboard_parts.append(p_side_r)

# 4. Rear Lower Wall & Curtain (段ボール/カーテン)
p_rear_l = bd.Location((75.0, L + T_CARD/2, Z_ROOF/2)) * bd.Box(150.0, T_CARD, Z_ROOF)
cardboard_parts.append(p_rear_l)

p_rear_r = bd.Location((W - 75.0, L + T_CARD/2, Z_ROOF/2)) * bd.Box(150.0, T_CARD, Z_ROOF)
cardboard_parts.append(p_rear_r)

# Curtain (後部カーテン: 開口幅 600mm)
p_curtain = bd.Location((W/2, L + 1.0, (Z_ROOF - 50.0)/2)) * bd.Box(600.0, 2.0, Z_ROOF - 50.0)
panel_parts.append(p_curtain)

# 5. Clear Wrap Canopy (食品用/梱包用ラップ風防: 傾斜窓)
cy = (Y_NOSE_END + Y_CANOPY_END) / 2
cz = (Z_NOSE + Z_ROOF) / 2
p_windshield = bd.Location((W/2, cy, cz + 2.0), (rot_angle_x, 0, 0)) * bd.Box(W, 2.0, L_rafter)
wrap_parts.append(p_windshield)

# 6. Gullwing Doors (アクリル板ガルウィングドア: 左右)
DOOR_L = L - Y_CANOPY_END
DOOR_H = Z_ROOF - Z_NOSE

p_door_l = bd.Location((-T_ACRYL/2, Y_CANOPY_END + DOOR_L/2, Z_NOSE + DOOR_H/2)) * bd.Box(T_ACRYL, DOOR_L, DOOR_H)
acrylic_parts.append(p_door_l)

p_door_r = bd.Location((W + T_ACRYL/2, Y_CANOPY_END + DOOR_L/2, Z_NOSE + DOOR_H/2)) * bd.Box(T_ACRYL, DOOR_L, DOOR_H)
acrylic_parts.append(p_door_r)

# 7. Interior Seat Cushion & Flight Stick
p_seat_cushion = bd.Location((X_SEAT_CENTER, Y_SEAT + L_SEAT/2, H_SEAT + 25.0)) * bd.Box(W_SEAT, L_SEAT, 50.0)
panel_parts.append(p_seat_cushion)

p_seat_back = bd.Location((X_SEAT_CENTER, Y_SEAT + L_SEAT - 20.0, H_SEAT + 250.0), (10.0, 0, 0)) * bd.Box(W_SEAT, 40.0, 500.0)
panel_parts.append(p_seat_back)

# Flight Joystick
stick_base = bd.Location((W/2, 600.0, 560.0)) * bd.Cylinder(radius=40, height=20)
stick_rod = bd.Location((W/2, 600.0, 560.0 + 90.0)) * bd.Cylinder(radius=12, height=160)
stick_grip = bd.Location((W/2, 605.0, 560.0 + 180.0)) * bd.Box(30, 40, 70)
panel_parts.extend([stick_base, stick_rod, stick_grip])

all_panels = panel_parts + cardboard_parts + acrylic_parts + wrap_parts

# ------------------------------------------
# Combine and Export
# ------------------------------------------
print("Exporting CAD files...")

# Frame Compound
frame_compound = bd.Compound(frame_parts)
bd.export_step(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.step"))
bd.export_stl(frame_compound, os.path.join(OUT_DIR, "cockpit_frame.stl"))
print("Exported: cockpit_frame.step, cockpit_frame.stl")

# Panels Compound
panel_compound = bd.Compound(all_panels)
bd.export_step(panel_compound, os.path.join(OUT_DIR, "cockpit_panels.step"))
bd.export_stl(panel_compound, os.path.join(OUT_DIR, "cockpit_panels.stl"))
print("Exported: cockpit_panels.step, cockpit_panels.stl")

# Full Assembly Compound
full_assembly = bd.Compound(frame_parts + all_panels)
bd.export_step(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.step"))
bd.export_stl(full_assembly, os.path.join(OUT_DIR, "cockpit_assembly_full.stl"))
print("Exported: cockpit_assembly_full.step, cockpit_assembly_full.stl")

# ------------------------------------------
# Wood Optimization & Cut List Calculation
# ------------------------------------------
total_wood_length = sum(item["length_mm"] * item["qty"] for item in cut_list)
print(f"Total wooden beam length needed: {total_wood_length:.1f} mm ({total_wood_length/1000:.2f} m)")

# Group identical parts
grouped_cut_list = {}
for item in cut_list:
    key = (item["name"], item["length_mm"])
    if key not in grouped_cut_list:
        grouped_cut_list[key] = {"name": item["name"], "length_mm": item["length_mm"], "qty": 0}
    grouped_cut_list[key]["qty"] += item["qty"]

# Stock cutting simulation (standard 3000mm and 4000mm lumber)
def cutting_stock_greedy(cuts, stock_length=3000, saw_kerf=3):
    items = []
    for c in cuts:
        items.extend([{"name": c["name"], "len": c["length_mm"]}] * c["qty"])
    items.sort(key=lambda x: x["len"], reverse=True)
    
    stocks = []
    for item in items:
        placed = False
        for stock in stocks:
            remaining = stock["remaining"]
            if remaining >= item["len"]:
                stock["cuts"].append(item)
                stock["remaining"] -= (item["len"] + saw_kerf)
                placed = True
                break
        if not placed:
            stocks.append({
                "cuts": [item],
                "remaining": stock_length - (item["len"] + saw_kerf)
            })
    return stocks

stock_3m = cutting_stock_greedy(list(grouped_cut_list.values()), stock_length=3000)
stock_4m = cutting_stock_greedy(list(grouped_cut_list.values()), stock_length=4000)

summary_data = {
    "dimensions_mm": {"width": W, "length": L, "height": H, "timber_cross_section": f"{T}x{T}"},
    "total_wood_length_m": round(total_wood_length / 1000, 2),
    "stock_3m_required": len(stock_3m),
    "stock_4m_required": len(stock_4m),
    "cut_list": list(grouped_cut_list.values()),
    "cutting_plan_3m": [
        {
            "stock_id": i + 1,
            "cuts": [c["name"] + f" ({c['len']}mm)" for c in s["cuts"]],
            "used_mm": 3000 - s["remaining"],
            "remaining_mm": s["remaining"]
        }
        for i, s in enumerate(stock_3m)
    ],
    "cutting_plan_4m": [
        {
            "stock_id": i + 1,
            "cuts": [c["name"] + f" ({c['len']}mm)" for c in s["cuts"]],
            "used_mm": 4000 - s["remaining"],
            "remaining_mm": s["remaining"]
        }
        for i, s in enumerate(stock_4m)
    ]
}

with open(os.path.join(OUT_DIR, "cut_list.json"), "w", encoding="utf-8") as f:
    json.dump(summary_data, f, ensure_ascii=False, indent=2)

print(f"Stock 3m required: {len(stock_3m)} bars")
print(f"Stock 4m required: {len(stock_4m)} bars")
print("CAD generation completed successfully!")
