from Point2D import Point2D
from MathHelperFunctions import MathHelperFunctions
from math import sqrt
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, TextBox

class BezierCurve:

    def __init__(self, p):
        self.t = MathHelperFunctions.linspace(0, 1, 200)
        self.p = p
    
    def __repr__(self):
        return "Bezier Curve of order {} connecting points ({}, {}) and ({}, {})".format(len(self.p), self.p[0].get_x(), self.p[0].get_y(), self.p[len(self.p)-1].get_x(), self.p[len(self.p)-1].get_y())
    
    def add_control_points(self, points):
        for i in range(len(points)):
            self.p.insert(i+1, points[i])
    
    def remove_control_points(self):
        del self.p[1:len(self.p)-1]
    
    def update_control_points(self, points):
        self.remove_control_points()
        self.add_control_points(points)
    
    def control_points_from_file(self, filename):
        control_points = []
        with open(filename, "r") as f:
            for line in f.readlines():
                point = line.rstrip().split(" ")
                control_points.append(Point2D(float(point[0]), float(point[1])))
        self.update_control_points(control_points)

    def get_points(self):
        return self.p
    
    def generate_x(self):
        n = len(self.get_points())
        return [ sum( [MathHelperFunctions.choose(n-1, i)*(1-t)**((n-1)-i)*(t**i) * self.p[i].get_x() for i in range(n)] ) for t in self.t ]

    def generate_y(self):
        n = len(self.get_points())
        return [ sum( [MathHelperFunctions.choose(n-1, i)*(1-t)**((n-1)-i)*(t**i) * self.p[i].get_y() for i in range(n)] ) for t in self.t ]

    def rough_path(self):
        self.lines = [BezierCurve([self.p[i-1], self.p[i]]) for i in range(1, len(self.p))]
        return self.lines
    
    def generate_x_derivative(self):
        xdata = self.generate_x()
        return [round((xdata[i]-xdata[i-1])/(1/len(self.t)), 2) for i in range(1, len(xdata))]
    
    def generate_y_derivative(self):
        ydata = self.generate_y()
        return [round((ydata[i]-ydata[i-1])/(1/len(self.t)), 2) for i in range(1, len(ydata))]

    def generate_derivative(self):
        dx = self.generate_x_derivative()
        dy = self.generate_y_derivative()
        return [ round(dy[i]/dx[i],2) for i in range(len(dx))]

    def plot(self):
        plt.style.use("classic")
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)
        plt.grid()
        plt.title("Bezier Curve")
        plt.xlabel("X [Position]")
        plt.ylabel("Y [Position]")
        xdata, ydata = [], []
        ln, = plt.plot([], [], color='k')
        points, = plt.plot([], [], color='b', marker='x')
        paths, = plt.plot([], [], color='b')
        # dt = self.generate_derivative()
        # dx = self.generate_x_derivative()
        # dy = self.generate_y_derivative()

        def draw_control_points():
            self.control_points_from_file("control_points.txt")
            control_point_x = [self.get_points()[i].get_x() for i in range(len(self.get_points()))]
            points.set_xdata(control_point_x)
            control_point_y = [self.get_points()[i].get_y() for i in range(len(self.get_points()))]
            points.set_ydata(control_point_y)
            paths.set_xdata([path.generate_x() for path in self.rough_path()])
            paths.set_ydata([path.generate_y() for path in self.rough_path()])

            ax.set_xlim(min(control_point_x)-1, max(control_point_x)+1)
            ax.set_ylim(min(control_point_y)-1, max(control_point_y)+1)

        draw_control_points()

        def update(t):
            draw_control_points()
            # dt = self.generate_derivative()
            # dx = self.generate_x_derivative()
            # dy = self.generate_y_derivative()
            xdata = self.generate_x()[:int(t*199)]
            ydata = self.generate_y()[:int(t*199)]
            # derivative_box.set_val(str(dt[int(t*198)]))
            # dx_box.set_val(str(dx[int(t*198)]))
            # dy_box.set_val(str(dy[int(t*198)]))
            ln.set_data(xdata, ydata)

        axslider1 = plt.axes([0.25, 0.15, 0.50, 0.02])
        time_slider = Slider(axslider1, "t", 0, 1, 0)

        # axbox1 = plt.axes([0.25, 0.05, 0.05, 0.05])
        # derivative_box = TextBox(axbox1, 'dy/dx ', initial=str(dt[0]))

        # axbox2 = plt.axes([0.5, 0.05, 0.05, 0.05])
        # dx_box = TextBox(axbox2, 'dx/dt ', initial=str(dx[0]))

        # axbox3 = plt.axes([0.75, 0.05, 0.05, 0.05])
        # dy_box = TextBox(axbox3, 'dy/dt ', initial=str(dy[0]))

        time_slider.on_changed(update)
        
        plt.show()