import random

class UserAgents:
    def __init__(self) -> None:
        self.pathToFile = "./src/input/useragents.txt"
        
    def getAmount(self) -> None:
        with open(self.pathToFile, "r+") as reader:
           return len(reader.read().splitlines())
           
    def gen(self) -> str:
        with open(self.pathToFile, "r+") as getter:
            return random.choice(getter.read().splitlines())
        
