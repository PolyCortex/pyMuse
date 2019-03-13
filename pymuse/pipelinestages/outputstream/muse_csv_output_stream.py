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

    def _initialization_hook(self):
        try:
            self._csv_file = open(self._file_name, 'w', newline='');
        except PermissionError as err:
            print("MuseCSVOutputStream: Cannot open file: %s"%(err))
            raise err

        self._csv_writer = writer(self._csv_file)
        self._data = self._queue_in.get()
        print("data, values :", self._data.values)
        self._setHeaderFile(len(self._data.values))

    def execute(self):
        self._csv_writer.writerow([self._data.time] + [value for value in self._data.values])
        self._data = self._queue_in.get()
    
    def _shutdown_hook(self):
        self._csv_file.close()

    def _setHeaderFile(self, nb_samples):
        value_column_names = ["%s %i"%(self._column_prefix, x) for x in range(nb_samples)]
        column_names = [TIME_COLUMN_NAME] + value_column_names
        self._csv_writer.writerow(column_names)
