import random, math

# For Flappy Bird (NeuroEvolution)
class NonLinearNeuron:
    def __init__(self):
        self.w1 = random.uniform(-1, 1)
        self.w2 = random.uniform(-1, 1)
        self.w3 = random.uniform(-1, 1)
        self.w4 = random.uniform(-1, 1)
        self.w5 = random.uniform(-1, 1)
        self.b = random.uniform(-1, 1)

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def prediction(self, y, vel, pipe_x, pipe_gap_h, pipe_gap):
        return self.sigmoid(y * self.w1 + vel * self.w2 + pipe_x * self.w3 + pipe_gap_h * self.w4 + pipe_gap * self.w5 + self.b)