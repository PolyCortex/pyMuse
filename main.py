
from pymuse.pipeline import Pipeline, PipelineFork
from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.pipelinestages.outputstream.muse_csv_output_stream import MuseCSVOutputStream
from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream
from pymuse.pipelinestages.astage import AStage
from pymuse.signal import Signal, SignalData
import time

museOSCInputStream = MuseOSCInputStream()
pipeline = Pipeline(museOSCInputStream.get_signal("eeg"), AStage("1"), PipelineFork([AStage("2"), MuseCSVOutputStream()], [AStage("3")] ))
pipeline.start()
museOSCInputStream.start()
