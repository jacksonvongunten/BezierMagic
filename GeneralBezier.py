from math import sqrt
from Point2D import Point2D
from MathHelperFunctions import MathHelperFunctions
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

class GeneralBezier:

    def __init__(self, p):
        self.t = MathHelperFunctions.linspace(0, 1, 200)
        self.p = p
    
    def __repr__(self):
        return "Bezier Curve of order {} connecting points ({}, {}) and ({}, {})".format(len(self.p), self.p[0].get_x(), self.p[0].get_y(), self.p[len(self.p)-1].get_x(), self.p[len(self.p)-1].get_y())
    
    def add_control_points(self, points):
        for i in range(len(points)):
            self.p.insert(i+1, points[i])

    def get_points(self):
        return self.p
    
    def generate_x(self):
        n = len(self.get_points())
        return [ sum( [MathHelperFunctions.choose(n-1, i)*(1-t)**((n-1)-i)*(t**i) * self.p[i].get_x() for i in range(n)] ) for t in self.t ]

    def generate_y(self):
        n = len(self.get_points())
        return [ sum( [MathHelperFunctions.choose(n-1, i)*(1-t)**((n-1)-i)*(t**i) * self.p[i].get_y() for i in range(n)] ) for t in self.t ]

    def rough_path(self):
        self.lines = [GeneralBezier([self.p[i-1], self.p[i]]) for i in range(1, len(self.p))]
        return self.lines
    
    def generate_x_velocity(self):
        dt = 1/len(self.t)
        x_derivatives = []
        x_positions = self.generate_x()
        for i in range(1, len(x_positions)):
            x_derivatives.append((x_positions[i]-x_positions[i-1])/dt)
        return x_derivatives
    
    def generate_y_velocity(self):
        dt = 1/len(self.t)
        y_derivatives = []
        y_positions = self.generate_y()
        for i in range(1, len(y_positions)):
            y_derivatives.append((y_positions[i]-y_positions[i-1])/dt)
        return y_derivatives
    
    def generate_velocity(self):
        return [ sqrt(v[0]**2 + v[1]**2) for v in zip(self.generate_x_velocity(), self.generate_y_velocity()) ]

    def generate_x_acceleration(self):
        dt = 1/len(self.t)
        x_derivatives = []
        x_velocities = self.generate_x_velocity()
        for i in range(1, len(x_velocities)):
            x_derivatives.append((x_velocities[i]-x_velocities[i-1])/dt)
        return x_derivatives
    
    def generate_y_acceleration(self):
        dt = 1/len(self.t)
        y_derivatives = []
        y_velocities = self.generate_y_velocity()
        for i in range(1, len(y_velocities)):
            y_derivatives.append((y_velocities[i]-y_velocities[i-1])/dt)
        return y_derivatives

    def generate_acceleration(self):
        return [ sqrt(a[0]**2 + a[1]**2) for a in zip(self.generate_x_acceleration(), self.generate_y_acceleration()) ]

    def plot(self):
        velocities = self.generate_velocity()
        accelerations = self.generate_acceleration()
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)
        plt.grid()
        plt.title("Bezier Curve")
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        xdata, ydata = [], []
        ln, = plt.plot([], [], color='k')

        def update(t):
            xdata = self.generate_x()[:int(t*199)]
            ydata = self.generate_y()[:int(t*199)]
            ln.set_data(xdata, ydata)
            velocity_slider.set_val(velocities[int(t*198)])
            acceleration_slider.set_val(accelerations[int(t*197)])

        for i in range(len(self.get_points())):
            plt.plot(self.get_points()[i].get_x(), self.get_points()[i].get_y(), marker="x", color="b")
        for path in self.rough_path():
            plt.plot(path.generate_x(), path.generate_y(), color='b', linestyle="dashed")

        axslider1 = plt.axes([0.25, 0.15, 0.50, 0.02])
        time_slider = Slider(axslider1, "Time", 0, 1, 0)

        axslider2 = plt.axes([0.25, 0.1, 0.50, 0.02])
        velocity_slider = Slider(axslider2, "Velocity", 0, max(velocities), 0)

        axslider3 = plt.axes([0.25, 0.05, 0.50, 0.02])
        acceleration_slider = Slider(axslider3, "Acceleration", 0, max(accelerations), 0)

        time_slider.on_changed(update)
        
        plt.show()