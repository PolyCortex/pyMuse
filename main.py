from pymuse.pipeline import Pipeline
from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.pipelinestages.outputstream.muse_csv_output_stream import MuseCSVOutputStream
from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream
from pymuse.pipelinestages.astage import AStage
from threading import active_count

museOSCInputStream = MuseOSCInputStream()
pipeline = Pipeline(museOSCInputStream.get_signal("eeg"), AStage(), MuseCSVOutputStream())
museOSCInputStream.start()
pipeline.start()
while(True):
    pass