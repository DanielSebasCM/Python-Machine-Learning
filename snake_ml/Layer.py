import numpy as np


class Layer:
    def __init__(self, inputNodes: int, outputNodes: int, activation='relu', scale: float = 0.1) -> None:
        self.scale = scale
        shape = (inputNodes, outputNodes)
        self.weights = np.random.uniform(0, self.scale, shape)
        self.bias = np.zeros(outputNodes)
        if activation == 'relu':
            self.activation = self.relu
        elif activation == 'softmax':
            self.activation = self.softmax
        else:
            raise Exception("Activation function not found")

        self.z = None

    def relu(self, z):
        return np.maximum(0, z)

    def forward(self, input):
        self.z = np.dot(input, self.weights) + self.bias
        return self.activation(self.z)

    def mutate(self, rate):
        rate = rate / 100
        self.weights += np.random.uniform(-rate,
                                          rate, self.weights.shape) * self.scale
        self.bias += np.random.uniform(-rate,
                                       rate, self.bias.shape) * self.scale

    def softmax(self, z):
        exp_values = np.exp(z - np.max(z, axis=1, keepdims=True))
        probapillities = exp_values/np.sum(exp_values, axis=1, keepdims=True)
        return probapillities
