import math


def y_bar_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net, parent_section_web_thickness):
    return (((parent_section_flange_width * parent_section_flange_thickness) * (dt_net - parent_section_flange_thickness / 2)
             + (parent_section_web_thickness * (dt_net - parent_section_flange_thickness) ** 2 / 2))
            / ((parent_section_flange_width * parent_section_flange_thickness) + parent_section_web_thickness * (dt_net - parent_section_flange_thickness)))


def ix_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net, y_bar_tee_net, parent_section_web_thickness):
    return (((parent_section_flange_width * parent_section_flange_thickness ** 3) / 12)
            + (parent_section_flange_thickness * parent_section_flange_width * (dt_net - y_bar_tee_net - parent_section_flange_thickness / 2) ** 2)
            + (parent_section_web_thickness * (dt_net - parent_section_flange_thickness) ** 3 / 12)
            + (parent_section_web_thickness * (dt_net - parent_section_flange_thickness) * (y_bar_tee_net - (dt_net - parent_section_flange_thickness) / 2) ** 2))


def iy_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net, parent_section_web_thickness):
    return ((parent_section_flange_thickness * parent_section_flange_width ** 3 / 12)
            + ((dt_net - parent_section_flange_thickness) * parent_section_web_thickness ** 3 / 12))


def zx_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net, parent_section_web_thickness, area_tee_net):
    if parent_section_flange_thickness <= area_tee_net/(2*parent_section_flange_width):
        zx = ((parent_section_web_thickness * (dt_net - parent_section_flange_thickness)**2)/4
              + (parent_section_flange_width * dt_net * parent_section_flange_thickness)/2
              - (parent_section_flange_width**2 - parent_section_flange_thickness**2)/(4*parent_section_web_thickness))
    else:
        zx = (((parent_section_web_thickness * dt_net**2)/2
              + (parent_section_flange_width * parent_section_flange_thickness**2)/4)
              - (parent_section_flange_width * parent_section_flange_thickness * parent_section_web_thickness)/2
              - ((dt_net - parent_section_flange_thickness)**2 * parent_section_web_thickness**2)/(4 * parent_section_flange_width))
    return zx


def zy_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net, parent_section_web_thickness):
    return ((parent_section_flange_thickness * parent_section_flange_width**2)/4
            + ((dt_net - parent_section_flange_thickness) * parent_section_web_thickness**2)/4)


def tee_web_compactness_function(tee_depth, web_thickness):
    return tee_depth / web_thickness


def flange_to_width_ratio_function(flange_width, flange_thickness):
    return flange_width / (2 * flange_thickness)


def lc_to_r_ratio_function(opening_diameter, r, kx=0.65):
    return (kx * (opening_diameter/2))/r


def f_elastic_buckling_function(governing_lc_to_r_ratio, youngs_modulus):
    return (math.pi**2 * youngs_modulus) / governing_lc_to_r_ratio**2


def fey_function(opening_diameter, ry, youngs_modulus):
    return (math.pi**2 * youngs_modulus) / (opening_diameter/2/ry)**2


def r_naught_bar_squared_function(y_naught, ix_tee_critical, iy, area_tee_critical):
    return y_naught**2 + (ix_tee_critical + iy)/area_tee_critical


def torsional_inertia_function(parent_section_flange_width, parent_section_flange_thickness, dt_critical, parent_section_web_thickness):
    return (parent_section_flange_width * parent_section_flange_thickness ** 3 + (dt_critical - parent_section_flange_thickness / 2) * parent_section_web_thickness ** 3) / 3


def fez_function(opening_diameter, youngs_modulus, shear_modulus, torsional_inertia, area_tee_critical, r_naught_bar_squared):
    return (((math.pi**2 * youngs_modulus/6.89 / (opening_diameter/25.4/2)**2) + shear_modulus/6.89 * torsional_inertia/25.4**4) * (1 / (area_tee_critical/25.4**2 * r_naught_bar_squared/25.4**2)))


def H_function(y_naught, r_naught_bar_squared):
    return 1 - (y_naught**2/r_naught_bar_squared)


def fe_function(fey, fez, H):
    return (fey + fez)/(2*H) * (1 - math.sqrt(1-(4*fey*fez*H/(fey + fez)**2)))


def f_critical_eq3_2_function(yield_strength, f_elastic_buckling):
    return (0.658**(yield_strength/f_elastic_buckling)) * yield_strength


def nominal_axial_force_function(f_critical, area_tee_critical):
    return f_critical * area_tee_critical


def elastic_moment_function(parent_web_thickness, spacing, opening_diameter, yield_strength):
    return ((parent_web_thickness * (spacing - opening_diameter + 0.564*opening_diameter)**2)/6) * yield_strength


def c1_function(opening_diameter, parent_web_thickness):
    return 5.097 + 0.1464*(opening_diameter/parent_web_thickness) - 0.00174*(opening_diameter/parent_web_thickness)**2


def c2_function(opening_diameter, parent_web_thickness):
    return 1.441 + 0.0625*(opening_diameter/parent_web_thickness) - 0.000683*(opening_diameter/parent_web_thickness)**2


def c3_function(opening_diameter, parent_web_thickness):
    return 3.645 + 0.0853*(opening_diameter/parent_web_thickness) - 0.00108*(opening_diameter/parent_web_thickness)**2


def moment_allowed_function(c1, c2, c3, elastic_moment, s_parameter, opening_diameter):
    return (c1*(s_parameter/opening_diameter) - c2*(s_parameter/opening_diameter)**2 - c3) * elastic_moment


def get_max_value_from_column(tableWidget, column):
    num_rows = tableWidget.rowCount()
    max_value = float('-inf')  # Initialize to negative infinity to ensure any number will be larger

    for row in range(num_rows):
        item = tableWidget.item(row, column)
        if item:
            try:
                value = float(item.text())
                if value > max_value:
                    max_value = value
            except ValueError:
                pass  # Ignore cells that do not contain valid numbers

    return max_value

