import unittest
from queue import Queue

from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.signal import Signal, SignalData
from pymuse.pipeline import Pipeline, PipelineFork

N = 20
DATA_RATE = 200 # per sec
DATA = [(1, 2, 3, 4)] * N
EXPECTED_DATA_LAST_STAGE_1 = [SignalData(0, (4,5,6,7))] * N
EXPECTED_DATA_LAST_STAGE_2 = [SignalData(0, (3,4,5,6))] * N

# Mock stage of a pipeline that just increment every values by 1
class MockStage(PipelineStage):
    def __init__(self):
        super().__init__()
        self.cnt = 0

    def _execute(self):
        if self.cnt < 20:
            data = self._queue_in.get()
            data.values = tuple([el + 1 for el in data.values])
            data.time = 0 # We ensure time=0 to simplify the test
            self._write_queues_out(data)
            self.cnt += 1
        else:
            self.shutdown()

class PipelineTest(unittest.TestCase):
    def test_read(self):
        signal = Signal(N, DATA_RATE)
        lastStage1 = MockStage()
        lastStage2 = MockStage()

        pipeline = Pipeline(signal, MockStage(), PipelineFork([MockStage(), lastStage1], [lastStage2]))
        pipeline.start()

        for data in DATA:
            signal.push(data)

        lastStage1.join()
        lastStage2.join()
        self.assertEqual(list(pipeline.get_output_queue(0).queue), EXPECTED_DATA_LAST_STAGE_1)
        self.assertEqual(list(pipeline.get_output_queue(1).queue), EXPECTED_DATA_LAST_STAGE_2)

if __name__ == '__main__':
    unittest.main()
