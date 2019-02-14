from pymuse.pipeline import Pipeline
from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.pipelinestages.outputstream.muse_csv_output_stream import MuseCSVOutputStream
from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream

museOSCInputStream = MuseOSCInputStream()
pipeline = Pipeline(museOSCInputStream.get_signal("eeg"), MuseCSVOutputStream())
pipeline.start()