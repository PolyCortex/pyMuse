from csv import writer, QUOTE_MINIMAL
from pymuse.pipelinestages.pipeline_stage import PipelineStage

class MuseCSVOutputStream(PipelineStage):
    def __init__(self):
        super().__init__()

    def run(self): # Pour l'instant, ce sera une étape bidon du pipeline qui ne fait que mettre les résultats sur la sortie standard.
        while(True):
            data = self._queue_in.get()
            print(data)
            self._queue_out.put(data)
            
        # with open('asd.csv', 'w', newline='') as csv_file:
        #     csv_writer = writer(csv_file, delimiter=',', quotechar='|', quoting=QUOTE_MINIMAL)
        #     while(True):
        #         while(self._queue_in.qsize = )