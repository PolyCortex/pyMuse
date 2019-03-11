from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.signal import Signal, SignalData
from pymuse.pipeline import Pipeline, PipelineFork
import unittest
from queue import Queue

N = 20
DATA_RATE = 200 # per sec
DATA = [(1, 2, 3, 4)] * N
EXPECTED_DATA_LAST_STAGE_1 = [SignalData(0, (4,5,6,7))] * N
EXPECTED_DATA_LAST_STAGE_2 = [SignalData(0, (3,4,5,6))] * N

# Mock stage of a pipeline that just increment every values by 1
class MockStage(PipelineStage):
    def __init__(self, isLastStage = False):
        self.isLastStage = isLastStage
        self.lastStageOutput = Queue(N)
        super().__init__()

    def run(self):
        for _ in range(N):
            data = self._queue_in.get()
            data.values = tuple([el + 1 for el in data.values])
            data.time = 0 # We ensure time=0 to simplify the test
            self._write_queues_out(data)
            if self.isLastStage:
                self.lastStageOutput.put(data)

class PipelineTest(unittest.TestCase):
    def check_queue_out_result(self, stage, expected_queue_out):
        self.assertEqual(list(stage._queues_out[0].queue), expected_queue_out)

    def test_read(self):
        signal = Signal(N, DATA_RATE)
        lastStage1 = MockStage(True)
        lastStage2 = MockStage(True)

        pipeline = Pipeline(signal, MockStage(), PipelineFork([MockStage(), lastStage1], [lastStage2]))
        pipeline.start()

        for data in DATA:
            signal.push(data)

        lastStage1.join()
        lastStage2.join()

        self.assertEqual(list(lastStage1.lastStageOutput.queue), EXPECTED_DATA_LAST_STAGE_1)
        self.assertEqual(list(lastStage2.lastStageOutput.queue), EXPECTED_DATA_LAST_STAGE_2)

if __name__ == '__main__':
    unittest.main()
