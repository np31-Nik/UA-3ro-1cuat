class Casilla():
    def __init__(self, f, c):
        self.fila=f
        self.col=c

    def __eq__(self,other):
        if isinstance(other,Casilla):
            return self.fila == other.fila and self.col == other.col
        return False
        
    def getFila (self):
        return self.fila
    
    def getCol (self):
        return self.col
        
