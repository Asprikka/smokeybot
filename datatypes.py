class Vape:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

    def dict(self):
        return self.__dict__
