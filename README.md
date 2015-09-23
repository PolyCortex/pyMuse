# pyMuse

This repository contains tools for getting Muse signals using Python.

## Installation & dependences
You will need some tools to get started with Muse headset and pyMuse:
* Muse SDK --> https://sites.google.com/a/interaxon.ca/muse-developer-site/download
* Python 2.7
* matplotlib --> pip install matplotlib
* numpy --> pip install numpy
* liblo and pyliblo --> https://github.com/marionleborgne/cloudbrain#install-liblo

Don't hesitate to go on [Muse Developer website](https://sites.google.com/a/interaxon.ca/muse-developer-site/home) to get information.

## Getting started
1. Connect your Muse headset with your computer by bluetooth
2. Start MuseIO (in a terminal):
  ```
  muse-io --osc osc.udp://localhost:5001,osc.udp://localhost:5002
  ```
3. Start EEG display script (in a new terminal):
  ```
  python eeg_display.py
  ```
## Save Muse data and stream offline

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
