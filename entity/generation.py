import numpy as np
import matplotlib.pyplot as plt

from entity.pathology import ConcretePathology
from entity.state import PathologyState, SubjectState
from entity.subject import Subject


class Generation:

    def __init__(self, dimension: int):
        self.dimension = dimension if dimension % 2 == 1 else dimension + 1  # create boards with a center point
        self.board = create_board(self.dimension)
        set_sick_subject(self.board)

    def draw(self):
        draw_board = np.array([subject.draw() for subject in self.board])
        draw_board = draw_board.reshape((self.dimension, self.dimension, 3))

        dx, dy = 100, 100

        plt.axis('off')
        plt.grid()
        plt.imshow(draw_board)
        plt.show()
        return draw_board

    def __enter__(self) -> 'Generation':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def create_board(dimension: int):
    board = np.array([Subject(age=int(np.random.uniform(10, 100, 1))) for _ in range(dimension * dimension)])
    return board


def set_sick_subject(board: np.ndarray, where: int = None):
    if where is None:
        where = board.size // 2

    # TODO: get pathology from config
    subject = board[where]
    subject.disease = ConcretePathology(subject, 0.15, 0.03, 7, 14)
    subject.disease.state = PathologyState.INFECTIOUS
    subject.state = SubjectState.SICK
