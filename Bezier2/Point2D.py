class Point2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y