import numpy as np
from globalObjects import GlobalData
def computeUnroll(x1, y1, x2, y2, cmoParameter):
    dy = y2 - y1
    dx = x2 - x1
    if cmoParameter["type"] == "top to bottom": 
        denominator = dy + GlobalData.imgHeight + cmoParameter["scanGap"] * GlobalData.imgHeight/cmoParameter["scanDuration"]
        newX2 = x2 - dx*dy/denominator
        newY2 = y2 - dy**2/denominator
        return newX2, newY2

    if cmoParameter["type"] == "left to right": 
        denominator = dx + GlobalData.imgWidth + cmoParameter["scanGap"] * GlobalData.imgWidth/cmoParameter["scanDuration"]
        newX2 = x2 - dx**2/denominator
        newY2 = y2 - dx*dy/denominator
        return newX2, newY2

    if cmoParameter["type"] == "bottom to top": 
        denominator = dy + GlobalData.imgHeight + cmoParameter["scanGap"] * GlobalData.imgHeight/cmoParameter["scanDuration"]
        newX2 = x2 + dx*dy/denominator
        newY2 = y2 + dy**2/denominator
        return newX2, newY2

    if cmoParameter["type"] == "right to left": 
        denominator = dx + GlobalData.imgWidth + cmoParameter["scanGap"] * GlobalData.imgWidth/cmoParameter["scanDuration"]
        newX2 = x2 + dx**2/denominator
        newY2 = y2 + dx*dy/denominator
        return newX2, newY2
    

