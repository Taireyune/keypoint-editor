# Key Point Editor

**Key Point Editor** is a GUI that allow users to obtain human pose landmark 
coordinates from input videos. Since human pose-estimation inferences are not 
perfect, this tool provide users with the means to edit the coordinates by 
hand for human motion analysis research.

The GUI is written mainly with PyQt, numpy, and cv2 libraries.
This repository shows the functions and sample code of the GUI. Please email 
tyleryuanwu@gmail.com or usalanzhang@gmail.com to request related source code.

## Functions     

* [**Human pose inference from video**](https://github.com/Taireyune/keypoint-editor#Human-pose-inference-from-video)
* [**Edit key point coordinates**](https://github.com/Taireyune/keypoint-editor#Edit-key-point-coordinates)
* [**Correction of camera and movement distortions**](https://github.com/Taireyune/keypoint-editor#Distortion-corrections)
* [**Save/open/export data**](https://github.com/Taireyune/keypoint-editor#Save-open-or-export-data)

## Human pose inference from video
### Load video
<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/load_video.png" 
width="840" height="525" alt="load video">
### Apply inference
There is several recognition models to choose from to get the most optimal inference.
The models are based on [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation) 
with various wrapper pre and post processing techniques.
This repository contain a snippet of the 
[post processing](https://github.com/Taireyune/keypoint-editor/blob/master/sample_code/PredictionPostProcess.py).

### Show and inspect inference
All video frames can be zoomed and panned using the mouse and Ctrl key based on 
[PyQt tools by marcel-goldschen-ohm](https://github.com/marcel-goldschen-ohm/PyQtImageViewer). 
[Here is the sample code](https://github.com/Taireyune/keypoint-editor/blob/master/sample_code/QtImageViewer.py).

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/show_inspect.gif" 
alt="inspect inference">

## Edit key point coordinates
### Add and delete objects
Besides the inference key points, users can add other built-in objects or add their own.

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/add_object.png" 
width="840" height="525" alt="add object">

You can of course delete too.

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/delete_object.png" 
width="840" height="525" alt="delete object">

### Edit key points

Any inference error can be corrected manually. Users can choose to see the whole 
point trajectory and use the auto-next function to go to the next frame or object
after each edit.

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/shoulder_edit.gif" 
alt="shoulder edit">

Can't have an editor without 
[undo and redo](https://github.com/Taireyune/keypoint-editor/blob/master/sample_code/ActionRecord.py).

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/undo.png" 
width="840" height="525" alt="undo edit">

## Distortion corrections
### Camera calibration
Checker board video can be used to obtain camera parameters automatically. 
The parameters are used to correct distortions or used in 3D reconstruction computations.

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/camera_calibration.png" 
width="840" height="525" alt="camera calibration">

Depending on the camera used, other camera parameters can be set here. Motion-based
distortions can be corrected using these parameters. 
Link to the 
[dialog](https://github.com/Taireyune/keypoint-editor/blob/master/sample_code/ParameterDialog.py) 
and the 
[computations](https://github.com/Taireyune/keypoint-editor/blob/master/sample_code/ComputeUnroll.py).

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/cmo_parameters.png" 
width="840" height="525" alt="cmo parameters">

### Key point smoothing
Often the inference errors can be mitigated by smoothing. Screenshot shows the point
trajectory with inference noise.

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/smoothing_before.png" 
width="840" height="525" alt="smooth before">

The default settings are based on video information.

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/smoothing_settings.png" 
width="840" height="525" alt="smooth settings">

This is the tragectory after smoothing.

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/smoothing_after.png" 
width="840" height="525" alt="smooth after">

## Save open or export data
### Save and open works
Unfinished work can be saved and reopened. Pixel coordinates and real distance 
coordinates can be exported for 2D analysis or further 3D triangulation
with other camera views. 

### Export data
Before exporting, the GUI will ask if the parameters from the calibrations and 
setting will be used to adjust the 2D point coordinates for more accurate analysis. 

<img 
src="https://github.com/Taireyune/keypoint-editor/blob/master/images/exported_data.png" 
width="840" height="525" alt="exported data">


