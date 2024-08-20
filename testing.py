import math


def fez_function(opening_diameter, youngs_modulus, shear_modulus, torsional_inertia, area_tee_critical,
                 r_naught_bar_squared):
    return (((math.pi**2 * youngs_modulus/6.89 / (opening_diameter/25.4/2)**2) + shear_modulus/6.89 * torsional_inertia/25.4**4) * (1/
            (area_tee_critical/25.4**2 * r_naught_bar_squared/25.4**2)))


y_si = fez_function(156.21*2, 199955, 77204, 9573.322798, 974.1916, 4929.94)
# y_emp = fez_function(6.15*2, 29000, 11200, 0.023, 1.51, 7.64)
print(y_si)
