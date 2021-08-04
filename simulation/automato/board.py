import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import SubplotBase
from matplotlib.figure import Figure

from simulation.automato.cell import Cell
from simulation.entity.pathology import ConcretePathology
from simulation.entity.state import SubjectState
from simulation.settings import BoardSettings, SystemSettings, ProgressSettings


class Board:

    def __init__(self):
        dimension = BoardSettings.DIMENSION
        self.dimension = dimension if dimension % 2 == 1 else dimension + 1  # create boards with a center point
        self.board = self.initialize_board()
        self.figure, self.axis = self.initialize_figure()

    def initialize_board(self) -> np.ndarray:
        """Create board with cell that contains subjects (one is sick)"""

        board = np.empty((self.dimension, self.dimension), dtype=object)

        # create all cells (health subjects)
        for x in range(self.dimension):
            for y in range(self.dimension):
                board[x, y] = Cell(x, y)

        # create one sick subject in the middle of the board
        center_index = board.shape[0] // 2
        cell: Cell = board[center_index, center_index]
        cell.data.disease = ConcretePathology(cell.data)
        cell.data.state = SubjectState.INFECTIOUS

        return board

    @staticmethod
    def initialize_figure() -> tuple[Figure, SubplotBase]:
        """Create output figure and axis"""

        width, height = SystemSettings.IMAGE_OUTPUT_RESOLUTION
        dpi = SystemSettings.IMAGE_OUTPUT_DPI

        figure = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
        axis = plt.subplot(1, 1, 1)
        axis.axis('off')

        return figure, axis

    def get_neighbours(self, cell: Cell) -> list[Cell]:
        # Algorithm from https://stackoverflow.com/questions/51657128/how-to-access-the-adjacent-cells-of-each-elements-of-matrix-in-python
        x, y = cell.x, cell.y

        neighbours: np.ndarray = np.concatenate(list(row[y - (y > 0): y + 2]
                                                     for row in self.board[x - (x > 0):x + 2]))
        neighbours: list = neighbours.tolist()
        neighbours.remove(self.board[x][y])
        return neighbours

    def is_finished(self) -> bool:
        return np.any(self.board)

    def filter_sick(self):
        return self.board[np.bool_(self.board) == True]  # noqa: it has to be '==' and not 'is'

    def filter_health(self):
        return self.board[np.bool_(self.board) == False]  # noqa: it has to be '==' and not 'is'

    def draw(self):
        """Draw board as figure"""

        func = np.frompyfunc(lambda cell: cell.data.draw(), 1, 1)

        draw_board = np.array(func(self.board).tolist())
        draw_board = draw_board.astype(np.uint8)

        img = self.axis.imshow(draw_board)
        self.figure.savefig(
            f'{SystemSettings.IMAGE_OUTPUT_PATH}/{ProgressSettings.CURRENT_TIME.get():0>5}.png',
            bbox_inches='tight'
        )

        return img
