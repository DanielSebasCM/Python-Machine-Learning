from Config import *
import copy


class Layer:
    def __init__(self, inputNodes: int, outputNodes: int, activation='sigmoid', scale: float = 1) -> None:
        self.scale = scale
        shape = (inputNodes, outputNodes)
        self.weights = np.random.normal(0, self.scale * 0.3, shape)
        self.bias = np.random.normal(0, self.scale * 0.3, (1, outputNodes))
        if activation == 'relu':
            self.activation = self.relu
        elif activation == 'softmax':
            self.activation = self.softmax
        elif activation == 'sigmoid':
            self.activation = self.sigmoid
        else:
            raise Exception("Activation function not found")

        self.z = None

    def forward(self, input):
        self.z = np.dot(input, self.weights) + self.bias
        return self.activation(self.z)

    def copy(self) -> "Layer":
        return copy.deepcopy(self)

    def mutate(self, rate):
        mask = np.random.random(self.weights.shape) < rate
        self.weights[mask] += np.random.normal(0,
                                               0.2, self.weights.shape)[mask] * self.scale

        self.weights[self.weights > 1] = 1
        self.weights[self.weights < -1] = -1

        mask = np.random.random(self.bias.shape) < rate
        self.bias[mask] += np.random.normal(0,
                                            0.1, self.bias.shape)[mask] * self.scale

        self.bias[self.bias > 1] = 1
        self.bias[self.bias < -1] = -1

    def crossover(self, partner: "Layer") -> "Layer":
        # child = self.copy()

        # randRowstart, randRowEnd = self.getRandStartEnd(self.weights.shape[0])
        # randColStart, randColEnd = self.getRandStartEnd(self.weights.shape[1])
        # child.weights[randRowstart:randRowEnd,
        #               randColStart:randColEnd] = partner.weights[randRowstart:randRowEnd, randColStart:randColEnd]

        # randBiasStart, randBiasEnd = self.getRandStartEnd(self.bias.shape[0])
        # child.bias[randBiasStart:randBiasEnd] = partner.bias[randBiasStart:randBiasEnd]

        # return child

        child = self.copy()

        for i in range(self.weights.shape[0]):
            for j in range(self.weights.shape[1]):
                if np.random.random() < 0.5:
                    child.weights[i, j] = partner.weights[i, j]

        for i in range(self.bias.shape[0]):
            if np.random.random() < 0.5:
                child.bias[i] = partner.bias[i]

        return child

    def getRandStartEnd(self, size):
        start = np.random.randint(0, size)
        end = np.random.randint(0, size)
        if start > end:
            start, end = end, start
        return start, end

    def relu(self, z):
        return np.maximum(0, z)

    def softmax(self, z):
        exp_values = np.exp(z - np.max(z, axis=1, keepdims=True))
        probapillities = exp_values/np.sum(exp_values, axis=1, keepdims=True)
        return probapillities

    def sigmoid(self, z):
        return 1/(1+np.exp(-z))
