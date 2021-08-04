from simulation.automato.board import Board
from simulation.automato.cell import Cell
from simulation.report.report import Report
from simulation.settings import ProgressSettings


class Progress:

    def __init__(self):
        self.board = Board()
        self.report = Report(self.board)

    def progress(self):
        with Report(self.board) as report:
            while self.board.is_finished():
                self.increase()
                report.record()
                self.board.draw()

                sick_cell: Cell
                for sick_cell in self.board.filter_sick():
                    neighbours = self.board.get_neighbours(sick_cell)
                    subject = sick_cell.data
                    subject.contact([cell.data for cell in neighbours])
                    subject.disease.progress()

            report.record()
            self.board.draw()

    @staticmethod
    def increase():
        ProgressSettings.CURRENT_N_DAY += 1

    def __enter__(self) -> 'Progress':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
