from globalObjects import GlobalData

#Record user action for undo and redo commands                                
class recordItem:              
    def __init__(self, subjectName, partName, x, y):
        self.frame = GlobalData.currentFrame
        self.subjectName = subjectName
        self.partName = partName
        self.x = x
        self.y = y
     
def updateRecord(item):
    if GlobalData.recordIdx == len(GlobalData.recordList) and GlobalData.recordIdx < 10:
        GlobalData.recordList.append(item)
        GlobalData.recordIdx += 1
    elif GlobalData.recordIdx >= 10 and len(GlobalData.recordList) >= 10:
        GlobalData.recordList.append(item)
        GlobalData.recordList = GlobalData.recordList[-10:]
        GlobalData.recordIdx = 10
    elif GlobalData.recordIdx < len(GlobalData.recordList):
        GlobalData.recordList[GlobalData.recordIdx:] = []
        GlobalData.recordList.append(item)
        GlobalData.recordIdx += 1
        
def undoAction():
    if GlobalData.recordIdx-1 >= 0:
        recordItem = GlobalData.recordList[GlobalData.recordIdx-1]        
        GlobalData.currentFrame = recordItem.frame
        subject_found = [subject for subject in GlobalData.global_subject_list if subject.name == recordItem.subjectName]
        part_found = [part for part in subject_found[0].parts if part.name == recordItem.partName] 
        part_found[0].x[GlobalData.currentFrame-1] = recordItem.x
        part_found[0].y[GlobalData.currentFrame-1] = recordItem.y
        GlobalData.recordIdx -= 1
    else:
        pass

def redoAction():
    if GlobalData.recordIdx <= 10:
        recordItem = GlobalData.recordList[GlobalData.recordIdx]        
        GlobalData.currentFrame = recordItem.frame
        subject_found = [subject for subject in GlobalData.global_subject_list if subject.name == recordItem.subjectName]
        part_found = [part for part in subject_found[0].parts if part.name == recordItem.partName] 
        part_found[0].x[GlobalData.currentFrame-1] = recordItem.x
        part_found[0].y[GlobalData.currentFrame-1] = recordItem.y
        GlobalData.recordIdx += 1
    else:
        pass
            