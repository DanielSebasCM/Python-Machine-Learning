import numpy as np

class Layer:
    def __init__(self, inputNodes, outputNodes, activation='relu') -> None:
        self.weights = np.random.uniform(0, 0.5, (outputNodes, inputNodes))
        self.bias = np.random.uniform(0, 0.5, (outputNodes, 1))
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
        self.z = np.dot(self.weights, input) + self.bias
        return self.activation(self.z)

    def mutate(self, rate):
        rate = rate / 100
        self.weights += np.random.uniform(-rate, rate, self.weights.shape)
        self.bias += np.random.uniform(-rate, rate, self.bias.shape)

    def copy(self):
        layer = Layer(self.weights.shape[1], self.weights.shape[0])
        layer.weights = self.weights.copy()
        layer.bias = self.bias.copy()
        return layer

    def softmax(self, z):
        exp_values = np.exp(z - np.max(z, axis=1, keepdims=True))
        probapillities = exp_values/np.sum(exp_values, axis=1, keepdims=True)
        return probapillities
