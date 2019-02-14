from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.signal import Signal
from queue import Queue

from pymuse.constants import PIPELINE_QUEUE_SIZE

class PipelineFork():
    def __init__(self, *args):
        self.forked_branches: list[list] = args

class Pipeline():

    def __init__(self, input_signal: Signal, stages: list[PipelineStage]):
        self._input_signal = input_signal
        self._stages: list[PipelineStage] = stages
        self._link_stages(self._stages)

    def _link_pipeline_fork (self, stages: list, index: int):
            for i, fork in enumerate(stages[index].forked_branches):
                stages[index - 1].set_queue_out(fork[0].queue_in, i)
                self._link_stages(fork)

    def _link_stages(self, stages: list):
        for i in range(1, len(stages)):
            if type(stages[i]) == PipelineFork:
                self._link_pipeline_fork(stages, i)
            else:
                stages[i - 1].set_queue_out(stages[i].queue_in)
        if type(stages[-1]) == PipelineStage:
            stages[-1].set_queue_out(Queue(PIPELINE_QUEUE_SIZE))


    def start(self):
        for stage in self._stages:
            stage.start()
