# ReaperTimecodeExport

A small python script to convert the csv files exported from Reaper to a xml format the MA understands - only tested on MA2

# ONLY USE TIMESTAMPS IN HH:MM:SS:Frame with 30 FPS

you can configure stuff by hand but i just throw it togehther that it worked

Table of Contents
======

- [Usage](#usage)
- [Installation](#installation)
  - [I know python](#pythonexpert)
  - [I know how to use a terminal](#terminal)
  - [What is a terminal?](#beginner)
    - [My System is Windows](#Windows)
    - [My System is Mac](#Mac)

# Usage
python ReaperTimecodeExport [your exported.csv file]

# Installation

<a name="pythonexpert"></a>
## I know python
- You just need lxml

<a name="terminal"></a>
## I know how to use a terminal
- [Download](https://www.python.org/downloads/) Python and install it
- check if pip is installed `pip --version` 
- run `pip install lxml`

<a name="beginner"></a>
## What is a terminal?
For any system:
- [Download](https://www.python.org/downloads/) Python and install it
- [Download](https://github.com/12xx12/ReaperTimecodeExport/archive/master.zip) the repo as a zip and unzip it

<a name="Windows"></a>
### My System is Windows
For setup:
- Double click the "easyinstall.cmd"
If any error messages appear feel free to message me or open an issue I'll try to come back to you
You may now remove any file *except* the "ReaperTimecodeExport.py" and "run.bat"

Fou usage:
- Move the ReaperTimecodeExport.py file and you exported csv file to the same folder
- Run the `run.bat` file by double clicking it. This processes all .csv files in the folder

<a name="Mac"></a>
### My System is Mac
coming if I get a hold of a mac sometime

Here is a [link](https://lifehacker.com/launch-an-os-x-terminal-window-from-a-specific-folder-1466745514) to a page that explains how to open the terminal in a folder directly.
Open the directory you unzipped the downloaded stuff that way

then proceed as described [here](#terminal)
