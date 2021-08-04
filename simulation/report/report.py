import numpy as np
import pandas as pd

from simulation.automato.board import Board
from simulation.settings import ProgressSettings, SystemSettings


class Report:

    def __init__(self, board: Board):
        self.flatten_board, self.data = self.initialize_report(board)

    @staticmethod
    def initialize_report(board: Board) -> tuple[np.ndarray, pd.DataFrame]:
        flatten_board = np.reshape(board.board, (board.dimension * board.dimension))

        report = pd.DataFrame(index=range(flatten_board.size), columns=['id', 'age'])
        report['id'] = [cell.data.id for cell in flatten_board]
        report['age'] = [cell.data.age for cell in flatten_board]

        return flatten_board, report

    def record(self):
        self.data[ProgressSettings.CURRENT_N_DAY] = [cell.data.state.value for cell in self.flatten_board]

    def __enter__(self) -> 'Report':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.data.to_csv(f'{SystemSettings.REPORT_OUTPUT_PATH}/raw.csv', index=False, sep=';')
