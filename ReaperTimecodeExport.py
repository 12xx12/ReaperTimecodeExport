"""

    A simple (and shitty) script to read a Reaper created .csv file and convert it to a macro and a timecode sheet
    Author: 12xx12 - 12xx12100@gmail.com
    dependency lxml: pip install lxml

"""

import csv
import os
import sys
from datetime import datetime

from lxml import etree as xml


def minutesToFrames(time: str):
    """
    converts the time given in HH:MM::SS:Frames to a time in Frames
    :param time: string to convert
    :return: the time og the string in frames
    """
    times = time.split(":")
    res = 0
    for k, timeUnit in enumerate(times):
        if k == 0:
            res += int(timeUnit) * 30 * 60 * 60
        elif k == 1:
            res += int(timeUnit) * 30 * 60
        elif k == 2:
            res += int(timeUnit) * 30
        elif k == 3:
            res += int(timeUnit)
    return str(res)


if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: ReaperTimecodeExport [your exported file.csv]")
    exit(-1)

sequenceNumber = 1  # the number of the sequence to export to
pageNumber = 1  # the number of the page of the executor to save to
execNumber = 1  # the number of the executor to save to
fadeTime = 0  # default fade time - exported to every cue

timeCodeSlot = 2  # the timecode slot to read from
autoStart = True  # enable autostart for the exec

if not os.path.isdir("./importexport"):
    try:
        os.mkdir("importexport")
    except OSError as err:
        print(format(err))

if not os.path.isdir("./macros"):
    try:
        os.mkdir("macros")
    except OSError as err:
        print(format(err))

# ---------------------------------------------------------------------------------------------------------------------
# reads the input file and writes everything in one array

array = []
try:
    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            helperArry = []
            for j, element in enumerate(row):
                helperArry.append(row[element])
            array.append(helperArry)
except IOError as err:
    print(format(err))
    exit(-1)

# ---------------------------------------------------------------------------------------------------------------------
# creating the timecode file

MA = xml.XML("<MA xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
             "xmlns=\"http://schemas.malighting.de/grandma2/xml/MA\" "
             "xsi:schemaLocation=\"http://schemas.malighting.de/grandma2/xml/MA "
             "http://schemas.malighting.de/grandma2/xml/3.3.4/MA.xsd\" major_vers=\"3\" minor_vers=\"3\" "
             "stream_vers=\"4\"></MA>")

Info = xml.SubElement(MA, "Info")
Info.set("datetime", str(datetime.now())[:-7].replace(" ", "T"))
Info.set("showfile", "Insert funny name here")

TimeCode = xml.SubElement(MA, "Timecode")
TimeCode.set("index", "0")
TimeCode.set("name", sys.argv[1][:-4])
TimeCode.set("length", minutesToFrames(array[len(array) - 1][2]))
TimeCode.set("slot", "TC Slot " + str(timeCodeSlot))
TimeCode.set("frame_format", "30 FPS")
if autoStart:
    TimeCode.set("m_autostart", "true")
TimeCode.set("no_status_call", "true")

Track = xml.SubElement(TimeCode, "Track")
Track.set("index", "0")
Track.set("active", "true")
Track.set("expanded", "true")

Object = xml.SubElement(Track, "Object")
Object.set("name", sys.argv[1][:-4] + " " + str(pageNumber) + "." + str(execNumber))

# this seems to be the type no of page
Type = xml.SubElement(Object, "No")
Type.text = "30"

sequence = xml.SubElement(Object, "No")
sequence.text = str(sequenceNumber)

Page = xml.SubElement(Object, "No")
Page.text = str(pageNumber)

Exec = xml.SubElement(Object, "No")
Exec.text = str(execNumber)

SubTrack = xml.SubElement(Track, "SubTrack")
SubTrack.set("index", "0")

for i, e in enumerate(array):
    Event = xml.SubElement(SubTrack, "Event")
    Event.set("index", str(i))
    Event.set("time", minutesToFrames(e[2]))
    Event.set("command", "Goto")
    Event.set("pressed", "true")
    Event.set("step", str(i + 1))
    Cue = xml.SubElement(Event, "Cue")
    if e[1]:
        Cue.set("name", e[1])
    else:
        Cue.set("name", str(i + 1))
    theOneEverywhere = xml.SubElement(Cue, "No")
    theOneEverywhere.text = "1"
    Sequence = xml.SubElement(Cue, "No")
    Sequence.text = str(sequenceNumber)
    CueNumber = xml.SubElement(Cue, "No")
    CueNumber.text = str(i + 1)

tree = xml.ElementTree(MA)
try:
    tree.write("importexport/timecode" + sys.argv[1][:-4] + ".xml", encoding="UTF-8", xml_declaration=True, pretty_print=True)
except IOError as err:
    print(format(err))

with open("importexport/timecode" + sys.argv[1][:-4] + ".xml", 'r+') as fd:
    contents = fd.readlines()
    copy = contents[0]
    contents[0] = copy[:-1] + " <?xml-stylesheet type=\"text/xsl\" href=\"styles/timecode@sheet.xsl\"?>\n"
    fd.seek(0)
    fd.writelines(contents)

if len(sys.argv) == 3 and sys.argv[2] != "--nolog":
    print("Exported the timecode file successful!")

# -----------------------------------------------------------------------------------------------
# creating the macro file

MA2 = xml.XML("<MA xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
              "xmlns=\"http://schemas.malighting.de/grandma2/xml/MA\" "
              "xsi:schemaLocation=\"http://schemas.malighting.de/grandma2/xml/MA "
              "http://schemas.malighting.de/grandma2/xml/3.3.4/MA.xsd\" "
              "major_vers=\"3\" minor_vers=\"3\" stream_vers=\"4\"></MA>")
Macro = xml.SubElement(MA2, "Macro")
Macro.set("index", "1")
Macro.set("name", "import" + sys.argv[1][:-4])

j = 1
i = 0
for i, e in enumerate(array):
    Macroline = xml.SubElement(Macro, "Macroline")
    Macroline.set("index", str(j))
    text = xml.SubElement(Macroline, "text")
    if array[i][1]:
        text.text = "Store Sequence " + str(sequenceNumber) + " Cue " + str(i + 1) + " \"" + array[i][1] + "\" /o /nc"
    else:
        text.text = "Store Sequence " + str(sequenceNumber) + " Cue " + str(i + 1) + " \"" + str(i + 1) + "\" /o /nc"
    j += 1
    Macroline = xml.SubElement(Macro, "Macroline")
    Macroline.set("index", str(j))
    text = xml.SubElement(Macroline, "text")
    text.text = "Assign Sequence " + str(sequenceNumber) + " Cue " + str(i + 1) + " /fade=" + str(fadeTime) + ".00 "
    j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "Label Sequence " + str(sequenceNumber) + " \"" + sys.argv[1][:-4] + "\""
j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "Assign Sequence " + str(sequenceNumber) + " At Exec 1." + str(pageNumber) + "." + str(execNumber)
j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "SelectDrive 4"
j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "Import \"timecode" + sys.argv[1][:-4] + "\" At Timecode 1 /o"
j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "Label Timecode 1 \"" + sys.argv[1][:-4] + "\""
j += 1

tree = xml.ElementTree(MA2)
try:
    tree.write("Macros\macro" + sys.argv[1][:-4] + ".xml", encoding="UTF-8", xml_declaration=True, pretty_print=True)
except IOError as err:
    print(format(err))
if len(sys.argv) == 3 and sys.argv[2] != "--nolog":
    print("Exported the macro file successful!")

    print("Now copy the two folders onto the gma2 folder on your USB-drive and import the macro and run it\n"
          "If you are running onPC and you are loading from the internal storage you need to change the SelectDrive"
          " to 1 im the macro")
