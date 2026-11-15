"""Case for an ESP32-C6-DevKitC-1 used as an ESB Networks P1 reader.

Generates base.stl and lid.stl next to this file:

    pip install manifold3d trimesh numpy
    python case.py

All sizes are in millimetres. Change the parameters below and run it again.
Board dimensions come from Espressif's drawing, esp32-c6-devkitc-1-dimensions_v1.2.

Coordinates: x across the case, y along it (y = 0 is the end with the USB
ports and the cable entry, which should face down when mounted), z up from
the back of the case (the side that goes against the cabinet wall).
"""

from pathlib import Path

import numpy as np
import trimesh
from manifold3d import CrossSection, Error, JoinType, Manifold, Mesh

# --- Board (Espressif drawing v1.2) ---------------------------------------
PCB_W = 25.4          # board width
PCB_L = 51.8          # board length, not counting the antenna
PCB_T = 1.6           # board thickness
ANT_OVERHANG = 6.35   # module antenna sticking out past the board's top edge
MODULE_W = 18.0       # module width, centred on the board
MODULE_PCB_T = 0.8    # thickness of the module's own board (antenna overhang)
USB_X = 19.88         # centre of the port labelled "USB", from the board's left edge
USB_Z = 1.6           # centre of the USB-C socket above the board's top surface

# --- Case -------------------------------------------------------------------
WALL = 2.0            # side and end walls
FLOOR = 2.0           # back of the case
LID_T = 2.0           # lid plate
CORNER_R = 2.5        # rounding of the outside vertical edges

BELOW = 24.0          # space under the board for Dupont plugs on the header pins
ABOVE = 8.0           # space above the board's top surface
CHANNEL = 9.0         # wiring channel beside the board, where the cable comes in

GAP_LEFT = 0.4        # clearances around the board
GAP_RIGHT = 0.6
GAP_USB_END = 0.3
GAP_TOP = 0.8

USB_OPENING = (11.5, 7.0)   # width, height of the opening for a USB-C plug
CABLE = (7.0, 4.5)          # width, height of the opening for the RJ12 cable
DRAIN_D = 3.0               # drain hole in the bottom end wall

LIP_H = 3.5           # lid lip that drops inside the walls
LIP_T = 1.2
LID_CLEAR = 0.2       # gap between lid lip and walls
SNAP = 0.45           # how far the snap bumps stand proud of the lip
POST_GAP = 0.15       # gap left between the lid's hold-down posts and the board

# Clips: one springy arm on each long side of the lid runs down the outside of
# the base and hooks under the back edge. They need nothing on the base, so a
# base printed before the clips were added still works.
CLIP_W = 12.0         # width of each arm
CLIP_T = 2.0          # arm thickness
CLIP_GAP = 0.2        # gap between arm and the base's side wall
HOOK = 1.0            # how far the hook reaches under the back edge
HOOK_T = 1.5          # hook thickness
HOOK_GAP = 0.1        # play between hook and the back of the case

EAR_LEN = 9.0         # mounting ears at each end, for a strap or cable ties
EAR_W = 22.0
EAR_T = 2.5
SLOT = (12.0, 3.5)

# --- Derived sizes -----------------------------------------------------------
IN_W = CHANNEL + GAP_LEFT + PCB_W + GAP_RIGHT
IN_L = GAP_USB_END + PCB_L + ANT_OVERHANG + GAP_TOP
IN_H = BELOW + PCB_T + ABOVE
OUT_W = IN_W + 2 * WALL
OUT_L = IN_L + 2 * WALL
BASE_H = FLOOR + IN_H

BX = WALL + CHANNEL + GAP_LEFT   # board's left edge
BY = WALL + GAP_USB_END          # board's USB edge
BZ = FLOOR + BELOW               # underside of the board
PCB_TOP = BZ + PCB_T


def box(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def rounded_prism(w, l, h, r):
    xs = CrossSection.square([w - 2 * r, l - 2 * r]).translate([r, r])
    xs = xs.offset(r, JoinType.Round, circular_segments=48)
    return Manifold.extrude(xs, h)


def cylinder_y(x, z, d, y0, y1):
    """A cylinder running along y, centred on (x, z)."""
    c = Manifold.cylinder(y1 - y0, d / 2, circular_segments=40)
    return c.rotate([-90, 0, 0]).translate([x, y0, z])


def base():
    shell = rounded_prism(OUT_W, OUT_L, BASE_H, CORNER_R)
    shell -= box(WALL, WALL, FLOOR, WALL + IN_W, WALL + IN_L, BASE_H + 1)

    # Mounting ears on the back plane, one at each end, with a strap slot.
    # Each ear overlaps the case by 3 mm so it fuses with the end wall.
    ex = (OUT_W - EAR_W) / 2
    for y0 in (-EAR_LEN, OUT_L - 3.0):
        ear = rounded_prism(EAR_W, EAR_LEN + 3.0, EAR_T, 2.0).translate([ex, y0, 0])
        slot_y = (-EAR_LEN / 2 - SLOT[1] / 2) if y0 < 0 else (OUT_L + EAR_LEN / 2 - SLOT[1] / 2)
        ear -= box((OUT_W - SLOT[0]) / 2, slot_y, -1, (OUT_W + SLOT[0]) / 2, slot_y + SLOT[1], EAR_T + 1)
        shell += ear
    shell -= box(WALL, WALL, FLOOR, WALL + IN_W, WALL + IN_L, BASE_H + 1)

    # Support under the board at the USB end, between the two USB sockets.
    shell += box(BX + 11.0, BY + 0.8, FLOOR - 0.01, BX + 14.3, BY + 8.5, BZ)
    # Support under the root of the antenna overhang, with side guides
    # either side of the module. It also stops the board sliding up.
    y0, y1 = BY + PCB_L + 0.4, BY + PCB_L + 2.0
    m0 = BX + (PCB_W - MODULE_W) / 2
    m1 = m0 + MODULE_W
    shell += box(m0 - 0.3, y0, FLOOR - 0.01, m1 + 0.3, y1, PCB_TOP)
    for x0 in (m0 - 1.3, m1 + 0.3):
        shell += box(x0, y0, FLOOR - 0.01, x0 + 1.0, y1, PCB_TOP + MODULE_PCB_T + 0.5)
    # Guide for the board's left edge, in the pin-free stretch near the USB end.
    shell += box(BX - GAP_LEFT - 1.2, BY + 2.0, FLOOR - 0.01, BX - GAP_LEFT, BY + 8.0, PCB_TOP + 1.0)

    # Bottom end wall: USB-C opening, cable opening (closed by the lid's tab), drain.
    ux = BX + USB_X
    uz = PCB_TOP + USB_Z
    shell -= box(ux - USB_OPENING[0] / 2, -1, uz - USB_OPENING[1] / 2,
                 ux + USB_OPENING[0] / 2, WALL + 1, uz + USB_OPENING[1] / 2)
    cx = WALL + CHANNEL / 2
    cable_floor = BZ - 1.0
    shell -= box(cx - CABLE[0] / 2, -1, cable_floor, cx + CABLE[0] / 2, WALL + 1, BASE_H + 1)
    shell -= cylinder_y(BX + 8.0, FLOOR + DRAIN_D / 2 + 1.0, DRAIN_D, -1, WALL + 1)

    # Grooves for the lid's snap bumps, on the inside of both long walls.
    gz = BASE_H - LIP_H / 2
    for yc in (OUT_L * 0.3, OUT_L * 0.7):
        for x0 in (WALL - 0.6, OUT_W - WALL):
            shell -= box(x0, yc - 8.0, gz - 0.6, x0 + 0.6, yc + 8.0, gz + 0.6)
    return shell, cable_floor


def lid(cable_floor):
    plate = rounded_prism(OUT_W, OUT_L, LID_T, CORNER_R).translate([0, 0, BASE_H])
    z0 = BASE_H - LIP_H

    # Lip that drops inside the walls.
    x0, y0 = WALL + LID_CLEAR, WALL + LID_CLEAR
    x1, y1 = OUT_W - WALL - LID_CLEAR, OUT_L - WALL - LID_CLEAR
    lip = box(x0, y0, z0, x1, y1, BASE_H + 0.01)
    lip -= box(x0 + LIP_T, y0 + LIP_T, z0 - 1, x1 - LIP_T, y1 - LIP_T, BASE_H + 1)
    part = plate + lip

    # Snap bumps on the lip, matching the base's grooves.
    gz = BASE_H - LIP_H / 2
    for yc in (OUT_L * 0.3, OUT_L * 0.7):
        part += box(x0 - SNAP, yc - 7.0, gz - 0.45, x0, yc + 7.0, gz + 0.45)
        part += box(x1, yc - 7.0, gz - 0.45, x1 + SNAP, yc + 7.0, gz + 0.45)

    # Tab that closes the cable opening down to the cable's height.
    cx = WALL + CHANNEL / 2
    part += box(cx - CABLE[0] / 2 + 0.2, 0, cable_floor + CABLE[1],
                cx + CABLE[0] / 2 - 0.2, WALL, BASE_H + 0.01)

    # Hold-down posts: one between the USB sockets, one on the antenna overhang.
    part += box(BX + 11.0, BY + 0.8, PCB_TOP + POST_GAP, BX + 14.3, BY + 2.6, BASE_H + 0.01)
    part += box(BX + 10.0, BY + PCB_L + 0.4, PCB_TOP + MODULE_PCB_T + POST_GAP,
                BX + 15.4, BY + PCB_L + 2.0, BASE_H + 0.01)
    part += clips()
    return part


def xz_prism(points, y_centre, width):
    """Extrude a convex polygon drawn in the x-z plane along y, centred on y_centre.

    Built directly from vertices (rather than extruded and rotated) so every
    coordinate is exact and the faces line up with the rest of the lid.
    """
    pts = list(points)
    area = sum(x0 * z1 - x1 * z0 for (x0, z0), (x1, z1) in zip(pts, pts[1:] + pts[:1]))
    if area < 0:
        pts.reverse()
    n = len(pts)
    y0, y1 = y_centre - width / 2, y_centre + width / 2
    verts = [(x, y0, z) for x, z in pts] + [(x, y1, z) for x, z in pts]
    tris = []
    for k in range(1, n - 1):
        tris.append((0, k, k + 1))               # cap at y0, facing -y
        tris.append((n, n + k + 1, n + k))       # cap at y1, facing +y
    for k in range(n):
        a, b = k, (k + 1) % n
        tris.append((a, n + a, n + b))
        tris.append((a, n + b, b))
    mesh = Mesh(vert_properties=np.array(verts, dtype=np.float32), tri_verts=np.array(tris, dtype=np.uint32))
    m = Manifold(mesh)
    if m.volume() < 0 or m.status() != Error.NoError:
        raise ValueError("bad prism")
    return m


def clips():
    """Two clip arms, attached to the lid plate, in assembled coordinates."""
    part = Manifold()
    yc = OUT_L / 2
    top = BASE_H + LID_T
    z_hook = -HOOK_GAP
    z_end = z_hook - HOOK_T
    for side in (-1, 1):
        def x(v):
            # v is measured outward from the side wall; flip it for the right side.
            return -v if side < 0 else OUT_W + v
        a_in, a_out = CLIP_GAP, CLIP_GAP + CLIP_T
        # Arm, from the lid plate down past the back of the case.
        arm = [(x(a_in), z_end), (x(a_out), z_end), (x(a_out), top), (x(a_in), top)]
        # Bridge joining the arm to the lid plate.
        bridge = [(x(a_out), BASE_H), (x(-1.5), BASE_H), (x(-1.5), top), (x(a_out), top)]
        # Hook under the back edge, with a sloped lead-in so it rides over the
        # wall as the lid is pressed on.
        hook = [(x(a_in), z_hook), (x(-HOOK), z_hook), (x(-HOOK), z_hook - 0.3), (x(a_in), z_end)]
        # Pull tab at the tip, to flick the arm outward when taking the lid off.
        tab = [(x(a_out), z_end), (x(a_out + 2.0), z_end), (x(a_out + 2.0), z_end + 1.0), (x(a_out), z_end + 4.0)]
        for poly in (arm, bridge, hook, tab):
            part += xz_prism(poly, yc, CLIP_W)
    return part


def to_trimesh(m):
    mesh = m.to_mesh()
    return trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3],
                           faces=np.asarray(mesh.tri_verts), process=True)


def main():
    out = Path(__file__).resolve().parent
    b, cable_floor = base()
    lid_part = lid(cable_floor)
    # Print the lid plate-down: flip it over and sit it on the bed.
    lid_print = lid_part.rotate([180, 0, 0])
    lo = lid_print.bounding_box()
    lid_print = lid_print.translate([0, -lo[1], -lo[2]])
    for name, m in (("base", b), ("lid", lid_print)):
        t = to_trimesh(m)
        t.export(out / f"{name}.stl")
        lo, hi = t.bounds
        print(f"{name}.stl: {hi[0]-lo[0]:.1f} x {hi[1]-lo[1]:.1f} x {hi[2]-lo[2]:.1f} mm, "
              f"watertight={t.is_watertight}, volume={t.volume/1000:.1f} cm3")
    # Assembled view, for checking only.
    to_trimesh(b + lid_part).export(out / "assembled-preview.stl")


if __name__ == "__main__":
    main()
