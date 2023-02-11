from Snake import Snake
from Config import *


class Population:

    def __init__(self, nSnakes) -> None:
        self.populationSize = nSnakes
        self.snakes = np.array([Snake() for _ in range(nSnakes)])
        self.chooseSnake = self.turnamentSelection

    def turnamentSelection(self) -> Snake:
        k = self.populationSize//8
        snakes: ndarray = np.random.choice(self.snakes, k, replace=False)

        # return best snake by fitness
        return snakes[np.argmax([snake.getFitness() for snake in snakes])]

    def bestSnake(self) -> Snake:
        return self.snakes[np.argmax([snake.getFitness() for snake in self.snakes])]

    def createNextGeneration(self) -> None:
        # Create new snakes
        newSnakes = np.array([Snake(createBrain=False)
                             for _ in range(self.populationSize)])

        # Select the best snake
        newSnakes[0].brain = self.bestSnake().brain.copy()

        # Crossover and mutate
        for i in range(1, self.populationSize):
            parentA = self.chooseSnake()
            parentB = self.chooseSnake()

            childBrain = parentA.brain.crossover(parentB.brain)
            childBrain.mutate(0.3)

            newSnakes[i].brain = childBrain

        # Replace the old snakes
        self.snakes = newSnakes
