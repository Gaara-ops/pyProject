
import xml.dom.minidom as xmldom
import os
import matplotlib.pyplot as plt
import numpy as np

xmlfilepath = os.path.abspath('E:/00.vrp')
print(f"xmlpath:{xmlfilepath}")

domobj = xmldom.parse(xmlfilepath)
print("xmldom.parse:", type(domobj))

vrprotocal = domobj.getElementsByTagName("VRProtocol")
print(type(vrprotocal),len(vrprotocal))
contents = vrprotocal[0].getElementsByTagName("Content")
print(type(contents),len(contents))
# threshold
FocusWindow = contents[0].getElementsByTagName("FocusWindow")
print(type(FocusWindow),len(FocusWindow))
MaxThreshold = FocusWindow[0].getAttribute("MaxThreshold")
MinThreshold = FocusWindow[0].getAttribute("MinThreshold")
# color
Palette = contents[0].getElementsByTagName("Palette")
print(type(Palette),len(Palette))
ColorItems = Palette[0].getElementsByTagName("ITEM")
print(type(ColorItems),len(ColorItems))
for colorItem in ColorItems:
    Color = colorItem.getAttribute("Color")
    Position = colorItem.getAttribute("Position")
    print(Position,Color)
# opacity
OpacityCurve = contents[0].getElementsByTagName("OpacityCurve")
print(type(OpacityCurve),len(OpacityCurve))
OpacityItems = OpacityCurve[0].getElementsByTagName("ITEM")
print(type(OpacityItems),len(OpacityItems))

ctarr = []
opacityarr = []

for opacityItem in OpacityItems:
    opacity = opacityItem.getAttribute("Opacity")
    threshold = opacityItem.getAttribute("Threshold")
    ctarr.append(threshold)
    opacityarr.append(opacity)

plt.plot(ctarr,opacityarr)
plt.draw()
plt.pause(10)
plt.savefig('test.jpg')
plt.close()

print("end!")
