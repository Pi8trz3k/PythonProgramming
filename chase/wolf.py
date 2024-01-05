import simulation_objects as so

class Wolf(so.SimulationObjects):
    def __init__(self):
        super().__init__(0.000, 0.000, 1)

    def to_dict(self):
        return [self.get_x(), self.get_y()]