

from time import sleep
from precise_runner import PreciseEngine, PreciseRunner

engine = PreciseEngine('precise-engine/precise-engine', 'geektime.pb')
runner = PreciseRunner(engine, on_activation=lambda: print('hello'))
runner.start()

# Sleep forever
while True:
    sleep(10)
