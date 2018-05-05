
# PlainController class which will hold the controller that can then be accessed in order to read training
# data for the neural network
class StaticController:
    def __init__(self):
        self.state_space_dim = None
        self.state_space_etas = None
        self.state_space_bounds = None

        self.input_space_dim = None
        self.input_space_etas = None
        self.input_space_bounds = None

        self.states = []
        self.inputs = []
        
    # Getters
    def getStateSpaceDim(self): return self.state_space_dim
    def getStateSpaceEtas(self): return self.state_space_etas
    def getStateSpaceBounds(self): return self.state_space_bounds
    def getInputSpaceDim(self): return self.input_space_dim
    def getInputSpaceEtas(self): return self.input_space_etas
    def getInputSpaceBounds(self): return self.input_space_bounds
    
    def getState(self, id): return self.states[id]
    def getInput(self, id): return self.inputs[id]
    
    # Get the input id and state id for a given state id
    def getPairFromStateId(self, id):
        for i in range(self.size()):
            if(self.states[i] == id):
                return [self.states[i], self.inputs[i]]
        return None
        
    # Get the input id corresponding to a given state id
    def getInputFromStateId(self, id):
        for i in range(self.size()):
            if(self.states[i]  == id):
                return self.inputs[i]
        print("ID does not correspond to a state in the winning domain.")
        return None
    
    # Get lowest state id contained in the controller
    def getLowestStateID(self):
        return min(int(s) for s in self.states)
    
    # Get highest state id contained in the controller
    def getHighestStateID(self):
        return max(int(s) for s in self.states)
    
    # Get lowest input id contained in the controller
    def getLowestInputID(self):
        return min(int(i) for i in self.inputs)
    
    # Get highest input id contained in the controller
    def getHighestInputID(self):
        return max(int(i) for i in self.inputs)
        
    # Setters
    def setStateSpaceDim(self, value): self.state_space_dim = value
    def setStateSpaceEtas(self, value): self.state_space_etas = value
    def setStateSpaceBounds(self, value): self.state_space_bounds = value
    def setInputSpaceDim(self, value): self.input_space_dim = value
    def setInputSpaceEtas(self, value): self.input_space_etas = value
    def setInputSpaceBounds(self, value): self.input_space_bounds = value

    def setStateInput(self, s, i):
        self.states.append(int(s))
        self.inputs.append(int(i))
        
    # Get the size of the controller
    def size(self):
        if(len(self.states) == len(self.inputs)):
            return len(self.states)
        print("Controller states length and inputs length seem to be deviating.");
        return 0
    
    
            

    





