import numpy as np
import matplotlib.pyplot as plt

class DifferentialDrive:

    def __init__(self, trackwidth, path, v_max, a_max, j_max):
        self.path = path
        self.trackwidth = trackwidth
        self.v_max = v_max
        self.a_max = a_max
        self.j_max = j_max
        self.t = 0

        self.velocities = []
        self.x_velocities = []
        self.y_velocities = []
    
    def get_velocities_along_path(self):
        delta = 0.01
        length = self.path.get_length_at_t(1)
        t_k = [ self.v_max/self.a_max, self.a_max/self.j_max ]
        t = [ np.arange(0, t_i, delta) for t_i in t_k ]
        h_k = [ (1/t_k[i])*np.ones(t[i].size) for i in range(len(t_k)) ]
        
        t_0 = length/self.v_max
        t_y = np.arange(0, t_0, delta)
        y = self.v_max*np.ones(t_y.size)
        for h in h_k:
            y = np.convolve(y, h)*delta
        
        t = np.arange(0, t_0+sum(t_k), delta)
        self.t = t[:len(y)]

        self.velocities = y