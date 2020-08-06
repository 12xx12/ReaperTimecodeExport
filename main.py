import csv
import sys
from datetime import datetime

from lxml import etree as xml

sequencenumber = 1
pagenumber = 1
execnumber = 1
fadetime = 1


def minutestoframes(time: str):
    times = time.split(":")
    res = 0
    for i, timeunit in enumerate(times):
        if i == 0:
            res += int(timeunit) * 30 * 60 * 60
        elif i == 1:
            res += int(timeunit) * 30 * 60
        elif i == 2:
            res += int(timeunit) * 30
        elif i == 3:
            res += int(timeunit)
    return str(res)


array = []
with open(sys.argv[1], 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        helperarry = []
        for j, element in enumerate(row):
            # # = 0
            # Name = 1
            # Start = 2
            # print(i, element)
            if row[element] != "":
                helperarry.append(row[element])
        array.append(helperarry)

# ------------------------------------------------------------------------------------
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
TimeCode.set("lenght", minutestoframes(array[len(array) - 1][2]))
TimeCode.set("slot", "TC Slot 1")
TimeCode.set("frame_format", "30 FPS")
TimeCode.set("m_autostart", "true")
TimeCode.set("no_status_call", "true")

Track = xml.SubElement(TimeCode, "Track")
Track.set("index", "0")
Track.set("active", "true")
Track.set("expanded", "true")

Object = xml.SubElement(Track, "Object")
Object.set("name", sys.argv[1][:-4] + " " + str(pagenumber) + "." + str(execnumber))

Type = xml.SubElement(Object, "No")
Type.text = "30"

sequence = xml.SubElement(Object, "No")
sequence.text = str(sequencenumber)

Page = xml.SubElement(Object, "No")
Page.text = str(pagenumber)

Exec = xml.SubElement(Object, "No")
Exec.text = str(execnumber)

Subtrack = xml.SubElement(Track, "SubTrack")
Subtrack.set("index", "0")

for i, e in enumerate(array):
    Event = xml.SubElement(Subtrack, "Event")
    Event.set("index", str(i))
    Event.set("time", minutestoframes(e[2]))
    Event.set("command", "Goto")
    Event.set("pressed", "true")
    Event.set("step", str(i + 1))
    Cue = xml.SubElement(Event, "Cue")
    Cue.set("name", e[1])
    theOneEverywhere = xml.SubElement(Cue, "No")
    theOneEverywhere.text = "1"
    Sequence = xml.SubElement(Cue, "No")
    Sequence.text = str(sequencenumber)
    Cuenumber = xml.SubElement(Cue, "No")
    Cuenumber.text = str(i + 1)

tree = xml.ElementTree(MA)
tree.write("importexport\export.xml", encoding="UTF-8", xml_declaration=True, pretty_print=True)

with open("importexport\export.xml", 'r+') as fd:
    contents = fd.readlines()
    copy = contents[0]
    contents[0] = copy[:-1] + " <?xml-stylesheet type=\"text/xsl\" href=\"styles/timecode@sheet.xsl\"?>\n"
    fd.seek(0)
    fd.writelines(contents)

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
    text.text = "Store Sequence " + str(sequencenumber) + " Cue " + str(i + 1) + " \"" + array[i][1] + "\" /o /nc"
    j += 1
    Macroline = xml.SubElement(Macro, "Macroline")
    Macroline.set("index", str(j))
    text = xml.SubElement(Macroline, "text")
    text.text = "Assign Sequence " + str(sequencenumber) + " Cue " + str(i + 1) + " /fade=" + str(fadetime) + ".00 "
    j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "Label Sequence " + str(sequencenumber) + " \"" + sys.argv[1][:-4] + "\""
j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "Assign Sequence " + str(sequencenumber) + " At Exec 1." + str(pagenumber) + "." + str(execnumber)
j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "SelectDrive 4"
j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "Import \"export.xml\" At Timecode 1 /o"
j += 1

Macroline = xml.SubElement(Macro, "Macroline")
Macroline.set("index", str(j))
text = xml.SubElement(Macroline, "text")
text.text = "Label Timecode 1 \"" + sys.argv[1][:-4] + "\""
j += 1

tree = xml.ElementTree(MA2)
tree.write("Macros\macro.xml", encoding="UTF-8", xml_declaration=True, pretty_print=True)
