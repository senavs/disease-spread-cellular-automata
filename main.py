import matplotlib

from simulation.automato.progress import Progress

matplotlib.use('Agg')

with Progress() as process:
    process.progress()
