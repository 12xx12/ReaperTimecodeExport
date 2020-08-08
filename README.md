# ReaperTimecodeExport

A small python script to convert the csv files exported from Reaper to a xml format the MA understands - only tested on MA2

# ONLY USE TIMESTAMPS IN HH:MM:SS:Frame with 30 FPS

you can configure stuff by hand but i just throw it togehther that it worked

usage: ReaperTimecodExport.py [filename with .csv]

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
You may now remove any file *except* the "ReaperTimecodeExport.py"

Fou usage:
- Move the ReaperTimecodeExport.py file and you exported csv file to the same folder
- Do a shift right click into the folder you put yout exported files into
- Choose: "Open command windows here"
- copy this `python ReaperTimecodeExport.py ` and add your \*.csv file. You may autocomplete by pushing tab
<details><summary>Explanation</summary>
<p>
Sorry - nothing here ATM
</p>
</details>

<a name="Mac"></a>
### My System is Mac
