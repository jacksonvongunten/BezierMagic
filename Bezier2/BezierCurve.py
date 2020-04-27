from Point2D import Point2D
import numpy as np
import scipy.signal as signal
from scipy.special import binom
from matplotlib import pyplot as plt

class BezierCurve:

    def __init__(self, points):
        self.points = points
        self.t = np.linspace(0, 1, 1000)
        self.dt = self.t[1] - self.t[0]
        self.x = []
        self.y = []
        self.dx = []
        self.dy = []
        self.dx2 = []
        self.dy2 = []

        self.headings = []
        self.t_v = []
        self.velocities = []
    
    def get_points(self):
        return [(point.get_x(), point.get_y()) for point in self.points]
    
    def get_t(self):
        return self.t
    
    def add_control_points(self, control_points):
        for i in range(len(control_points)):
            self.points.insert(i+1, control_points[i])
    
    def remove_control_points(self):
        del self.points[1:len(self.points)-1]
    
    def update_control_points(self, control_points):
        self.remove_control_points()
        self.add_control_points(control_points)
    
    def load_control_points_from_file(self, filename):
        control_points = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                point = line.rstrip().split(" ")
                control_points.append(Point2D(float(point[0]), float(point[1])))
        self.update_control_points(control_points)
        self.x_coords()
        self.y_coords()
        self.get_x_derivative()
        self.get_y_derivative()
        self.get_x_second_derivative()
        self.get_y_second_derivative()
    
    def x_coords(self):
        n = len(self.points)
        self.x = [ sum( [binom(n-1, i)*(1-t)**((n-1)-i)*(t**i) * self.points[i].get_x() for i in range(n)] ) for t in self.t ]
        return self.x

    def y_coords(self):
        n = len(self.points)
        self.y = [ sum( [binom(n-1, i)*(1-t)**((n-1)-i)*(t**i) * self.points[i].get_y() for i in range(n)] ) for t in self.t ]
        return self.y

    def get_x_derivative(self):
        self.dx = [(self.x[i]-self.x[i-1])/(self.dt) for i in range(1, len(self.x))]
        return self.dx
    
    def get_y_derivative(self):
        self.dy = [(self.y[i]-self.y[i-1])/(self.dt) for i in range(1, len(self.y))]
        return self.dy
    
    def get_x_second_derivative(self):
        self.dx2 = [(self.dx[i]-self.dx[i-1])/(self.dt) for i in range(1, len(self.dx))]
        return self.dx2
    
    def get_y_second_derivative(self):
        self.dy2 = [(self.dy[i]-self.dy[i-1])/(self.dt) for i in range(1, len(self.dy))]
        return self.dy2
    
    def get_curvature_at_t(self, t):
        index = int(t*self.t.size-3)
        curvature = (self.dx[index]*self.dy2[index] - self.dy[index]*self.dx2[index])/((self.dx[index]**2 + self.dy[index]**2)**(1.5))
        if curvature != 0:
            return curvature
        else:
            return 0

    def get_tangent_points(self):
        magnitudes = [ np.sqrt(self.dx[i]**2 + self.dy[i]**2) for i in range(len(self.dx)) ]
        return [ (self.dx[i]/magnitudes[i], self.dy[i]/magnitudes[i]) for i in range(len(magnitudes)) ]
    
    def get_normal_points(self):
        tangent_points = self.get_tangent_points()
        return [ (-y, x) for (x, y) in tangent_points ]

    def control_point_path(self):
        return [BezierCurve([self.points[i-1], self.points[i]]) for i in range(1, len(self.points))]
    
    def get_length_at_t(self, t):
        length = int(t*self.t.size-1)
        return sum( [self.dt*np.sqrt(self.dx[i]**2 + self.dy[i]**2) for i in range(length)] )
    
    def get_headings(self):
        self.headings = [ np.arctan2(self.dy[i], self.dx[i]) for i in range(len(self.dx)) ]
        return self.headings
    
    def get_velocities_along_path(self, v_max, a_max, j_max):
        delta = 0.001
        length = self.get_length_at_t(1)
        t_0 = np.arange(0, length/v_max, delta)
        y_0 = v_max*np.ones(t_0.size)

        filter_t_1 = np.arange(0, v_max/a_max, delta)
        filter_y_1 = (a_max/v_max)*np.ones(filter_t_1.size)

        filter_t_2 = np.arange(0, a_max/j_max, delta)
        filter_y_2 = (j_max/a_max)*np.ones(filter_t_2.size)

        y = np.convolve(filter_y_1, y_0)*delta
        y = np.convolve(filter_y_2, y)*delta
        t = np.linspace(0, t_0[-1]+filter_t_1[-1]+filter_t_2[-1], y.size)

        t_new = np.linspace(0, t_0[-1]+filter_t_1[-1]+filter_t_2[-1], 1000)
        y_new = np.interp(t_new, t, y)

        self.t_v = t_new
        self.velocities = y_new
    
    def get_linear_velocity_at_t(self, t):
        return self.velocities[int(t*self.t.size-1)]

    def get_angular_velocity_at_t(self, t):
        return self.velocities[int(t*self.t.size-1)]*self.get_curvature_at_t(t)
    
    def get_right_velocity_at_t(self, trackwidth, t):
        if self.get_curvature_at_t(t):
            return self.get_angular_velocity_at_t(t)*((1/self.get_curvature_at_t(t))+(trackwidth/2))
        else:
            return self.get_linear_velocity_at_t(t)
    
    def get_left_velocity_at_t(self, trackwidth, t):
        if self.get_curvature_at_t(t):
            return self.get_angular_velocity_at_t(t)*((1/self.get_curvature_at_t(t))-(trackwidth/2))
        else:
            return self.get_linear_velocity_at_t(t)
    
    def generate_file_of_dense_points(self):
        with open("path.txt", "w") as f:
            for point in zip(self.x, self.y):
                f.write("({} {})\n".format(point[0], point[1]))
    
    def generate_file_of_states(self, trackwidth):
        velocities = [ (self.t_v[int(t*self.t_v.size-1)], self.get_linear_velocity_at_t(t), self.get_headings()[int(t*self.t.size-2)], self.get_left_velocity_at_t(trackwidth, t), self.get_right_velocity_at_t(trackwidth, t)) for t in self.t[1:] ]
        with open("states.txt", "w") as f:
            for velocity in velocities:
                f.write("t={}, v={}, theta={}, v_L={}, v_R={}\n".format(velocity[0], velocity[1], velocity[2], velocity[3], velocity[4]))