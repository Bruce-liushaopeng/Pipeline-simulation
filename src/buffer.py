class Buffer():
    def __init__(self, componentType, workstation):
        self.component = componentType
        self.workstation = workstation
        self.capacity = 2
        self.current = 0

    def getComponentType(self):
        return self.component
    
    def isFull(self):
        if (self.current < self.capacity):
            return True
        return False
    
    def put(self):
        self.current += 1
        
    def nonEmpty(self):
        return self.current>0
