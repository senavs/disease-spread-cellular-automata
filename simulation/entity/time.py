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

    def __init__(self):
        dimension = BoardSettings.DIMENSION
        self.dimension = dimension if dimension % 2 == 1 else dimension + 1  # create boards with a center point
        self.board = create_board(self.dimension)
        self.figure, self.axis = create_figure(*SystemSettings.IMAGE_OUTPUT_RESOLUTION, SystemSettings.IMAGE_OUTPUT_DPI)

        set_sick_subject(self.board, BoardSettings.SICK_SUBJECT_LOCATION)

    def draw(self) -> np.ndarray:
        func = np.frompyfunc(lambda subject: subject.draw(), 1, 1)

        draw_board = np.array(func(self.board).tolist())
        draw_board = draw_board.astype(np.uint8)

        img = self.axis.imshow(draw_board)
        self.figure.savefig(f'{SystemSettings.IMAGE_OUTPUT_PATH}/{self.current_time:0>5}.png', bbox_inches='tight')
        return img

    def progress(self):
        while np.any(self.board):
            self.current_time += 1
            self.draw()

            for x, row in enumerate(self.board):
                for y, subject in enumerate(row):
                    neighbours = get_neighbours(self.board, x, y)
                    subject.contact(neighbours)
                    subject.disease.progress()
        self.draw()

    def __enter__(self) -> 'Time':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def create_board(dimension: int) -> np.ndarray:
    board = np.array([Subject() for _ in range(dimension * dimension)])
    board = board.reshape((dimension, dimension))
    return board


def create_figure(width: int, height: int, dpi: int) -> tuple[Figure, SubplotBase]:
    figure = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    axis = plt.subplot(1, 1, 1)
    axis.axis('off')
    return figure, axis


def set_sick_subject(board: np.ndarray, location: int = None):
    if location is None:
        location = board.shape[0] // 2

    subject = board[location, location]
    subject.disease = ConcretePathology(subject)
    subject.state = SubjectState.INFECTIOUS


def get_neighbours(board: np.ndarray, x: int, y: int) -> list:
    # Algorithm from https://stackoverflow.com/questions/51657128/how-to-access-the-adjacent-cells-of-each-elements-of-matrix-in-python
    neighbours = np.concatenate(list(row[y - (y > 0): y + 2]
                                     for row in board[x - (x > 0):x + 2]))
    neighbours = neighbours.tolist()
    neighbours.remove(board[x][y])
    return neighbours
