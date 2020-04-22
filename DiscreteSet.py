class DiscreteSet:

    def __init__(self, start, end, length):
        self.start = start
        self.end = end
        self.length = length
        self.dt = (end-start)/length
        self.set = [start+self.dt*i for i in range(length)]
    
    def get(self):
        return self.set
    
    def get_dt(self):
        return self.dt