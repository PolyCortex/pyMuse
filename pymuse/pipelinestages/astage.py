from csv import writer, QUOTE_MINIMAL
from pymuse.pipelinestages.pipeline_stage import PipelineStage
import time
from pymuse.signal import SignalData
from queue import Queue

class AStage(PipelineStage):
    def __init__(self):
        super().__init__()

    def run(self): # Pour l'instant, ce sera une étape bidon du pipeline qui ne fait que relayer vers la prochaine étape
        print('AStage Forked!')
        time_val = time.time()
        for i in range(256*4):
            data = self._queue_in.get()
            self._queues_out[0].put(data)
        print("AStage exec time: " + str(time.time() - time_val))
