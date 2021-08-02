import matplotlib

from simulation.entity.time import Time

matplotlib.use('Agg')

with Time() as time:
    time.progress()
