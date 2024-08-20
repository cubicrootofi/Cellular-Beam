import os
import pandas as pd
import sys
import math
import PyPDF2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from os import path
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.patches import Circle
from qt_material import *
from anastruct import SystemElements
from cellular_beam_equations import *
from mpl import *
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, blue
from PyQt5.QtWidgets import QFileDialog


class MainApp(QMainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        uic.loadUi(path.join(path.dirname(__file__), "eng_waleed.ui"), self)
        self.setWindowTitle('Cellular Beam Designer')
        self.setWindowIcon(QIcon(r"C:\Users\joeys\PycharmProjects\pythonProject1\Steel Designer Project\icons\app.jpg"))

        self.canvas = MplCanvas(self, width=5, height=4, dpi=150)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.tabWidget_2.tabBar().hide()
        self.canvas.get_circle_states()

        # Find the second tab of tabWidget_2
        second_tab = self.tabWidget_2.widget(4)

        # Create a layout for the second tab if it doesn't already exist
        self.tab2_layout = QVBoxLayout(second_tab)

        # Add canvas and toolbar to the layout of the second tab
        self.tab2_layout.addWidget(self.canvas)
        self.tab2_layout.addWidget(self.toolbar)

        self.comboBox_2.currentTextChanged.connect(self.yield_stress_iSection)

        self.actionExport_to_PDF.triggered.connect(self.export_to_pdf)
        # self.actionShow_FBD.triggered.connect(self.structural_analysis_FBD)
        # self.actionShow_BMD.triggered.connect(self.structural_analysis_BMD)
        # self.actionShow_SFD.triggered.connect(self.structural_analysis_SFD)
        # self.actionShow_NFD.triggered.connect(self.structural_analysis_NFD)
        # self.actionShow_Displacement.triggered.connect(self.structural_analysis_DISP)

        self.treeWidget.itemClicked.connect(self.on_tree_item_clicked)

        self.pushButton.clicked.connect(self.update_plot)
        self.pushButton.clicked.connect(self.canvas.get_circle_states)
        self.pushButton_update.clicked.connect(self.updated_circles_states)

        self.ipe_sections = {
    "W12X14":{
        "area": 26.838,
        "h": 302.26,
        "b": 100.8,
        "s": 5.08,
        "t": 5.715
    },
    "IPE80": {
        "area": 7.64,
        "weight": 6,
        "h": 80,
        "b": 46,
        "s": 3.8,
        "r": 5,
        "t": 5.2,
        "c": 10.2,
        "h-2c": 59,
        "Ix": 80.1,
        "Sx": 20,
        "rx": 3.24,
        "Iy": 8.49,
        "Sy": 3.69,
        "ry": 1.05
    },
    "IPE100": {
        "area": 10.3,
        "weight": 8.1,
        "h": 100,
        "b": 55,
        "s": 4.1,
        "r": 7,
        "t": 5.7,
        "c": 12.7,
        "h-2c": 74,
        "Ix": 171,
        "Sx": 34.2,
        "rx": 4.07,
        "Iy": 15.9,
        "Sy": 5.79,
        "ry": 1.24
    },
    "IPE120": {
        "area": 13.2,
        "weight": 10.4,
        "h": 120,
        "b": 64,
        "s": 4.4,
        "r": 7,
        "t": 6.3,
        "c": 13.3,
        "h-2c": 93,
        "Ix": 318,
        "Sx": 53,
        "rx": 4.9,
        "Iy": 27.7,
        "Sy": 8.65,
        "ry": 1.45
    },
    "IPE140": {
        "area": 16.4,
        "weight": 12.9,
        "h": 140,
        "b": 73,
        "s": 4.7,
        "r": 7,
        "t": 6.9,
        "c": 13.9,
        "h-2c": 112,
        "Ix": 541,
        "Sx": 77.3,
        "rx": 5.74,
        "Iy": 44.9,
        "Sy": 12.3,
        "ry": 1.65
    },
    "IPE160": {
        "area": 20.1,
        "weight": 15.8,
        "h": 160,
        "b": 82,
        "s": 5,
        "r": 9,
        "t": 7.4,
        "c": 16.4,
        "h-2c": 127,
        "Ix": 869,
        "Sx": 109,
        "rx": 6.58,
        "Iy": 68.3,
        "Sy": 16.7,
        "ry": 1.84
    },
    "IPE180": {
        "area": 23.9,
        "weight": 18.8,
        "h": 180,
        "b": 91,
        "s": 5.3,
        "r": 9,
        "t": 8,
        "c": 17,
        "h-2c": 146,
        "Ix": 1320,
        "Sx": 146,
        "rx": 7.42,
        "Iy": 101,
        "Sy": 22.2,
        "ry": 2.05
    },
    "IPE200": {
        "area": 28.5,
        "weight": 22.4,
        "h": 200,
        "b": 100,
        "s": 5.6,
        "r": 12,
        "t": 8.5,
        "c": 20.5,
        "h-2c": 159,
        "Ix": 1940,
        "Sx": 194,
        "rx": 8.26,
        "Iy": 142,
        "Sy": 28.5,
        "ry": 2.24
    },
    "IPE220": {
        "area": 33.4,
        "weight": 26.2,
        "h": 220,
        "b": 110,
        "s": 5.9,
        "r": 12,
        "t": 9.2,
        "c": 21.2,
        "h-2c": 177,
        "Ix": 2770,
        "Sx": 252,
        "rx": 9.11,
        "Iy": 205,
        "Sy": 37.3,
        "ry": 2.48
    },
    "IPE240": {
        "area": 39.1,
        "weight": 30.7,
        "h": 240,
        "b": 120,
        "s": 6.2,
        "r": 15,
        "t": 9.8,
        "c": 24.8,
        "h-2c": 190,
        "Ix": 3890,
        "Sx": 324,
        "rx": 9.97,
        "Iy": 284,
        "Sy": 47.3,
        "ry": 2.69
    },
    "IPE270": {
        "area": 45.9,
        "weight": 36.1,
        "h": 270,
        "b": 135,
        "s": 6.6,
        "r": 15,
        "t": 10.2,
        "c": 25.2,
        "h-2c": 219,
        "Ix": 5790,
        "Sx": 429,
        "rx": 11.2,
        "Iy": 420,
        "Sy": 62.2,
        "ry": 3.02
    },
    "IPE300": {
        "area": 53.8,
        "weight": 42.2,
        "h": 300,
        "b": 150,
        "s": 7.1,
        "r": 15,
        "t": 10.7,
        "c": 25.7,
        "h-2c": 248,
        "Ix": 8360,
        "Sx": 557,
        "rx": 12.5,
        "Iy": 604,
        "Sy": 80.5,
        "ry": 3.35
    },
    "IPE330": {
        "area": 62.6,
        "weight": 49.1,
        "h": 330,
        "b": 160,
        "s": 7.5,
        "r": 18,
        "t": 11.5,
        "c": 29.5,
        "h-2c": 271,
        "Ix": 11770,
        "Sx": 713,
        "rx": 13.7,
        "Iy": 788,
        "Sy": 98.5,
        "ry": 3.55
    },
    "IPE360": {
        "area": 72.7,
        "weight": 57.1,
        "h": 360,
        "b": 170,
        "s": 8,
        "r": 18,
        "t": 12.7,
        "c": 30.7,
        "h-2c": 298,
        "Ix": 16270,
        "Sx": 904,
        "rx": 15,
        "Iy": 1040,
        "Sy": 123,
        "ry": 3.79
    },
    "IPE400": {
        "area": 84.5,
        "weight": 66.3,
        "h": 400,
        "b": 180,
        "s": 8.6,
        "r": 21,
        "t": 13.5,
        "c": 34.5,
        "h-2c": 331,
        "Ix": 23130,
        "Sx": 1160,
        "rx": 16.5,
        "Iy": 1320,
        "Sy": 146,
        "ry": 3.95
    },
    "IPE450": {
        "area": 98.8,
        "weight": 77.6,
        "h": 450,
        "b": 190,
        "s": 9.4,
        "r": 21,
        "t": 14.6,
        "c": 35.6,
        "h-2c": 378,
        "Ix": 33740,
        "Sx": 1500,
        "rx": 18.5,
        "Iy": 1680,
        "Sy": 176,
        "ry": 4.12
    },
    "IPE500": {
        "area": 116,
        "weight": 90.7,
        "h": 500,
        "b": 200,
        "s": 10.2,
        "r": 21,
        "t": 16,
        "c": 37,
        "h-2c": 426,
        "Ix": 48200,
        "Sx": 1930,
        "rx": 20.4,
        "Iy": 2140,
        "Sy": 214,
        "ry": 4.31
    },
    "IPE550": {
        "area": 134,
        "weight": 106,
        "h": 550,
        "b": 210,
        "s": 11.1,
        "r": 24,
        "t": 17.2,
        "c": 41.2,
        "h-2c": 467,
        "Ix": 67120,
        "Sx": 2440,
        "rx": 22.3,
        "Iy": 2670,
        "Sy": 254,
        "ry": 4.45
    },
    "IPE600": {
        "area": 156,
        "weight": 122,
        "h": 600,
        "b": 220,
        "s": 12,
        "r": 24,
        "t": 19,
        "c": 43,
        "h-2c": 514,
        "Ix": 92080,
        "Sx": 3070,
        "rx": 24.3,
        "Iy": 3390,
        "Sy": 308,
        "ry": 4.66
    }
}

        self.yield_stress_iSection()
        self.label_46.setText('Ready')

    def yield_stress_iSection(self):
        selected_text = self.comboBox_2.currentText()
        if selected_text == 'ST. 37':
            self.lineEdit_5.setText('2.4')
            self.lineEdit_6.setText('3.6')
        elif selected_text == 'ST. 44':
            self.lineEdit_5.setText('2.8')
            self.lineEdit_6.setText('4.4')
        elif selected_text == 'ST. 52':
            self.lineEdit_5.setText('3.6')
            self.lineEdit_6.setText('5.2')
        else:
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')

    def on_tree_item_clicked(self, item, column):
        if item.text(column) == "General - Moment":
            self.tabWidget_2.setCurrentIndex(0)
        elif item.text(column) == "General - Shear":
            self.tabWidget_2.setCurrentIndex(1)
        elif item.text(column) == "Frame":
            self.tabWidget_2.setCurrentIndex(2)
        elif item.text(column) == "Frame Statical System":
            self.tabWidget_2.setCurrentIndex(3)
        elif item.text(column) == "Cellular Beam Elevation":
            self.tabWidget_2.setCurrentIndex(4)

    def update_plot(self):
        # Step 1: Retrieve and handle default values for input parameters
        selected_section    = self.comboBox.currentText()
        num_openings        = self.spinBox.value()
        dimensions          = self.ipe_sections[selected_section]
        span                = float(self.lineEdit.text()) if self.lineEdit.text() else 1
        opening_diameter    = float(self.lineEdit_2.text()) if self.lineEdit_2.text() else 1
        youngs_modulus      = float(self.lineEdit_3.text()) if self.lineEdit_3.text() else 210000
        shear_modulus       = float(self.lineEdit_4.text()) if self.lineEdit_4.text() else 77200
        yield_strength      = float(self.lineEdit_5.text()) * 98.07 if self.lineEdit_5.text() else 0
        beta_factor         = float(self.lineEdit_7.text()) if self.lineEdit_7.text() else 0
        col_depth           = float(self.lineEdit_col.text()) if self.lineEdit_col.text() else 0
        frame_height        = float(self.lineEdit_col_2.text()) if self.lineEdit_col_2.text() else 5
        dg                  = float(self.lineEdit_col_3.text()) if self.lineEdit_col_3.text() else 0
        s_parameter         = float(self.lineEdit_spacing.text()) if self.lineEdit_spacing.text() else 0

        edge_to_edge_distance = s_parameter - opening_diameter
        e_parameter = frame_height / span
        clear_span = span - col_depth / 1000

        # Step 2: Extract dimensions
        parent_section_flange_width     = dimensions['b']
        parent_section_flange_thickness = dimensions['t']
        parent_section_web_thickness    = dimensions['s']
        beam_depth                      = dimensions["h"]

        Lact = (num_openings - 1) * s_parameter + opening_diameter + 2

        if Lact >= clear_span * 1000:
            self.label_46.setText(
                "Beam length is too short for the specified number of openings with the given spacing.")
            return

        flange_thickness = dimensions["t"]
        half_depth = beam_depth / 2000

        # Step 3: Support reactions and bending moments
        support_reaction_y = 0.5
        support_reaction_x = (3 / (4 * frame_height)) * ((0.5 * span) / (2 * beta_factor * e_parameter + 3))
        bending_moment_at_beam_ends = -(0.75 * ((0.5 * span) / (2 * beta_factor * e_parameter + 3)))
        bending_moment_at_beam_midspan = (span / 8) * ((4 * beta_factor * e_parameter + 3) / (2 * beta_factor * e_parameter + 3))

        # Step 4: Net section properties
        z_parameter = s_parameter / opening_diameter
        q_parameter = dg / opening_diameter
        r_parameter = dg / beam_depth

        if not self.lineEdit_2.text():
            self.label_15.setText("")
            self.label_32.setText("")
            self.label_119.setText("")
        else:
            self.label_15.setText(f"{z_parameter:.2f}")
            self.label_32.setText(f"{round(q_parameter, 2)}")
            self.label_119.setText(f"{r_parameter:.2f}")

        self.label_19.setText(f"{clear_span}")
        self.label_22.setText(f"{self.lineEdit.text()} m")
        self.label_33.setText(f"{self.lineEdit_col_2.text()} m")
        self.label_35.setText(f"{round(e_parameter, 2)}")
        self.label_36.setText(f"{beta_factor}")
        self.label_39.setText(f"{support_reaction_y}")
        self.label_40.setText(f"{round(support_reaction_x, 2)}")
        self.label_43.setText(f"{round(bending_moment_at_beam_ends, 2)}")
        self.label_45.setText(f"{round(bending_moment_at_beam_midspan, 2)}")
        self.statusBar().showMessage(
            f"Edge-to-edge distance between adjacent openings, e = {edge_to_edge_distance:.1f} mm")

        if 1.08 <= z_parameter <= 1.5 and 1.25 <= q_parameter <= 1.75 and 1.3 <= r_parameter <= 1.5:
            self.label_46.setText("All Good!")
        else:
            self.label_46.setText(f"Careful! Z = {z_parameter:.2f} | q = {q_parameter:.2f} | R = {r_parameter:.2f}")

        if 1.08 <= z_parameter <= 1.5:
            self.label_16.setText("o.k.")
        else:
            self.label_16.setText("N/A")

        if 1.25 <= q_parameter <= 1.75:
            self.label_30.setText("o.k.")
        else:
            self.label_30.setText("N/A")

        if 1.3 <= r_parameter <= 1.5:
            self.label_124.setText("o.k.")
        else:
            self.label_124.setText("N/A")

        if edge_to_edge_distance < 1:
            self.label_46.setText(
                f"Beam length is too short for {num_openings} openings with {opening_diameter} mm diameter.")
            return

        # Step 5: Plot the beam and openings
        self.canvas.ax.clear()
        self.canvas.circles.clear()
        self.circle_positions = []

        center_x = span / 2

        # Handle odd number of openings
        if num_openings % 2 == 1:
            half_openings = num_openings // 2
            for i in range(half_openings + 1):
                pos_x = center_x + i * s_parameter / 1000
                neg_x = center_x - i * s_parameter / 1000
                if i == 0:
                    self.circle_positions.append((half_openings + 1, pos_x))
                    circle = Circle((pos_x, 0), opening_diameter / 2000, edgecolor='black', facecolor=(0, 0, 1, 0))
                    self.canvas.ax.add_patch(circle)
                    self.canvas.circles.append(circle)
                    self.canvas.ax.text(pos_x, 0, str(half_openings + 1), color='red', ha='center', va='center',
                                        fontsize='medium')
                else:
                    self.circle_positions.append((half_openings + 1 - i, neg_x))
                    self.circle_positions.append((half_openings + 1 + i, pos_x))
                    circle_neg = Circle((neg_x, 0), opening_diameter / 2000, edgecolor='black', facecolor=(0, 0, 1, 0))
                    circle_pos = Circle((pos_x, 0), opening_diameter / 2000, edgecolor='black', facecolor=(0, 0, 1, 0))
                    self.canvas.ax.add_patch(circle_neg)
                    self.canvas.ax.add_patch(circle_pos)
                    self.canvas.circles.append(circle_neg)
                    self.canvas.circles.append(circle_pos)
                    self.canvas.ax.text(neg_x, 0, str(half_openings + 1 - i), color='red', ha='center', va='center',
                                        fontsize='medium')
                    self.canvas.ax.text(pos_x, 0, str(half_openings + 1 + i), color='red', ha='center', va='center',
                                        fontsize='medium')
        # Handle even number of openings
        else:
            half_openings = num_openings // 2
            for i in range(half_openings):
                pos_x = center_x + (i + 0.5) * s_parameter / 1000
                neg_x = center_x - (i + 0.5) * s_parameter / 1000
                self.circle_positions.append((half_openings - i, neg_x))
                self.circle_positions.append((half_openings + 1 + i, pos_x))
                circle_neg = Circle((neg_x, 0), opening_diameter / 2000, edgecolor='black', facecolor=(0, 0, 1, 0))
                circle_pos = Circle((pos_x, 0), opening_diameter / 2000, edgecolor='black', facecolor=(0, 0, 1, 0))
                self.canvas.ax.add_patch(circle_neg)
                self.canvas.ax.add_patch(circle_pos)
                self.canvas.circles.append(circle_neg)
                self.canvas.circles.append(circle_pos)
                self.canvas.ax.text(neg_x, 0, str(half_openings - i), color='red', ha='center', va='center',
                                    fontsize='medium')
                self.canvas.ax.text(pos_x, 0, str(half_openings + 1 + i), color='red', ha='center', va='center',
                                    fontsize='medium')

        # Draw the web and flanges of the beam
        self.canvas.ax.plot([0, span], [0, 0], color='black', linewidth=0.5)
        self.canvas.ax.plot([0, span], [
            half_depth if not hasattr(self, 'lineEdit_col_3') or self.lineEdit_col_3.text() == "" else dg / 2000,
            half_depth if not hasattr(self, 'lineEdit_col_3') or self.lineEdit_col_3.text() == "" else dg / 2000],
                            color='black', linewidth=(flange_thickness / (span * 1.4)))
        self.canvas.ax.plot([0, span], [
            -half_depth if not hasattr(self, 'lineEdit_col_3') or self.lineEdit_col_3.text() == "" else -dg / 2000,
            -half_depth if not hasattr(self, 'lineEdit_col_3') or self.lineEdit_col_3.text() == "" else -dg / 2000],
                            color='black', linewidth=(flange_thickness / (span * 1.4)))

        self.canvas.ax.set_xlim(0, span)
        self.canvas.ax.set_ylim(
            -half_depth if not hasattr(self, 'lineEdit_col_3') or self.lineEdit_col_3.text() == "" else -dg / 2000,
            half_depth if not hasattr(self, 'lineEdit_col_3') or self.lineEdit_col_3.text() == "" else dg / 2000)
        self.canvas.ax.set_aspect(aspect='equal', adjustable='box')
        self.canvas.ax.set_xlabel("Beam Length (m)")
        self.canvas.ax.set_ylabel(
            "h (mm)" if not hasattr(self, 'lineEdit_col_3') or self.lineEdit_col_3.text() == "" else "dg (mm)")
        self.canvas.ax.set_title("""Point Load (kN)
|
|
|
v""")

        self.canvas.draw()

        # Step 6: Calculations for table values
        dt_net = (dg - opening_diameter) / 2
        area_tee_net = parent_section_flange_width * parent_section_flange_thickness + (
                dt_net - parent_section_flange_thickness) * parent_section_web_thickness
        area_net = 2 * area_tee_net
        y_bar_beam = dg / 2
        y_bar_tee_net = y_bar_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net, parent_section_web_thickness)
        ix_tee_net = ix_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net,
                                     y_bar_tee_net,
                                     parent_section_web_thickness)
        iy_tee_net = iy_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net,
                                     parent_section_web_thickness)
        rx_tee_net = math.sqrt(ix_tee_net / area_tee_net)
        ry_tee_net = math.sqrt(iy_tee_net / area_tee_net)
        sx_top_tee_net = ix_tee_net / (dt_net - y_bar_tee_net)
        sx_bot_tee_net = ix_tee_net / y_bar_tee_net
        zx_tee_net = zx_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net,
                                     parent_section_web_thickness, area_tee_net)
        zy_tee_net = zy_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net,
                                     parent_section_web_thickness)

        # Step 7: Calculations for critical tee section properties
        y = math.sqrt(((opening_diameter / 2) ** 2) - ((0.225 * opening_diameter) ** 2))
        dt_critical = (opening_diameter / 2) - y + dt_net
        area_tee_critical = parent_section_flange_width * parent_section_flange_thickness + (
                dt_critical - parent_section_flange_thickness) * parent_section_web_thickness
        area_critical = 2 * area_tee_critical
        y_bar_tee_critical = y_bar_tee_function(parent_section_flange_width, parent_section_flange_thickness,
                                                dt_critical,
                                                parent_section_web_thickness)
        ix_tee_critical = ix_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_critical,
                                          y_bar_tee_critical, parent_section_web_thickness)
        iy_tee_critical = iy_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_critical,
                                          parent_section_web_thickness)
        torsional_inertia = torsional_inertia_function(parent_section_flange_width, parent_section_flange_thickness,
                                                       dt_critical, parent_section_web_thickness)
        rx_tee_critical = math.sqrt(ix_tee_critical / area_tee_critical)
        ry_tee_critical = math.sqrt(iy_tee_critical / area_tee_critical)
        sx_top_tee_critical = ix_tee_critical / (dt_critical - y_bar_tee_critical)
        sx_bot_tee_critical = ix_tee_critical / y_bar_tee_critical
        zx_tee_critical = zx_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_critical,
                                          parent_section_web_thickness, area_tee_critical)
        zy_tee_critical = zy_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_critical,
                                          parent_section_web_thickness)

        # Beam Net Section Properties
        d_effec_net = dg - 2 * (dt_net - y_bar_tee_net)
        ix_net = 2 * ix_tee_net + area_net * (d_effec_net / 2) ** 2
        sx_net = ix_net / (dg / 2)
        zx_net = area_net * (d_effec_net / 2)

        # Beam Critical Section Properties
        d_effec_critical = dg - 2 * (dt_critical - y_bar_tee_net)
        ix_critical = 2 * ix_tee_critical + area_critical * (d_effec_critical / 2) ** 2
        sx_critical = ix_critical / (dg / 2)
        zx_critical = area_critical * (d_effec_critical / 2)

        # Beam Gross Section Properties
        area_gross = area_net + opening_diameter * parent_section_web_thickness
        ix_gross = ix_net + (parent_section_web_thickness * opening_diameter ** 3) / 12
        sx_gross = ix_gross / (dg / 2)

        # Compactness
        web_compact_limit = tee_web_compactness_function(dt_critical, parent_section_web_thickness)
        flange_to_width_ratio = flange_to_width_ratio_function(parent_section_flange_width,
                                                               parent_section_flange_thickness)

        # Lc/r ratio
        lc_to_rx = lc_to_r_ratio_function(opening_diameter, rx_tee_critical)
        lc_to_ry = lc_to_r_ratio_function(opening_diameter, ry_tee_critical, 1)
        governing_lc_to_r_ratio = max(lc_to_rx, lc_to_ry)
        f_elastic_buckling_section_E3 = f_elastic_buckling_function(governing_lc_to_r_ratio, youngs_modulus) # in N/mm^2

        if governing_lc_to_r_ratio <= (4.71 * math.sqrt(youngs_modulus / yield_strength)):
            f_critical_eq3_2 = f_critical_eq3_2_function(yield_strength, f_elastic_buckling_section_E3)
        else:
            f_critical_eq3_2 = 0.887 * f_elastic_buckling_section_E3

        y_naught = y_bar_tee_critical - parent_section_flange_thickness / 2
        r_naught_bar_squared = r_naught_bar_squared_function(y_naught, ix_tee_critical, iy_tee_critical,
                                                             area_tee_critical)
        fey = fey_function(opening_diameter, ry_tee_critical, youngs_modulus)
        fez_ksi = (fez_function(opening_diameter, youngs_modulus, shear_modulus, torsional_inertia, area_tee_critical, r_naught_bar_squared))
        fez_mpa = fez_ksi*6.89476
        H = H_function(y_naught, r_naught_bar_squared)

        fe = fe_function(fey, fez_mpa, H)
        f_critical_E4 = f_critical_eq3_2_function(yield_strength, fe)

        nominal_axial_force_flexural_buckling = nominal_axial_force_function(f_critical_eq3_2,
                                                                             area_tee_critical) / 1000
        nominal_axial_force_flexural_torsional_buckling = nominal_axial_force_function(f_critical_E4,
                                                                                       area_tee_critical) / 1000

        min_axial_capacity = min(nominal_axial_force_flexural_buckling, nominal_axial_force_flexural_torsional_buckling)

        # Flexural Capacity
        if web_compact_limit <= 0.84 * math.sqrt(youngs_modulus / yield_strength):
            f_critical = yield_strength
            nominal_web_buckling_moment = f_critical * sx_bot_tee_critical / 10 ** 6
        elif 0.84 * math.sqrt(youngs_modulus / yield_strength) < web_compact_limit <= 1.52 * math.sqrt(
                youngs_modulus / yield_strength):
            f_critical = (1.43 - 0.515 * web_compact_limit * math.sqrt(
                youngs_modulus / yield_strength)) * yield_strength
            nominal_web_buckling_moment = f_critical * sx_bot_tee_critical / 10 ** 6
        else:
            f_critical = 1.52 * youngs_modulus / web_compact_limit ** 2
            nominal_web_buckling_moment = f_critical * sx_bot_tee_critical / 10 ** 6

        moment_capacity = min_axial_capacity * d_effec_critical
        yielding_moment = yield_strength * sx_bot_tee_critical / 10 ** 6
        vierendeel_shear = yielding_moment * 8 / opening_diameter

        # Find the summary tab
        summary_tab = self.tabWidget.widget(0)

        # Ensure the summary tab has a layout
        if summary_tab.layout() is None:
            summary_tab.setLayout(QVBoxLayout())

        # Check if the table already exists and remove it if it does
        for i in reversed(range(summary_tab.layout().count())):
            widget = summary_tab.layout().itemAt(i).widget()
            if isinstance(widget, QTableWidget):
                widget.deleteLater()
        try:
            # Create and configure the table widget
            table = QTableWidget()
            circle_states = self.canvas.get_circle_states()
            table.setRowCount(len(self.canvas.circles))
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels(
                ["Opening No.", "Xi (m)", "Shear Force (kN)", "Bending Moment (kNm)", "Local Axial Force (kN)",
                 "Vierendeel Moment (kNm)"])

            # Pair each circle with its state and sort by the circle's x position
            circles_with_states = [(circle, state) for circle, state in zip(self.canvas.circles, circle_states)]
            circles_with_states.sort(key=lambda x: x[0].center[0])

            for row, (circle, state) in enumerate(circles_with_states):
                num_item = QTableWidgetItem()
                num_item.setData(Qt.DisplayRole, row + 1)
                pos = circle.center[0]
                pos_item = QTableWidgetItem(f"{pos:.3f}")

                if state == 0:  # If opening is closed
                    shear_force = 0
                    bending_moment_opening_center = 0
                    local_axial_force = 0
                    vierendeel_moment = 0
                else:  # Normal calculations
                    if pos < span / 2:
                        shear_force = 0.5
                        bending_moment_opening_center = bending_moment_at_beam_ends + (support_reaction_y * pos)
                        local_axial_force = (bending_moment_opening_center / d_effec_critical) * 1000
                        vierendeel_moment = (shear_force / 2) * (opening_diameter / 4)
                    elif pos == span / 2:
                        shear_force = 1
                        bending_moment_opening_center = bending_moment_at_beam_ends + (support_reaction_y * pos)
                        local_axial_force = (bending_moment_opening_center / d_effec_critical) * 1000
                        vierendeel_moment = (shear_force / 2) * (opening_diameter / 4)
                    else:
                        shear_force = -0.5
                        bending_moment_opening_center = bending_moment_at_beam_ends + (support_reaction_y * pos) - (
                                pos - span / 2)
                        local_axial_force = (bending_moment_opening_center / d_effec_critical) * 1000
                        vierendeel_moment = (shear_force / 2) * (opening_diameter / 4)

                shear_item = QTableWidgetItem(f"{shear_force:.2f}")
                bending_moment_opening_center_item = QTableWidgetItem(f"{bending_moment_opening_center:.2f}")
                local_axial_force_item = QTableWidgetItem(f"{local_axial_force:.2f}")
                vierendeel_moment_item = QTableWidgetItem(f"{vierendeel_moment:.2f}")

                # Center-align the text in the cells
                num_item.setTextAlignment(Qt.AlignCenter)
                pos_item.setTextAlignment(Qt.AlignCenter)
                shear_item.setTextAlignment(Qt.AlignCenter)
                bending_moment_opening_center_item.setTextAlignment(Qt.AlignCenter)
                local_axial_force_item.setTextAlignment(Qt.AlignCenter)
                vierendeel_moment_item.setTextAlignment(Qt.AlignCenter)

                table.setItem(row, 0, num_item)
                table.setItem(row, 1, pos_item)
                table.setItem(row, 2, shear_item)
                table.setItem(row, 3, bending_moment_opening_center_item)
                table.setItem(row, 4, local_axial_force_item)
                table.setItem(row, 5, vierendeel_moment_item)
        except AttributeError as e:
            self.statusBar().showMessage(f"Error: there are no openings found!{e}")
        # Adjust column sizes to fit content
        table.resizeColumnsToContents()

        # Add the table to the layout of the summary tab
        table_layout = summary_tab.layout()
        table_layout.addWidget(table)

        # # Step 10: Calculate the moment differences
        # moment_values = []
        # for row in range(table.rowCount()):
        #     item = table.item(row, 3)
        #     if item is not None:
        #         moment_values.append(float(item.text()))
        #     else:
        #         moment_values.append(0)  # or handle the missing value appropriately
        #
        # moment_difference = [moment_values[i - 1] - moment_values[i] for i in range(1, len(moment_values))]
        # max_net_moment = max(moment_difference)
        #
        # # Step 11: Additional calculations and display results
        # c1 = c1_function(opening_diameter, parent_section_web_thickness)
        # c2 = c2_function(opening_diameter, parent_section_web_thickness)
        # c3 = c3_function(opening_diameter, parent_section_web_thickness)
        # elastic_moment = elastic_moment_function(parent_section_web_thickness, s_parameter, opening_diameter,
        #                                          yield_strength)
        # moment_allowed = moment_allowed_function(c1, c2, c3, elastic_moment, s_parameter, opening_diameter) / 10 ** 6
        # axial_nominal_capacity_regarding_web_post_buckling = moment_allowed / max_net_moment
        # self.label_hzShear_2.setText(f"{axial_nominal_capacity_regarding_web_post_buckling:.2f}")

        # summary_tab.layout().addWidget(table)

        if flange_to_width_ratio <= 0.38*math.sqrt(youngs_modulus/yield_strength):
            self.label_54.setText("COMPACT")
        elif 0.38*math.sqrt(youngs_modulus/yield_strength) < flange_to_width_ratio <= math.sqrt(youngs_modulus/yield_strength):
            self.label_54.setText("NON-COMPACT")
        else:
            self.label_54.setText("SLENDER")

        self.label_24.setText(f"{flange_to_width_ratio:.2f}")

        if web_compact_limit < 0.75*math.sqrt(youngs_modulus/yield_strength):
            self.label_55.setText("NON-SLENDER")
        else:
            self.label_55.setText("SLENDER")

        self.label_56.setText(f"{lc_to_rx:.2f}")
        self.label_58.setText(f"{lc_to_ry:.2f}")

        if lc_to_rx > lc_to_ry:
            self.label_66.setText("Governs.")
            self.label_67.setText("")
        elif lc_to_rx < lc_to_ry:
            self.label_67.setText("Governs.")
            self.label_66.setText("")
        else:
            self.label_66.setText("Equal.")
            self.label_67.setText("Equal.")

        self.label_71.setText(f"{nominal_axial_force_flexural_buckling:.2f}")
        self.label_26.setText(f"{nominal_axial_force_flexural_torsional_buckling:.2f}")

        if nominal_axial_force_flexural_buckling > nominal_axial_force_flexural_torsional_buckling:
            self.label_73.setText("Governs.")
            self.label_74.setText("")
        elif nominal_axial_force_flexural_buckling < nominal_axial_force_flexural_torsional_buckling:
            self.label_73.setText("Governs.")
            self.label_74.setText("")
        else:
            self.label_74.setText("Equal.")
            self.label_73.setText("Equal.")

        self.label_yieldMoment.setText(f"{yielding_moment:.2f}")
        self.label_webBucklingMoment.setText(f"{nominal_web_buckling_moment:.2f}")
        self.label_29.setText(f"{web_compact_limit:.2f}")
        self.label_15.setText(f"{round(z_parameter, 2)}")
        self.label_19.setText(f"{clear_span}")
        self.label_22.setText(f"{self.lineEdit.text()} m")
        self.label_32.setText(f"{round(q_parameter, 2)}")
        self.label_33.setText(f"{self.lineEdit_col_2.text()} m")
        self.label_35.setText(f"{round(e_parameter, 2)}")
        self.label_36.setText(f"{beta_factor}")
        self.label_39.setText(f"{support_reaction_y}")
        self.label_40.setText(f"{round(support_reaction_x, 2)}")
        self.label_43.setText(f"{round(bending_moment_at_beam_ends, 2)}")
        self.label_45.setText(f"{round(bending_moment_at_beam_midspan, 2)}")

        self.label_51.setText(f"{round(y_bar_tee_net/10, 2)}")
        self.label_49.setText(f"{round(ix_tee_net/10**4, 2)}")
        self.label_53.setText(f"{round(iy_tee_net/10**4, 2)}")
        self.label_65.setText(f"{round(sx_top_tee_net/10**3, 2)}")
        self.label_69.setText(f"{round(sx_bot_tee_net/10**3, 2)}")
        self.label_91.setText(f"{round(zx_tee_net/10**3, 2)}")
        self.label_93.setText(f"{round(zy_tee_net/10**3, 2)}")
        self.label_61.setText(f"{round(rx_tee_net/10, 2)}")
        self.label_63.setText(f"{round(ry_tee_net/10, 2)}")

        self.label_85.setText(f"{round(y_bar_tee_critical/10, 2)}")
        self.label_81.setText(f"{round(ix_tee_critical/10**4, 2)}")
        self.label_77.setText(f"{round(iy_tee_critical/10**4, 2)}")
        self.label_78.setText(f"{round(sx_top_tee_critical/10**3, 2)}")
        self.label_89.setText(f"{round(sx_bot_tee_critical/10**3, 2)}")
        self.label_95.setText(f"{round(zx_tee_critical/10**3, 2)}")
        self.label_97.setText(f"{round(zy_tee_critical/10**3, 2)}")
        self.label_87.setText(f"{round(ry_tee_critical/10, 2)}")
        self.label_84.setText(f"{round(rx_tee_critical/10, 2)}")

        self.label_123.setText(f"{round(y_bar_beam/10, 2)}")
        self.label_178.setText(f"{round(d_effec_net/10, 2)}")
        self.label_120.setText(f"{round(ix_net/10**4, 2)}")
        self.label_116.setText(f"{round(sx_net/10**3, 2)}")
        self.label_130.setText(f"{round(zx_net/10**3, 2)}")

        self.label_150.setText(f"{round(y_bar_beam/10, 2)}")
        self.label_182.setText(f"{round(d_effec_critical/10 ,2)}")
        self.label_147.setText(f"{round(ix_critical/10**4, 2)}")
        self.label_143.setText(f"{round(sx_critical/10**3, 2)}")
        self.label_157.setText(f"{round(zx_critical/10**3, 2)}")

        self.label_177.setText(f"{round(area_gross/10**2, 2)}")
        self.label_174.setText(f"{round(ix_gross/10**4, 2)}")
        self.label_170.setText(f"{round(sx_gross/10**3, 2)}")

    # except Exception as e:
    #     self.label_46.setText(f"Error: Check your inputs! ----- {e}")

    def updated_circles_states(self):
        # Step 1: Retrieve and handle default values for input parameters
        selected_section    = self.comboBox.currentText()
        dimensions          = self.ipe_sections[selected_section]
        span                = float(self.lineEdit.text()) if self.lineEdit.text() else 1
        opening_diameter    = float(self.lineEdit_2.text()) if self.lineEdit_2.text() else 1
        beta_factor         = float(self.lineEdit_7.text()) if self.lineEdit_7.text() else 0
        frame_height        = float(self.lineEdit_col_2.text()) if self.lineEdit_col_2.text() else 5
        dg                  = float(self.lineEdit_col_3.text()) if self.lineEdit_col_3.text() else 0

        e_parameter = frame_height / span

        # Step 2: Extract dimensions
        parent_section_flange_width     = dimensions['b']
        parent_section_flange_thickness = dimensions['t']
        parent_section_web_thickness    = dimensions['s']
        bending_moment_at_beam_ends = -(0.75 * ((0.5 * span) / (2 * beta_factor * e_parameter + 3)))
        support_reaction_y = 0.5
        dt_net = (dg - opening_diameter) / 2
        y = math.sqrt(((opening_diameter / 2) ** 2) - ((0.225 * opening_diameter) ** 2))
        dt_critical = (opening_diameter / 2) - y + dt_net
        y_bar_tee_net = y_bar_tee_function(parent_section_flange_width, parent_section_flange_thickness, dt_net, parent_section_web_thickness)
        d_effec_critical = dg - 2 * (dt_critical - y_bar_tee_net)


        # Find the summary tab
        summary_tab = self.tabWidget.widget(0)

        # Ensure the summary tab has a layout
        if summary_tab.layout() is None:
            summary_tab.setLayout(QVBoxLayout())

        # Check if the table already exists and remove it if it does
        for i in reversed(range(summary_tab.layout().count())):
            widget = summary_tab.layout().itemAt(i).widget()
            if isinstance(widget, QTableWidget):
                widget.deleteLater()
        try:
            # Create and configure the table widget
            table = QTableWidget()
            circle_states = self.canvas.get_circle_states()
            table.setRowCount(len(self.canvas.circles))
            table.setColumnCount(6)
            table.setHorizontalHeaderLabels(
                ["Opening No.", "Xi (m)", "Shear Force (kN)", "Bending Moment (kNm)", "Local Axial Force (kN)",
                 "Vierendeel Moment (kNm)"])

            # Pair each circle with its state and sort by the circle's x position
            circles_with_states = [(circle, state) for circle, state in zip(self.canvas.circles, circle_states)]
            circles_with_states.sort(key=lambda x: x[0].center[0])

            for row, (circle, state) in enumerate(circles_with_states):
                num_item = QTableWidgetItem()
                num_item.setData(Qt.DisplayRole, row + 1)
                pos = circle.center[0]
                pos_item = QTableWidgetItem(f"{pos:.3f}")

                if state == 0:  # If opening is closed
                    shear_force = 0
                    bending_moment_opening_center = 0
                    local_axial_force = 0
                    vierendeel_moment = 0
                else:  # Normal calculations
                    if pos < span / 2:
                        shear_force = 0.5
                        bending_moment_opening_center = bending_moment_at_beam_ends + (support_reaction_y * pos)
                        local_axial_force = (bending_moment_opening_center / d_effec_critical) * 1000
                        vierendeel_moment = (shear_force / 2) * (opening_diameter / 4)
                    elif pos == span / 2:
                        shear_force = 1
                        bending_moment_opening_center = bending_moment_at_beam_ends + (support_reaction_y * pos)
                        local_axial_force = (bending_moment_opening_center / d_effec_critical) * 1000
                        vierendeel_moment = (shear_force / 2) * (opening_diameter / 4)
                    else:
                        shear_force = -0.5
                        bending_moment_opening_center = bending_moment_at_beam_ends + (support_reaction_y * pos) - (
                                pos - span / 2)
                        local_axial_force = (bending_moment_opening_center / d_effec_critical) * 1000
                        vierendeel_moment = (shear_force / 2) * (opening_diameter / 4)

                shear_item = QTableWidgetItem(f"{shear_force:.2f}")
                bending_moment_opening_center_item = QTableWidgetItem(f"{bending_moment_opening_center:.2f}")
                local_axial_force_item = QTableWidgetItem(f"{local_axial_force:.2f}")
                vierendeel_moment_item = QTableWidgetItem(f"{vierendeel_moment:.2f}")

                # Center-align the text in the cells
                num_item.setTextAlignment(Qt.AlignCenter)
                pos_item.setTextAlignment(Qt.AlignCenter)
                shear_item.setTextAlignment(Qt.AlignCenter)
                bending_moment_opening_center_item.setTextAlignment(Qt.AlignCenter)
                local_axial_force_item.setTextAlignment(Qt.AlignCenter)
                vierendeel_moment_item.setTextAlignment(Qt.AlignCenter)

                table.setItem(row, 0, num_item)
                table.setItem(row, 1, pos_item)
                table.setItem(row, 2, shear_item)
                table.setItem(row, 3, bending_moment_opening_center_item)
                table.setItem(row, 4, local_axial_force_item)
                table.setItem(row, 5, vierendeel_moment_item)
        except AttributeError as e:
            self.statusBar().showMessage(f"Error: there are no openings found!{e}")
        # Adjust column sizes to fit content
        table.resizeColumnsToContents()

        # Add the table to the layout of the summary tab
        table_layout = summary_tab.layout()
        table_layout.addWidget(table)

    def export_to_pdf(self):
        try:
            # Open a file dialog to choose the directory and file name
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)",
                                                       options=options)

            if not file_path:
                self.label_46.setText("PDF export cancelled.")
                return

            if not file_path.endswith('.pdf'):
                file_path += '.pdf'

            # Create a PdfPages object to save the Matplotlib figure
            pdf_fig_path = file_path.replace('.pdf', '_fig.pdf')
            with PdfPages(pdf_fig_path) as pdf:
                self.canvas.figure.savefig(pdf, format='pdf')

            # Create a canvas for the report
            pdf_report_path = file_path.replace('.pdf', '_report.pdf')
            c = canvas.Canvas(pdf_report_path, pagesize=letter)
            width, height = letter

            # Title
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, height - 40, "Beam Analysis Results")

            # Results
            c.setFont("Helvetica", 12)
            y_position = height - 60

            def draw_text(label, value, y_pos):
                c.setFillColor(black)
                c.drawString(100, y_pos, label)
                c.setFillColor(blue)
                c.drawString(300, y_pos, value)
                return y_pos - 20

            y_position = draw_text("Frame Height:", f"{self.lineEdit_col_2.text()} m", y_position)
            y_position = draw_text("Frame Span:", f"{self.lineEdit.text()} m", y_position)
            y_position = draw_text("Column Depth:", f"{self.lineEdit_col.text()} mm", y_position)
            y_position = draw_text("Beam Clear Span:", f"{self.label_19.text()} m", y_position)
            y_position = draw_text("Beta Factor:", f"{self.lineEdit_7.text()}", y_position)
            y_position = draw_text("Selected Section:", f"{self.comboBox.currentText()}", y_position)
            y_position = draw_text("Number of Openings:", f"{self.spinBox.value()} openings", y_position)
            y_position = draw_text("Opening Diameter:", f"{self.lineEdit_2.text()} mm", y_position)
            y_position = draw_text("Young's Modulus:", f"{float(self.lineEdit_3.text()) if self.lineEdit_3.text() else 210000 } MPa", y_position)
            y_position = draw_text("Shear Modulus:", f"{float(self.lineEdit_4.text()) if self.lineEdit_4.text() else 77200} MPa", y_position)
            y_position = draw_text("dg:", f"{self.lineEdit_col_3.text()} mm", y_position)
            y_position = draw_text("Spacing:", f"{self.lineEdit_spacing.text()} mm", y_position)
            y_position = draw_text("Pn due to Flexural Buckling:", f"{self.label_71.text()} kN", y_position)
            y_position = draw_text("Pn due to Flexural-Torsional Buckling:", f"{self.label_26.text()} kN", y_position)
            y_position = draw_text("My due to yielding:", f"{self.label_yieldMoment.text()} kN-m", y_position)
            y_position = draw_text("Mwb due to Web Buckling:", f"{self.label_webBucklingMoment.text()} kN-m", y_position)


            c.showPage()
            c.save()

            # Merge the two PDFs
            with open(file_path, 'wb') as final_pdf:
                pdf_writer = PyPDF2.PdfWriter()

                # Add the figure PDF
                with open(pdf_fig_path, 'rb') as fig_pdf:
                    pdf_reader = PyPDF2.PdfReader(fig_pdf)
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                # Add the report PDF
                with open(pdf_report_path, 'rb') as report_pdf:
                    pdf_reader = PyPDF2.PdfReader(report_pdf)
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                pdf_writer.write(final_pdf)

            # Remove the temporary files
            os.remove(pdf_fig_path)
            os.remove(pdf_report_path)

            self.label_46.setText("PDF exported successfully.")

        except Exception as e:
            self.label_46.setText(f"Error: Check your inputs!   {e}")


# def show_summary_table(self):
    #     try:
    #         selected_section = self.comboBox.currentText()
    #         span = float(self.lineEdit.text()) if self.lineEdit.text() else 1  # Beam length in meters
    #         beta_factor = float(self.lineEdit_7.text()) if self.lineEdit_7.text() else 0
    #         frame_height = float(self.lineEdit_col_2.text()) if self.lineEdit_col_2.text() else 5  # Frame height in m
    #         e_parameter = frame_height / span
    #         support_reaction_y = 0.5
    #         support_reaction_x = (3 / (4 * frame_height)) * ((0.5 * span) / (2 * beta_factor * e_parameter + 3))
    #         bending_moment_at_beam_ends = -(0.75 * ((0.5 * span) / (2 * beta_factor * e_parameter + 3)))
    #         bending_moment_at_beam_midspan = (span / 8) * (
    #                     (4 * beta_factor * e_parameter + 3) / (2 * beta_factor * e_parameter + 3))
    #         opening_diameter = float(self.lineEdit_2.text()) if self.lineEdit_2.text() else 1  # Opening diameter in mm
    #         dimensions = self.ipe_sections[selected_section]
    #         dg = float(self.lineEdit_col_3.text()) if self.lineEdit_col_3.text() else 0
    #
    #         parent_section_depth = dimensions['h']
    #         parent_section_flange_width = dimensions['b']
    #         parent_section_flange_thickness = dimensions['t']
    #         parent_section_web_thickness = dimensions['s']
    #
    #         dt_net = (dg - opening_diameter) / 2
    #         y = math.sqrt((opening_diameter / 2) ** 2 - (0.225 * opening_diameter) ** 2)
    #         dt_critical = (opening_diameter / 2) - y + dt_net
    #         y_bar_tee_net = self.y_bar_tee_function(parent_section_flange_width, parent_section_flange_thickness,
    #                                                 dt_net, parent_section_web_thickness)
    #         d_effec_critical = dg - 2 * (dt_critical - y_bar_tee_net)
    #
    #         # Find the summary tab
    #         summary_tab = self.tabWidget.widget(0)
    #
    #         # Ensure the summary tab has a layout
    #         if summary_tab.layout() is None:
    #             summary_tab.setLayout(QVBoxLayout())
    #
    #         # Check if the table already exists and remove it if it does
    #         for i in reversed(range(summary_tab.layout().count())):
    #             widget = summary_tab.layout().itemAt(i).widget()
    #             if isinstance(widget, QTableWidget):
    #                 widget.deleteLater()
    #
    #         # Create and configure the table widget
    #         table = QTableWidget()
    #         table.setRowCount(len(self.circle_positions))
    #         table.setColumnCount(6)
    #         table.setHorizontalHeaderLabels(
    #             ["Opening No.", "Xi (m)", "Global Mr (kNm)", "Local Pr (kN)", "Global Vr (kN)", "Local Mvr (kNm)"])
    #
    #         for row, (num, pos) in enumerate(self.circle_positions):
    #             num_item = QTableWidgetItem(str(num))
    #             pos_item = QTableWidgetItem(f"{pos:.2f}")
    #
    #             # Calculate shear force and bending moment
    #             if pos < span / 2:
    #                 shear_force = 0.5
    #                 local_axial_force = bending_moment_at_beam_ends + (support_reaction_y * pos)
    #                 local_axial_force = local_axial_force / d_effec_critical
    #                 vierendeel_moment = (shear_force / 2) * (opening_diameter / 4)
    #             elif pos == span / 2:
    #                 shear_force = 1
    #                 local_axial_force = bending_moment_at_beam_ends + (support_reaction_y * pos)
    #                 local_axial_force = local_axial_force / d_effec_critical
    #                 vierendeel_moment = (shear_force / 2) * (opening_diameter / 4)
    #             else:
    #                 shear_force = -0.5
    #                 local_axial_force = bending_moment_at_beam_ends + (support_reaction_y * pos) - (
    #                             pos - span / 2)
    #                 local_axial_force = local_axial_force / d_effec_critical
    #                 vierendeel_moment = (shear_force / 2) * (opening_diameter / 4)
    #
    #             shear_item = QTableWidgetItem(f"{shear_force:.2f}")
    #             local_axial_force_item = QTableWidgetItem(f"{local_axial_force:.2f}")
    #             local_axial_force_item = QTableWidgetItem(f"{local_axial_force:.2f}")
    #             vierendeel_moment_item = QTableWidgetItem(f"{vierendeel_moment:.2f}")
    #
    #             # Center-align the text in the cells
    #             num_item.setTextAlignment(Qt.AlignCenter)
    #             pos_item.setTextAlignment(Qt.AlignCenter)
    #             shear_item.setTextAlignment(Qt.AlignCenter)
    #             local_axial_force_item.setTextAlignment(Qt.AlignCenter)
    #             local_axial_force_item.setTextAlignment(Qt.AlignCenter)
    #             vierendeel_moment_item.setTextAlignment(Qt.AlignCenter)
    #
    #             table.setItem(row, 0, num_item)
    #             table.setItem(row, 1, pos_item)
    #             table.setItem(row, 2, local_axial_force_item)
    #             table.setItem(row, 3, local_axial_force_item)
    #             table.setItem(row, 4, shear_item)
    #             table.setItem(row, 5, vierendeel_moment_item)
    #
    #         table.resizeColumnsToContents()
    #         table.sortByColumn(1)
    #
    #         table_layout = summary_tab.layout()
    #         table_layout.addWidget(table)
    #     except Exception as e:
    #         self.label_46.setText(f"Error: {e}!")

# def section_geometry(self):
    #     opening_diameter = float(self.lineEdit_2.text()) / 1000 if self.lineEdit_2.text() else 0  # Opening diameter in meters
    #     selected_section = self.comboBox.currentText()
    #     dimensions = self.ipe_sections[selected_section]
    #     parent_section_depth = dimensions['h']
    #     parent_section_flange_width = dimensions['b']
    #     parent_section_flange_thickness = dimensions['t']
    #     parent_section_web_thickness = dimensions['s']
    #     dt_net = (dg - opening_diameter) / 2
    #     y = math.sqrt((opening_diameter / 2)**2 - (0.225 * opening_diameter)**2)
    #     dt_critical = (opening_diameter / 2) - y + dt_net
    #     area_tee_net = parent_section_flange_width * parent_section_flange_thickness + (dt_net - parent_section_flange_thickness) * parent_section_web_thickness
    #     area_net = 2 * area_tee_net
    #     y_bar_tee = dg / 2
    #     y_bar_tee_net = (((parent_section_flange_width * parent_section_flange_thickness) * (dt_net - parent_section_flange_thickness / 2)
    #                      + (parent_section_web_thickness * (dt_net - parent_section_flange_thickness)**2 / 2))
    #                      / ((parent_section_flange_width * parent_section_flange_thickness)
    #                         + parent_section_web_thickness * (dt_net - parent_section_flange_thickness)))
    #     ix_tee_net = (((parent_section_flange_width**3 * parent_section_flange_thickness) / 12)
    #                   + (parent_section_flange_thickness * parent_section_flange_width * (dt_net - y_bar_tee_net - parent_section_flange_thickness / 2))
    #                   + (parent_section_web_thickness**3 * (dt_net - parent_section_flange_thickness) / 12)
    #                   + (parent_section_web_thickness * (dt_net - parent_section_flange_thickness) * (dt_net - parent_section_flange_thickness - (dt_net - parent_section_flange_thickness) / 2)))
    #     self.label_49.setText(f"{ix_tee_net}")

    # def structural_analysis_FBD(self):
    #     ss = SystemElements(EA=15000, EI=5000)
    #
    #     # Add beams to the system.
    #     ss.add_element(location=[0, 5])
    #     ss.add_element(location=[[0, 5], [2.5, 5]])
    #     ss.add_element(location=[[2.5, 5], [5, 5]])
    #     ss.add_element(location=[[5, 5], [5, 0]])
    #
    #     # Add a fixed support at node 1.
    #     ss.add_support_hinged(node_id=1)
    #
    #     # Add a rotational spring support at node 4.
    #     ss.add_support_hinged(node_id=5)
    #
    #     # Add loads.
    #     ss.point_load(Fz=-1, node_id=3)
    #
    #     # Solve
    #     ss.solve()
    #
    #     # Get visual results.
    #     ss.show_structure()
    #
    # def structural_analysis_BMD(self):
    #
    #     youngs_modulus = float(self.lineEdit_3.text()) if self.lineEdit_3.text() else 200000
    #     beam_inertia = float(self.lineEdit_8.text()) if self.lineEdit_3.text() else 0
    #     beam_area = 10
    #     column_inertia = 171000 * 100**-4
    #     column_area = 270 * 100*-2
    #     ss = SystemElements()
    #     span = float(self.lineEdit.text()) if self.lineEdit.text() else 0
    #     frame_height = float(self.lineEdit_col_2.text()) if self.lineEdit_col_2.text() else 0
    #     # Add beams to the system.
    #     ss.add_element(location=[[0, 0], [0, frame_height]], EA=youngs_modulus * column_area * 1000, EI=youngs_modulus * column_inertia * 1000)
    #     ss.add_element(location=[[0, frame_height], [(span/2), frame_height]], EA=youngs_modulus * beam_area * 1000, EI=youngs_modulus * beam_inertia * 1000)
    #     ss.add_element(location=[[(span/2), frame_height], [span, frame_height]], EA=youngs_modulus * beam_area * 1000, EI=youngs_modulus * beam_inertia * 1000)
    #     ss.add_element(location=[[span, frame_height], [span, 0]], EA=youngs_modulus * column_area * 1000, EI=youngs_modulus * column_inertia * 1000)
    #
    #     # Add a fixed support at node 1.
    #     ss.add_support_hinged(node_id=1)
    #
    #     # Add a rotational spring support at node 4.
    #     ss.add_support_hinged(node_id=5)
    #
    #     # Add loads.
    #     ss.point_load(Fz=-1000, node_id=3)
    #
    #     # Solve
    #     ss.solve()
    #     ss.show_bending_moment()
    #
    # def structural_analysis_SFD(self):
    #     ss = SystemElements(EA=15000, EI=5000)
    #
    #     # Add beams to the system.
    #     ss.add_element(location=[0, 5])
    #     ss.add_element(location=[[0, 5], [2.5, 5]])
    #     ss.add_element(location=[[2.5, 5], [5, 5]])
    #     ss.add_element(location=[[5, 5], [5, 0]])
    #
    #     # Add a fixed support at node 1.
    #     ss.add_support_hinged(node_id=1)
    #
    #     # Add a rotational spring support at node 4.
    #     ss.add_support_hinged(node_id=5)
    #
    #     # Add loads.
    #     ss.point_load(Fz=-1, node_id=3)
    #
    #     # Solve
    #     ss.solve()
    #     ss.show_shear_force()
    #
    # def structural_analysis_NFD(self):
    #     ss = SystemElements(EA=15000, EI=5000)
    #
    #     # Add beams to the system.
    #     ss.add_element(location=[0, 5])
    #     ss.add_element(location=[[0, 5], [2.5, 5]])
    #     ss.add_element(location=[[2.5, 5], [5, 5]])
    #     ss.add_element(location=[[5, 5], [5, 0]])
    #
    #     # Add a fixed support at node 1.
    #     ss.add_support_hinged(node_id=1)
    #
    #     # Add a rotational spring support at node 4.
    #     ss.add_support_hinged(node_id=5)
    #
    #     # Add loads.
    #     ss.point_load(Fz=-1, node_id=3)
    #
    #     # Solve
    #     ss.solve()
    #     ss.show_axial_force()
    #
    # def structural_analysis_DISP(self):
    #     ss = SystemElements(EA=15000, EI=5000)
    #
    #     # Add beams to the system.
    #     ss.add_element(location=[0, 5])
    #     ss.add_element(location=[[0, 5], [2.5, 5]])
    #     ss.add_element(location=[[2.5, 5], [5, 5]])
    #     ss.add_element(location=[[5, 5], [5, 0]])
    #
    #     # Add a fixed support at node 1.
    #     ss.add_support_hinged(node_id=1)
    #
    #     # Add a rotational spring support at node 4.
    #     ss.add_support_hinged(node_id=5)
    #
    #     # Add loads.
    #     ss.point_load(Fz=-1, node_id=3)
    #
    #     # Solve
    #     ss.solve()
    #     ss.show_displacement()
    #
    # def structural_analysis_results(self):
    #     ss = SystemElements(EA=15000, EI=5000)
    #
    #     # Add beams to the system.
    #     ss.add_element(location=[0, 5])
    #     ss.add_element(location=[[0, 5], [2.5, 5]])
    #     ss.add_element(location=[[2.5, 5], [5, 5]])
    #     ss.add_element(location=[[5, 5], [5, 0]])
    #
    #     # Add a fixed support at node 1.
    #     ss.add_support_hinged(node_id=1)
    #
    #     # Add a rotational spring support at node 4.
    #     ss.add_support_hinged(node_id=5)
    #
    #     # Add loads.
    #     ss.point_load(Fz=-30, node_id=3)
    #
    #     # Solve
    #     ss.solve()
    #     ss.show_results()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
