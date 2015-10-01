# pyMuse

This repository contains tools for getting Muse signals using Python.

## Installation & dependences
You will need some tools to get started with Muse headset and pyMuse:
* Muse SDK --> https://sites.google.com/a/interaxon.ca/muse-developer-site/download
* Python 2.7
* matplotlib --> pip install matplotlib
* numpy --> pip install numpy
* liblo and pyliblo

Don't hesitate to go on [Muse Developer website](https://sites.google.com/a/interaxon.ca/muse-developer-site/home) to get information.

### liblo and pyliblo install

For MacOS users that use homebrew, see https://github.com/marionleborgne/cloudbrain#install-liblo

Otherwise, here are the following steps to follow (first two are for liblo, the last two are for pyliblo):

1. Download liblo on the sourceforge [webpage](http://liblo.sourceforge.net)
2. Extract the archive file, open a terminal in that folder and type `./configure`. Then `make` and finally `make install`. Note that everything is explained in detail in the `INSTALL` file.
3. Dowload pyliblo on the package [webpage](http://das.nasophon.de/pyliblo/)
4. Extract the archive file, open a terminal in that folder and type `python setup.py build` then `python setup.py install`

## Getting started
### Display your Muse data with eeg displayer
1. Connect your Muse headset with your computer by bluetooth
2. Start MuseIO (in a terminal):
  ```
  muse-io --osc osc.udp://localhost:5001,osc.udp://localhost:5002
  ```
3. Start EEG display script (in a new terminal):
  ```
  python eeg_display.py
  ```

### Save Muse data and stream offline

See the [developer webpage](http://www.choosemuse.com/developer-kit/) for details.

1. Connect your Muse headset with your computer by bluetooth
2. Start MuseIO (in a terminal):
  ```
  muse-io --osc osc.udp://localhost:5001,osc.udp://localhost:5002
  ```
3. Start MuseLab (a GUI for real-time visualization of brainwaves). It allows you to record the whole data for offline analysis (via the *Recording* tab). You might also look at the *Markers* tab to add triggers to your experiment.
4. Stop MuseIO and MuseLab now that data have been recorded.
5. Run MusePlayer to stream the datat to a server.
  ```
  muse-player -f you_recorded_data.muse -s osc.udp://localhost:5001
  ```
Note that you can add your recorded data to the following [repository](https://github.com/PolyCortex/MuseData) to share it with the other members.
6. Now you can display your recorded session using eeg displayer, or processing with your favorite software.
