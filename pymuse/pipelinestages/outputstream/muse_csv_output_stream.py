from csv import writer, QUOTE_MINIMAL
from pymuse.pipelinestages.pipeline_stage import PipelineStage
import time
from pymuse.signal import SignalData
from queue import Queue

class MuseCSVOutputStream(PipelineStage):
    def __init__(self):
        super().__init__()

    def execute(self): # Pour l'instant, ce sera une étape bidon du pipeline qui ne fait que mettre les résultats sur la sortie standard.
        print('MuseCSVOutputStream Forked!')

        time_val = time.time()
        for i in range(256*4):
            data = self._queue_in.get()
        print("Exec time of MuseCSVOutputStream "+ str(time.time() - time_val))

        # with open('asd.csv', 'w', newline='') as csv_file:
        #     csv_writer = writer(csv_file, delimiter=',', quotechar='|', quoting=QUOTE_MINIMAL)
        #     while(True):
        #         while(self._queue_in.qsize = )
