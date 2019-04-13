![](https://lh3.googleusercontent.com/aLAHpZfer0HIiBXKj7tx4TAW9CnxOLVt3wht1yxNsFVPlMeJfd8yK-TSoTBJ_eEjuwWs8W3fqcOL "Logo")

# pyMuse

This repository contains tools for gathering and processing Muse signals using Python. With pyMuse you can configure and run an EEG pipeline faster than light.

## Features

[](https://emojipedia.org/construction-sign/) 🚧 Pymuse is still a work in progress. But we aim to have a flexible and extensible architecture so you can use it to your own sauce.

For now, pyMuse already contains a lot of features:

- EEG acquisition methods like MuseOSCInputStream to get data from MuseDirect.
- Pipeline creation is extensible and modulable to your own needs. If you need a need a custom stage for your pipeline, just inherit from PipelineStage. 
- Pipeline can be forked to process multiple outputs from a same source signal.
- Each PipelineStage has its own thread and are automatically linked together by thread-safe queues. They provides hooks for their initialization and their shutdown.

Of course, many more will come in the following months. Stay tuned.

## Example

   ``` python
   from pymuse.pipeline import Pipeline
from pymuse.configureshutdown import configure_shutdown
from pymuse.inputstream.muse_osc_input_stream import MuseOSCInputStream
from pymuse.pipelinestages.outputstream.muse_csv_output_stream import MuseCSVOutputStream

muse_osc_input_stream = MuseOSCInputStream(['eeg', 'beta_relative']) # Signal acquisition module
pipeline = Pipeline( # Pipeline modules are automagically linked together
muse_osc_input_stream.get_signal('eeg'),
MuseCSVOutputStream("recorded_eeg.csv")
)
# Ensure resources are freed when application is shutted down
configure_shutdown(muse_osc_input_stream, pipeline)
pipeline.start()
muse_osc_input_stream.start()
   ```

## Installation & dependencies

You will need a few tools to get started with the Muse headset and pyMuse:

*  [MuseDirect](https://www.microsoft.com/en-us/p/muse-direct/9p0mbp6nv07x?activetab=pivot:overviewtab) (Windows)

*  [Python 3.7](https://www.python.org/downloads/release/python-373/)

Do not hesitate to visit the [Muse Developer website](http://developer.choosemuse.com/) for additional information and to access the docs.

### Installation of this package

Ensure you have downloaded the correct Python distribution and the pyMuse package (e.g., using `git clone`).


Open a terminal, go into the package and type:

`pip install -r requirements.txt`.

The installer should install all requirements, including:
* numpy
* scipy
* matplotlib
*  [python-osc > 1.7.0](https://github.com/attwad/python-osc/)
