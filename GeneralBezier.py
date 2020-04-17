from Point2D import Point2D
from MathHelperFunctions import MathHelperFunctions
from matplotlib import pyplot as plt

class GeneralBezier:

    def __init__(self, p):
        self.t = MathHelperFunctions.linspace(0, 1, 1000)
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

    def plot(self):
        for i in range(len(self.get_points())):
            plt.plot(self.get_points()[i].get_x(), self.get_points()[i].get_y(), marker="x", color="b")
        for path in self.rough_path():
            plt.plot(path.generate_x(), path.generate_y(), color='b', linestyle="dashed")
        plt.plot(self.generate_x(), self.generate_y(), color="k")
        plt.grid()
        plt.title("Bezier Curve")
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.show()