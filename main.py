from pymuse.pipeline import Pipeline, PipelineFork
from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.pipelinestages.outputstream.muse_csv_output_stream import MuseCSVOutputStream
from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream
from pymuse.signal import Signal, SignalData
from pymuse.configureshutdown import configure_shutdown
import time

museOSCInputStream = MuseOSCInputStream()
out = MuseCSVOutputStream()
pipeline = Pipeline(museOSCInputStream.get_signal("eeg"), out)
configure_shutdown(out, museOSCInputStream)

pipeline.start()
museOSCInputStream.start()

while True:
    time.sleep(100)