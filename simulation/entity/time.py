import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure, SubplotBase

from simulation.settings import SystemSettings, BoardSettings
from simulation.entity.pathology import ConcretePathology
from simulation.entity.state import SubjectState
from simulation.entity.subject import Subject


class Time:
    board: np.ndarray
    current_time: int = 0
    figure: Figure
    ax: SubplotBase

    def __init__(self):
        dimension = BoardSettings.DIMENSION
        self.dimension = dimension if dimension % 2 == 1 else dimension + 1  # create boards with a center point

        self.create_board()
        self.create_figure()
        self.set_sick_subject()

    def create_board(self):
        self.board = np.array([Subject() for _ in range(self.dimension * self.dimension)])
        self.board = self.board.reshape((self.dimension, self.dimension))

    def create_figure(self):
        self.figure = plt.figure(
            figsize=(
                SystemSettings.IMAGE_OUTPUT_RESOLUTION[0] / SystemSettings.IMAGE_OUTPUT_DPI,
                SystemSettings.IMAGE_OUTPUT_RESOLUTION[1] / SystemSettings.IMAGE_OUTPUT_DPI
            ),
            dpi=SystemSettings.IMAGE_OUTPUT_DPI
        )
        self.ax = plt.subplot(1, 1, 1)
        self.ax.axis('off')  # noqa

    def set_sick_subject(self):
        location = BoardSettings.SICK_SUBJECT_LOCATION
        if location is None:
            location = self.board.shape[0] // 2

        subject = self.board[location, location]
        subject.disease = ConcretePathology(subject)
        subject.state = SubjectState.INFECTIOUS

    def draw(self) -> np.ndarray:
        func = np.frompyfunc(lambda subject: subject.draw(), 1, 1)

        draw_board = np.array(func(self.board).tolist())
        draw_board = draw_board.astype(np.uint8)

        img = self.ax.imshow(draw_board)  # noqa
        self.figure.savefig(f'{SystemSettings.IMAGE_OUTPUT_PATH}/{self.current_time:0>5}.png', bbox_inches='tight')
        return img

    def get_neighbours(self, x: int, y: int) -> list:
        # Algorithm from https://stackoverflow.com/questions/51657128/how-to-access-the-adjacent-cells-of-each-elements-of-matrix-in-python
        neighbours = np.concatenate(list(row[y - (y > 0): y + 2]
                                         for row in self.board[x - (x > 0):x + 2]))
        neighbours = neighbours.tolist()
        neighbours.remove(self.board[x][y])  # noqa
        return neighbours  # noqa

    def progress(self):
        for _ in range(100):
            self.current_time += 1
            self.draw()

            for x, row in enumerate(self.board):
                for y, subject in enumerate(row):
                    neighbours = self.get_neighbours(x, y)
                    subject.contact(neighbours)
                    subject.disease.progress()

    def __enter__(self) -> 'Time':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
