from math import sqrt, atan2

class Point2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = sqrt(self.x**2 + self.y**2)
        self.theta = atan2(self.y, self.x)
        self.cartestian = (self.x, self.y)
        self.polar = (self.r, self.theta)
    
    def __repr__(self):
        return "Cartestian: ({}, {})\nPolar: ({}, {})".format(self.x, self.y, self.r, self.theta)
    
    def get_cartestian(self):
        return self.cartestian
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_polar(self):
        return self.polar