#%%
import os
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QBitmap, QPen, QBrush, QCursor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
import numpy as np
from views.ActionRecord import recordItem, updateRecord
from globalObjects import GlobalData
from utils import utils

#Tyler modified from author: marcel-goldschen-ohm <marcel.goldschen@gmail.com>
#Takes QImage and display in widget. Zoomable, drag-pannable

class QImageViewer(QGraphicsView):
    # Mouse button signals emit image scene (x, y) coordinates.
    # !!! For image (row, column) matrix indexing, row = y and column = x.
    leftMouseButtonPressed = pyqtSignal(float, float)
    leftMouseButtonReleased = pyqtSignal(float, float) 
    
    def __init__(self, widget):
        super(QImageViewer, self).__init__()

        self.mainWindow = utils.get_app()

        # Image is displayed as a QPixmap in a QGraphicsScene attached to this QGraphicsView.
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        # Store a local handle to the scene's current image pixmap.
        self._pixmapHandle = None

        # Image aspect ratio mode.
        # !!! ONLY applies to full image. Aspect ratio is always ignored when zooming.
        #   Qt.IgnoreAspectRatio: Scale image to fit viewport.
        #   Qt.KeepAspectRatio: Scale image to fit inside viewport, preserving aspect ratio.
        #   Qt.KeepAspectRatioByExpanding: Scale image to fill the viewport, preserving aspect ratio.
        self.aspectRatioMode = Qt.KeepAspectRatioByExpanding

        # Scroll bar behaviour.
        #   Qt.ScrollBarAlwaysOff: Never shows a scroll bar.
        #   Qt.ScrollBarAlwaysOn: Always shows a scroll bar.
        #   Qt.ScrollBarAsNeeded: Shows a scroll bar only when zoomed.
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Flags for enabling/disabling mouse interaction.
        self.KeyControl = False
        self.isPanning = False

        # Cursor settings
        cursorbit = QBitmap(QPixmap(utils.get_path(["iconImages", "CursorBit.png"])))
        cursormask = QBitmap(QPixmap(utils.get_path(["iconImages", "CursorMask.png"])))
        self.crossHair = QCursor(cursorbit, cursormask, -1, -1)
#        self.setCursor(self.crossHair)
        
        # Mouse coordinate updates
        self.setMouseTracking(True)
        self.digitizerOn = False
        
        # Ty edit: anchor at mouse position
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        #self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)


        # Ty edit: record the zoom, pan, and others
        self.InitialFrame = True
        self.Zoom_recorder = 0
        GlobalData.currentFrame = 1
        GlobalData.totalFrames = 0
        
        self.ViewRectX = 0
        self.ViewRectY = 0
        self.ViewRectWidth = 0
        self.ViewRectHeight = 0
        
        # Ty keypoint drawing initialization
        self.SceneSize = 4.5
        self.ViewSize = self.SceneSize * (4/5)**self.Zoom_recorder
        self.BoxDrawer = QPen(Qt.green) 
        self.BoxDrawer.setWidth(0.01)
        self.BoxFill = QBrush(Qt.green)
        self.key_points = []
        
        # Ty draw trail lines initialization
        self.displayLineOn = False
        self.LineDrawer = QPen(Qt.green)
        self.LineWidth = (4/5)**self.Zoom_recorder
        self.LineDrawer.setWidth(self.LineWidth)
        self.LinePath = []

    def hasImage(self):
        """ Returns whether or not the scene contains an image pixmap.
        """
        return self._pixmapHandle is not None

    def clearImage(self):
        """ Removes the current image pixmap from the scene if it exists.
        """
        if self.hasImage():
            self.scene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    def pixmap(self):
        """ Returns the scene's current image pixmap as a QPixmap, or else None if no image exists.
        :rtype: QPixmap | None
        """
        if self.hasImage():
            return self._pixmapHandle.pixmap()
        return None

    def image(self):
        """ Returns the scene's current image pixmap as a QImage, or else None if no image exists.
        :rtype: QImage | None
        """
        if self.hasImage():
            return self._pixmapHandle.pixmap().toImage()
        return None

    def setImage(self, fileName):
        """ Set the scene's current image pixmap to the input QImage or QPixmap.
        Raises a RuntimeError if the input image has type other than QImage or QPixmap.
        :type image: QImage | QPixmap
        """
        image = QImage(fileName)
        if type(image) is QPixmap:
            pixmap = image
        elif type(image) is QImage:
            pixmap = QPixmap.fromImage(image)
        else:
            raise RuntimeError("ImageViewer.setImage: Argument must be a QImage or QPixmap.")
        if self.hasImage():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self.scene.addPixmap(pixmap)
            
        self.setSceneRect(QRectF(pixmap.rect()))  # Set scene size to image size.
        self.updateViewer()
        self.mainWindow.ShowFrame.setText('frame:%3d' % GlobalData.currentFrame) ##put framenumber as text
        self.mainWindow.qtSceneViewer.setImage(fileName)

    def updateViewer(self):
        """ Show current zoom (if showing entire image, apply current aspect ratio mode).
        """
        if not self.hasImage():
            return
        if self.InitialFrame:
            self.fitInView(self.sceneRect(), self.aspectRatioMode)  # Show entire image (use current aspect ratio mode).
            self.GetFrame()
            self.YellowBox = self.mainWindow.qtSceneViewer.DrawViewBox(self.ViewRectX,self.ViewRectY,self.ViewRectWidth,self.ViewRectHeight)
        
    def GetFrame(self):       
        Rect = self.rect()
        Rect = self.mapToScene(Rect)
        self.ViewRectX = Rect[0].x()
        self.ViewRectY = Rect[0].y()
        RectD = Rect[2] - Rect[0]
        self.ViewRectWidth = RectD.x()
        self.ViewRectHeight = RectD.y()

    def wheelEvent(self, event):  #need to have the setting on Qt.KeepAspectRatioByExpanding
        if event.angleDelta().y() < 0 and self.KeyControl is True:
            factor = 4/5
            self.Zoom_recorder -= 1
        elif event.angleDelta().y() > 0 and self.KeyControl is True:
            factor = 5/4
            self.Zoom_recorder += 1 
        else:
            factor = 1
            
        if factor != 1 and self.KeyControl is True:
            self.scale(factor, factor)
            self.ViewSize = self.SceneSize * (4/5)**self.Zoom_recorder
            self.LineWidth = (4/5)**self.Zoom_recorder
            self.GetFrame()
            self.YellowBox = self.mainWindow.qtSceneViewer.DrawViewBox(
                    self.ViewRectX, self.ViewRectY,
                    self.ViewRectWidth, self.ViewRectHeight)
            
            self.draw_key_points()
            self.draw_line_path()

    def Zoom_large(self): 
        factor = 9/8
        self.Zoom_recorder += 1
        self.scale(factor, factor)
        factor = 1
        self.GetFrame() 
        self.YellowBox = self.mainWindow.qtSceneViewer.DrawViewBox(self.ViewRectX,self.ViewRectY,self.ViewRectWidth,self.ViewRectHeight)
        self.ViewSize = self.SceneSize * (4/5)**self.Zoom_recorder
        self.LineWidth = (4/5)**self.Zoom_recorder
        
        self.draw_key_points()
        self.draw_line_path()
       
    def Zoom_small(self): 
        factor = 8/9
        self.Zoom_recorder -= 1
        self.scale(factor, factor)
        factor = 1
        self.GetFrame()
        self.YellowBox = self.mainWindow.qtSceneViewer.DrawViewBox(self.ViewRectX,self.ViewRectY,self.ViewRectWidth,self.ViewRectHeight)
        self.ViewSize = self.SceneSize * (4/5)**self.Zoom_recorder
        self.LineWidth = (4/5)**self.Zoom_recorder
        
        self.draw_key_points()
        self.draw_line_path()

    def mouseMoveEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        self.sX = int(round(scenePos.x()))
        self.sY = int(round(scenePos.y()))
        self.mainWindow.CursorXY.setText('x:%4d y:%4d ' % (self.sX, GlobalData.imgHeight - self.sY)) ##put coordinate as text

        QGraphicsView.mouseMoveEvent(self, event) 
        if self.isPanning is True and self.mouseLeftPress is True:
            self.GetFrame()
            self.YellowBox = self.mainWindow.qtSceneViewer.DrawViewBox(
                    self.ViewRectX, self.ViewRectY, 
                    self.ViewRectWidth,self.ViewRectHeight)
   
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseLeftPress = True
            if self.KeyControl:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
                self.isPanning = True
                
            if self.digitizerOn is True and self.KeyControl is False:
                self.add_coordinate(self.sX, self.sY)    

                if self.mainWindow.AutoNextMode.autoNextMode == 0:
                    pass
                if self.mainWindow.AutoNextMode.autoNextMode == 1:
                    self.next_frame()
                if self.mainWindow.AutoNextMode.autoNextMode == 2:
                    self.prev_frame()
                if self.mainWindow.AutoNextMode.autoNextMode == 3:
                    self.mainWindow.visableItemsLayout.selectNextItem()                                                            
        QGraphicsView.mousePressEvent(self, event)
        
    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
            self.mouseLeftPress = False
            self.isPanning = False

        self.leftMouseButtonReleased.emit(self.sX, self.sY)
            
    def next_frame(self):
        # Frame increment
        if GlobalData.currentFrame == GlobalData.totalFrames:
            pass
        else:
            GlobalData.currentFrame += 1
            self.setImage(os.path.join(GlobalData.videoPath, str(GlobalData.currentFrame) + ".jpg"))
            self.mainWindow.Slider.setValue(GlobalData.currentFrame)
            self.draw_key_points()

    def prev_frame(self):
        # Frame decrement
        if GlobalData.currentFrame == 1:
            pass
        else:
            GlobalData.currentFrame -= 1
            self.setImage(os.path.join(GlobalData.videoPath, str(GlobalData.currentFrame) + ".jpg"))
            self.mainWindow.Slider.setValue(GlobalData.currentFrame)
            self.draw_key_points()
            
    def slider_frame(self):
        GlobalData.currentFrame = self.mainWindow.Slider.value()
        self.setImage(os.path.join(GlobalData.videoPath, str(GlobalData.currentFrame) + ".jpg"))
        self.draw_key_points()
        
    def draw_key_points(self):
        if self.mainWindow.video_file_loaded == True and self.mainWindow.freezeAllEdite == False:        
            # Grab all points references at the current frame
            if self.key_points:
                for reference in self.key_points:
                    self.scene.removeItem(reference)
            self.key_points = []
            for subject in GlobalData.global_subject_list:
                for part in subject.parts:
                    if part.checked == True:
                        x = part.x[GlobalData.currentFrame-1]
                        y = part.y[GlobalData.currentFrame-1]
                        reference = self.add_key_point(x, y)
                        if reference == None:
                            continue
                        else:
                            reference.setVisible(True)
                        self.key_points.append(reference)    
                
    def add_coordinate(self, x, y):
        selected_items = self.mainWindow.visableItemsLayout._visable_items.selectedItems()
        if len(selected_items) > 0:
            first_item = selected_items[0]
            parent_item = first_item.parent()
            # If the selected item is a child, then we can add coordinates
            if parent_item != None:
                subject_found = [subject for subject in GlobalData.global_subject_list if subject.name == parent_item.text(0)]
                part_found = [part for part in subject_found[0].parts if part.name == first_item.text(0)]                 
                item = recordItem(subject_found[0].name, part_found[0].name, part_found[0].x[GlobalData.currentFrame-1], part_found[0].y[GlobalData.currentFrame-1])               
                part_found[0].x[GlobalData.currentFrame-1] = x
                part_found[0].y[GlobalData.currentFrame-1] = y
                self.draw_key_points()
                self.draw_line_path()
                updateRecord(item)
                self.mainWindow.Undo_action.setEnabled(True)
                self.mainWindow.Redo_action.setEnabled(False)
                
    def add_key_point(self, x, y): 
        if None in (x, y):
            reference = None
        else:
            reference = self.scene.addRect(x - self.ViewSize, y - self.ViewSize, 2*self.ViewSize, 2*self.ViewSize, self.BoxDrawer, self.BoxFill) 
        return reference

    def draw_line_path(self): 
        if self.LinePath:
            for segment in self.LinePath:
                self.scene.removeItem(segment) 
                    
        if self.displayLineOn:                    
            self.LinePath = []
            self.LineDrawer.setWidth(self.LineWidth)
            #We will draw the object that is checked in the tree widget

            selected_items = self.mainWindow.visableItemsLayout._visable_items.selectedItems()
            if len(selected_items) > 0:
                first_item = selected_items[0]
                parent_item = first_item.parent()
                # If the selected item is a child, then we can add coordinates
                if parent_item != None:
                    subject_found = [subject for subject in GlobalData.global_subject_list if subject.name == parent_item.text(0)]
                    part_found = [part for part in subject_found[0].parts if part.name == first_item.text(0)]                 
                    for i in range(GlobalData.totalFrames - 1):
                        if None in (part_found[0].x[i], part_found[0].y[i], part_found[0].x[i+1], part_found[0].y[i+1]):
                            continue
                        else:
                            segment = self.scene.addLine(part_found[0].x[i], part_found[0].y[i], part_found[0].x[i+1], part_found[0].y[i+1], self.LineDrawer)
                            self.LinePath.append(segment)

    def keyPressEvent(self, event):
        #present in both mainWindow and QtImageViewer
        if event.key() == Qt.Key_Control:
            self.KeyControl = True

        if event.key() == Qt.Key_Down:
            self.mainWindow.visableItemsLayout.selectNextItem()
       
        if event.key() == Qt.Key_Up:
            self.mainWindow.visableItemsLayout.selectPreviousItem()
            
    def keyReleaseEvent(self, event):
        #present in both mainWindow and QtImageViewer
        if event.key() == Qt.Key_Control:
            self.KeyControl = False     