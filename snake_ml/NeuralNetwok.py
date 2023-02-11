from Config import *
from Layer import Layer
import copy

class NeuralNetwork:

    def __init__(self, inputNodes: int, hiddenNodes: list[int], outputNodes: int):
        self.inputNodes = inputNodes
        self.hiddenNodes = hiddenNodes
        self.outputNodes = outputNodes
        self.layers: list[Layer] = []

        self.layers.append(Layer(inputNodes, hiddenNodes[0]))

        for i in range(len(hiddenNodes) - 1):
            self.layers.append(Layer(hiddenNodes[i], hiddenNodes[i+1]))

        self.layers.append(
            Layer(hiddenNodes[-1], outputNodes, activation="softmax"))

    def forward(self, input: np.ndarray) -> np.ndarray:
        output = input
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def copy(self) -> "NeuralNetwork":
        return copy.deepcopy(self)

    def mutate(self, rate):
        for layer in self.layers:
            layer.mutate(rate)

    def crossover(self, partner: "NeuralNetwork") -> "NeuralNetwork":
        child = NeuralNetwork(
            self.inputNodes, self.hiddenNodes, self.outputNodes)

        for i in range(len(self.layers)):
            child.layers[i] = self.layers[i].crossover(partner.layers[i])

        return child
