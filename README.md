# Key Point Editor

**Key Point Editor** is a GUI that allow users to obtain human pose landmark 
coordinates from input videos. Since human pose-estimation inferences are not 
perfect, this tool provide users with the means to edit the coordinates by 
hand for human motion analysis research.

This repository shows the functions and sample code of the GUI. Please email 
tyleryuanwu@gmail.com or alanzhang@gmail.com to request related source code.

## Functions     

* [Human pose inference from video](https://github.com/Taireyune/keypoint_editor#Human-pose-inference-from-video)
* [Edit key point coordinates](https://github.com/Taireyune/keypoint_editor#Edit-key-point-coordinates)
* [Correction of camera and movement distortions](https://github.com/Taireyune/keypoint_editor#Distortion-corrections)
* [Save/open/export data](https://github.com/Taireyune/keypoint_editor#Save-open-or-export-data)

## Human pose inference from video
### Load video
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/load_video.png" 
width="840" height="525" alt="load video">
### Apply inference
There is several recognition models to choose from to get the most optimal inference.
The models are based on [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation) 
with various wrapper pre and post processing techniques.
This repository contain a snippet of the post-processing.

### Show and inspect inference
Each frame can be zoomed and panned using the mouse and Ctrl key based on 
[PyQt tools](https://github.com/marcel-goldschen-ohm/QtOpenGLViewer).
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/show_inspect.gif" 
alt="inspect inference">

## Edit key point coordinates
### Add and delete objects
Besides the inference key points, users can add other built-in objects or add their own.

<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/add_object.png" 
width="840" height="525" alt="add object">

You can of course delete too.

<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/delete_object.png" 
width="840" height="525" alt="delete object">

### Edit key points

Any inference error can be corrected manually. Users can choose to see the whole 
point trajectory and use the auto-next function to go to the next frame or object
after each edit.

<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/shoulder_edit.gif" 
alt="shoulder edit">

Can't have an editor without the undo/redo button.

<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/undo.png" 
width="840" height="525" alt="undo edit">

## Distortion corrections
### Camera calibration
Checker board video used to obtain camera parameters automatically. The parameters
are used to correct distortions or used in 3D reconstruction computations.

<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/camera_calibration.png" 
width="840" height="525" alt="camera calibration">

Depending on the camera used, other camera parameters can be set here. Motion based
distortions can be corrected using these parameters. 

<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/cmo_parameters.png" 
width="840" height="525" alt="cmo parameters">

### Key point smoothing
Most of the inference errors can be mitigated by smoothing. Here is the point
trajectory with inference noise.

<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/smoothing_before.png" 
width="840" height="525" alt="smooth before">

Here we can use default settings.

<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/smoothing_settings.png" 
width="840" height="525" alt="smooth settings">

The tragectory after smoothing.

<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/smoothing_after.png" 
width="840" height="525" alt="smooth after">

## Save open or export data
### Save and open works
Unfinished work can be saved and reopened. Pixel coordinates and real distances 
(parallel to the camera plane with distoration corrections) can be exported for 2D analysis or further 3D triangulation
with other camera views. 

### export data
<img 
src="https://github.com/Taireyune/keypoint_editor/blob/master/images/exported_data.png" 
width="840" height="525" alt="exported data">


