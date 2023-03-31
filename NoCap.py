import cadquery as cq

d_cap = 20.64  # Outer diameter of keycap.
h_cap_walls = 8  # Height of keycap walls.
t_cap_top = 2  # Thickness of top of keycap.
t_cap_walls = 1.5  # Thickness of keycap walls
r_cap_top_fillet = 1.5  # Fillet radius for top edge of keycap.

slop_w_shaft = 0  # Increase if stem doesn't fit into switch housing due to width.
slop_l_shaft = 0  # Increase if stem doesn't fit into switch housing due to length.

slop_t_stem = 0  # Increase if stem slot is too thin (i.e. the - of the + is too thin).
slop_l_stem = 0  # Increase if stem slot has insufficient length (i.e. the - of the + is too short).
slop_h_stem = 0.2  # Increase if stem doesn't go all the way into the stem shaft.

h_stem_slot_chamfer = 0.8 # Height of stem slot chamfer.
l_stem_slot_chamfer = 0.4 # Length of stem slot chamfer.

# Don't change anything after here unless you need to.
t_stem = 1.17 + slop_t_stem  # Thickness of stem based on Cherry MX specifications (+-0.02).
l_stem = 4.1 + slop_l_stem  # End-to-end width/length of the slot for the stem based on Cherry MX specifications (+-0.05).
h_stem = 3.6 + slop_h_stem  # Height of stem slot.

w_shaft = 4.7 - slop_w_shaft  # Outer width of stem shaft.
l_shaft = 6.5 - slop_l_shaft  # Outer length of stem shaft.
h_shaft = 4.6  # Height of stem shaft.

w_corner_gaps = 5  # Width of the gaps that give clearance to the corners of the switch when pressed.
h_corner_gaps = h_cap_walls - (h_shaft + t_cap_top)  # Height of the switch corner gaps.


'''
Draw a sketch of the stem slot.
'''
def stem_slot():
    return (
        cq.Sketch()
        .rect(w_shaft, t_stem)
        .rect(t_stem, l_stem)
        .clean()
    )


'''
Chamfer the inner edges of the stem slot.

This is done in three steps in order to work around an annoying CadQuery bug
with asymmetric chamfers of multiple edges.
'''
def chamfer_stem_slot(cap):
    return (
        cap
        .faces(">Z[-2]")
        .edges("#Z except (>>X or <<X or >>Y or <<Y)")
        .edges("not (<<X and <<Y[2] or <<X[-2] and <<Y[1])")
        .chamfer(l_stem_slot_chamfer, h_stem_slot_chamfer)

        .faces(">Z[-2]")
        .edges("#Z except (>>X or <<X or >>Y or <<Y)")
        .edges("<<X[-2]")
        .chamfer(h_stem_slot_chamfer, l_stem_slot_chamfer)

        .faces(">Z[-2]")
        .edges("#Z except (>>X or <<X or >>Y or <<Y)")
        .edges(">>Y[-4] or >>Y[-2]")
        .chamfer(l_stem_slot_chamfer, h_stem_slot_chamfer)
    )


def cap():
    return (
        cq.Workplane("XY")

        # Top of cap
        .circle(d_cap / 2)
        .extrude(t_cap_top)

        # Fillet top edge
        .faces("<Z")
        .fillet(r_cap_top_fillet)

        # Walls of cap
        .faces(">Z")
        .workplane().tag("cap_top_underside")
        .circle(d_cap / 2)
        .circle(d_cap / 2 - t_cap_walls)
        .extrude(h_cap_walls - t_cap_top)

        # Stem shaft
        .workplaneFromTagged("cap_top_underside")
        .rect(w_shaft, l_shaft)
        .extrude(h_shaft)
        .edges("|Z")
        .fillet(0.5)

        # Stem slot
        .faces(">Z[-2]").workplane()
        .placeSketch(stem_slot())
        .cutBlind(-h_stem)
    )


result = chamfer_stem_slot(cap())