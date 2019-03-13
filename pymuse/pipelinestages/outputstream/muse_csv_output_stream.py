from csv import writer
from datetime import date
import time
from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.signal import SignalData

DEFAULT_FILE_NAME = "MuseData%s.csv"%date.today()
DEFAULT_COLUMN_PREFIX = "electrode"
TIME_COLUMN_NAME = "time"

class MuseCSVOutputStream(PipelineStage):
    def __init__(self, file_name=DEFAULT_FILE_NAME, column_prefix=DEFAULT_COLUMN_PREFIX):
        super().__init__()
        self._file_name = file_name
        self._column_prefix = column_prefix

    def execute(self): # Pour l'instant, ce sera une étape bidon du pipeline qui ne fait que mettre les résultats sur la sortie standard.
        print('MuseCSVOutputStream Forked!')
        timeinit = time.time()
        try:
            with open(self._file_name, 'w', newline='') as csv_file:
                csv_writer = writer(csv_file)
                print("before")
                data = self._queue_in.get()
                print("data, values :", data.values)
                self._setHeaderFile(csv_writer, len(data.values))
                for i in range(256*3 - 1):
                    csv_writer.writerow([data.time] + [electrode for electrode in data.values])
                    data = self._queue_in.get()
        except PermissionError as err:
            print("MuseCSVOutputStream: Cannot open file: %s"%(err))
        
        print("finished, exec time: ", time.time() - timeinit)


    def _setHeaderFile(self, csv_writer, nb_samples):
        value_column_names = ["%s %i"%(self._column_prefix, x) for x in range(nb_samples)]
        column_names = [TIME_COLUMN_NAME] + value_column_names
        csv_writer.writerow(column_names)
