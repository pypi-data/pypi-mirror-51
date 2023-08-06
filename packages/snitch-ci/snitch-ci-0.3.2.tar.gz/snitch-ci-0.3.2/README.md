Snitch, an input event recorder and player
==========================================

Snitch is a Python3 program using the Qt5 framework for GUI and the pyautogui and pynput modules for automation.


## Prerequisites

A working installation of Python3 with pip package installer.

In order to record and control the mouse on Linux systems, the packages `python3-tk` and `python3-dev` are required.


## Installation

For now Snitch is available on the PyPI test repository. Install by running the command:

    pip install snitch-ci

You can then run the program with:

    snitch


## Building from sources

First you need to install the dependencies with:

    pip install -r requirements.txt

Then generate the code for Qt interface and assets using:

    bash build.sh

You can now run the program as a python package:

    python -m snitch


### Note about scrot

The pyautogui on Linux depends on the scrot utility for screen captures. This utility only works with X11. The most recent versions of gnome-shell are based on Wayland instead of X11. For those versions, the scrot utility produces only black pictures.

One workaround is installing the Gnome native capture utility gnome-screenshot and creating a wrapper script acting as scrot. The most basic working way is putting the following script in the `/usr/bin/scrot` file (and granting it execution permissions):

    #! /bin/bash
    gnome-screenshot -f $@
