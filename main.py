
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

lastStage.join()


import matplotlib.pyplot as plt
import queue
import sys, os
datas_TP9 = []
time = []

for _ in range(int(3* 256)):
    data = lastStage.output_queue.get()
    datas_TP9.append(data.values[2])
    time.append(data.time)

print("time:" + str(len(time)))
print("tp9:" + str(len(datas_TP9)))

plt.plot(time, datas_TP9)
plt.xlabel('time(s)')
plt.ylabel('amplitude uV')
plt.title('TP9')
plt.show()

