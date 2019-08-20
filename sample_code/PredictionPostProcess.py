#%%
import numpy as np
from math import sqrt
from globalObjects import GlobalData
from config import ConfigConstants as config
from globalObjects.Part import Part as GPart
from globalObjects.Subject import Subject as GSubject
from beans.FillBlanks import fillBlanks

#This file contains the classes for rearranging the key point prediction data such
#that the same person in the video would be associated with the same person label
#in the data.
#Note that this file assumes the maximum number of detected individual is 5.
#18 is the number of key parts. This may be changed in the future.
#the assoScore function and the extreme values 2500 and 3000 should be adjusted
#when the above parameters change

class AssoScore:
    
    #initial settings. Equation coefficient.
    def __init__(self, Ax, Ay, Bx, By):
        self.penalty = 0
        self.Score = 0
        self.exponential = 1.59
        self.Coefficient = 1
        
        for i in range(18):
            self.CalculateScore(Ax[i], Ay[i], Bx[i], By[i])
    
    #Give output    
    def ScoreOutput(self):
        if self.penalty == 18:
            assoScore = 2500
        else:
            assoScore = self.PenaltyFunction()
        return assoScore
    
    #Equation to calculate score    
    def PenaltyFunction(self):
        assoScore = self.Score/(1.0 * (18 - self.penalty)) + self.exponential**(self.penalty * self.Coefficient)
        return assoScore
    
    #Find distance between points
    def PointDist(self, Ax, Ay, Bx, By):
        Pdistance = sqrt((Ax - Bx)**2 + (Ay - By)**2)
        return Pdistance
     
    #Compute score    
    def CalculateScore(self, Ax, Ay, Bx, By):
        if None in (Ax, Ay, Bx, By):
            self.penalty += 1
        else:
            self.Score += self.PointDist(Ax, Ay, Bx, By)
            
class FrameAssociation:
    def __init__(self, frameA, frameB):
        self.SubA = len(frameA)
        self.SubB = len(frameB)
        self.AssoArray = np.zeros((self.SubA, self.SubB), dtype=float)
        self.pairList = []
        self.FillAssoArray(frameA, frameB)
        self.FillPairList()
        self.outputData = self.IDrearrangement(frameA, frameB)

    #creates an array that hold the score to every pair of combination           
    def FillAssoArray(self, frameA, frameB):
        for personsA in range(self.SubA):
            subjectAx = frameA[personsA].partX
            subjectAy = frameA[personsA].partY  
            
            for personsB in range(self.SubB):
                subjectBx = frameB[personsB].partX
                subjectBy = frameB[personsB].partY            
                assoScore = AssoScore(subjectAx, subjectAy, subjectBx, subjectBy)
                self.AssoArray[personsA, personsB] = assoScore.ScoreOutput() 
    
    #creates a list that contain the index pair for the best association.
    #Each time a minimum score is found, that row and column will be filled with 3000 so that
    #   it will not be chosen again.      
    def FillPairList(self):
        if self.SubA >= self.SubB:
            for i in range(self.SubB):
                index = np.unravel_index(np.argmin(self.AssoArray), self.AssoArray.shape)
                self.pairList.append(index)
                self.AssoArray[index[0], :] = np.full((1, self.SubB), 3000)
                self.AssoArray[:, index[1]] = np.full((1, self.SubA), 3000)
                
        else:
            for i in range(self.SubA):
                index = np.unravel_index(np.argmin(self.AssoArray), self.AssoArray.shape)
                self.pairList.append(index)
                self.AssoArray[index[0], :] = np.full((1, self.SubB), 3000)
                self.AssoArray[:, index[1]] = np.full((1, self.SubA), 3000)     
    
    #Based on the list created in FillPairList, rearrange the ID in the subject objects.
    def IDrearrangement(self, frameA, frameB):
        #When there is more subjects in frame A: 
        if self.SubA >= self.SubB:
            for i, pairs in enumerate(self.pairList): 
                frameB[pairs[1]].ID = frameA[pairs[0]].ID
            return frameB

        #When there is more subjects in frame B, the unpaired subjects get new ID             
        if self.SubA < self.SubB:
            IDrecord = list(range(1, 11))
            frameBSub = list(range(self.SubB))
            for pairs in self.pairList:
                NewID = frameA[pairs[0]].ID + 0
                frameB[pairs[1]].ID = NewID + 0           
                frameBSub.remove(pairs[1])
                IDrecord[NewID-1] = None
            
            for leftOver in frameBSub:
                for i in IDrecord:
                    if i != None:
                        frameB[leftOver].ID = i + 0
                        IDrecord[i-1] = None
                        break
                                       
            return frameB

#Turn keyPointData from having an object with each index of a list representing
#   a coordinate of each body part into each index of a list representing a
#   a coordinate of each frame.
def Horizontalize(keyPointData):
    for frameIdx, frame in enumerate(keyPointData):              
        #for loops for each subject in frame
        for k, subject in enumerate(frame):
            subjectName = "Person_" + str(subject.ID)
            foundMatch = False
            #forloop for each global subject that may match
            for i in range(len(GlobalData.global_subject_list)):
                if GlobalData.global_subject_list[i].name == subjectName:
                    foundMatch = True
                    for j in range(len(subject.partX)):
                        GlobalData.global_subject_list[i].parts[config.part_convert[j]].x[frameIdx] = subject.partX[j]
                        GlobalData.global_subject_list[i].parts[config.part_convert[j]].y[frameIdx] = subject.partY[j]
                    break
          
            if not foundMatch:
                #create new global_subject
                #create new parts:
                formatParts = []
                partDict = config.part_dict["person"]
                for parts in partDict: 
                    newPart = GPart(partDict[parts]['label'], partDict[parts]['index'], partDict[parts]['type'])
                    newPart.x = [None] * GlobalData.totalFrames
                    newPart.y = [None] * GlobalData.totalFrames                        
                    formatParts.append(newPart)                        
                newSubject = GSubject(subjectName, "person", formatParts)    
                
                for j in range(len(subject.partX)):
                    newSubject.parts[config.part_convert[j]].x[frameIdx] = subject.partX[j]
                    newSubject.parts[config.part_convert[j]].y[frameIdx] = subject.partY[j]
                GlobalData.global_subject_list.append(newSubject)

    for subject in GlobalData.global_subject_list:
        for part in subject.parts:
            part.x = fillBlanks(part.x)
            part.y = fillBlanks(part.y)
