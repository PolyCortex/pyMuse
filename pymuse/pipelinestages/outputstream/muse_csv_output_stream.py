from csv import writer
from datetime import datetime

from pymuse.inputstream.muse_constants import MUSE_EEG_ACQUISITION_FREQUENCY
from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.signal import SignalData

DEFAULT_FILE_NAME = "MuseData%s.csv"%datetime.now()
DEFAULT_COLUMN_PREFIX = "electrode"
TIME_COLUMN_NAME = "time"

class MuseCSVOutputStream(PipelineStage):
    """
    Pipeline stage that creates and writes to a csv file  all incoming data from the precedent stage.

    It should be used as the last stage in a pipeline.  Otherwise, you can fork the pipeline into a
    MuseCSVOutputStream to extract data from an intermediate stage.
    """

    def __init__(self, file_name=DEFAULT_FILE_NAME, column_prefix=DEFAULT_COLUMN_PREFIX, buffer_max=MUSE_EEG_ACQUISITION_FREQUENCY):
        super().__init__()
        self._FILE_NAME = file_name
        self._COLUMN_PREFIX = column_prefix
        self._BUFFER_MAX = buffer_max
        self._buffer = []
    
    def _execute(self):
        if len(self._buffer) >= self._BUFFER_MAX:
            self._flush_buffer()

        self._buffer.append(self._queue_in.get())

    def _initialization_hook(self):
        try:
            self._csv_file = open(self._FILE_NAME, 'w', newline='')
        except PermissionError as err:
            print("MuseCSVOutputStream: Cannot open file: %s"%(err))
            raise err

        self._csv_writer = writer(self._csv_file)
        self._buffer.append(self._queue_in.get())
        self._setHeaderFile(len(self._buffer[0].values))
        print("MuseCSVOutputStream: Started writing to " + self._FILE_NAME)
    
    def _flush_buffer(self):
        rows = [[data.time] + [value for value in data.values] for data in self._buffer]
        self._csv_writer.writerows(rows)
        self._buffer = []
    
    def _shutdown_hook(self):
        if len(self._buffer) > 0:
            self._flush_buffer()
        self._csv_file.close()

    def _setHeaderFile(self, nb_samples):
        value_column_names = ["%s %i"%(self._COLUMN_PREFIX, x) for x in range(nb_samples)]
        column_names = [TIME_COLUMN_NAME] + value_column_names
        self._csv_writer.writerow(column_names)
