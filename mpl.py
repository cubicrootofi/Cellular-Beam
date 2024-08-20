import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Circle

class MplCanvas(FigureCanvas):
    """
    Canvas for Matplotlib plots in PyQt5.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.circles = []

    def on_click(self, event):
        """
        Handles click events on the canvas.
        """
        for circle in self.circles:
            if circle.contains_point((event.x, event.y)):
                if circle.get_facecolor() == (0, 0, 1, 0):  # Currently open (black edge, no fill)
                    circle.set_facecolor('black')  # Close it (black fill)
                else:
                    circle.set_facecolor((0, 0, 1, 0))  # Open it (no fill)
                self.draw()
                break

    def get_circle_states(self):
        """
        Returns a list indicating the open (1) or closed (0) state of each circle.
        """
        circle_states = []
        for circle in self.circles:
            if circle.get_facecolor() == (0, 0, 1, 0):  # Open
                circle_states.append(1)
            else:  # Closed
                circle_states.append(0)
        return circle_states
