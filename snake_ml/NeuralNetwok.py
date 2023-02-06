import numpy as np
from Layer import Layer


class NeuralNetwork:

    def __init__(self, inputNodes, hiddenNodes: list, outputNodes):
        self.inputNodes: int = inputNodes
        self.hiddenNodes: int = hiddenNodes
        self.outputNodes: int = outputNodes
        self.layers: list[Layer] = []

        self.layers.append(Layer(inputNodes, hiddenNodes))

        for hiddenNode in hiddenNodes:
            self.layers.append(Layer(hiddenNode, hiddenNode))

        self.layers.append(Layer(hiddenNodes, outputNodes))

    def forward(self, input):
        output = input
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def mutate(self, rate):
        for layer in self.layers:
            layer.mutate(rate)

    def copy(self):
        nn = NeuralNetwork(self.inputNodes, self.hiddenNodes, self.outputNodes)
        for i in range(len(self.layers)):
            nn.layers[i] = self.layers[i].copy()
        return nn
