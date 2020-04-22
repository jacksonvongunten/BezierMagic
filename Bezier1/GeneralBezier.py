from Point2D import Point2D
from MathHelperFunctions import MathHelperFunctions
from math import sqrt, atan2, pi, cos, sin
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, TextBox
import matplotlib.patches as patches

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
    
    def generate_tangent_vector(self):
        x = self.generate_x()
        y = self.generate_y()
        dx = self.generate_x_derivative()
        dy = self.generate_y_derivative()
        vectors = [(dx[i], dy[i]) for i in range(len(dx))]
        magnitudes = [sqrt(v[0]**2 + v[1]**2) for v in vectors]
        return [(vectors[i][0]/magnitudes[i], vectors[i][1]/magnitudes[i]) for i in range(len(vectors))]
    
    def generate_normal_vector(self):
        T = self.generate_tangent_vector()
        return [ (v[1], -v[0]) for v in T ]
    
    def generate_heading(self):
        T = self.generate_tangent_vector()
        return [ atan2(t[1], t[0]) for t in T ]

    def generate_trajectories(self):
        xdata = self.generate_x()
        ydata = self.generate_y()
        headings = self.generate_heading()
        left_x = [xdata[i] - 0.5*sin(headings[i]) for i in range(len(headings))]
        left_y = [ydata[i] + 0.5*cos(headings[i]) for i in range(len(headings))]
        right_x = [xdata[i] + 0.5*sin(headings[i]) for i in range(len(headings))]
        right_y = [ydata[i] - 0.5*cos(headings[i]) for i in range(len(headings))]
        return ((left_x, left_y), (right_x, right_y))    

    def plot(self):
        plt.style.use("classic")
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)
        plt.grid()
        plt.title("Bezier Curve")
        plt.xlabel("X [Position]")
        plt.ylabel("Y [Position]")
        xdata, ydata = [], []
        ln, = plt.plot([], [], color='k', linestyle='dashed')
        points, = plt.plot([], [], color='b', marker='x')
        paths, = plt.plot([], [], color='b')
        tangent, = plt.plot([], [], color='r', marker='x')
        left_traj, = plt.plot([], [], color='r')
        right_traj, = plt.plot([], [], color='r')
        rect1 = patches.Rectangle((1, 0), 3, 3, color='r')
        rect2 = patches.Rectangle((6, 3), 2, 1, color='r')
        ax.add_patch(rect1)
        ax.add_patch(rect2)

        def draw_control_points():
            self.control_points_from_file("control_points.txt")
            waypoints = self.get_points()
            control_point_x = [point.get_x() for point in waypoints]
            points.set_xdata(control_point_x)
            control_point_y = [point.get_y() for point in waypoints]
            points.set_ydata(control_point_y)
            rough_paths = self.rough_path()
            paths.set_xdata([path.generate_x() for path in rough_paths])
            paths.set_ydata([path.generate_y() for path in rough_paths])
            ax.set_xlim(min(control_point_x)-1, max(control_point_x)+1)
            ax.set_ylim(min(control_point_y)-1, max(control_point_y)+1)

        draw_control_points()

        def update(t):
            ax.set_aspect('equal')
            
            draw_control_points()
            xdata = self.generate_x()[:int(t*199)]
            ydata = self.generate_y()[:int(t*199)]

            left_trajectory_data, right_trajectory_data = self.generate_trajectories()

            ln.set_data(xdata, ydata)
            if t != 0:
                left_traj.set_data(left_trajectory_data[0][:int(t*199)], left_trajectory_data[1][:int(t*199)])
                right_traj.set_data(right_trajectory_data[0][:int(t*199)], right_trajectory_data[1][:int(t*199)])
            else:
                left_traj.set_data(0, 0)
                right_traj.set_data(0, 0)

        axslider1 = plt.axes([0.25, 0.15, 0.50, 0.02])
        time_slider = Slider(axslider1, "t", 0, 1, 0)

        time_slider.on_changed(update)
        
        plt.show()