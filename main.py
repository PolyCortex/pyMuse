
from pymuse.pipeline import Pipeline, PipelineFork
from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.pipelinestages.astage import AStage
from pymuse.pipelinestages.outputstream.muse_csv_output_stream import MuseCSVOutputStream
from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream
from pymuse.signal import Signal, SignalData
import time

museOSCInputStream = MuseOSCInputStream()
lastStage = AStage()

pipeline = Pipeline(museOSCInputStream.get_signal("eeg"), lastStage)
pipeline.start()

museOSCInputStream.start()

pipeline.join()


import matplotlib.pyplot as plt
import queue
datas_TP9 = []
time = []

try:
    while True:
        datas_TP9.append(lastStage.output_queue.get_nowait().values[0])
        time.append(lastStage.output_queue.get_nowait().time)
except queue.Empty:
    pass

plt.plot(time, datas_TP9,'ks-',label='Actual')
plt.xlabel('time(s)')
plt.ylabel('amplitude uV')
plt.title('TP9')
plt.show()

