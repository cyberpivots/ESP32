// Provisional low-voltage fixture plate.
// Units are millimeters. Parameters must be checked against measured hardware.

$fn = 32;

plate_length_mm = 180;
plate_width_mm = 120;
plate_thickness_mm = 3;
corner_radius_mm = 6;

slot_length_mm = 22;
slot_width_mm = 4;
slot_edge_offset_mm = 14;
slot_column_spacing_mm = 38;
slot_row_offset_mm = 32;

label_zone_width_mm = 42;
label_zone_height_mm = 14;
label_zone_wall_mm = 1.0;
label_zone_raise_mm = 0.45;

grid_spacing_mm = 10;
grid_line_width_mm = 0.35;
grid_line_raise_mm = 0.25;
grid_margin_mm = 12;

module rounded_rect_2d(width_mm, depth_mm, radius_mm) {
    hull() {
        translate([-(width_mm / 2) + radius_mm, -(depth_mm / 2) + radius_mm])
            circle(r = radius_mm);
        translate([(width_mm / 2) - radius_mm, -(depth_mm / 2) + radius_mm])
            circle(r = radius_mm);
        translate([-(width_mm / 2) + radius_mm, (depth_mm / 2) - radius_mm])
            circle(r = radius_mm);
        translate([(width_mm / 2) - radius_mm, (depth_mm / 2) - radius_mm])
            circle(r = radius_mm);
    }
}

module rounded_slot_2d(length_mm, width_mm) {
    hull() {
        translate([-(length_mm / 2) + (width_mm / 2), 0])
            circle(d = width_mm);
        translate([(length_mm / 2) - (width_mm / 2), 0])
            circle(d = width_mm);
    }
}

module plate_base() {
    linear_extrude(height = plate_thickness_mm)
        rounded_rect_2d(plate_length_mm, plate_width_mm, corner_radius_mm);
}

module cable_tie_slot(x_mm, y_mm, angle_deg = 0) {
    translate([x_mm, y_mm, -0.1])
        rotate([0, 0, angle_deg])
            linear_extrude(height = plate_thickness_mm + 0.2)
                rounded_slot_2d(slot_length_mm, slot_width_mm);
}

module label_zone(x_mm, y_mm, width_mm, height_mm) {
    translate([x_mm, y_mm, plate_thickness_mm]) {
        translate([0, -(height_mm / 2) + (label_zone_wall_mm / 2), 0])
            cube([width_mm, label_zone_wall_mm, label_zone_raise_mm], center = true);
        translate([0, (height_mm / 2) - (label_zone_wall_mm / 2), 0])
            cube([width_mm, label_zone_wall_mm, label_zone_raise_mm], center = true);
        translate([-(width_mm / 2) + (label_zone_wall_mm / 2), 0, 0])
            cube([label_zone_wall_mm, height_mm, label_zone_raise_mm], center = true);
        translate([(width_mm / 2) - (label_zone_wall_mm / 2), 0, 0])
            cube([label_zone_wall_mm, height_mm, label_zone_raise_mm], center = true);
    }
}

module measurement_grid() {
    line_height = grid_line_raise_mm;
    x_span = plate_length_mm - (2 * grid_margin_mm);
    y_span = plate_width_mm - (2 * grid_margin_mm);

    for (x_mm = [-x_span / 2 : grid_spacing_mm : x_span / 2]) {
        translate([x_mm, 0, plate_thickness_mm + (line_height / 2)])
            cube([grid_line_width_mm, y_span, line_height], center = true);
    }

    for (y_mm = [-y_span / 2 : grid_spacing_mm : y_span / 2]) {
        translate([0, y_mm, plate_thickness_mm + (line_height / 2)])
            cube([x_span, grid_line_width_mm, line_height], center = true);
    }
}

module label_zones() {
    label_y = (plate_width_mm / 2) - 18;
    label_x_step = label_zone_width_mm + 8;

    for (index = [-1.5 : 1 : 1.5]) {
        label_zone(index * label_x_step, label_y, label_zone_width_mm, label_zone_height_mm);
    }

    label_zone(0, -label_y, plate_length_mm - 30, label_zone_height_mm);
}

module cable_tie_slots() {
    for (x_mm = [-(slot_column_spacing_mm * 2) : slot_column_spacing_mm : (slot_column_spacing_mm * 2)]) {
        cable_tie_slot(x_mm, (plate_width_mm / 2) - slot_edge_offset_mm, 0);
        cable_tie_slot(x_mm, -(plate_width_mm / 2) + slot_edge_offset_mm, 0);
    }

    for (y_mm = [-slot_row_offset_mm, 0, slot_row_offset_mm]) {
        cable_tie_slot(-(plate_length_mm / 2) + slot_edge_offset_mm, y_mm, 90);
        cable_tie_slot((plate_length_mm / 2) - slot_edge_offset_mm, y_mm, 90);
    }
}

difference() {
    union() {
        plate_base();
        measurement_grid();
        label_zones();
    }

    cable_tie_slots();
}
