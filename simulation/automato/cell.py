from simulation.entity.subject import Subject


class Cell:

    def __init__(self, x: int, y: int):
        self.x, self.y = int(x), int(y)
        self.data: Subject = Subject()

    def __bool__(self):
        return bool(self.data)

    def __str__(self):
        return f'Cell({self.data})'
