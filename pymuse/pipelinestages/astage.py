from pymuse.pipelinestages.pipeline_stage import PipelineStage
from queue import Queue
import time

class AStage(PipelineStage):
    def __init__(self):
        self.output_queue = Queue()
        super().__init__()

    def execute(self): # Pour l'instant, ce sera une étape bidon du pipeline qui ne fait que mettre les résultats sur la sortie standard.
        #print('Astage Forked!')

        time_val = time.time()
        #print("I'm alive")
        """
        for _ in range(256*3):
            data = self._queue_in.get()
            self.output_queue.put(data)
        """
        #print("Exec time of MuseCSVOutputStream "+ str(time.time() - time_val))
