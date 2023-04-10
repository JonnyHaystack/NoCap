# %%
from build123d import *
from ocp_vscode import show, set_port, set_defaults

set_port(3939)
set_defaults(grid=(True, True, True), axes=True, axes0=True)

# %%

d_cap = 20.64  # Outer diameter of keycap.
h_cap = 8  # Overall height of keycap.
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

'''Don't change anything after here unless you need to.'''

t_stem = 1.17 + slop_t_stem  # Thickness of stem based on Cherry MX specifications (+-0.02).
l_stem = 4.1 + slop_l_stem  # End-to-end width/length of the slot for the stem based on Cherry MX specifications (+-0.05).
h_stem = 3.6 + slop_h_stem  # Height of stem slot.

w_shaft = 4.7 - slop_w_shaft  # Outer width of stem shaft.
l_shaft = 6.5 - slop_l_shaft  # Outer length of stem shaft.
h_shaft = 4.6  # Height of stem shaft.

w_corner_gaps = 5  # Width of the gaps that give clearance to the corners of the switch when pressed.
h_corner_gaps = h_cap - (h_shaft + t_cap_top)  # Height of the switch corner gaps.

with BuildPart() as cap:
    # Create the main body of the keycap.
    with BuildSketch() as cap_sk:
        Circle(d_cap / 2)
    extrude(amount=h_cap)
    fillet(cap.edges().sort_by(Axis.Z)[0], radius=r_cap_top_fillet)

    # Hollow out the body of the keycap.
    with BuildSketch(cap.faces().sort_by(Axis.Z)[-1]) as cap_hollow_sk:
        Circle(d_cap / 2 - t_cap_walls)
    extrude(amount=-(h_cap - t_cap_top), mode=Mode.SUBTRACT)

    # Create sketch of the stem on the inside of the keycap's top.
    cap_top_inside = cap.faces().filter_by(Axis.Z).sort_by(Axis.Z)[-2]
    with BuildSketch(cap_top_inside) as stem_sk:
        stem_shaft = Rectangle(width=l_shaft, height=w_shaft)
        fillet(stem_shaft.vertices(), radius=0.5)
        Rectangle(width=t_stem, height=w_shaft, mode=Mode.SUBTRACT)
        Rectangle(width=l_stem, height=t_stem, mode=Mode.SUBTRACT)
    stem = extrude(amount=h_shaft)

    # Select and chamfer the top inner edges of the stem.
    stem_top_inner_edges = (
        stem.edges()
        .group_by(Axis.Z)[-1]
        .filter_by_position(Axis.X, -l_stem / 2, l_stem / 2)
        .filter_by_position(Axis.Y, -w_shaft / 2, w_shaft / 2, (False, False))
    )
    chamfer(stem_top_inner_edges, h_stem_slot_chamfer, l_stem_slot_chamfer)

    # Cut notches in switch corner positions to prevent the walls colliding
    # with the switch.
    with BuildSketch(cap.faces().sort_by(Axis.Z)[-1]) as corner_gaps_sk:
        Rectangle(w_corner_gaps, d_cap, 45)
        mirror()
    extrude(amount=-h_corner_gaps, mode=Mode.SUBTRACT)

show(
    cap,
    # stem_top_inner_edges,
    colors=["gold", "cyan", "magenta"],
    # transparent=True,
)

cap.part.export_step("NoCap.step")
cap.part.export_stl("NoCap.stl")
