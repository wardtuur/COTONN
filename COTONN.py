from Importer import Importer
from Exporter import Exporter
from NeuralNetworkManager import NeuralNetworkManager
from StaticController import StaticController
from DataSet import DataSet

from NeuralNetworkManager import NNTypes
from NeuralNetworkManager import NNOptimizer
from NeuralNetworkManager import NNActivationFunction

import matplotlib.pyplot as plt

# Main class from which all functions are called
class COTONN:
    def __init__(self):
        self.version = "0.5.1"
        
        self.importer = Importer()
        self.exporter = Exporter(self.version)
        self.nnm = NeuralNetworkManager()
        self.staticController = StaticController()
        
        self.debug_mode = False
        
        self.importer.setDebugMode(False)
        self.nnm.setDebugMode(self.debug_mode)
        
        print("COTONN v" + self.version + "\n")
        
    
    # Clean memory function
    def cleanMemory(self):
        del self.nnm.nn
        del self.nnm
        del self.staticController
        del self.exporter
        del self.importer


    # Generate MLP from fullset
    def fullSetMLP(self, filename, layer_width, layer_height, learning_rate, dropout_rate, fitness_threshold, batch_size, display_step):
        self.staticController = self.importer.readStaticController(filename)
        
        fullSet = DataSet()
        fullSet.readSetFromController(self.staticController)
        fullSet.formatToBinary()
        
        self.nnm.setDebugMode(True)
        self.nnm.setType(NNTypes.MLP)
        self.nnm.setTrainingMethod(NNOptimizer.Adam)
        self.nnm.setActivationFunction(NNActivationFunction.Sigmoid)
        self.nnm.setDataSet(fullSet)
        
        self.nnm.setDropoutRate(dropout_rate)
        self.nnm.rectangularHiddenLayers(layer_width, layer_height)
        self.nnm.initialize(learning_rate, fitness_threshold, batch_size, display_step, -1, 5000)
        
        self.nnm.train()
        
        self.nnm.plot()

        fitness, wrong_states = self.nnm.checkFitness(fullSet)
        self.nnm.randomCheck(fullSet)

        self.exporter.setSaveLocation("./nn/")
        self.exporter.saveNetwork(self.nnm)
        self.exporter.saveWrongStates(wrong_states)
        self.exporter.saveRawMLP(self.nnm)
        
        self.nnm.close()
        
        self.cleanMemory()

    # Generate MLP from subset
    def subSetMLP(self, filename, percentage, layer_width, layer_height, learning_rate, dropout_rate, fitness_threshold, batch_size, display_step):
        self.staticController = self.importer.readStaticController(filename)
        
        fullSet = DataSet()
        fullSet.readSetFromController(self.staticController)
        fullSet.formatToBinary()

        subSet = DataSet()
        subSet.readSubsetFromController(self.staticController, percentage)
        subSet.formatToBinary()
        
        self.nnm.setDebugMode(True)
        self.nnm.setType(NNTypes.MLP)
        self.nnm.setTrainingMethod(NNOptimizer.Adam)
        self.nnm.setActivationFunction(NNActivationFunction.Sigmoid)
        self.nnm.setDataSet(subSet)
        
        self.nnm.setDropoutRate(dropout_rate)
        self.nnm.rectangularHiddenLayers(layer_width, layer_height)
        self.nnm.initialize(learning_rate, fitness_threshold, batch_size, display_step, -1, 5000)
        
        self.nnm.train()

        fitness, wrong_states = self.nnm.checkFitness(fullSet)
        self.nnm.randomCheck(fullSet)
        
        self.exporter.setSaveLocation("./nn/")
        self.exporter.saveNetwork(self.nnm)
        self.exporter.saveWrongStates(wrong_states)
        self.exporter.saveRawMLP(self.nnm)
        
        self.nnm.close()
        
        self.cleanMemory()


    # Scout learningrate convergence
    def scoutLearningRateConvergence(self, filename, layer_width, layer_height, epoch_threshold, rates, batch_size, display_step):
        self.staticController = self.importer.readStaticController(filename)

        dataSet = DataSet()
        dataSet.readSetFromController(self.staticController)
        dataSet.formatToBinary()

        self.nnm.setDebugMode(False)

        fitnesses = []

        for r in rates:
            print("\nLearning rate: " + str(r))
            self.nnm.setType(NNTypes.MLP)
            self.nnm.setTrainingMethod(NNOptimizer.Adam)
            self.nnm.setActivationFunction(NNActivationFunction.Sigmoid)
            self.nnm.setDataSet(dataSet)
            
            self.nnm.rectangularHiddenLayers(layer_width, layer_height)
            self.nnm.initializeNeuralNetwork()
            
            self.nnm.initializeTraining(r, 1.0, batch_size, display_step, epoch_threshold)
            self.nnm.train()

            fitness, wrong_states = self.nnm.checkFitness(dataSet)
            self.fitnesses.append(fitness)

            self.nnm.close()

        # Plot
        plt.semilogx(rates, fitnesses, 'r-')
        plt.xlabel("Rates")
        plt.ylabel("Fitness")
        plt.grid()
        (x1,x2,y1,y2) = plt.axis()
        plt.axis((min(rates),max(rates),0.0,y2+0.1))
        plt.show()
        
        self.cleanMemory()

cotonn = COTONN()
#cotonn.fullSetMLP("controllers/dcdc/controller", 2, 2**4, 0.01, 0.05, 0.999, 100, 1000)
cotonn.subSetMLP("controllers/vehicle/controller_large", 0.25, 2, 2**6, 0.01, 0.05, 0.9, 100, 1000)