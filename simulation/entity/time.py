import numpy as np
import matplotlib.pyplot as plt

from simulation.settings import SystemSettings, BoardSettings
from simulation.entity.pathology import ConcretePathology
from simulation.entity.state import PathologyState, SubjectState
from simulation.entity.subject import Subject


class Time:
    board: np.ndarray
    current_time: int = 0

    def __init__(self):
        dimension = BoardSettings.DIMENSION
        self.dimension = dimension if dimension % 2 == 1 else dimension + 1  # create boards with a center point

        self.create_board()
        self.set_sick_subject()

    def create_board(self):
        self.board = np.array([Subject() for _ in range(self.dimension * self.dimension)])

    def set_sick_subject(self):
        location = BoardSettings.SICK_SUBJECT_LOCATION
        if location is None:
            location = self.board.size // 2

        subject = self.board[location]
        subject.disease = ConcretePathology(subject)
        subject.disease.state = PathologyState.INFECTIOUS
        subject.state = SubjectState.SICK

    def draw(self) -> np.ndarray:
        draw_board = np.array([subject.draw() for subject in self.board], dtype=int)
        draw_board = draw_board.reshape((self.dimension, self.dimension, 3))
        draw_board = draw_board.astype(np.uint8)

        plt.imsave(f'{SystemSettings.IMAGE_OUTPUT_PATH}/{self.current_time:0<5}.png', draw_board)
        return draw_board

    def filter_infectious(self) -> list:
        return list(filter(lambda subject: subject.disease.state == PathologyState.INFECTIOUS, self.board))

    def process(self):
        while self.filter_infectious():
            self.current_time += 1

            # TODO: call subject and pathology process method

            self.draw()

    def __enter__(self) -> 'Time':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
