use <BOSL/constants.scad>
include <BOSL/shapes.scad>
include <BOSL/transforms.scad>

$fn=100;

E = 0.004;

d_cap = 20.64; // Outer diameter of keycap.
h_cap_walls = 8; // Height of keycap walls.
t_cap_top = 2; // Thickness of top of keycap.
t_cap_walls = 1.5; // Thickness of keycap walls

slop_w_shaft = 0; // Increase if stem doesn't fit into switch housing due to width.
slop_l_shaft = 0; // Increase if stem doesn't fit into switch housing due to length.

slop_t_stem = 0; // Increase if stem slot is too thin (i.e. the - of the + is too thin).
slop_l_stem = 0; // Increase if stem slot has insufficient length (i.e. the - of the + is too short).
slop_h_stem = 0.2; // Increase if stem doesn't go all the way into the stem shaft.

t_stem = 1.17 + slop_t_stem; // Thickness of stem based on Cherry MX specifications (+-0.02).
l_stem = 4.1 + slop_l_stem; // End-to-end width/length of the slot for the stem based on Cherry MX specifications (+-0.05).
h_stem = 3.6 + slop_h_stem; // Height of stem slot.

w_shaft = 4.7 + slop_w_shaft; // Outer width of stem shaft.
l_shaft = 6.5 + slop_l_shaft; // Outer length of stem shaft.
h_shaft = 4.6; // Height of stem shaft.

chamfer_cap_top = 1.5; // Chamfer radius for top edge of keycap.

cap();

translate([0, 0, t_cap_top - E])
  stem_shaft();

module cap() {
  difference() {
    // Base shape of cap.
    cyl(d=d_cap, h=h_cap_walls, align=V_UP, fillet1=1.5);

    // Hollow out the cap.
    translate([0, 0, t_cap_top])
      cyl(d=d_cap - t_cap_walls * 2, h=h_cap_walls, align=V_UP);

    // Cut notches at the bottom of the cap's walls.
    zrot_copies([-45, 45]) translate([0, 0, t_cap_top + h_shaft])
      cuboid(
        [d_cap + E, 5, h_cap_walls - (h_shaft + t_cap_top) + E],
        align=V_UP,
      );
  }
}

module stem_shaft() {
  difference() {
    // Main body of stem shaft.
    cuboid(
      [w_shaft, l_shaft, h_shaft],
      align=V_UP,
      fillet=0.5,
      edges=EDGES_Z_ALL,
    );

    // Slot for stem to go into.
    translate([0, 0, h_shaft - h_stem]) {
      cuboid([w_shaft + E, t_stem, h_stem + E], align=V_UP);
      cuboid([t_stem, l_stem, h_stem + E], align=V_UP);
    }
  }
}
