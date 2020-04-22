from Point2D import Point2D
from DiscreteSet import DiscreteSet
from matplotlib import pyplot as plt
from functools import reduce
import operator as op
from math import sqrt

def comb(n, r):
    r = min(r, n-r)
    numerator = reduce(op.mul, range(n, n-r, -1), 1)
    denominator = reduce(op.mul, range(1, r+1), 1)
    return numerator / denominator

class BezierCurve:

    def __init__(self, points):
        self.points = points
        self.t = DiscreteSet(0, 1, 250)
    
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
    
    def x_coords(self):
        n = len(self.points)
        return [ sum( [comb(n-1, i)*(1-t)**((n-1)-i)*(t**i) * self.points[i].get_x() for i in range(n)] ) for t in self.t.get() ]

    def y_coords(self):
        n = len(self.points)
        return [ sum( [comb(n-1, i)*(1-t)**((n-1)-i)*(t**i) * self.points[i].get_y() for i in range(n)] ) for t in self.t.get() ]

    def get_x_derivative(self):
        x = self.x_coords()
        return [(x[i]-x[i-1])/(self.t.dt) for i in range(1, len(x))]
    
    def get_y_derivative(self):
        y = self.y_coords()
        return [(y[i]-y[i-1])/(self.t.dt) for i in range(1, len(y))]
    
    def get_tangent_points(self):
        dx = self.get_x_derivative()
        dy = self.get_y_derivative()
        magnitudes = [ sqrt(dx[i]**2 + dy[i]**2) for i in range(len(dx)) ]
        return [ (dx[i]/magnitudes[i], dy[i]/magnitudes[i]) for i in range(len(magnitudes)) ]
    
    def get_normal_points(self):
        tangent_points = self.get_tangent_points()
        return [ (-y, x) for (x, y) in tangent_points ]

    def control_point_path(self):
        return [BezierCurve([self.points[i-1], self.points[i]]) for i in range(1, len(self.points))]